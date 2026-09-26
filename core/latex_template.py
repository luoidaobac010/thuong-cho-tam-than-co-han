"""
latex_template.py
LaTeX template chuẩn của Cô Thương.
Trích xuất từ loi_giai_so_sanh_thuat_toan.tex và loi_giai_so_sanh_thuat_toan_bai_2.tex.
"""

# LaTeX preamble chuẩn — giữ nguyên format của cô
LATEX_PREAMBLE = r"""\documentclass[12pt,a4paper]{article}

% ===== PACKAGES =====
\usepackage[utf8]{inputenc}
\usepackage[vietnamese]{babel}
% babel vietnamese biến " thành shorthand, "chuỗi" trong \text{} làm hỏng compile
\AtBeginDocument{\shorthandoff{"}}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{geometry}
\usepackage{enumitem}
% Model đôi khi lồng list > 4 cấp ("Too deeply nested"): nâng giới hạn, cấp 1-4 giữ nhãn mặc định
\setlistdepth{9}
\renewlist{itemize}{itemize}{9}
\renewlist{enumerate}{enumerate}{9}
\setlist[itemize,1]{label=\textbullet}
\setlist[itemize,2]{label=\normalfont\bfseries\textendash}
\setlist[itemize,3]{label=\textasteriskcentered}
\setlist[itemize,4,5,6,7,8,9]{label=\textperiodcentered}
\setlist[enumerate,1]{label=\arabic*.}
\setlist[enumerate,2]{label=(\alph*)}
\setlist[enumerate,3]{label=\roman*.}
\setlist[enumerate,4]{label=\Alph*.}
\setlist[enumerate,5,6,7,8,9]{label=\arabic*.}
\usepackage{array}
\usepackage{booktabs}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{tcolorbox}
% Đề thi hay có code/mã giả, model tự dùng các môi trường này
\usepackage{listings}
\usepackage{algorithm}
\usepackage{algpseudocode}
\lstset{basicstyle=\ttfamily\small, breaklines=true, columns=fullflexible}

\geometry{a4paper, margin=2.5cm}

% ===== CUSTOM STYLES =====
\definecolor{mainblue}{RGB}{0,90,160}
\definecolor{darkgreen}{RGB}{0,120,60}
\definecolor{resultbg}{RGB}{230,245,255}

\newtcolorbox{resultbox}{
  colback=resultbg, colframe=mainblue,
  boxrule=0.8pt, arc=3pt,
  left=8pt, right=8pt, top=6pt, bottom=6pt,
  fonttitle=\bfseries, title=Kết quả
}

\newtcolorbox{notebox}[1][]{
  colback=yellow!8, colframe=orange!70!black,
  boxrule=0.6pt, arc=3pt,
  left=8pt, right=8pt, top=6pt, bottom=6pt,
  fonttitle=\bfseries, title={Lưu ý}, #1
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textit{Phân tích \& Thiết kế Thuật toán}}
\fancyhead[R]{\textit{GV: Huỳnh Thị Thanh Thương}}
\fancyfoot[C]{\thepage}
"""


def wrap_in_template(
    body_content: str,
    title: str = "Bài giải",
    subtitle: str = "",
) -> str:
    """
    Wrap LaTeX body content vào template hoàn chỉnh.

    Args:
        body_content: Nội dung LaTeX (sections, text, math...).
        title: Tiêu đề chính của document.
        subtitle: Dòng phụ dưới tiêu đề.

    Returns:
        Full LaTeX document string, ready to compile with pdflatex.
    """
    # Build title block
    title_block = f"\\title{{\\textbf{{{title}}}"
    if subtitle:
        title_block += f"\\\\[6pt]\n\\large ({subtitle})"
    title_block += "}\n\\author{}\n\\date{}"

    document = f"""{LATEX_PREAMBLE}

{title_block}

\\begin{{document}}
\\maketitle
\\thispagestyle{{fancy}}

{body_content}

\\end{{document}}
"""
    return document


def get_preamble() -> str:
    """Trả về preamble LaTeX để nhúng vào prompt nếu cần."""
    return LATEX_PREAMBLE
