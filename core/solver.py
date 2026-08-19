"""
solver.py
Engine chính của CoThuong-AI.
Nhận đề bài → Gọi LLM → Sinh lời giải LaTeX theo phong cách cô Thương.
"""

import json
import sys
from pathlib import Path

import google.generativeai as genai

from .config import LLMConfig, load_config
from .latex_template import wrap_in_template
from .persona import get_system_prompt, get_system_prompt_with_examples


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
        """Khởi tạo Gemini model."""
        if self.config.provider != "gemini":
            raise NotImplementedError(
                f"Provider '{self.config.provider}' chưa được hỗ trợ. "
                f"Hiện tại chỉ hỗ trợ 'gemini'."
            )
        
        genai.configure(api_key=self.config.api_key)
        
        self.model = genai.GenerativeModel(
            model_name=self.config.model,
            system_instruction=self.system_prompt,
            generation_config=genai.GenerationConfig(
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_output_tokens,
                top_p=self.config.top_p,
            ),
        )
    
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
        
        response = self.model.generate_content(user_prompt)
        
        if not response.text:
            raise RuntimeError("❌ Model không trả về kết quả. Kiểm tra lại API key và quota.")
        
        body_content = self._clean_response(response.text)
        
        if wrap_template:
            if not title:
                title = f"Bài giải: {problem[:80]}"
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
    
    def _find_relevant_segments(self, problem: str) -> list[dict]:
        """Tìm các đoạn transcript liên quan đến đề bài."""
        if not self.knowledge_base:
            return []
        
        segments = self.knowledge_base.get("teaching_segments", [])
        problem_lower = problem.lower()
        
        # Simple keyword matching (could upgrade to embedding search later)
        keywords_in_problem = []
        common_terms = [
            'sắp xếp', 'so sánh', 'hàm', 'big o', 'omega', 'theta',
            'đệ quy', 'sigma', 'tổng', 'log', 'giai thừa', 'mũ',
            'bậc', 'tăng trưởng', 'tiệm cận', 'độ phức tạp',
            'chứng minh', 'xác định',
        ]
        for term in common_terms:
            if term in problem_lower:
                keywords_in_problem.append(term)
        
        if not keywords_in_problem:
            return segments[:3]  # Return top 3 by relevance score
        
        # Score segments by overlap with problem keywords
        scored = []
        for seg in segments:
            seg_lower = seg["content"].lower()
            overlap = sum(1 for kw in keywords_in_problem if kw in seg_lower)
            if overlap > 0:
                scored.append((overlap, seg))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:3]]
    
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
