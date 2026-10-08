import os
import sys
import shutil
import argparse
from pathlib import Path

# Đảm bảo in UTF-8 không bị lỗi trên Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SOURCE_DIR = Path(__file__).resolve().parent

def scaffold_project(target_dir: str, include_large_media: bool = False):
    target_path = Path(target_dir).resolve()
    print(f"Bắt đầu scaffold Minesweeper Visualizer tới: {target_path}")

    if target_path.exists() and any(target_path.iterdir()):
        print(f"Thư mục đích đã tồn tại và không rỗng. Sẽ cập nhật các file.")
    
    target_path.mkdir(parents=True, exist_ok=True)

    # Danh sách các file/folder bỏ qua nếu không cần thiết
    ignore_patterns = ["__pycache__", "*.pyc", ".git"]
    if not include_large_media:
        ignore_patterns.extend(["*.mp4", "*.webm", "build", "*.zip"])

    def _ignore(folder, files):
        ignored = []
        for f in files:
            p = Path(folder) / f
            for pat in ignore_patterns:
                if p.match(pat) or f == pat.replace("*", ""):
                    ignored.append(f)
                    break
        return ignored

    # Copy files
    for item in SOURCE_DIR.iterdir():
        if item.name in ["scaffold_minesweeper.py", "__pycache__", ".git"]:
            continue
        dest_item = target_path / item.name
        if item.is_dir():
            if dest_item.exists():
                shutil.rmtree(dest_item)
            shutil.copytree(item, dest_item, ignore=_ignore)
            print(f"  + Thư mục: {item.name}/")
        else:
            if not (not include_large_media and item.suffix in [".mp4", ".zip"]):
                shutil.copy2(item, dest_item)
                print(f"  + File: {item.name}")

    print("\nHoàn thành scaffold dự án thành công!")
    print(f"Mở file web visualizer trực tiếp tại: {target_path / 'index.html'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script tu dong scaffold du an Minesweeper Visualizer")
    parser.add_argument("target", nargs="?", default="./minesweeper_visualizer_copy", help="Duong dan thu muc dich")
    parser.add_argument("--all", action="store_true", help="Copy ca video mp4/media va file zip")
    args = parser.parse_args()

    scaffold_project(args.target, include_large_media=args.all)
