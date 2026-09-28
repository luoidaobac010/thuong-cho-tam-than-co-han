"""
solver.py
Engine chính của CoThuong-AI.
Nhận đề bài → Gọi LLM → Sinh lời giải LaTeX theo phong cách cô Thương.
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

from .config import LLMConfig, load_config
from .latex_template import wrap_in_template
from .persona import get_system_prompt, get_system_prompt_with_examples

# Ép agy trả về đúng 1 field LaTeX body, khỏi phải gỡ code fence
AGY_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {"latex_body": {"type": "string"}},
    "required": ["latex_body"],
}

_LATEX_SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def _escape_latex(text: str) -> str:
    """Escape ký tự đặc biệt để chèn text thô (đề bài) vào LaTeX."""
    return "".join(_LATEX_SPECIAL.get(ch, ch) for ch in text)


_TABULAR_RE = re.compile(
    r"(\\begin\{tabular\}\{)([^{}]*(?:\{[^{}]*\}[^{}]*)*)(\})(.*?)(\\end\{tabular\})",
    re.DOTALL,
)


def _fix_tabular_columns(text: str) -> str:
    """Thêm cột nếu hàng nhiều ô hơn spec (model hay khai thiếu 1 cột -> lỗi
    'Extra alignment tab' làm hỏng cả PDF).
    simplify: chỉ đếm & ở hàng, bỏ qua \\& và bảng lồng nhau."""
    def fix(m: re.Match) -> str:
        spec, body = m.group(2), m.group(4)
        if "\\begin{tabular}" in body:
            return m.group(0)
        declared = len(re.findall(r"[lcrXpmb]", re.sub(r"[@<>!]?\{[^{}]*\}", "", spec)))
        rows = re.split(r"\\\\", body)
        needed = max(len(re.findall(r"(?<!\\)&", row)) + 1 for row in rows)
        if needed <= declared:
            return m.group(0)
        extra = ("c|" if spec.rstrip().endswith("|") else "c") * (needed - declared)
        return m.group(1) + spec + extra + m.group(3) + body + m.group(5)
    return _TABULAR_RE.sub(fix, text)


def parse_pages(spec: str | None, total: int) -> list[int]:
    """'1-3,5' -> [0, 1, 2, 4] (0-based). None/'' -> tất cả trang."""
    if not spec:
        return list(range(total))
    pages: list[int] = []
    try:
        for part in spec.split(","):
            part = part.strip()
            if "-" in part:
                a, b = (int(x) for x in part.split("-", 1))
                if a > b:
                    raise ValueError(f"❌ Khoảng trang '{part}' bị ngược, viết {b}-{a}.")
                pages.extend(range(a, b + 1))
            elif part:
                pages.append(int(part))
    except ValueError as e:
        if str(e).startswith("❌"):
            raise
        raise ValueError(f"❌ --pages '{spec}' không hợp lệ, vd '19-26' hoặc '1,3,5'.") from None
    if not pages:
        raise ValueError(f"❌ --pages '{spec}' không chọn trang nào.")
    bad = [p for p in pages if not 1 <= p <= total]
    if bad:
        raise ValueError(f"❌ Trang {bad} ngoài phạm vi 1-{total}.")
    return [p - 1 for p in dict.fromkeys(pages)]


# Chữ PDF cho retrieval. page.get_text() của PDF xuất từ XeTeX/pandoc dính chữ tiếng Việt
# ("đểtrị", "kếthuật": 13 lần "giảm để trị" trong md, 0 lần trong chữ PDF), bẻ tiêu đề
# thành 2 dòng ("Quay" / "lui") và không có dòng "#"/"**" nên cả trang thành 1 mục khi
# xét tên chiến lược. Dựng lại từng dòng từ toạ độ ký tự, dòng đậm đầu block thành tiêu đề.
_MATH_ALNUM = range(0x1D400, 0x1D800)  # chữ toán (𝑛, 𝑇): khoảng hở của chúng không phải dấu cách
_LIST_MARK = re.compile(r"\s*(\d+\.|[•\-])\s*")


def _letter(ch: str) -> bool:
    return ch.isalpha() and ord(ch) not in _MATH_ALNUM


def _line_text(line: dict) -> str:
    """Nối ký tự của 1 dòng, chèn dấu cách giữa 2 chữ cái hở > 0.15 cỡ chữ.
    Trên PDF của repo, chữ cùng từ hở <= 0.12, ranh giới từ bị dính hở ~0.2 trở lên."""
    out, prev = [], None
    for span in line["spans"]:
        for ch in span["chars"]:
            c = ch["c"]
            if prev and _letter(prev[0]) and _letter(c) and ch["bbox"][0] - prev[1] > 0.15 * prev[2]:
                out.append(" ")
            out.append(c)
            prev = (c, ch["bbox"][2], span["size"])
    return unicodedata.normalize("NFC", "".join(out)).strip()


def _glue(a: str, b: str) -> str:
    return a[:-1] + b if a.endswith("-") else a + " " + b


def _join(lines: list[str]) -> list[str]:
    """Dòng bắt đầu bằng chữ thường là phần tiếp của dòng trước (xuống dòng trong câu)."""
    out: list[str] = []
    for s in lines:
        if out and s[0].islower():
            out[-1] = _glue(out[-1], s)
        else:
            out.append(s)
    return out


def _is_bold(span: dict) -> bool:
    return bool(span["flags"] & 16) or "bold" in span["font"].lower()


def _alnum_spans(line: dict) -> list[dict]:
    return [s for s in line["spans"] if any(c["c"].isalnum() for c in s["chars"])]


def _all_bold(line: dict) -> bool:
    """Mọi span có chữ/số đều đậm. Dấu mục đứng đầu ("6.", "•") được phép không đậm."""
    spans = _alnum_spans(line)
    if spans and not _is_bold(spans[0]) and _LIST_MARK.fullmatch("".join(c["c"] for c in spans[0]["chars"])):
        spans = spans[1:]
    return bool(spans) and all(_is_bold(s) for s in spans)


def _page_items(page) -> tuple[list[tuple[str, str, float]], Counter]:
    """[(loại, chữ, cỡ)] của 1 trang: "head" = các dòng đậm liền nhau ở đầu 1 block."""
    items: list[tuple[str, str, float]] = []
    sizes: Counter = Counter()
    for b in page.get_text("rawdict")["blocks"]:
        if b.get("type") != 0:
            continue
        lines = []
        for ln in b["lines"]:
            t = _line_text(ln)
            if t:
                lines.append((ln, t))
                for s in ln["spans"]:
                    sizes[round(s["size"], 1)] += sum(not c["c"].isspace() for c in s["chars"])
        k = 0
        while k < len(lines) and _all_bold(lines[k][0]):
            k += 1
        if k:
            head = lines[0][1]
            for _, t in lines[1:k]:
                head = _glue(head, t)
            size = max(round(s["size"], 1) for ln, _ in lines[:k] for s in _alnum_spans(ln))
            items.append(("head", head, size))
        items += [("text", t, 0.0) for t in _join([t for _, t in lines[k:]])]
    return items, sizes


def _pdf_text(doc, order: list[int]) -> str:
    """Chữ các trang trong order, tiêu đề viết lại như md để _find_relevant_segments chia mục:
    cỡ lớn hơn chữ thân -> "#" theo hạng cỡ, "Câu N" giữ nguyên, còn lại -> dòng in đậm.
    simplify: chọn --pages từ giữa tài liệu thì mất tiêu đề của các trang trước. Mang tiêu đề
    đang mở sang trang sau (đã thử) sửa được trang giữa chuyên đề nhưng kéo đoạn chữa bài vào
    3 trang đề không liên quan, nên bỏ."""
    items, sizes = {}, Counter()
    for i in range(doc.page_count):
        items[i], sz = _page_items(doc[i])
        sizes += sz
    body = sizes.most_common(1)[0][0] if sizes else 0.0
    big = sorted({s for v in items.values() for kind, _, s in v if kind == "head" and s > body + 0.5}, reverse=True)
    rank = {s: min(r + 1, 6) for r, s in enumerate(big)}

    def render(kind: str, t: str, s: float) -> str:
        if kind == "text":
            return t
        if s > body + 0.5:
            return "#" * rank[s] + " " + t
        if re.match(r"câu\s*\d", t, re.IGNORECASE):
            return t
        return "\n**" + t + "**"

    return "\n".join("\n".join(render(*it) for it in items[i]) for i in order)


def render_pdf_pages(pdf_path: Path, pages_spec: str | None = None,
                     dpi: int = 110) -> tuple[dict[str, bytes], str]:
    """Render các trang PDF thành PNG (tên -> bytes) + text trích được để retrieval."""
    try:
        import pymupdf
    except ImportError:
        raise RuntimeError("❌ Cần PyMuPDF để đọc PDF: pip install -r requirements.txt") from None

    doc = pymupdf.open(pdf_path)
    order = parse_pages(pages_spec, doc.page_count)
    images: dict[str, bytes] = {}
    for i in order:
        images[f"page_{i + 1:02d}.png"] = doc[i].get_pixmap(dpi=dpi).tobytes("png")
    text = _pdf_text(doc, order)
    doc.close()
    return images, text


# Chủ đề -> từ khoá. Đề bài khớp từ nào của chủ đề thì cả chủ đề được dùng để
# chấm điểm đoạn transcript (nên đề ghi "backtracking" vẫn tìm ra đoạn "quay lui").
# Từ khoá VN lấy theo tần suất thực tế trong data/buoi*_clean.md (buổi 1-9).
# simplify: keyword matching, nâng cấp lên embedding search nếu cần chính xác hơn.
TOPIC_KEYWORDS = {
    "tiem_can": ["big o", "omega", "theta", "tiệm cận", "tăng trưởng", "bậc",
                 "so sánh", "giai thừa", "log", "mũ"],
    "do_phuc_tap": ["độ phức tạp", "phân tích thuật toán", "vòng lặp", "phép toán cơ bản"],
    "tong_dem": ["sigma", "tổng", "đếm", "tổ hợp", "chỉnh hợp"],
    "de_quy": ["đệ quy", "truy hồi", "hàm sinh", "phương trình đặc trưng",
               "recurrence", "recursive"],
    "toi_uu": ["tối ưu", "mô hình hóa", "mô hình", "hàm mục tiêu", "ràng buộc",
               "optimization"],
    "quay_lui": ["quay lui", "vét cạn", "hoán vị", "nhánh cận", "n hậu",
                 "mã đi tuần", "sudoku", "backtrack", "brute force"],
    "chia_de_tri": ["chia để trị", "giảm để trị", "sắp xếp", "nhị phân",
                    "merge sort", "quick sort", "divide and conquer", "decrease and conquer"],
    "tham_lam": ["tham lam", "ba lô phân số", "greedy"],
    "qhd": ["quy hoạch động", "bài toán con", "bảng", "cái túi", "ba lô",
            "dãy con", "fibonacci", "knapsack", "dynamic programming"],
}

# Bài cô chữa trên lớp -> từ khoá chỉ bài đó dùng (tên bài, thuật ngữ riêng).
# Đề nhắc bài nào thì đoạn chứa từ khoá của bài đó xếp trước đoạn chỉ khớp chủ đề,
# vì từ khoá chủ đề đông hơn (vd "tối ưu", "bảng") nên đếm chung sẽ lấn đoạn chữa bài.
# Chỉ lấy từ gần như không có ngoài đoạn chữa bài (đếm trên data/buoi*_clean.md).
# Không dùng từ chung như "ma trận" (đề đếm phép nhân 2 ma trận vuông), "màu", hay
# "tương thích" đứng riêng (đề nhân chuỗi ma trận hay ghi "kích thước tương thích").
BAI_KEYWORDS = {
    # b10:109-173. "activity-select" bắt cả cách ghi CLRS "activity-selection",
    # "GREEDY-ACTIVITY-SELECTOR" (slide của cô là tiếng Anh, b10:109)
    "chon_hoat_dong": ["chọn hoạt động", "hoạt động tương thích", "công việc tương thích",
                       "activity selection", "activity-select", "interval scheduling",
                       "lựa chọn công việc", "thời gian bắt đầu", "thời gian kết thúc",
                       "thời điểm bắt đầu", "thời điểm kết thúc", "lịch họp", "cuộc họp"],
    # b10:51-107
    "to_mau": ["tô màu", "số màu", "coloring"],
    # b9:323-443, b10:183-233
    "nhan_chuoi_ma_tran": ["chuỗi ma trận", "dãy ma trận", "matrix chain", "matrix-chain",
                           "mcm", "nhân vô hướng"],
    # b10:235-325
    "lcs": ["dãy con chung", "chuỗi con chung", "xâu con chung", "lcs", "longest common"],
}

# Chiến lược cô dùng khi chữa từng bài trong BAI_KEYWORDS
BAI_STRATEGY = {
    "chon_hoat_dong": "tham_lam", "to_mau": "tham_lam",
    "nhan_chuoi_ma_tran": "qhd", "lcs": "qhd",
}
# Tên chiến lược mà đề hay ghi. Đề ghi chiến lược mà không có chiến lược cô dùng cho bài
# (vd "tô màu đồ thị bằng quay lui") thì không ưu tiên đoạn cô chữa bài đó.
# simplify: đề dùng bài làm ví dụ cho chiến lược khác (vd "chọn hoạt động bằng quy hoạch
# động", "LCS bằng quay lui") cũng mất ưu tiên bài. Nâng cấp nếu cần: hạ bài xuống sau chủ đề
# thay vì bỏ hẳn. Không có chữ "vét cạn": đề MCM hay so vét cạn với QHĐ.
STRATEGY_NAMES = {
    "tham_lam": ["tham lam", "greedy"],
    "qhd": ["quy hoạch động", "dynamic programming"],
    "quay_lui": ["quay lui", "backtrack"],
    "chia_de_tri": ["chia để trị", "giảm để trị", "divide and conquer", "decrease and conquer"],
}


class CoThuongSolver:
    """
    AI Solver mô phỏng phong cách giải bài tập của Cô Thương.
    """

    def __init__(
        self,
        config: LLMConfig | None = None,
        knowledge_base_path: Path | None = None,
    ):
        self.config = config or load_config()
        self.config.validate()

        # Load knowledge base if available
        self.knowledge_base = None
        if knowledge_base_path is None:
            default_kb = (
                Path(__file__).resolve().parent.parent
                / "data" / "knowledge_base.json"
            )
            if default_kb.exists():
                knowledge_base_path = default_kb

        if knowledge_base_path and knowledge_base_path.exists():
            with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)

        # Build system prompt
        self._build_system_prompt()

        # Initialize Gemini
        self._init_model()

    def _build_system_prompt(self) -> None:
        """Xây dựng system prompt với few-shot examples nếu có."""
        if self.knowledge_base and self.knowledge_base.get("latex_examples"):
            self.system_prompt = get_system_prompt_with_examples(
                self.knowledge_base["latex_examples"]
            )
        else:
            self.system_prompt = get_system_prompt()

    def _init_model(self) -> None:
        """Khởi tạo client theo provider."""
        if self.config.provider == "agy":
            return  # agy là CLI, gọi qua subprocess mỗi lần solve

        # Import lazy để user dùng agy không cần cài google-genai
        from google import genai
        from google.genai import types

        self.client = genai.Client(api_key=self.config.api_key)
        self.generate_config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_output_tokens,
            top_p=self.config.top_p,
        )

    def _call_gemini(self, user_prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.config.model,
            contents=user_prompt,
            config=self.generate_config,
        )
        if not response.text:
            raise RuntimeError("❌ Model không trả về kết quả. Kiểm tra lại API key và quota.")
        return response.text

    def _call_agy(self, user_prompt: str,
                  files: dict[str, bytes] | None = None,
                  persona: bool = True) -> str:
        """Gọi Antigravity CLI ở headless mode, trả về LaTeX body.

        files: ghi vào thư mục làm việc tạm để agy tự đọc (vd ảnh trang đề).
        Đọc file trong workspace không cần permission, khác với chạy lệnh shell.
        persona: False cho tác vụ kỹ thuật (sửa LaTeX), khỏi gửi persona dài.
        """
        # agy không có flag system prompt nên ghép persona vào đầu prompt
        prompt = f"{self.system_prompt}\n\n---\n\n{user_prompt}" if persona else user_prompt
        cmd = [
            "agy", "-p", prompt,
            "--output-format", "json",
            "--json-schema", json.dumps(AGY_OUTPUT_SCHEMA),
            "--print-timeout", self.config.agy_timeout,
            "--sandbox",
        ]
        if self.config.model:
            cmd += ["--model", self.config.model]

        # agy là agent, được ghi file trong workspace: chạy trong thư mục tạm
        # để nó không đụng vào repo
        with tempfile.TemporaryDirectory(prefix="cothuong-agy-") as tmp:
            for name, data in (files or {}).items():
                (Path(tmp) / name).write_bytes(data)
            proc = subprocess.run(
                cmd, cwd=tmp, capture_output=True, text=True, encoding="utf-8"
            )

        try:
            result = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"❌ agy trả về output không phải JSON (exit={proc.returncode}).\n"
                f"   stderr: {proc.stderr.strip()[:500]}"
            ) from e

        if result.get("status") != "SUCCESS":
            raise RuntimeError(
                f"❌ agy lỗi ({result.get('status')}): "
                f"{result.get('error') or proc.stderr.strip()[:500]}\n"
                f"   Nếu chưa đăng nhập: chạy `agy` 1 lần ở terminal."
            )

        body = (result.get("structured_output") or {}).get("latex_body")
        denied = result.get("denied_actions")
        if not body and not result.get("response") and denied:
            # Model cố chạy lệnh shell, headless tự từ chối nên dừng giữa chừng
            raise RuntimeError(
                f"❌ agy dừng vì model cố dùng tool bị chặn ({denied}). Chạy lại, "
                f"hoặc chia nhỏ --pages để model tự tính không cần chạy lệnh."
            )
        # Fallback nếu schema không được áp: dùng response thô
        return body or result.get("response", "")

    def solve(
        self,
        problem: str,
        title: str | None = None,
        subtitle: str = "Có lập luận/giải thích theo hướng dẫn giảng viên",
        wrap_template: bool = True,
    ) -> str:
        """
        Giải một bài tập thuật toán.

        Args:
            problem: Đề bài (text hoặc LaTeX).
            title: Tiêu đề document (tự sinh nếu không cung cấp).
            subtitle: Dòng phụ dưới tiêu đề.
            wrap_template: Nếu True, wrap output vào full LaTeX document.

        Returns:
            LaTeX string (full document hoặc body-only).
        """
        user_prompt = self._build_user_prompt(problem)

        print(f"🤖 Đang gọi {self.config.model}...")

        if self.config.provider == "agy":
            raw = self._call_agy(user_prompt)
        else:
            raw = self._call_gemini(user_prompt)

        if not raw.strip():
            raise RuntimeError("❌ Model không trả về kết quả.")

        body_content = self._clean_response(raw)

        if wrap_template:
            if not title:
                # Đề bài là text thô (có thể chứa ^ _ & ...), phải escape
                # trước khi chèn vào \title, nếu không LaTeX báo "Missing $"
                title = f"Bài giải: {_escape_latex(problem[:80])}"
                if len(problem) > 80:
                    title += "..."
            return wrap_in_template(body_content, title=title, subtitle=subtitle)

        return body_content

    def solve_pdf(
        self,
        pdf_path: Path,
        pages: str | None = None,
        title: str | None = None,
        subtitle: str = "Có lập luận/giải thích theo hướng dẫn giảng viên",
        wrap_template: bool = True,
    ) -> str:
        """Giải toàn bộ bài tập trong file PDF đề (agy đọc ảnh từng trang)."""
        if self.config.provider != "agy":
            # simplify: chỉ agy. Gemini cần gửi ảnh qua types.Part.from_bytes nếu cần
            raise ValueError("❌ --input-pdf hiện chỉ hỗ trợ provider agy.")

        images, pdf_text = render_pdf_pages(Path(pdf_path), pages)
        names = ", ".join(images)
        problem = (
            f"Đề bài nằm trong {len(images)} ảnh ở thư mục làm việc hiện tại: {names}.\n"
            "Hãy mở và đọc KỸ từng ảnh theo thứ tự bằng công cụ xem file. Bạn KHÔNG có "
            "quyền chạy lệnh shell/python (sẽ bị từ chối và mất hết kết quả): mọi phép "
            "tính phải tự làm. Chỉ giải các trang là bài tập/đề thi, bỏ qua trang lý thuyết, "
            "trang bìa. Giải ĐẦY ĐỦ mọi bài, mỗi bài một \\section{Bài ...} và chép lại "
            "đề trước khi giải.\n"
            "Trả toàn bộ LaTeX body vào field latex_body."
        )
        user_prompt = self._build_user_prompt(problem, retrieval_text=pdf_text)

        print(f"🤖 Đang gọi {self.config.model} với {len(images)} trang...")
        raw = self._call_agy(user_prompt, files=images)
        if not raw.strip():
            raise RuntimeError("❌ Model không trả về kết quả.")

        body_content = self._clean_response(raw)
        if wrap_template:
            title = title or f"Bài giải: {_escape_latex(Path(pdf_path).stem)}"
            return wrap_in_template(body_content, title=title, subtitle=subtitle)
        return body_content

    def fix_latex_error(self, tex: str, line_no: int, error: str,
                        before: int = 20, after: int = 10) -> str | None:
        """Nhờ agy sửa tối thiểu đoạn quanh dòng lỗi LaTeX, ghép lại vào file.

        Chỉ gửi 1 đoạn (không gửi cả bài) để model không viết lại nội dung lời giải.
        Trả về None nếu không sửa được.
        """
        if self.config.provider != "agy":
            return None  # simplify: chỉ agy, gemini thì thêm nhánh _call_gemini nếu cần
        lines = tex.split("\n")
        if not 1 <= line_no <= len(lines):
            return None
        start = max(0, line_no - 1 - before)
        end = min(len(lines), line_no + after)
        snippet = "\n".join(lines[start:end])
        prompt = (
            "Bạn là chuyên gia LaTeX. Biên dịch XeLaTeX báo lỗi:\n"
            f"  {error}\n"
            f"tại dòng {line_no} của file. Dưới đây là đoạn từ dòng {start + 1} đến {end}:\n"
            "<<<\n" f"{snippet}\n" ">>>\n"
            "Sửa TỐI THIỂU để hết lỗi (vd thêm \\] hoặc \\end{...} bị thiếu, cân bằng ngoặc). "
            "KHÔNG đổi nội dung chữ/toán, KHÔNG thêm preamble. KHÔNG chạy lệnh shell. "
            "Trả về TOÀN BỘ đoạn đã sửa (cùng phạm vi dòng) trong field latex_body, "
            "không kèm <<< >>>."
        )
        fixed = self._call_agy(prompt, persona=False).strip()
        # Model đôi khi trả kèm dấu bao <<< >>> của prompt
        if fixed.startswith("<<<"):
            fixed = fixed[3:]
        if fixed.endswith(">>>"):
            fixed = fixed[:-3]
        fixed = fixed.strip("\n")
        # Chặn trường hợp model trả rỗng hoặc cắt mất phần lớn đoạn
        if not fixed.strip() or len(fixed) < 0.5 * len(snippet):
            return None
        result = "\n".join(lines[:start] + fixed.split("\n") + lines[end:])
        # Đoạn chạm cuối file thì model hay nuốt newline cuối: trả lại cho giống gốc
        if tex.endswith("\n") and not result.endswith("\n"):
            result += "\n"
        return result

    def _build_user_prompt(self, problem: str,
                           retrieval_text: str | None = None) -> str:
        """Xây dựng user prompt từ đề bài."""
        prompt = f"""Hãy giải bài tập sau theo đúng phong cách của bạn (Cô Thương).
Trình bày lời giải bằng LaTeX body (KHÔNG bao gồm preamble, \\documentclass, \\begin{{document}}).
Giải thích từng bước rõ ràng, dùng ngôn ngữ bình dân.

## ĐỀ BÀI:
{problem}

## YÊU CẦU:
- Giải từng bước, có lập luận.
- Đóng khung kết quả cuối cùng trong \\begin{{resultbox}}...\\end{{resultbox}}.
- Nếu có lưu ý quan trọng, dùng \\begin{{notebox}}...\\end{{notebox}}.
- Output CHỈNH LaTeX body content, không có preamble.
- KHÔNG chạy lệnh shell/python, kể cả `ls`: lệnh bị từ chối và mất hết kết quả. Đề đã
  nằm đủ ở trên, mọi phép tính tự làm.
"""

        # Thêm teaching context nếu có
        if self.knowledge_base:
            relevant_segments = self._find_relevant_segments(retrieval_text or problem)
            if relevant_segments:
                prompt += "\n## CONTEXT TỪ BÀI GIẢNG (để tham khảo phong cách):\n"
                for seg in relevant_segments[:3]:
                    prompt += f"---\n{seg['content'][:500]}\n---\n\n"

        return prompt

    def _find_relevant_segments(self, problem: str, top_k: int = 3) -> list[dict]:
        """Tìm các đoạn transcript liên quan đến đề bài theo bài cô chữa và chủ đề."""
        if not self.knowledge_base:
            return []

        segments = self.knowledge_base.get("teaching_segments", [])
        problem_lower = problem.lower()

        # Chủ đề nào có ít nhất 1 từ khoá xuất hiện trong đề
        matched_topics = [
            topic for topic, words in TOPIC_KEYWORDS.items()
            if any(w in problem_lower for w in words)
        ]
        # Bài cô chữa nào được đề nhắc tới, bỏ bài mà đề ghi làm bằng chiến lược khác.
        # Chỉ xét tên chiến lược trong cùng mục với tên bài. Mục bắt đầu ở dòng tiêu đề ("#", "Câu N")
        # hoặc dòng in đậm sau dòng trống. Mục không ghi chiến lược thì lấy của tiêu đề cha gần nhất
        # có ghi (cha = tiêu đề cấp nhỏ hơn, dòng in đậm là cấp sâu nhất).
        # simplify: gạch đầu dòng cùng mục vẫn tính chung. Tách riêng từng gạch đầu dòng thì tờ A4
        # hỏng: "10. Tô màu đồ thị" nằm trong danh sách quay lui nhưng không ghi chữ "quay lui".
        sections, prev = [], ""  # [cấp, chữ của mục]
        for ln in problem_lower.split("\n"):
            m = re.match(r"\s*(#{1,6})\s", ln)
            if m:
                level = len(m.group(1))
            elif re.match(r"\s*câu\s*\d", ln):
                level = 3
            elif re.match(r"\s*\*\*", ln) and not prev.strip():
                level = 7
            else:
                level = None
            if level or not sections:
                sections.append([level or 8, ln])
            else:
                sections[-1][1] += "\n" + ln
            prev = ln

        def strategies(text):
            return {s for s, names in STRATEGY_NAMES.items() if any(n in text for n in names)}

        def asked_for(words):
            found = set()
            for k, (level, text) in enumerate(sections):
                if any(w in text for w in words):
                    own = strategies(text)
                    for j in range(k - 1, -1, -1):
                        if own:
                            break
                        if sections[j][0] < level:
                            level = sections[j][0]
                            own = strategies(sections[j][1])
                    found |= own
            return found

        matched_bai = []
        for bai, words in BAI_KEYWORDS.items():
            if any(w in problem_lower for w in words):
                asked = asked_for(words)
                if not asked or BAI_STRATEGY[bai] in asked:
                    matched_bai.append(words)
        bai_words = {w for words in matched_bai for w in words}

        def by_relevance(seg: dict) -> int:
            return seg.get("relevance_score", 0)

        if not matched_topics and not bai_words:
            # KB không sort sẵn theo relevance_score nên phải sort ở đây
            return sorted(segments, key=by_relevance, reverse=True)[:top_k]

        search_words = {w for t in matched_topics for w in TOPIC_KEYWORDS[t]}
        scored = []
        for seg in segments:
            seg_lower = seg["content"].lower()
            # Ưu tiên đoạn cô chữa đúng bài, rồi đoạn phủ nhiều chủ đề, rồi nhiều từ khoá
            bai_hits = sum(1 for w in bai_words if w in seg_lower)
            topic_hits = sum(
                1 for t in matched_topics
                if any(w in seg_lower for w in TOPIC_KEYWORDS[t])
            )
            word_hits = sum(1 for w in search_words if w in seg_lower)
            if bai_hits or word_hits:
                scored.append((bai_hits, topic_hits, word_hits, by_relevance(seg), seg))

        scored.sort(key=lambda x: x[:4], reverse=True)
        return [s[4] for s in scored[:top_k]]

    def _clean_response(self, response_text: str) -> str:
        """Loại bỏ markdown code fences nếu model trả về."""
        text = response_text.strip()

        # Remove ```latex ... ``` wrapper
        if text.startswith("```latex"):
            text = text[len("```latex"):].strip()
        elif text.startswith("```"):
            text = text[3:].strip()

        if text.endswith("```"):
            text = text[:-3].strip()

        # Remove preamble if model accidentally includes it
        if r'\documentclass' in text:
            # Try to extract just the body
            body_match = re.search(
                r'\\begin\{document\}(.+?)\\end\{document\}',
                text, re.DOTALL
            )
            if body_match:
                text = body_match.group(1).strip()
                # Remove \maketitle and \thispagestyle
                text = re.sub(r'\\maketitle\s*', '', text)
                text = re.sub(r'\\thispagestyle\{[^}]+\}\s*', '', text)

        return _fix_tabular_columns(text)

    def solve_interactive(self) -> None:
        """Chế độ tương tác: nhập đề bài từ terminal."""
        print("=" * 60)
        print("🎓 CoThuong-AI — Giải bài tập thuật toán")
        print(f"   Model: {self.config.model}")
        print("   Nhập đề bài (Enter 2 lần để gửi, 'quit' để thoát)")
        print("=" * 60)

        while True:
            print("\n📝 Đề bài:")
            lines = []
            empty_count = 0
            eof = False
            while True:
                try:
                    line = input()
                except EOFError:
                    eof = True
                    break
                if line.strip() == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    lines.append(line)
                else:
                    empty_count = 0
                    if line.strip().lower() == "quit":
                        print("👋 Tạm biệt!")
                        return
                    lines.append(line)

            problem = "\n".join(lines).strip()
            if not problem:
                if eof:
                    # Ctrl-D ở dòng trống hoặc hết stdin (pipe, file): thoát. Nếu quay lại
                    # vòng lặp thì stdin pipe trả EOF ngay, in "Đề bài:" mãi không dừng.
                    print("👋 Tạm biệt!")
                    return
                continue

            try:
                result = self.solve(problem, wrap_template=False)
                print("\n" + "=" * 60)
                print("📄 LỜI GIẢI:")
                print("=" * 60)
                print(result)
            except Exception as e:
                print(f"\n❌ Lỗi: {e}")
