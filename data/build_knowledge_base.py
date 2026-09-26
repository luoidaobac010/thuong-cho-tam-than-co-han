"""
build_knowledge_base.py
Parse tất cả transcript (clean MD) và bài giải LaTeX để tạo knowledge base.

Output: knowledge_base.json chứa:
  - teaching_segments: Các đoạn giảng dạy trích từ transcript
  - latex_examples: Các cặp (đề bài, lời giải LaTeX) từ file .tex
  - latex_template: Template LaTeX chuẩn của cô Thương

Sử dụng:
    python -m data.build_knowledge_base [--data-dir DIR] [--output FILE]
"""

import argparse
import json
import re
from pathlib import Path


def extract_teaching_segments(md_path: Path) -> list[dict]:
    """
    Trích xuất các đoạn giảng dạy có giá trị từ transcript.
    Tập trung vào các đoạn cô giải thích khái niệm hoặc giải bài tập.
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Xác định buổi học từ tên file
    buoi_match = re.search(r'buoi(\d+)', md_path.stem)
    buoi_num = int(buoi_match.group(1)) if buoi_match else 0

    paragraphs = content.split('\n\n')
    segments = []

    # Các keyword cho thấy cô đang giải thích hoặc giải bài
    teaching_keywords = [
        'ký hiệu', 'tiệm cận', 'big o', 'omega', 'theta',
        'thuật toán', 'thực toán', 'độ phức tạp', 'hàm',
        'bài tập', 'bài số', 'câu', 'ví dụ',
        'chứng minh', 'tính chất', 'định nghĩa', 'công thức',
        'sắp xếp', 'so sánh', 'tăng trưởng', 'bậc',
        'đệ quy', 'vòng lặp', 'tối ưu', 'mô hình',
        'sigma', 'tổng', 'log', 'mũ', 'giai thừa',
        'kết luận', 'chấm điểm', 'đề thi',
    ]

    for i, para in enumerate(paragraphs):
        para_lower = para.lower()

        # Skip paragraphs that are too short or are just noise
        if len(para.strip()) < 100:
            continue

        # Check if paragraph contains teaching content
        relevance_score = sum(
            1 for kw in teaching_keywords if kw in para_lower
        )

        if relevance_score >= 2:
            segments.append({
                "buoi": buoi_num,
                "paragraph_index": i,
                "content": para.strip(),
                "relevance_score": relevance_score,
                "keywords_found": [
                    kw for kw in teaching_keywords if kw in para_lower
                ],
            })

    # Sort by relevance and keep top segments
    segments.sort(key=lambda x: x["relevance_score"], reverse=True)
    return segments


def extract_latex_examples(tex_path: Path) -> list[dict]:
    """
    Parse file LaTeX để trích xuất các cặp (đề bài, lời giải).
    Mỗi \\section hoặc \\subsection là một bài/câu.
    """
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    examples = []

    # Extract title
    title_match = re.search(r'\\title\{(.+?)\}', content, re.DOTALL)
    doc_title = title_match.group(1) if title_match else tex_path.stem
    # Clean LaTeX commands from title
    doc_title = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', doc_title)
    doc_title = re.sub(r'\\\\.*', '', doc_title).strip()

    # Extract body (between \begin{document} and \end{document})
    body_match = re.search(
        r'\\begin\{document\}(.+?)\\end\{document\}', content, re.DOTALL
    )
    if not body_match:
        return examples

    body = body_match.group(1)

    # Split by \section or \section*
    sections = re.split(r'(\\section\*?\{[^}]+\})', body)

    current_section = ""
    for part in sections:
        section_match = re.match(r'\\section\*?\{([^}]+)\}', part)
        if section_match:
            current_section = section_match.group(1)
            continue

        if not current_section or len(part.strip()) < 50:
            continue

        # Extract subsections within this section
        subsections = re.split(r'(\\subsection\*?\{[^}]+\})', part)

        if len(subsections) <= 1:
            # No subsections — treat entire section as one example
            examples.append({
                "source_file": tex_path.name,
                "section": current_section,
                "subsection": "",
                "latex_content": part.strip(),
            })
        else:
            current_subsection = ""
            for sub_part in subsections:
                sub_match = re.match(r'\\subsection\*?\{([^}]+)\}', sub_part)
                if sub_match:
                    current_subsection = sub_match.group(1)
                    continue
                if current_subsection and len(sub_part.strip()) > 30:
                    examples.append({
                        "source_file": tex_path.name,
                        "section": current_section,
                        "subsection": current_subsection,
                        "latex_content": sub_part.strip(),
                    })

    return examples


def extract_latex_template(tex_path: Path) -> dict:
    """
    Extract LaTeX preamble template (packages, colors, custom environments).
    """
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract preamble (everything before \begin{document})
    preamble_match = re.search(
        r'^(.+?)\\begin\{document\}', content, re.DOTALL
    )
    preamble = preamble_match.group(1).strip() if preamble_match else ""

    return {
        "source_file": tex_path.name,
        "preamble": preamble,
    }


def build_knowledge_base(
    data_dir: Path,
    output_path: Path,
) -> dict:
    """Build the complete knowledge base from all available data."""

    knowledge_base = {
        "metadata": {
            "description": "Knowledge base for CoThuong-AI",
            # Chỉ ghi tên thư mục, không ghi absolute path (lộ path máy, không portable)
            "data_dir": data_dir.resolve().name,
        },
        "teaching_segments": [],
        "latex_examples": [],
        "latex_template": None,
    }

    # 1. Process all transcript files
    print("📝 Processing transcripts...")
    md_files = sorted(data_dir.glob("buoi*_clean.md"))
    for md_path in md_files:
        segments = extract_teaching_segments(md_path)
        knowledge_base["teaching_segments"].extend(segments)
        print(f"   ✓ {md_path.name}: {len(segments)} teaching segments")

    # 2. Process all LaTeX files
    print("\n📐 Processing LaTeX examples...")
    tex_files = sorted(data_dir.glob("loi_giai*.tex"))
    for tex_path in tex_files:
        examples = extract_latex_examples(tex_path)
        knowledge_base["latex_examples"].extend(examples)
        print(f"   ✓ {tex_path.name}: {len(examples)} examples")

    # 3. Extract LaTeX template (from first .tex file)
    if tex_files:
        template = extract_latex_template(tex_files[0])
        knowledge_base["latex_template"] = template
        print(f"\n📋 LaTeX template extracted from: {tex_files[0].name}")

    # 4. Save knowledge base
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("📊 Knowledge Base Summary:")
    print(f"   Teaching segments: {len(knowledge_base['teaching_segments'])}")
    print(f"   LaTeX examples: {len(knowledge_base['latex_examples'])}")
    print(f"   Has LaTeX template: {knowledge_base['latex_template'] is not None}")
    print(f"   Saved to: {output_path}")

    return knowledge_base


def main():
    parser = argparse.ArgumentParser(
        description="Build knowledge base from transcripts and LaTeX files"
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Directory containing clean MD and LaTeX files",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file path",
    )

    args = parser.parse_args()

    if args.data_dir:
        data_dir = Path(args.data_dir)
    else:
        data_dir = Path(__file__).resolve().parent

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).resolve().parent / "knowledge_base.json"

    build_knowledge_base(data_dir, output_path)


if __name__ == "__main__":
    main()
