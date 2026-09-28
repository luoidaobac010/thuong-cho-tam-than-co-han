"""
Unit test offline cho core/ (không gọi agy/Gemini thật, không tốn quota).

Chạy: python3 -m unittest discover -s tests -v
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from core import solver as solver_mod
from core.config import DEFAULT_MODELS, LLMConfig, load_config
from core.persona import get_system_prompt
from core.solver import CoThuongSolver, _escape_latex

KB_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"


def make_agy_solver(**kwargs) -> CoThuongSolver:
    """Tạo solver provider agy mà không cần agy cài trên máy."""
    with mock.patch("core.config.shutil.which", return_value="/usr/bin/agy"):
        return CoThuongSolver(config=LLMConfig(provider="agy"), **kwargs)


class EscapeLatexTest(unittest.TestCase):
    def test_escapes_all_special_chars(self):
        self.assertEqual(
            _escape_latex(r"a^2 b_i & 50% $x$ #1 {y} ~z \cmd"),
            r"a\textasciicircum{}2 b\_i \& 50\% \$x\$ \#1 \{y\} "
            r"\textasciitilde{}z \textbackslash{}cmd",
        )

    def test_plain_vietnamese_unchanged(self):
        self.assertEqual(_escape_latex("Chứng minh thuộc Theta"), "Chứng minh thuộc Theta")

    def test_backslash_not_double_escaped(self):
        # "\" phải thành \textbackslash{} chứ không bị escape tiếp phần {}
        self.assertEqual(_escape_latex("\\"), r"\textbackslash{}")


class CleanResponseTest(unittest.TestCase):
    def setUp(self):
        self.s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))

    def test_strips_latex_fence(self):
        self.assertEqual(self.s._clean_response("```latex\n\\section{A}\n```"), "\\section{A}")

    def test_strips_plain_fence(self):
        self.assertEqual(self.s._clean_response("```\nabc\n```"), "abc")

    def test_extracts_body_from_full_document(self):
        doc = "\\documentclass{article}\n\\begin{document}\n\\maketitle\nBODY\n\\end{document}"
        self.assertEqual(self.s._clean_response(doc), "BODY")


class ConfigTest(unittest.TestCase):
    def test_default_provider_is_agy(self):
        c = LLMConfig()
        self.assertEqual(c.provider, "agy")
        self.assertEqual(c.model, DEFAULT_MODELS["agy"])

    def test_agy_does_not_need_api_key(self):
        with mock.patch("core.config.shutil.which", return_value="/usr/bin/agy"):
            LLMConfig(provider="agy").validate()  # không raise

    def test_agy_missing_binary_raises(self):
        with mock.patch("core.config.shutil.which", return_value=None):
            with self.assertRaisesRegex(ValueError, "antigravity-cli"):
                LLMConfig(provider="agy").validate()

    def test_gemini_requires_api_key(self):
        with mock.patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            with self.assertRaisesRegex(ValueError, "API key"):
                LLMConfig(provider="gemini").validate()

    def test_env_provider_switch_resets_model(self):
        env = {"COTHUONG_PROVIDER": "gemini", "COTHUONG_MODEL": "", "GEMINI_API_KEY": ""}
        with mock.patch.dict(os.environ, env), \
                mock.patch("core.config.get_default_config_path", return_value=Path("/nonexistent")):
            c = load_config()
        self.assertEqual((c.provider, c.model), ("gemini", DEFAULT_MODELS["gemini"]))

    def test_env_provider_case_insensitive(self):
        env = {"COTHUONG_PROVIDER": " Gemini ", "COTHUONG_MODEL": "", "GEMINI_API_KEY": ""}
        with mock.patch.dict(os.environ, env), \
                mock.patch("core.config.get_default_config_path", return_value=Path("/nonexistent")):
            c = load_config()
        self.assertEqual((c.provider, c.model), ("gemini", DEFAULT_MODELS["gemini"]))


def fake_run(stdout: str, returncode: int = 0, stderr: str = ""):
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)


class CallAgyTest(unittest.TestCase):
    def setUp(self):
        self.s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))

    def _call(self, completed):
        with mock.patch.object(solver_mod.subprocess, "run", return_value=completed) as run:
            out = self.s._call_agy("PROMPT")
        return out, run

    def test_success_returns_structured_latex_body(self):
        payload = {"status": "SUCCESS", "response": "raw",
                   "structured_output": {"latex_body": "\\frac{1}{2}"}}
        out, run = self._call(fake_run(json.dumps(payload)))
        self.assertEqual(out, "\\frac{1}{2}")

        cmd = run.call_args.args[0]
        kwargs = run.call_args.kwargs
        self.assertEqual(cmd[0], "agy")
        self.assertIn("--sandbox", cmd)
        self.assertNotIn("--dangerously-skip-permissions", cmd)
        self.assertEqual(cmd[cmd.index("--output-format") + 1], "json")
        self.assertEqual(cmd[cmd.index("--model") + 1], DEFAULT_MODELS["agy"])
        # persona được ghép vào đầu prompt
        prompt = cmd[cmd.index("-p") + 1]
        self.assertTrue(prompt.startswith(self.s.system_prompt))
        self.assertTrue(prompt.endswith("PROMPT"))
        # chạy trong thư mục tạm, không phải repo
        self.assertIn("cothuong-agy-", kwargs["cwd"])

    def test_falls_back_to_response_without_structured_output(self):
        out, _ = self._call(fake_run(json.dumps({"status": "SUCCESS", "response": "RAW"})))
        self.assertEqual(out, "RAW")

    def test_error_status_raises_with_message(self):
        payload = {"status": "ERROR", "error": "model not recognized"}
        with self.assertRaisesRegex(RuntimeError, "model not recognized"):
            self._call(fake_run(json.dumps(payload), returncode=1))

    def test_non_json_output_raises(self):
        with self.assertRaisesRegex(RuntimeError, "không phải JSON"):
            self._call(fake_run("", returncode=1, stderr="authentication required"))

    def test_denied_tool_with_empty_output_raises_clear_error(self):
        # Output thật khi model cố chạy python ở headless mode
        payload = {"status": "SUCCESS", "response": "",
                   "denied_actions": [{"action": "command", "display_name": "RunCommand"}]}
        with self.assertRaisesRegex(RuntimeError, "tool bị chặn"):
            self._call(fake_run(json.dumps(payload)))


class SolveWrapTest(unittest.TestCase):
    def test_title_with_special_chars_is_escaped(self):
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        with mock.patch.object(s, "_call_agy", return_value="\\section{X}"):
            doc = s.solve("CM n^2 + a_i thuộc Theta(n^2)")
        self.assertIn(r"n\textasciicircum{}2 + a\_i", doc)
        self.assertIn("\\section{X}", doc)

    def test_text_prompt_forbids_shell_commands(self):
        # 4/19 lần gọi agy thật dừng vì model chạy `ls -la` ở bước đầu, headless từ chối
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        prompt = s._build_user_prompt("Tìm LCS của X = ACB và Y = CB")
        self.assertIn("KHÔNG chạy lệnh shell/python, kể cả `ls`", prompt)


class SolveInteractiveTest(unittest.TestCase):
    """Hết stdin (pipe, Ctrl-D) mà chưa nhập gì thì thoát, không in "Đề bài:" mãi."""

    def run_with(self, *inputs):
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        feed = iter(inputs)
        eofs = []

        def fake_input():
            try:
                return next(feed)
            except StopIteration:
                eofs.append(1)
                if len(eofs) > 3:  # báo lỗi thay vì để test treo
                    raise AssertionError("vẫn gọi input() sau EOF, vòng lặp không dừng") from None
                raise EOFError from None

        with mock.patch("builtins.input", side_effect=fake_input), \
             mock.patch.object(s, "_call_agy", return_value="\\section{X}") as agy, \
             mock.patch("builtins.print") as out:
            s.solve_interactive()
        prompts = sum("Đề bài:" in str(c.args[0]) for c in out.call_args_list if c.args)
        return agy.call_count, prompts

    def test_eof_after_one_problem_solves_then_exits(self):
        self.assertEqual(self.run_with("Tô màu đồ thị bằng quay lui", "", ""), (1, 2))

    def test_eof_with_unfinished_problem_still_solves_it(self):
        self.assertEqual(self.run_with("Tô màu đồ thị bằng quay lui"), (1, 2))

    def test_eof_right_away_exits(self):
        self.assertEqual(self.run_with(), (0, 1))

    def test_quit_still_works(self):
        self.assertEqual(self.run_with("quit"), (0, 1))


class FixTabularTest(unittest.TestCase):
    """Lỗi thật từ agy: khai 7 cột nhưng hàng có 8 ô -> XeTeX dừng, không ra PDF."""

    def test_adds_missing_column_keeps_border_style(self):
        src = "\\begin{tabular}{|c|c|}\n a & b & c \\\\\n\\end{tabular}"
        self.assertIn("{|c|c|c|}", solver_mod._fix_tabular_columns(src))

    def test_no_border_spec(self):
        src = "\\begin{tabular}{cc|c}\n a & b & c & d \\\\\n\\end{tabular}"
        self.assertIn("{cc|cc}", solver_mod._fix_tabular_columns(src))

    def test_correct_table_untouched_including_p_width_and_escaped_amp(self):
        src = "\\begin{tabular}{p{3cm}c}\n A \\& B & c \\\\\n\\end{tabular}"
        self.assertEqual(solver_mod._fix_tabular_columns(src), src)

    def test_clean_response_applies_fix(self):
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        out = s._clean_response("\\begin{tabular}{c}\n1 & 2 \\\\\n\\end{tabular}")
        self.assertIn("{cc}", out)


class FixEnvNestingTest(unittest.TestCase):
    """Lỗi thật từ agy (2/32 output): mở \\[ rồi viết \\end{enumerate} thay cho \\], các \\end
    sau đó lệch 1 bậc -> tectonic báo "\\begin{enumerate} ended by \\end{itemize}"."""

    def fix(self, text):
        return solver_mod._fix_env_nesting(text)

    def test_end_written_instead_of_display_math_close(self):
        # rút gọn từ output thật agy3/R05 dòng 130-147
        src = ("\\begin{itemize}\n\\item B2:\n\\begin{enumerate}\n\\item Tập màu cấm:\n\\[\nU = \\{c\\}\n"
               "\\end{enumerate}\n\\item Tìm màu nhỏ nhất.\n\\end{itemize}\n\\item B3.\n\\end{itemize}")
        want = ("\\begin{itemize}\n\\item B2:\n\\begin{enumerate}\n\\item Tập màu cấm:\n\\[\nU = \\{c\\}\n"
                "\\]\n\\item Tìm màu nhỏ nhất.\n\\end{enumerate}\n\\item B3.\n\\end{itemize}")
        self.assertEqual(self.fix(src), want)

    def test_correct_latex_untouched(self):
        src = ("\\title{A\\\\[6pt] B}\n\\begin{itemize}\n\\item Lãi 50\\% % ghi chú \\end{itemize}\n"
               "\\item $\\begin{cases} 0 \\\\ 1 \\end{cases}$\n\\[ x \\]\n\\end{itemize}\n"
               "\\begin{lstlisting}\nif a: \\end{itemize}\n\\end{lstlisting}")
        self.assertEqual(self.fix(src), src)

    def test_stray_end_dropped_and_unclosed_closed(self):
        self.assertEqual(self.fix("a\n\\end{itemize}\nb"), "a\n\nb")
        self.assertEqual(self.fix("\\begin{itemize}\n\\item a\n\\[ x"), "\\begin{itemize}\n\\item a\n\\[ x\n\\]\n\\end{itemize}")

    def test_repo_latex_samples_untouched(self):
        for p in (Path(__file__).resolve().parent.parent / "data").glob("*.tex"):
            text = p.read_text(encoding="utf-8")
            self.assertEqual(self.fix(text), text, p.name)

    @unittest.skipUnless(shutil.which("tectonic"), "cần tectonic")
    def test_fixed_output_compiles(self):
        import solve
        from core.latex_template import wrap_in_template
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        body = ("\\begin{itemize}\n\\item B2:\n\\begin{enumerate}\n\\item Tập màu cấm:\n\\[\nU = \\{c\\}\n"
                "\\end{enumerate}\n\\item Tìm màu nhỏ nhất.\n\\end{itemize}\n\\item B3.\n\\end{itemize}")
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "t.tex"
            tex.write_text(wrap_in_template(s._clean_response(body), title="Bài thử"), encoding="utf-8")
            with mock.patch("builtins.print"):
                self.assertTrue(solve.compile_pdf(tex))


class ParsePagesTest(unittest.TestCase):
    def test_all_when_empty(self):
        self.assertEqual(solver_mod.parse_pages(None, 3), [0, 1, 2])

    def test_ranges_and_dedup(self):
        self.assertEqual(solver_mod.parse_pages("2-3, 1,3", 5), [1, 2, 0])

    def test_out_of_range_raises(self):
        with self.assertRaisesRegex(ValueError, "ngoài phạm vi"):
            solver_mod.parse_pages("4", 3)

    def test_reversed_range_raises_instead_of_empty(self):
        # Trước đây '3-1' ra [] rồi vẫn gọi agy ~2 phút không giải trang nào
        with self.assertRaisesRegex(ValueError, "bị ngược, viết 1-3"):
            solver_mod.parse_pages("3-1", 4)

    def test_garbage_gives_friendly_error(self):
        for spec in ["a", "2-", "1,,x"]:
            with self.assertRaisesRegex(ValueError, "không hợp lệ"):
                solver_mod.parse_pages(spec, 4)

    def test_only_commas_selects_nothing(self):
        with self.assertRaisesRegex(ValueError, "không chọn trang nào"):
            solver_mod.parse_pages(",", 4)


def _has_pymupdf() -> bool:
    try:
        import pymupdf  # noqa: F401
        return True
    except ImportError:
        return False


@unittest.skipUnless(_has_pymupdf(), "cần pymupdf")
class SolvePdfTest(unittest.TestCase):
    """PDF thật -> ảnh được ghi vào thư mục tạm của agy, retrieval dùng text trích."""

    def setUp(self):
        import pymupdf
        self.tmp = tempfile.TemporaryDirectory()
        self.pdf = Path(self.tmp.name) / "de.pdf"
        doc = pymupdf.open()
        for text in ["Trang bia", "Bai 1: quy hoach dong cai tui"]:
            doc.new_page().insert_text((72, 72), text)
        doc.save(self.pdf)
        self.addCleanup(self.tmp.cleanup)

    def test_images_written_to_agy_cwd(self):
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        seen = {}

        def fake(cmd, cwd, **kw):
            seen["files"] = sorted(p.name for p in Path(cwd).iterdir())
            seen["png"] = (Path(cwd) / "page_02.png").read_bytes()[:8]
            seen["prompt"] = cmd[cmd.index("-p") + 1]
            payload = {"status": "SUCCESS", "structured_output": {"latex_body": "\\section{B1}"}}
            return fake_run(json.dumps(payload))

        with mock.patch.object(solver_mod.subprocess, "run", side_effect=fake), \
                mock.patch("builtins.print"):
            doc = s.solve_pdf(self.pdf, pages="2")

        self.assertEqual(seen["files"], ["page_02.png"])
        self.assertEqual(seen["png"], b"\x89PNG\r\n\x1a\n")
        self.assertIn("page_02.png", seen["prompt"])
        self.assertIn("\\section{B1}", doc)
        self.assertIn("Bài giải: de", doc)

    def test_gemini_not_supported(self):
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        s.config.provider = "gemini"
        with self.assertRaisesRegex(ValueError, "chỉ hỗ trợ provider agy"):
            s.solve_pdf(self.pdf)


EXAMS_DIR = Path(__file__).resolve().parent.parent / "bai_tap" / "Đề thi mẫu"


@unittest.skipUnless(_has_pymupdf(), "cần PyMuPDF")
class PdfRetrievalTextTest(unittest.TestCase):
    """Chữ PDF gửi retrieval: tách chữ dính, nối dòng bị bẻ, dòng đậm đầu block thành tiêu đề."""

    def make_pdf(self, lines):
        """lines: [(chữ, cỡ, đậm)], mỗi dòng 1 block riêng. Chữ nhập từng từ để điều khiển khoảng hở."""
        import pymupdf
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "de.pdf"
        doc = pymupdf.open()
        page = doc.new_page()
        y = 60
        for text, size, bold in lines:
            page.insert_text((72, y), text, fontsize=size, fontname="hebo" if bold else "helv")
            y += size * 2.5
        doc.save(path)
        return path

    def test_heading_bold_bigger_becomes_markdown_heading(self):
        # font helv không có dấu tiếng Việt nên dùng chữ không dấu ("Câu N" có dấu: test PDF thật bên dưới)
        path = self.make_pdf([("PHAN 2: QUAY LUI", 14, True), ("Muc 4 (2 diem) Thiet ke", 10, True),
                              ("Liet ke moi cach to mau", 10, False), ("Tong ket", 10, True), ("than bai", 10, False)])
        text = solver_mod.render_pdf_pages(path)[1]
        self.assertEqual(text.splitlines()[0], "# PHAN 2: QUAY LUI")
        # đậm cỡ bằng chữ thân -> dòng in đậm sau dòng trống (cách _find_relevant_segments chia mục)
        self.assertIn("\n\n**Muc 4 (2 diem) Thiet ke**\nLiet ke moi cach to mau\n", text)
        self.assertIn("\n\n**Tong ket**\nthan bai", text)

    def test_lowercase_line_joins_previous(self):
        self.assertEqual(solver_mod._join(["Thiết kế theo phương pháp Quay", "lui cho bài", "Câu 5"]),
                         ["Thiết kế theo phương pháp Quay lui cho bài", "Câu 5"])
        self.assertEqual(solver_mod._join(["Dynamic Program-", "ming - MCM"]), ["Dynamic Programming - MCM"])

    @unittest.skipUnless((EXAMS_DIR / "De_Thi_Va_Cau_Truc_PTTKTT_Co_Thuong_Buoi_9.pdf").exists(), "cần PDF đề buổi 9")
    def test_real_pdf_glued_words_split(self):
        # get_text() trả "Chia đểtrị", "Thiết kếthuật" nên từ khoá "chia để trị" không khớp
        pdf = EXAMS_DIR / "De_Thi_Va_Cau_Truc_PTTKTT_Co_Thuong_Buoi_9.pdf"
        text = solver_mod.render_pdf_pages(pdf, "3")[1]
        self.assertIn("chia để trị", text.lower())
        self.assertIn("thiết kế thuật toán", text.lower())
        self.assertNotIn("đểtrị", text.lower())
        lines = text.splitlines()
        self.assertIn("## PHẦN II: THIẾT KẾ THUẬT TOÁN (6.0 ĐIỂM)", lines)
        self.assertIn("Câu 4: Triển khai Mã giả thuật toán & Đánh giá (2.0 điểm)", lines)

    @unittest.skipUnless((EXAMS_DIR / "Ôn Luyện/Chuyen_De_Thuat_Toan_Quay_Lui_Backtracking.pdf").exists(),
                         "cần PDF chuyên đề quay lui")
    def test_real_pdf_headings_rebuilt(self):
        pdf = EXAMS_DIR / "Ôn Luyện/Chuyen_De_Thuat_Toan_Quay_Lui_Backtracking.pdf"
        heads = [ln for ln in solver_mod.render_pdf_pages(pdf)[1].splitlines() if ln.startswith("#")]
        # chỉ chèn cách giữa 2 chữ cái, "THỊ(" giữ nguyên như PDF
        self.assertIn("## DẠNG 9: BÀI TOÁN TÔ MÀU ĐỒ THỊ(M-COLORING PROBLEM)", heads)
        # tiêu đề bị bẻ 2 dòng ("... QUAY" / "LUI") được nối lại
        self.assertIn("# PHẦN 3: BẢNG TỔNG HỢP SO SÁNH ĐỘ PHỨC TẠP CÁC BÀI TOÁN QUAY LUI", heads)


@unittest.skipUnless(KB_PATH.exists(), "cần data/knowledge_base.json")
class RetrievalTest(unittest.TestCase):
    """Đề thuộc chủ đề nào thì phải lấy đoạn transcript của buổi dạy chủ đề đó."""

    @classmethod
    def setUpClass(cls):
        cls.s = make_agy_solver()

    def buoi(self, problem):
        return {seg["buoi"] for seg in self.s._find_relevant_segments(problem)}

    def lines(self, problem):
        # Mỗi đoạn trong buoi*_clean.md là 1 dòng, các đoạn cách nhau 1 dòng trống
        return [(seg["buoi"], 2 * seg["paragraph_index"] + 1)
                for seg in self.s._find_relevant_segments(problem)]

    def assert_from_lesson(self, problem, ranges):
        """Cả 3 đoạn phải nằm trong phần cô chữa bài đó: ranges = [(buổi, dòng đầu, dòng cuối)]."""
        got = self.lines(problem)
        self.assertEqual(len(got), 3)
        for buoi, line in got:
            self.assertTrue(any(buoi == b and lo <= line <= hi for b, lo, hi in ranges),
                            f"b{buoi}:{line} không thuộc {ranges}")

    def test_asymptotic(self):
        self.assertLessEqual(self.buoi("Chứng minh 3n^2+5n+2 thuộc Theta(n^2)"), {3, 4, 5})

    def test_dynamic_programming(self):
        # Buổi 10 ôn lại quy hoạch động (b10:175-325)
        self.assertLessEqual(self.buoi("Giải bài toán cái túi bằng quy hoạch động"), {8, 9, 10})

    def test_backtracking_english_maps_to_vietnamese(self):
        self.assertLessEqual(self.buoi("Solve N-Queens using backtracking"), {6, 7, 8})

    def test_greedy(self):
        self.assertLessEqual(self.buoi("Thuật toán tham lam cho ba lô phân số"), {7, 8, 9})

    def test_activity_selection_uses_lesson(self):
        # Chép từ đề dự thảo buổi 9, Bài toán 3.2
        self.assert_from_lesson(
            "Bài toán Lựa chọn công việc (Activity Selection) - Cho n công việc với thời gian "
            "bắt đầu s_i và kết thúc f_i. Tìm tập công việc tương thích tối đa bằng chiến lược "
            "Tham lam (Greedy).", [(10, 109, 173)])
        # Chép từ mock_exam_pttktt.md câu 4a: không có chữ "hoạt động", "tương thích"
        self.assert_from_lesson(
            "Dựa trên ý tưởng ở Câu 3, hãy viết Mã giả (Pseudo-code) hoàn chỉnh cho bài toán "
            "Xếp lịch họp. Đánh số bước rõ ràng.", [(10, 109, 173)])

    def test_map_coloring_uses_lesson(self):
        self.assert_from_lesson("Tô màu bản đồ bằng tham lam sao cho số màu ít nhất",
                                [(10, 51, 107)])

    def test_matrix_chain_uses_lesson(self):
        self.assert_from_lesson(
            "Nhân chuỗi ma trận (Matrix Chain Multiplication - MCM): điền bảng m và bảng s",
            [(9, 323, 443), (10, 183, 233)])

    def test_lcs_uses_lesson(self):
        self.assert_from_lesson("Tìm dãy con chung dài nhất (LCS) của hai chuỗi X và Y",
                                [(10, 235, 325)])

    def test_lesson_alternative_names(self):
        # Cách ghi theo CLRS (có gạch nối) và "dãy ma trận" thay cho "chuỗi ma trận"
        for problem, ranges in [
            ("Viết mã giả GREEDY-ACTIVITY-SELECTOR(s, f) và phân tích độ phức tạp.", [(10, 109, 173)]),
            ("Matrix-chain multiplication: compute m[i][j] and s[i][j].", [(9, 323, 443), (10, 183, 233)]),
            ("Bài toán nhân dãy ma trận: tìm cách đặt dấu ngoặc để số phép nhân ít nhất.",
             [(9, 323, 443), (10, 183, 233)]),
        ]:
            with self.subTest(problem=problem[:40]):
                self.assert_from_lesson(problem, ranges)

    def test_matrix_chain_with_compatible_sizes_is_not_activity_selection(self):
        # Đề nhân chuỗi ma trận hay ghi "kích thước tương thích": không được lấy bài chọn hoạt động
        self.assert_from_lesson(
            "Cho chuỗi 4 ma trận có kích thước tương thích p = (10, 20, 5, 15, 30). "
            "Tìm cách đặt ngoặc sao cho số phép nhân vô hướng ít nhất.",
            [(9, 323, 443), (10, 183, 233)])

    def test_other_strategy_skips_lesson(self):
        # Mục "Dạng 9: tô màu đồ thị" trong tài liệu quay lui: cô chữa tô màu bằng tham lam
        # (b10:51-107), đề hỏi quay lui thì phải lấy đoạn dạy quay lui (buổi 6-8)
        got = self.lines("Tô màu đồ thị bằng quay lui (m-coloring): mỗi đỉnh 1 trong m màu, "
                         "hai đỉnh kề khác màu")
        self.assertEqual(len(got), 3)
        self.assertFalse([x for x in got if x[0] == 10 and 51 <= x[1] <= 107], got)
        self.assertLessEqual({b for b, _ in got}, {6, 7, 8})
        # Đề ghi đúng chiến lược cô dùng thì vẫn lấy bài cô chữa
        self.assert_from_lesson("Tô màu đồ thị bằng thuật toán tham lam, dùng ít màu nhất",
                                [(10, 51, 107)])

    def test_every_lesson_has_strategy(self):
        self.assertEqual(set(solver_mod.BAI_STRATEGY), set(solver_mod.BAI_KEYWORDS))
        self.assertLessEqual(set(solver_mod.BAI_STRATEGY.values()), set(solver_mod.STRATEGY_NAMES))

    def test_strategy_of_next_section_keeps_lesson(self):
        # Tờ A4 (Đề cương đem theo, mục 6): LCS xong là tới tiêu đề "## 3. THAM LAM" của mục sau.
        # Tên chiến lược nằm xa tên bài thì không được làm mất đoạn cô chữa LCS
        self.assert_from_lesson(
            "- **(6) Dãy con chung dài nhất LCS ($|X| = n, |Y| = m$):** $c[i][j] = c[i-1][j-1] + 1$ "
            "nếu $x_i = y_j$, ngược lại $\\max(c[i-1][j], c[i][j-1])$. Cơ sở $c[i][0] = c[0][j] = 0$, "
            "đáp án ở ô cuối $c[n][m]$. Truy vết: bằng nhau thì ghi ký tự rồi đi chéo, "
            "khác nhau thì đi về ô lớn hơn.\n\n## 3. THAM LAM (GREEDY) - BA LÔ PHÂN SỐ",
            [(10, 235, 325)])

    def test_strategy_of_other_question_keeps_lesson(self):
        # Trang đề có 2 câu: câu 4 ghi quay lui, câu 5 nhân chuỗi ma trận không ghi chiến lược.
        # Chiến lược của câu 4 không được làm mất đoạn cô chữa nhân chuỗi ma trận
        self.assert_from_lesson(
            "### Câu 4 (2.0 điểm) Thiết kế thuật toán Quay lui\n"
            "Liệt kê tất cả hoán vị của n phần tử.\n\n"
            "### Câu 5 (2.0 điểm) Thiết kế thuật toán\n"
            "Cho dãy 4 ma trận A1 (5 x 6), A2 (6 x 7), A3 (7 x 2), A4 (2 x 3). "
            "Tìm cách nhân chuỗi ma trận với số phép nhân vô hướng ít nhất.",
            [(9, 323, 443), (10, 183, 233)])

    def test_bold_line_follows_its_heading(self):
        # Dòng in đậm ngay dưới tiêu đề, hoặc ý a) in đậm sau dòng trống, thuộc câu có tiêu đề đó:
        # tiêu đề ghi quay lui thì không lấy đoạn cô chữa tô màu bằng tham lam
        for problem in (
            ("## Câu 4 (2.0 điểm): Thiết kế thuật toán Quay lui\n**Bài toán: Tô màu đồ thị**\n"
             "Cho đồ thị G gồm n đỉnh và m màu. Liệt kê mọi cách tô."),
            ("### Câu 4 (2.0 điểm) Thiết kế thuật toán Quay lui\n\n"
             "**a) (1.0đ)** Liệt kê mọi cách tô màu đồ thị G bằng m màu."),
        ):
            got = self.lines(problem)
            self.assertFalse([x for x in got if x[0] == 10 and 51 <= x[1] <= 107], got)
        # Dòng in đậm sau dòng trống ở ngoài cùng là mục mới: chiến lược của nó không làm mất bài
        got = self.lines("- Tô màu bản đồ: mỗi bước chọn đỉnh bậc cao nhất, thử các màu đã dùng.\n\n"
                         "**Quay lui** (b6:157-209)\n- Mô hình Try(i): thử ứng viên, gọi Try(i+1), hoàn tác.")
        self.assertGreaterEqual(sum(1 for b, ln in got if b == 10 and 51 <= ln <= 107), 2, got)

    def test_square_matrix_product_is_not_matrix_chain(self):
        # "ma trận" không phải tên bài: câu đếm phép nhân 2 ma trận vuông không lấy bài nhân chuỗi ma trận
        got = self.lines("Đếm số phép nhân của giải thuật nhân hai ma trận vuông A, B kích thước n x n")
        self.assertFalse([x for x in got if (x[0] == 9 and 323 <= x[1] <= 443)
                          or (x[0] == 10 and 183 <= x[1] <= 233)])

    def test_no_match_falls_back_to_top_relevance(self):
        segs = self.s._find_relevant_segments("in hello world")
        self.assertEqual(len(segs), 3)
        top = max(x["relevance_score"] for x in self.s.knowledge_base["teaching_segments"])
        self.assertEqual(segs[0]["relevance_score"], top)


class PersonaTest(unittest.TestCase):
    def test_covers_all_exam_topics(self):
        p = get_system_prompt()
        for heading in ["Quy hoạch động", "Tham lam", "Quay lui", "Chia để trị"]:
            self.assertIn(heading, p)

    def test_example_includes_definition_proof(self):
        self.assertIn("c_1 = \\frac{1}{3}", get_system_prompt())


@unittest.skipUnless(shutil.which("tectonic"), "cần tectonic")
class CompilePdfTest(unittest.TestCase):
    """Dùng tectonic thật. Lần đầu trên máy mới có thể chậm do tải package."""

    def _compile(self, content: str):
        import solve
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp) / "t.tex"
            tex.write_text(content, encoding="utf-8")
            with mock.patch("builtins.print"):
                ok = solve.compile_pdf(tex)
            return ok, tex.with_suffix(".pdf").exists()

    def test_valid_document_produces_pdf(self):
        ok, has_pdf = self._compile(
            "\\documentclass{article}\\begin{document}Xin chào $n^2$\\end{document}"
        )
        self.assertTrue(ok)
        self.assertTrue(has_pdf)

    def test_broken_document_returns_false(self):
        ok, _ = self._compile("\\documentclass{article}\\begin{document}\\title{n^2}\\end{document}")
        self.assertFalse(ok)

    def test_template_has_multirow(self):
        # Lỗi thật: model điền bảng LCS bằng \multirow, template thiếu gói -> "Undefined control sequence"
        from core.latex_template import wrap_in_template
        body = "\\begin{tabular}{|c|c|}\\hline \\multirow{2}{*}{$M[i][j]$} & 1 \\\\ & 2 \\\\ \\hline\\end{tabular}"
        ok, has_pdf = self._compile(wrap_in_template(body, title="Bài thử"))
        self.assertTrue(ok)
        self.assertTrue(has_pdf)


class CleanVttCliTest(unittest.TestCase):
    """data/clean_vtt.py: trước đây '--help' bị coi là tên file -> FileNotFoundError."""

    SCRIPT = Path(__file__).resolve().parent.parent / "data" / "clean_vtt.py"

    def _run(self, *args, cwd=None):
        import sys
        return subprocess.run([sys.executable, str(self.SCRIPT), *args],
                              capture_output=True, text=True, cwd=cwd)

    def test_help(self):
        p = self._run("--help")
        self.assertEqual(p.returncode, 0)
        self.assertIn("usage", p.stdout.lower())

    def test_missing_file_clear_error(self):
        p = self._run("khong_ton_tai.vtt")
        self.assertEqual(p.returncode, 1)
        self.assertIn("Không tìm thấy file", p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_cleans_given_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            vtt = Path(tmp) / "buoi1.vi.vtt"
            vtt.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nXin chào\n"
                           "00:00:01.000 --> 00:00:02.000\nXin chào\n", encoding="utf-8")
            p = self._run(str(vtt))
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual((Path(tmp) / "buoi1_clean.md").read_text(encoding="utf-8"), "Xin chào")


# Lỗi thật gặp khi E2E: model quên đóng \[ trước \end{itemize}
BROKEN_DISPLAY_MATH = (
    "\\documentclass{article}\n\\begin{document}\n\\begin{itemize}\n"
    "\\item A:\n\\[\n  f(n) \\le c \\cdot g(n).\n\\end{itemize}\n\\end{document}\n"
)
FIXED_SNIPPET = (
    "\\documentclass{article}\n\\begin{document}\n\\begin{itemize}\n"
    "\\item A:\n\\[\n  f(n) \\le c \\cdot g(n).\n\\]\n\\end{itemize}\n\\end{document}"
)


class ParseLatexErrorTest(unittest.TestCase):
    def test_tectonic_format(self):
        import solve
        log = "note: x\nerror: de01.tex:106: LaTeX Error: Command \\end{equation*} invalid in math mode.\n"
        self.assertEqual(solve.parse_latex_error(log),
                         (106, "LaTeX Error: Command \\end{equation*} invalid in math mode."))

    def test_xelatex_format(self):
        import solve
        log = "! Extra alignment tab has been changed to \\cr.\n<template> \\endtemplate\nl.63 ... & $B$\n"
        self.assertEqual(solve.parse_latex_error(log),
                         (63, "Extra alignment tab has been changed to \\cr."))

    def test_no_error(self):
        import solve
        self.assertIsNone(solve.parse_latex_error("note: Writing `x.pdf`"))


class FixLatexErrorTest(unittest.TestCase):
    def setUp(self):
        self.s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))

    def test_splices_fixed_snippet_and_skips_persona(self):
        tex = "\n".join(f"L{i}" for i in range(1, 101))  # 100 dòng
        seen = {}

        def fake(prompt, files=None, persona=True):
            seen["prompt"], seen["persona"] = prompt, persona
            return "<<<\n" + "\n".join(f"F{i}" for i in range(30, 61)) + "\n>>>"

        with mock.patch.object(self.s, "_call_agy", side_effect=fake):
            out = self.s.fix_latex_error(tex, 50, "Missing $", before=20, after=10)

        self.assertFalse(seen["persona"])
        self.assertIn("L30", seen["prompt"])
        self.assertIn("L60", seen["prompt"])
        self.assertNotIn("L29\n", seen["prompt"])
        lines = out.split("\n")
        self.assertEqual(lines[:29], [f"L{i}" for i in range(1, 30)])  # trước đoạn giữ nguyên
        self.assertEqual(lines[29], "F30")
        self.assertEqual(lines[-40:], [f"L{i}" for i in range(61, 101)])  # sau đoạn giữ nguyên

    def test_rejects_truncated_answer(self):
        tex = "\n".join(f"line number {i}" for i in range(1, 60))
        with mock.patch.object(self.s, "_call_agy", return_value="x"):
            self.assertIsNone(self.s.fix_latex_error(tex, 30, "err"))

    def test_line_out_of_range(self):
        self.assertIsNone(self.s.fix_latex_error("a\nb", 99, "err"))


@unittest.skipUnless(shutil.which("tectonic"), "cần tectonic")
class CompileWithFixTest(unittest.TestCase):
    """tectonic thật + agy giả: lỗi -> sửa -> ra PDF, giữ bản gốc .orig.tex."""

    def _run(self, fixed_value):
        import solve
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        tex = Path(tmp.name) / "t.tex"
        tex.write_text(BROKEN_DISPLAY_MATH, encoding="utf-8")
        with mock.patch.object(s, "_call_agy", return_value=fixed_value) as call, \
                mock.patch("builtins.print"):
            ok = solve.compile_pdf_with_fix(tex, s)
        return ok, tex, call

    def test_fix_then_pdf(self):
        ok, tex, call = self._run(FIXED_SNIPPET)
        self.assertTrue(ok)
        self.assertEqual(call.call_count, 1)
        self.assertTrue(tex.with_suffix(".pdf").exists())
        self.assertEqual(tex.with_suffix(".orig.tex").read_text(encoding="utf-8"), BROKEN_DISPLAY_MATH)

    def test_bad_fix_fails_after_one_retry(self):
        ok, tex, call = self._run(BROKEN_DISPLAY_MATH.strip())
        self.assertFalse(ok)
        self.assertEqual(call.call_count, 1)  # chỉ thử sửa đúng 1 lần


if __name__ == "__main__":
    unittest.main()
