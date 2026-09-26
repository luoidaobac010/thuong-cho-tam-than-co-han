"""Tạo playlist_summary.txt (tiêu đề + URL từng buổi) từ playlist.json."""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

# download_subtitles.py ghi playlist.json bằng UTF-8
with open(DATA_DIR / 'playlist.json', 'r', encoding='utf-8') as f, \
        open(DATA_DIR / 'playlist_summary.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(f):
        data = json.loads(line)
        out.write(f"{i+1}. {data.get('title')} - {data.get('url')}\n")
