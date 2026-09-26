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


class SolveWrapTest(unittest.TestCase):
    def test_title_with_special_chars_is_escaped(self):
        s = make_agy_solver(knowledge_base_path=Path("/nonexistent"))
        with mock.patch.object(s, "_call_agy", return_value="\\section{X}"):
            doc = s.solve("CM n^2 + a_i thuộc Theta(n^2)")
        self.assertIn(r"n\textasciicircum{}2 + a\_i", doc)
        self.assertIn("\\section{X}", doc)


@unittest.skipUnless(KB_PATH.exists(), "cần data/knowledge_base.json")
class RetrievalTest(unittest.TestCase):
    """Đề thuộc chủ đề nào thì phải lấy đoạn transcript của buổi dạy chủ đề đó."""

    @classmethod
    def setUpClass(cls):
        cls.s = make_agy_solver()

    def buoi(self, problem):
        return {seg["buoi"] for seg in self.s._find_relevant_segments(problem)}

    def test_asymptotic(self):
        self.assertLessEqual(self.buoi("Chứng minh 3n^2+5n+2 thuộc Theta(n^2)"), {3, 4, 5})

    def test_dynamic_programming(self):
        self.assertLessEqual(self.buoi("Giải bài toán cái túi bằng quy hoạch động"), {8, 9})

    def test_backtracking_english_maps_to_vietnamese(self):
        self.assertLessEqual(self.buoi("Solve N-Queens using backtracking"), {6, 7, 8})

    def test_greedy(self):
        self.assertLessEqual(self.buoi("Thuật toán tham lam cho ba lô phân số"), {7, 8, 9})

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


if __name__ == "__main__":
    unittest.main()
