"""
solver.py
Engine chính của CoThuong-AI.
Nhận đề bài → Gọi LLM → Sinh lời giải LaTeX theo phong cách cô Thương.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
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
    
    def _call_agy(self, user_prompt: str) -> str:
        """Gọi Antigravity CLI ở headless mode, trả về LaTeX body."""
        # agy không có flag system prompt nên ghép persona vào đầu prompt
        prompt = f"{self.system_prompt}\n\n---\n\n{user_prompt}"
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
            proc = subprocess.run(
                cmd, cwd=tmp, capture_output=True, text=True, encoding="utf-8"
            )
        
        try:
            result = json.loads(proc.stdout)
        except json.JSONDecodeError:
            raise RuntimeError(
                f"❌ agy trả về output không phải JSON (exit={proc.returncode}).\n"
                f"   stderr: {proc.stderr.strip()[:500]}"
            )
        
        if result.get("status") != "SUCCESS":
            raise RuntimeError(
                f"❌ agy lỗi ({result.get('status')}): "
                f"{result.get('error') or proc.stderr.strip()[:500]}\n"
                f"   Nếu chưa đăng nhập: chạy `agy` 1 lần ở terminal."
            )
        
        body = (result.get("structured_output") or {}).get("latex_body")
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
    
    def _build_user_prompt(self, problem: str) -> str:
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
"""
        
        # Thêm teaching context nếu có
        if self.knowledge_base:
            relevant_segments = self._find_relevant_segments(problem)
            if relevant_segments:
                prompt += "\n## CONTEXT TỪ BÀI GIẢNG (để tham khảo phong cách):\n"
                for seg in relevant_segments[:3]:
                    prompt += f"---\n{seg['content'][:500]}\n---\n\n"
        
        return prompt
    
    def _find_relevant_segments(self, problem: str, top_k: int = 3) -> list[dict]:
        """Tìm các đoạn transcript liên quan đến đề bài theo chủ đề."""
        if not self.knowledge_base:
            return []
        
        segments = self.knowledge_base.get("teaching_segments", [])
        problem_lower = problem.lower()
        
        # Chủ đề nào có ít nhất 1 từ khoá xuất hiện trong đề
        matched_topics = [
            topic for topic, words in TOPIC_KEYWORDS.items()
            if any(w in problem_lower for w in words)
        ]
        
        def by_relevance(seg: dict) -> int:
            return seg.get("relevance_score", 0)
        
        if not matched_topics:
            # KB không sort sẵn theo relevance_score nên phải sort ở đây
            return sorted(segments, key=by_relevance, reverse=True)[:top_k]
        
        search_words = {w for t in matched_topics for w in TOPIC_KEYWORDS[t]}
        scored = []
        for seg in segments:
            seg_lower = seg["content"].lower()
            # Ưu tiên đoạn phủ nhiều chủ đề, rồi đến nhiều từ khoá
            topic_hits = sum(
                1 for t in matched_topics
                if any(w in seg_lower for w in TOPIC_KEYWORDS[t])
            )
            word_hits = sum(1 for w in search_words if w in seg_lower)
            if word_hits:
                scored.append((topic_hits, word_hits, by_relevance(seg), seg))
        
        scored.sort(key=lambda x: x[:3], reverse=True)
        return [s[3] for s in scored[:top_k]]
    
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
        import re
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
        
        return text
    
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
            while True:
                try:
                    line = input()
                except EOFError:
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
                continue
            
            try:
                result = self.solve(problem, wrap_template=False)
                print("\n" + "=" * 60)
                print("📄 LỜI GIẢI:")
                print("=" * 60)
                print(result)
            except Exception as e:
                print(f"\n❌ Lỗi: {e}")
