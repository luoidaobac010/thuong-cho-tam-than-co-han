---
name: solve-homework
description: >
  Pipeline giải bài tập PDF theo phong cách cô Thương.
  Được gọi bởi workflow /solve. Chứa scripts helper và template LaTeX.
triggers:
  - "/solve"
  - "giải bài tập"
  - "solve homework"
skills:
  - co-thuong-style
---

# Skill: Solve Homework Pipeline

## Mục đích

Orchestrate toàn bộ quy trình: **PDF → Extract → Search Transcript → Solve → LaTeX**.

## Scripts có sẵn

| Script | Chức năng | Usage |
|--------|----------|-------|
| `scripts/render_pdf.py` | Render PDF → PNG | `python render_pdf.py <path>` |

## Dependencies

- `PyMuPDF` (fitz) — để render PDF
- Transcript files: `data/buoi1_clean.md` → `buoi5_clean.md`
- Knowledge base: `data/knowledge_base.json`
- Style skill: `.agents/skills/co-thuong-style/SKILL.md`

## Pipeline Steps

### Step 1: Render PDF
```bash
python .agents/skills/solve-homework/scripts/render_pdf.py "<pdf_path>"
```
Output: `<pdf_name>_pages/page_XX.png`

### Step 2: Read pages
Dùng `view_file` đọc từng ảnh PNG để hiểu đề bài.

### Step 3: Search transcript
```
grep_search keywords → data/buoi4_clean.md (ưu tiên)
grep_search keywords → data/buoi5_clean.md
grep_search keywords → data/buoi2_clean.md, buoi3_clean.md
```

### Step 4: Load style
Đọc `.agents/skills/co-thuong-style/SKILL.md` trước khi giải.

### Step 5: Solve & output
Tạo file `<pdf_path>_solved.tex` cùng thư mục.

## LaTeX Template Structure

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[vietnamese]{babel}
\usepackage{amsmath,amssymb,amsthm}
\usepackage[most]{tcolorbox}

% Result box (blue) - cho kết quả cuối
\newtcolorbox{resultbox}[1][]{
  colback=blue!5!white, colframe=blue!75!black,
  fonttitle=\bfseries, title=#1
}

% Note box (yellow) - cho ghi chú phương pháp
\newtcolorbox{notebox}[1][]{
  colback=yellow!10!white, colframe=yellow!75!black,
  fonttitle=\bfseries, title=#1
}

\begin{document}
\title{Lời giải ...}
\author{Theo phong cách cô Huỳnh Thị Thanh Thương}
\maketitle

\section{Bài 1: ...}
% Giải từng bài...

\end{document}
```

## Quy tắc output

1. Tên file: `<tên PDF gốc>_solved.tex`
2. Cùng thư mục với PDF gốc
3. Mỗi bài = 1 `\section`
4. Mỗi câu con = 1 `\subsection`
5. Kết quả đóng khung trong `resultbox`
6. Ghi chú phương pháp trong `notebox`
