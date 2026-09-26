"""
solve.py — CLI Entry Point cho Thuong-cho-tam-than-co-han

Sử dụng:
    # Giải một bài tập, output ra file .tex
    python solve.py --problem "Sắp xếp các hàm sau theo bậc tăng trưởng: n², 2^n, n·log(n), n!" --output bai_giai.tex

    # Giải bài tập từ file đề
    python solve.py --problem-file de_bai.txt --output bai_giai.tex

    # Chế độ tương tác (nhập đề bài từ terminal)
    python solve.py --interactive

    # Cấu hình API key lần đầu
    python solve.py --setup

    # Dùng model khác
    python solve.py --model gemini-2.5-pro --problem "..."
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.config import DEFAULT_MODELS, LLMConfig, load_config, get_default_config_path
from core.solver import CoThuongSolver


def compile_pdf(tex_path: Path) -> bool:
    """Biên dịch .tex -> .pdf bằng tectonic (fallback xelatex). Trả về True nếu thành công."""
    # Template dùng tiếng Việt: tectonic/xelatex xử lý UTF-8 ổn hơn pdflatex
    if shutil.which("tectonic"):
        cmd = ["tectonic", "-X", "compile", tex_path.name]
    elif shutil.which("xelatex"):
        cmd = ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name]
    else:
        print("⚠️  Không tìm thấy tectonic/xelatex. Cài: brew install tectonic")
        return False
    
    print(f"📄 Đang biên dịch PDF bằng {cmd[0]} (lần đầu tectonic có thể mất vài phút tải package)...")
    proc = subprocess.run(cmd, cwd=tex_path.parent, capture_output=True, text=True)
    pdf_path = tex_path.with_suffix(".pdf")
    if proc.returncode == 0 and pdf_path.exists():
        print(f"✅ PDF: {pdf_path}")
        return True
    
    print(f"❌ Biên dịch lỗi (exit={proc.returncode}). 15 dòng cuối log:")
    for line in (proc.stderr or proc.stdout).strip().splitlines()[-15:]:
        print("   " + line)
    return False


def setup_config():
    """Hướng dẫn cấu hình API key lần đầu."""
    print("=" * 60)
    print("🔧 Thuong-cho-tam-than-co-han — Cấu hình ban đầu")
    print("=" * 60)
    
    config = load_config()
    
    # Provider
    print(f"\n📌 Chọn provider [agy/gemini] (Enter giữ '{config.provider}'):")
    new_provider = input("   Provider: ").strip().lower()
    if new_provider and new_provider != config.provider:
        config.provider = new_provider
        config.model = DEFAULT_MODELS.get(new_provider, "")
    
    print(f"\nProvider hiện tại: {config.provider}")
    print(f"Model hiện tại: {config.model}")
    
    # API Key (chỉ provider gemini cần, agy dùng đăng nhập Google)
    if config.provider == "gemini":
        print("\n📌 Nhập API key (nhấn Enter để giữ nguyên):")
        if config.api_key:
            masked = config.api_key[:8] + "..." + config.api_key[-4:]
            print(f"   Key hiện tại: {masked}")
        
        new_key = input("   API Key: ").strip()
        if new_key:
            config.api_key = new_key
    
    # Model
    print("\n📌 Chọn model (nhấn Enter để giữ mặc định):")
    if config.provider == "agy":
        print("   Xem danh sách: agy models (vd gemini-3.8-flash-medium, gemini-3.1-pro-high)")
    else:
        print("   Gợi ý: gemini-2.0-flash (nhanh), gemini-2.5-pro (chính xác hơn)")
    new_model = input(f"   Model [{config.model}]: ").strip()
    if new_model:
        config.model = new_model
    
    # Save
    config_path = get_default_config_path()
    config.to_file(config_path)
    print(f"\n✅ Đã lưu cấu hình vào: {config_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Thuong-cho-tam-than-co-han: Giải bài tập thuật toán theo phong cách Cô Thương",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python solve.py --setup
  python solve.py --problem "So sánh n² và n·log(n)" --output bai1.tex
  python solve.py --interactive
        """,
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--setup",
        action="store_true",
        help="Cấu hình API key và model",
    )
    mode_group.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Chế độ tương tác (nhập đề bài từ terminal)",
    )
    
    # Problem input
    parser.add_argument(
        "--problem", "-p",
        type=str,
        help="Đề bài cần giải (text hoặc LaTeX)",
    )
    parser.add_argument(
        "--problem-file", "-f",
        type=str,
        help="Đường dẫn file chứa đề bài",
    )
    
    # Output
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Đường dẫn file output .tex (mặc định: in ra terminal)",
    )
    parser.add_argument(
        "--title", "-t",
        type=str,
        default=None,
        help="Tiêu đề document LaTeX",
    )
    parser.add_argument(
        "--body-only",
        action="store_true",
        help="Chỉ output LaTeX body (không bao gồm preamble/template)",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Biên dịch luôn ra PDF sau khi lưu .tex (cần --output, dùng tectonic)",
    )
    
    # Model config
    parser.add_argument(
        "--provider",
        choices=["agy", "gemini"],
        default=None,
        help="agy (Antigravity CLI, mặc định) hoặc gemini (cần API key)",
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=None,
        help="Model slug (agy: xem `agy models`, vd gemini-3.1-pro-high)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API key (override config)",
    )
    
    # Knowledge base
    parser.add_argument(
        "--knowledge-base", "-kb",
        type=str,
        default=None,
        help="Đường dẫn file knowledge_base.json",
    )
    
    args = parser.parse_args()
    
    if args.pdf and (not args.output or args.body_only):
        parser.error("--pdf cần --output và không dùng cùng --body-only")
    
    # --- Setup mode ---
    if args.setup:
        setup_config()
        return
    
    # --- Load config ---
    config = load_config()
    if args.provider and args.provider != config.provider:
        config.provider = args.provider
        config.model = DEFAULT_MODELS.get(args.provider, "")
    if args.model:
        config.model = args.model
    if args.api_key:
        config.api_key = args.api_key
    
    # --- Knowledge base path ---
    kb_path = None
    if args.knowledge_base:
        kb_path = Path(args.knowledge_base)
    
    # --- Initialize solver ---
    try:
        solver = CoThuongSolver(config=config, knowledge_base_path=kb_path)
    except ValueError as e:
        print(str(e))
        print("\n💡 Chạy 'python solve.py --setup' để cấu hình provider/model.")
        sys.exit(1)
    
    # --- Interactive mode ---
    if args.interactive:
        solver.solve_interactive()
        return
    
    # --- Get problem text ---
    problem = None
    if args.problem:
        problem = args.problem
    elif args.problem_file:
        problem_path = Path(args.problem_file)
        if not problem_path.exists():
            print(f"❌ File không tồn tại: {problem_path}")
            sys.exit(1)
        with open(problem_path, 'r', encoding='utf-8') as f:
            problem = f.read().strip()
    else:
        parser.print_help()
        print("\n❌ Cần cung cấp đề bài qua --problem hoặc --problem-file")
        sys.exit(1)
    
    # --- Solve ---
    print(f"📚 Đề bài: {problem[:100]}{'...' if len(problem) > 100 else ''}")
    
    result = solver.solve(
        problem=problem,
        title=args.title,
        wrap_template=not args.body_only,
    )
    
    # --- Output ---
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"\n✅ Đã lưu lời giải vào: {output_path}")
        if args.pdf:
            if not compile_pdf(output_path.resolve()):
                sys.exit(2)
        else:
            print(f"   Biên dịch: tectonic -X compile \"{output_path}\" (hoặc thêm --pdf)")
    else:
        print("\n" + "=" * 60)
        print("📄 LỜI GIẢI:")
        print("=" * 60)
        print(result)


if __name__ == "__main__":
    main()
