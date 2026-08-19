import re
import sys

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

clean_vtt('buoi4.vi.vtt', 'buoi4_clean.md')
clean_vtt('buoi5.vi.vtt', 'buoi5_clean.md')
