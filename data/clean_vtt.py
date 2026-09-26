"""
clean_vtt.py
Chuyển file subtitle .vtt thành text thuần (_clean.md), gộp 15 dòng/đoạn.

Sử dụng:
    python data/clean_vtt.py                 # clean mọi data/buoi*.vi.vtt
    python data/clean_vtt.py a.vtt b.vtt     # clean các file chỉ định

Lưu ý: data/download_subtitles.py có hàm clean riêng (clean_vtt_file) và là
pipeline chính. Script này chỉ để clean lại thủ công.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def clean_vtt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove WebVTT header
    content = re.sub(r'^WEBVTT.*\n+', '', content)
    # Remove timestamps and alignments like 00:00:00.000 --> 00:00:02.000 align:start position:0%
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', content)
    # Remove HTML-like tags e.g. <c>
    content = re.sub(r'<[^>]+>', '', content)

    # Extract lines, removing duplicates that are adjacent
    lines = content.split('\n')
    cleaned_lines = []
    prev_line = ""
    for line in lines:
        line = line.strip()
        if not line or line.isdigit():  # skip empty lines or line numbers
            continue
        if line != prev_line:
            cleaned_lines.append(line)
            prev_line = line

    # Now group them into paragraphs, maybe joining every 10 lines
    paragraphs = []
    current_para = []
    for i, line in enumerate(cleaned_lines):
        current_para.append(line)
        if (i + 1) % 15 == 0:
            paragraphs.append(' '.join(current_para))
            current_para = []
    if current_para:
        paragraphs.append(' '.join(current_para))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(paragraphs))


def output_path_for(vtt_path: Path) -> Path:
    """buoi4.vi.vtt -> buoi4_clean.md (cùng thư mục)."""
    stem = vtt_path.name.split('.')[0]
    return vtt_path.with_name(f"{stem}_clean.md")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Chuyển .vtt thành _clean.md (gộp 15 dòng/đoạn).")
    parser.add_argument("files", nargs="*", type=Path,
                        help="file .vtt cần clean (mặc định: mọi data/buoi*.vi.vtt)")
    args = parser.parse_args(argv)

    inputs = args.files or sorted(Path(__file__).resolve().parent.glob("buoi*.vi.vtt"))
    missing = [p for p in inputs if not p.is_file()]
    if missing:
        print(f"❌ Không tìm thấy file: {', '.join(map(str, missing))}", file=sys.stderr)
        return 1

    for vtt in inputs:
        out = output_path_for(vtt)
        clean_vtt(vtt, out)
        print(f"✓ {vtt.name} -> {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
