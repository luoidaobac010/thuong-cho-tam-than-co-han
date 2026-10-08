import os
import sys
from pathlib import Path
import json

# Set standard output to utf-8 if possible
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright

def convert_md_to_html(md_text, title="Tài liệu"):
    json_md = json.dumps(md_text)
    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <!-- Marked for Markdown -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- KaTeX -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
    <!-- Highlight.js -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.8.0/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/npm/highlight.js@11.8.0/lib/highlight.min.js"></script>
    <style>
        @page {{
            size: A4;
            margin: 18mm 15mm 18mm 15mm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            font-size: 13.5px;
            padding: 0;
            margin: 0;
        }}
        h1 {{
            font-size: 19px;
            border-bottom: 2px solid #2b6cb0;
            padding-bottom: 6px;
            color: #1a365d;
            margin-top: 0;
        }}
        h2 {{
            font-size: 15px;
            color: #2b6cb0;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
            margin-top: 18px;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 13.5px;
            color: #2d3748;
            margin-top: 12px;
            page-break-after: avoid;
        }}
        pre {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px;
            overflow-x: auto;
            font-family: Consolas, Monaco, "Courier New", monospace;
            font-size: 12px;
            page-break-inside: avoid;
        }}
        code {{
            font-family: Consolas, Monaco, "Courier New", monospace;
            background: #edf2f7;
            padding: 2px 4px;
            border-radius: 4px;
            font-size: 12px;
        }}
        pre code {{
            background: transparent;
            padding: 0;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 12px 0;
        }}
        ul, ol {{
            padding-left: 20px;
            margin: 6px 0;
        }}
        li {{
            margin-bottom: 3px;
        }}
        p {{
            margin: 5px 0;
        }}
        blockquote {{
            border-left: 4px solid #3182ce;
            padding-left: 10px;
            color: #4a5568;
            margin: 8px 0;
            background: #ebf8ff;
            padding-top: 4px;
            padding-bottom: 4px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }}
        th, td {{
            border: 1px solid #cbd5e0;
            padding: 5px 8px;
            text-align: left;
        }}
        th {{
            background: #f7fafc;
        }}
    </style>
</head>
<body>
    <div id="content"></div>
    <script>
        const rawMd = {json_md};
        document.getElementById('content').innerHTML = marked.parse(rawMd);
        
        renderMathInElement(document.getElementById('content'), {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}},
                {{left: '\\(', right: '\\)', display: false}},
                {{left: '\\[', right: '\\]', display: true}}
            ],
            throwOnError: false
        }});
        
        document.querySelectorAll('pre code').forEach((block) => {{
            hljs.highlightElement(block);
        }});
    </script>
</body>
</html>
"""
    return html_template

def convert_dir(target_dir):
    target_path = Path(target_dir)
    md_files = list(target_path.glob("*.md"))
    print(f"Found {len(md_files)} markdown files")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for md_file in md_files:
            pdf_file = md_file.with_suffix(".pdf")
            print(f"Converting {md_file.name} -> {pdf_file.name}...")
            with open(md_file, "r", encoding="utf-8") as f:
                md_content = f.read()
            
            html_content = convert_md_to_html(md_content, title=md_file.stem)
            
            page = browser.new_page()
            page.set_content(html_content, wait_until="networkidle")
            page.wait_for_timeout(1500)
            
            page.pdf(
                path=str(pdf_file),
                format="A4",
                margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
                print_background=True
            )
            page.close()
            print(f"Successfully generated {pdf_file.name}")
        browser.close()

if __name__ == "__main__":
    dir_path = sys.argv[1] if len(sys.argv) > 1 else r"D:\Study\Cô Thương\thuong-cho-tam-than-co-han\bai_tap\On_Luyen_Thuat_Toan"
    convert_dir(dir_path)
