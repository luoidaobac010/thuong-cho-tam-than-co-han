"""
download_subtitles.py
Tải subtitle tiếng Việt (auto-generated) từ playlist YouTube của Cô Thương,
sau đó clean VTT thành markdown.

Sử dụng:
    python -m data.download_subtitles [--playlist-url URL] [--output-dir DIR]

Playlist mặc định:
    https://youtube.com/playlist?list=PLapjV_I0Y4vU&si=3h00kxl1mFBHzblm
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


DEFAULT_PLAYLIST_URL = "https://youtube.com/playlist?list=PLapjV_I0Y4vU&si=3h00kxl1mFBHzblm"


def clean_vtt_content(content: str) -> str:
    """Clean VTT subtitle content into readable markdown paragraphs."""
    # Remove WebVTT header
    content = re.sub(r'^WEBVTT.*\n+', '', content)
    # Remove timestamps and alignments
    content = re.sub(
        r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', content
    )
    # Remove HTML-like tags e.g. <c>
    content = re.sub(r'<[^>]+>', '', content)

    # Extract lines, removing duplicates that are adjacent
    lines = content.split('\n')
    cleaned_lines = []
    prev_line = ""
    for line in lines:
        line = line.strip()
        if not line or line.isdigit():
            continue
        if line != prev_line:
            cleaned_lines.append(line)
            prev_line = line

    # Group into paragraphs (every 15 lines)
    paragraphs = []
    current_para = []
    for i, line in enumerate(cleaned_lines):
        current_para.append(line)
        if (i + 1) % 15 == 0:
            paragraphs.append(' '.join(current_para))
            current_para = []
    if current_para:
        paragraphs.append(' '.join(current_para))

    return '\n\n'.join(paragraphs)


def clean_vtt_file(vtt_path: Path, output_path: Path) -> None:
    """Clean a single VTT file and save as markdown."""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    cleaned = clean_vtt_content(content)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"  ✓ Cleaned: {vtt_path.name} → {output_path.name}")


def download_playlist_metadata(playlist_url: str, output_dir: Path) -> list[dict]:
    """Download playlist metadata using yt-dlp --dump-json."""
    print(f"📋 Fetching playlist metadata from:\n   {playlist_url}")

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--flat-playlist",
        "--dump-json",
        "--no-warnings",
        playlist_url,
    ]

    result = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8"
    )

    if result.returncode != 0:
        print(f"❌ Error fetching playlist: {result.stderr}")
        sys.exit(1)

    entries = []
    for line in result.stdout.strip().split('\n'):
        if line.strip():
            entries.append(json.loads(line))

    # Save playlist metadata
    playlist_path = output_dir / "playlist.json"
    with open(playlist_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"   Found {len(entries)} videos in playlist")
    return entries


def download_subtitles(
    playlist_url: str,
    output_dir: Path,
    force: bool = False,
) -> None:
    """
    Download Vietnamese auto-generated subtitles for all videos in the playlist.
    Skips videos that already have VTT files unless force=True.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get playlist entries
    entries = download_playlist_metadata(playlist_url, output_dir)

    for entry in entries:
        video_id = entry.get("id", "")
        title = entry.get("title", video_id)
        url = entry.get("url", "") or f"https://www.youtube.com/watch?v={video_id}"

        # Determine buoi number from title
        buoi_match = re.search(r'[Bb]u[oổ][ỏií]\s*(\d+)', title)
        if buoi_match:
            buoi_num = buoi_match.group(1)
            base_name = f"buoi{buoi_num}"
        else:
            # Fallback: use video_id
            base_name = f"video_{video_id}"

        vtt_path = output_dir / f"{base_name}.vi.vtt"
        clean_path = output_dir / f"{base_name}_clean.md"

        # Skip if already exists
        if vtt_path.exists() and not force:
            print(f"⏭️  Skip (already exists): {base_name}.vi.vtt — {title}")
            # Still clean if clean file doesn't exist
            if not clean_path.exists():
                clean_vtt_file(vtt_path, clean_path)
            continue

        print(f"\n🔽 Downloading subtitle: {title}")
        print(f"   URL: {url}")

        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--write-auto-sub",
            "--sub-lang", "vi",
            "--sub-format", "vtt",
            "--skip-download",
            "--no-warnings",
            "-o", str(output_dir / f"{base_name}.%(ext)s"),
            url,
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8"
        )

        if result.returncode != 0:
            print(f"   ⚠️  Warning: {result.stderr.strip()}")

        # yt-dlp may save as .vi.vtt or .vtt — find the file
        possible_paths = [
            output_dir / f"{base_name}.vi.vtt",
            output_dir / f"{base_name}.vtt",
        ]

        found_vtt = None
        for p in possible_paths:
            if p.exists():
                found_vtt = p
                break

        if found_vtt:
            # Rename to standard format if needed
            if found_vtt != vtt_path:
                found_vtt.rename(vtt_path)
            print(f"   ✓ Saved: {vtt_path.name}")

            # Clean VTT → MD
            clean_vtt_file(vtt_path, clean_path)
        else:
            print(f"   ❌ No Vietnamese subtitle found for: {title}")

    # Summary
    vtt_files = list(output_dir.glob("*.vi.vtt"))
    clean_files = list(output_dir.glob("*_clean.md"))
    print(f"\n{'='*60}")
    print(f"📊 Summary:")
    print(f"   Videos in playlist: {len(entries)}")
    print(f"   VTT files: {len(vtt_files)}")
    print(f"   Clean MD files: {len(clean_files)}")
    print(f"   Output directory: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Download & clean subtitles from Cô Thương's playlist"
    )
    parser.add_argument(
        "--playlist-url",
        default=DEFAULT_PLAYLIST_URL,
        help="YouTube playlist URL (default: Cô Thương's PTTK playlist)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for VTT and MD files (default: parent of cothuong-ai/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if files already exist",
    )

    args = parser.parse_args()

    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        # Default: cothuong-ai/data/
        output_dir = Path(__file__).resolve().parent

    download_subtitles(args.playlist_url, output_dir, force=args.force)


if __name__ == "__main__":
    main()
