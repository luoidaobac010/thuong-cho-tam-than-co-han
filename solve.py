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
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.config import LLMConfig, load_config, get_default_config_path
from core.solver import CoThuongSolver


def setup_config():
    """Hướng dẫn cấu hình API key lần đầu."""
    print("=" * 60)
    print("🔧 Thuong-cho-tam-than-co-han — Cấu hình ban đầu")
    print("=" * 60)
    
    config = load_config()
    
    print(f"\nProvider hiện tại: {config.provider}")
    print(f"Model hiện tại: {config.model}")
    
    # API Key
    print("\n📌 Nhập API key (nhấn Enter để giữ nguyên):")
    if config.api_key:
        masked = config.api_key[:8] + "..." + config.api_key[-4:]
        print(f"   Key hiện tại: {masked}")
    
    new_key = input("   API Key: ").strip()
    if new_key:
        config.api_key = new_key
    
    # Model
    print("\n📌 Chọn model (nhấn Enter để giữ mặc định):")
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
    
    # Model config
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=None,
        help="Model LLM (ví dụ: gemini-2.0-flash, gemini-2.5-pro)",
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
    
    # --- Setup mode ---
    if args.setup:
        setup_config()
        return
    
    # --- Load config ---
    config = load_config()
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
        print("\n💡 Chạy 'python solve.py --setup' để cấu hình API key.")
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
        print(f"   Biên dịch: pdflatex {output_path}")
    else:
        print("\n" + "=" * 60)
        print("📄 LỜI GIẢI:")
        print("=" * 60)
        print(result)


if __name__ == "__main__":
    main()
