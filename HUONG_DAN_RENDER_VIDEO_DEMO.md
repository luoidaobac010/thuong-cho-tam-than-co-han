# Hướng Dẫn Tự Động Render Video Demo Thuyết Trình Bài Tập Lớn (CS112)

Tài liệu này hướng dẫn cách sử dụng pipeline Python (Playwright + Edge-TTS + FFmpeg) để tự động quay màn hình, lồng tiếng AI tiếng Việt và ghép video thuyết trình hoàn chỉnh cho **bất kỳ bài toán/web visualizer nào**.

---

## 1. Yêu cầu & Cài đặt môi trường

Cần cài đặt Python 3.10+ và các thư viện sau:

```bash
pip install edge-tts playwright imageio-ffmpeg mutagen
playwright install chromium
```

---

## 2. Template Script Python Dùng Chung (`render_demo_video.py`)

Lưu file sau thành `render_demo_video.py` và đặt cùng thư mục (hoặc chỉ định đường dẫn) tới file `index.html` của web app:

```python
import asyncio
import re
import shutil
import subprocess
import time
from pathlib import Path

import edge_tts
import imageio_ffmpeg
from mutagen.mp3 import MP3
from playwright.async_api import async_playwright

# -------------------------------------------------------------
# 1. CẤU HÌNH DỰ ÁN CỦA BẠN TẠI ĐÂY
# -------------------------------------------------------------
HERE = Path(__file__).parent.resolve()
# Đường dẫn tới file HTML ứng dụng của bạn
APP_URL = (HERE / "index.html").resolve().as_uri()
BUILD_DIR = HERE / "build_temp"
OUTPUT_VIDEO = HERE / "demo_video.mp4"

# Giọng đọc: 'vi-VN-NamMinhNeural' (Nam) hoặc 'vi-VN-HoaiMyNeural' (Nữ)
VOICE = "vi-VN-NamMinhNeural"
VIDEO_SIZE = {"width": 1600, "height": 900}
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# -------------------------------------------------------------
# 2. KỊCH BẢN LỜI THOẠI (TÙY BIẾN THEO ĐỀ TÀI CỦA BẠN)
# -------------------------------------------------------------
SCENES = [
    (
        "intro",
        "Em xin chào cô. Sau đây em xin trình bày bài tập lớn môn Phân tích và Thiết kế Thuật toán. "
        "Em xây dựng ứng dụng web để trực quan hóa quá trình giải thuật toán."
    ),
    (
        "model",
        "Giao diện bao gồm khu vực nhập dữ liệu đầu vào, bảng trực quan hóa từng bước "
        "và bảng hiển thị mã giả cùng nhật ký giải thuật ở bên phải."
    ),
    (
        "run_demo",
        "Khi bấm nút Bắt Đầu Giải, thuật toán sẽ duyệt qua các trạng thái, cập nhật trực quan "
        "theo thời gian thực và tự động dừng lại khi tìm được nghiệm tối ưu."
    ),
    (
        "step_by_step",
        "Ở chế độ chạy từng bước, người dùng có thể quan sát chi tiết từng bước chuyển trạng thái "
        "và lý do các nhánh xung đột bị cắt tỉa."
    ),
    (
        "outro",
        "Toàn bộ mã nguồn và báo cáo chi tiết quá trình làm việc cùng AI đã được đính kèm. "
        "Em xin chân thành cảm ơn cô đã theo dõi!"
    )
]

# -------------------------------------------------------------
# 3. OVERLAY PHỤ ĐỀ VÀ CON TRỎ CHUỘT ẢO
# -------------------------------------------------------------
OVERLAY_JS = """
() => {
  const style = document.createElement('style');
  style.textContent = `
    #demo-caption { position: fixed; left: 50%; bottom: 28px; transform: translateX(-50%);
      max-width: 1100px; padding: 12px 22px; background: rgba(0,0,0,.85); color: #fff;
      font: 500 18px/1.45 'Segoe UI', sans-serif; border-radius: 10px; z-index: 9999;
      text-align: center; border: 1px solid rgba(255,255,255,.15); box-shadow: 0 4px 15px rgba(0,0,0,.5); }
    #demo-cursor { position: fixed; width: 18px; height: 18px; border-radius: 50%;
      background: rgba(250,204,21,.9); border: 2px solid #fff; z-index: 10000;
      pointer-events: none; transform: translate(-50%, -50%); transition: left 0.3s ease, top 0.3s ease; }
  `;
  document.head.appendChild(style);
  const cap = document.createElement('div');
  cap.id = 'demo-caption';
  document.body.appendChild(cap);
  const cur = document.createElement('div');
  cur.id = 'demo-cursor';
  document.body.appendChild(cur);
}
"""

async def generate_speech_audio(scenes, build_dir):
    build_dir.mkdir(parents=True, exist_ok=True)
    audio_files = []
    durations = []
    
    print("🎙️ Đang tạo giọng đọc AI (Edge-TTS)...")
    for idx, (name, text) in enumerate(scenes):
        audio_path = build_dir / f"{idx:02d}_{name}.mp3"
        if not audio_path.exists():
            communicate = edge_tts.Communicate(text, VOICE, rate="+5%")
            await communicate.save(str(audio_path))
        
        # Đo thời lượng file audio
        length = MP3(str(audio_path)).info.length
        audio_files.append(audio_path)
        durations.append(length)
        print(f"  + Cảnh {idx+1}/{len(scenes)} [{name}]: {length:.2f}s")
        
    return audio_files, durations

async def record_browser_actions(scenes, durations, build_dir):
    print("🎬 Đang mở trình duyệt và tự động quay video...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=VIDEO_SIZE,
            record_video_dir=str(build_dir),
            record_video_size=VIDEO_SIZE
        )
        page = await context.new_page()
        await page.goto(APP_URL)
        await page.evaluate(OVERLAY_JS)

        async def set_caption(text):
            await page.evaluate("(t) => { document.getElementById('demo-caption').innerText = t; }", text)

        async def move_cursor(selector):
            box = await page.locator(selector).first.bounding_box()
            if box:
                cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                await page.evaluate("([x, y]) => { const c = document.getElementById('demo-cursor'); c.style.left = x+'px'; c.style.top = y+'px'; }", [cx, cy])

        # ---------------------------------------------------------
        # ĐIỀU KHIỂN HÀNH ĐỘNG TƯƠNG ỨNG TỪNG CẢNH TẠI ĐÂY
        # ---------------------------------------------------------
        for idx, (name, text) in enumerate(scenes):
            dur = durations[idx]
            await set_caption(text)
            
            if name == "intro":
                await asyncio.sleep(dur)
                
            elif name == "model":
                await asyncio.sleep(dur)
                
            elif name == "run_demo":
                # Thay selector bằng ID nút bấm trên web của bạn
                try:
                    await move_cursor("button:has-text('Giải'), #btn-solve, #btn-start")
                    await page.click("button:has-text('Giải'), #btn-solve, #btn-start")
                except Exception:
                    pass
                await asyncio.sleep(dur)
                
            elif name == "step_by_step":
                try:
                    await move_cursor("button:has-text('Từng bước'), #btn-step")
                    await page.click("button:has-text('Từng bước'), #btn-step")
                except Exception:
                    pass
                await asyncio.sleep(dur)
                
            elif name == "outro":
                await asyncio.sleep(dur)

        await set_caption("")
        await asyncio.sleep(1.0)
        
        # Đóng trang để hoàn tất ghi video
        await page.close()
        await context.close()
        await browser.close()
        
        # Lấy file video webm vừa sinh ra
        video_files = list(build_dir.glob("*.webm"))
        return video_files[0] if video_files else None

def mux_audio_and_video(audio_files, raw_video_path, output_mp4, build_dir):
    print("🎞️ Đang ghép âm thanh và video (FFmpeg)...")
    concat_txt = build_dir / "concat_audio.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for audio in audio_files:
            f.write(f"file '{audio.resolve().as_posix()}'\n")
            
    merged_audio = build_dir / "merged_audio.mp3"
    subprocess.run([
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(merged_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        FFMPEG_EXE, "-y",
        "-i", str(raw_video_path),
        "-i", str(merged_audio),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(output_mp4)
    ], check=True)
    print(f"✅ Xuất video thành công: {output_mp4}")

async def main():
    audio_files, durations = await generate_speech_audio(SCENES, BUILD_DIR)
    raw_video = await record_browser_actions(SCENES, durations, BUILD_DIR)
    if raw_video:
        mux_audio_and_video(audio_files, raw_video, OUTPUT_VIDEO, BUILD_DIR)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Cách Tùy Biến Cho Đề Tài Khác

Khi đổi sang bài toán khác (ví dụ: Sudoku, Tìm đường A*, Balo DP):

1. **Đổi đường dẫn file HTML:** Sửa biến `APP_URL` trỏ tới file `index.html` của bài mới.
2. **Sửa kịch bản `SCENES`:** Viết lại lời thoại các cảnh cho phù hợp với nội dung bài của bạn.
3. **Sửa các selector nút bấm:** Trong hàm `record_browser_actions`, thay các selector nút bấm (`#btn-solve`, `#btn-step`,...) bằng ID hoặc class tương ứng trên giao diện web của bạn.
4. **Chạy script:** Gõ lệnh:
   ```bash
   python render_demo_video.py
   ```
   Script sẽ tự động tạo ra file `demo_video.mp4` chuẩn Full HD có đầy đủ lời bình và phụ đề.
