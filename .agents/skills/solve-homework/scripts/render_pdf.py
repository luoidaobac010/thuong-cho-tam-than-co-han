"""
render_pdf.py - Render PDF pages to PNG images.

Usage:
    python render_pdf.py <pdf_path> [--output-dir DIR] [--dpi DPI]

Output:
    Creates _pages/ directory (next to PDF) with page_01.png, page_02.png, ...
"""

import argparse
import sys
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        print("Need PyMuPDF: pip install PyMuPDF")
        sys.exit(1)



def render_pdf(pdf_path: str, output_dir: str = None, dpi: int = 200) -> list[str]:
    """Render PDF to PNG images, return list of output paths."""
    pdf = Path(pdf_path)
    if not pdf.exists():
        print(f"File not found: {pdf}")
        sys.exit(1)

    # Output directory
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = pdf.parent / f"{pdf.stem}_pages"
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf))
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)

    output_files = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat)
        out_path = out_dir / f"page_{i + 1:02d}.png"
        pix.save(str(out_path))
        output_files.append(str(out_path))

    doc.close()

    print(f"Rendered {len(output_files)} pages -> {out_dir.name}")
    for f in output_files:
        print(f"   {Path(f).name}")

    return output_files


def main():
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG images")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: <pdf>_pages/)")
    parser.add_argument("--dpi", type=int, default=200, help="Resolution (default: 200)")
    args = parser.parse_args()

    render_pdf(args.pdf_path, args.output_dir, args.dpi)


if __name__ == "__main__":
    main()
