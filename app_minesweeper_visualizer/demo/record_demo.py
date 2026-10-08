"""Auto-record a narrated demo video of the Minesweeper visualizer.

Pipeline: edge-tts narration per scene -> Playwright drives the app and records
video (each scene lasts as long as its narration) -> ffmpeg muxes audio + video to MP4.

Usage: python record_demo.py
Output: demo_video.mp4 next to this script.
"""
import asyncio
import re
import shutil
import subprocess
import time
from pathlib import Path

import edge_tts
import imageio_ffmpeg
from playwright.async_api import async_playwright

HERE = Path(__file__).parent
APP_URL = (HERE.parent / "index.html").resolve().as_uri()
BUILD = HERE / "build"
OUTPUT = HERE / "demo_video.mp4"
VOICE = "vi-VN-NamMinhNeural"
SIZE = {"width": 1600, "height": 900}
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SCENES = [
    ("intro",
     "Em xin trình bày bài tập lớn môn Phân tích và Thiết kế Thuật toán. Em chọn bài Dò Mìn "
     "trên hệ thống WeCode, và xây dựng một ứng dụng web để trực quan hóa thuật toán giải."),
    ("model",
     "Đầu vào là ma trận A kích thước N nhân M. Mỗi ô của A cho biết tổng số mìn ở bốn ô kề cạnh "
     "theo hình chữ thập: trên, dưới, trái, phải. Đầu ra là ma trận nhị phân B, một là có mìn, "
     "không là an toàn, sao cho thỏa mãn mọi ràng buộc của A."),
    ("idea",
     "Nếu vét cạn toàn bộ bảng, độ phức tạp là hai mũ N nhân M. Nhận xét quan trọng: khi đã biết "
     "hàng đầu tiên, mỗi ô ở hàng sau được suy ra duy nhất từ ràng buộc của ô ngay phía trên nó. "
     "Vì vậy em chỉ quay lui trên hàng không, còn hai mũ M trạng thái, và cắt tỉa sớm theo đường "
     "chéo khi giá trị suy ra nằm ngoài không và một."),
    ("run_test1",
     "Chạy thử với test một, ma trận ba nhân ba. Ô xanh dương là ô đang thử, ô xanh lá là ô an toàn, "
     "ô đỏ là mìn. Khi gặp mâu thuẫn, thuật toán quay lui và thử giá trị còn lại."),
    ("step_test2",
     "Ở chế độ từng bước, ta theo dõi được từng lần gán giá trị. Dòng mã giả tương ứng được tô sáng "
     "ở bên phải, và nhật ký bên dưới ghi lại lý do mỗi nhánh bị cắt tỉa."),
    ("no_solution",
     "Với test bốn, mọi ô đều bằng bốn. Điều này không thể xảy ra, vì ô ở góc chỉ có hai ô kề. "
     "Thuật toán tỉa sạch các nhánh và kết luận vô nghiệm."),
    ("random",
     "Nút tạo lưới có nghiệm sẽ sinh ngẫu nhiên một bảng mìn, rồi tính ra ma trận gợi ý, nên luôn "
     "đảm bảo có lời giải. Với bảng sáu nhân sáu, thuật toán vẫn tìm ra nghiệm rất nhanh."),
    ("verify",
     "Kiểm tra lại kết quả: rê chuột vào một ô, tổng số mìn trong hình chữ thập ở bảng B "
     "đúng bằng con số tương ứng ở bảng A."),
    ("outro",
     "Ứng dụng được xây dựng với sự hỗ trợ của trợ lý AI. Quá trình thực hiện và các lỗi đã phát "
     "hiện, sửa chữa được trình bày chi tiết trong báo cáo. Em cảm ơn cô đã theo dõi."),
]

OVERLAY_JS = """
() => {
  const style = document.createElement('style');
  style.textContent = `
    #demo-caption { position: fixed; left: 50%; bottom: 28px; transform: translateX(-50%);
      max-width: 1100px; padding: 12px 22px; background: rgba(0,0,0,.82); color: #fff;
      font: 500 19px/1.45 'Plus Jakarta Sans', sans-serif; border-radius: 10px; z-index: 9999;
      text-align: center; border: 1px solid rgba(255,255,255,.12); }
    #demo-cursor { position: fixed; width: 18px; height: 18px; border-radius: 50%;
      background: rgba(250,204,21,.9); border: 2px solid #fff; z-index: 10000;
      pointer-events: none; transform: translate(-50%,-50%); left: -50px; top: -50px;
      transition: transform .1s; box-shadow: 0 0 12px rgba(250,204,21,.8); }
    #demo-cursor.down { transform: translate(-50%,-50%) scale(.7); }
    #demo-title { position: fixed; inset: 0; z-index: 9998; display: flex; flex-direction: column;
      align-items: center; justify-content: center; gap: 14px; background: #0c0f17;
      color: #f1f5f9; font-family: 'Plus Jakarta Sans', sans-serif; transition: opacity .6s; }
    #demo-title h1 { font-size: 46px; font-weight: 800; }
    #demo-title p { font-size: 22px; color: #94a3b8; }
    #demo-title .chip { font: 600 16px 'JetBrains Mono', monospace; color: #38bdf8;
      border: 1px solid #38bdf8; padding: 6px 14px; border-radius: 8px; }`;
  document.head.appendChild(style);
  const cap = Object.assign(document.createElement('div'), { id: 'demo-caption' });
  const cur = Object.assign(document.createElement('div'), { id: 'demo-cursor' });
  document.body.append(cap, cur);
  addEventListener('mousemove', e => { cur.style.left = e.clientX + 'px'; cur.style.top = e.clientY + 'px'; });
  addEventListener('mousedown', () => cur.classList.add('down'));
  addEventListener('mouseup', () => cur.classList.remove('down'));
}
"""


def audio_duration(path: Path) -> float:
    proc = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", proc.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


async def synthesize() -> list[tuple[Path, float]]:
    clips = []
    for i, (name, text) in enumerate(SCENES):
        path = BUILD / f"{i:02d}_{name}.mp3"
        await edge_tts.Communicate(text, VOICE, rate="+5%").save(str(path))
        clips.append((path, audio_duration(path)))
    return clips


class Director:
    def __init__(self, page):
        self.page = page
        self.t0 = time.monotonic()

    async def caption(self, text: str):
        await self.page.evaluate("t => document.getElementById('demo-caption').textContent = t", text)

    async def title_card(self, show: bool, title="", subtitle=""):
        if show:
            await self.page.evaluate(
                """([t, s]) => { const d = document.createElement('div'); d.id = 'demo-title';
                d.innerHTML = `<span class="chip">CS112 · Phân Tích & Thiết Kế Thuật Toán</span>
                <h1>${t}</h1><p>${s}</p>`; document.body.appendChild(d); }""",
                [title, subtitle])
        else:
            await self.page.evaluate(
                "() => { const d = document.getElementById('demo-title'); if (d) { d.style.opacity = 0; setTimeout(() => d.remove(), 700); } }")

    async def move(self, selector: str, steps=25):
        box = await self.page.locator(selector).first.bounding_box()
        await self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=steps)

    async def click(self, selector: str):
        await self.move(selector)
        await asyncio.sleep(0.25)
        await self.page.locator(selector).first.click()

    async def set_speed(self, ms: int):
        await self.page.evaluate(
            "ms => { document.getElementById('speedRange').value = ms; updateSpeed(ms); }", ms)

    async def preset(self, key: str):
        await self.move("#presetSelect")
        await self.page.select_option("#presetSelect", key)
        await asyncio.sleep(0.4)

    async def wait_solved(self, timeout=60):
        await self.page.wait_for_function(
            "() => document.getElementById('statusText').textContent.includes('nghiệm')", timeout=timeout * 1000)


async def scene_actions(d: Director, name: str):
    clue = lambda r, c: f'.cell-clue[data-r="{r}"][data-c="{c}"]'
    sol = lambda r, c: f"#sol_{r}_{c}"

    if name == "intro":
        await d.title_card(True, "Minesweeper Solver Visualizer",
                           "Bài Tập Lớn: Quay lui + Nhánh cận trên bài Dò Mìn (WeCode)")
        await asyncio.sleep(6)
        await d.title_card(False)
    elif name == "model":
        await d.preset("test1")
        for r, c in [(1, 1), (0, 0), (1, 2), (1, 1)]:
            await d.move(clue(r, c))
            await asyncio.sleep(2.2)
    elif name == "idea":
        await d.move("#l1")
        for line in ["#l2", "#l4", "#l6", "#l8", "#l9", "#l10"]:
            await d.move(line, steps=12)
            await asyncio.sleep(1.6)
    elif name == "run_test1":
        await d.preset("test1")
        await d.set_speed(450)
        await d.click("#btnPlay")
        await d.wait_solved()
    elif name == "step_test2":
        await d.preset("test2")
        for _ in range(14):
            await d.click("#btnStep")
            await asyncio.sleep(0.75)
    elif name == "no_solution":
        await d.preset("test4")
        await d.set_speed(300)
        await d.click("#btnPlay")
        await d.wait_solved()
        await d.move("#logBox")
    elif name == "random":
        await d.page.fill("#inputN", "6")
        await d.page.fill("#inputM", "6")
        await d.page.dispatch_event("#inputM", "change")
        await asyncio.sleep(0.6)
        await d.click("button:has-text('Tạo Grid Có Nghiệm')")
        await d.set_speed(60)
        await asyncio.sleep(0.8)
        await d.click("#btnPlay")
        await d.wait_solved()
    elif name == "verify":
        for r, c in [(2, 2), (0, 3), (4, 1)]:
            await d.move(sol(r, c))
            await asyncio.sleep(1.4)
            await d.move(clue(r, c))
            await asyncio.sleep(1.4)
    elif name == "outro":
        await d.title_card(True, "Cảm ơn cô đã theo dõi!",
                           "Source code · Video demo · Báo cáo quy trình thực hiện")


async def record(clips) -> tuple[Path, list[float]]:
    offsets = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport=SIZE, record_video_dir=str(BUILD), record_video_size=SIZE)
        page = await ctx.new_page()
        d = Director(page)
        await page.goto(APP_URL, wait_until="networkidle")
        await page.evaluate(OVERLAY_JS)
        await page.mouse.move(800, 450)
        await asyncio.sleep(0.8)

        for (name, text), (_, dur) in zip(SCENES, clips):
            offsets.append(time.monotonic() - d.t0)
            await d.caption(text)
            # Scene lasts at least as long as its narration, longer if the action needs it.
            await asyncio.gather(scene_actions(d, name), asyncio.sleep(dur + 0.5))

        await asyncio.sleep(1.5)
        video = page.video
        await ctx.close()
        await browser.close()
        return Path(await video.path()), offsets


def mux(video: Path, clips, offsets):
    inputs, filters = ["-i", str(video)], []
    for i, ((path, _), off) in enumerate(zip(clips, offsets), start=1):
        inputs += ["-i", str(path)]
        ms = int(off * 1000)
        filters.append(f"[{i}:a]adelay={ms}|{ms}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(1, len(clips) + 1))
    filters.append(f"{mix}amix=inputs={len(clips)}:duration=longest:normalize=0[aout]")
    subprocess.run([
        FFMPEG, "-y", *inputs, "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", str(OUTPUT),
    ], check=True, capture_output=True)


async def main():
    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir(parents=True)
    print("1/3 Generating narration...")
    clips = await synthesize()
    print(f"    {len(clips)} clips, {sum(d for _, d in clips):.1f}s of speech")
    print("2/3 Recording browser...")
    video, offsets = await record(clips)
    print("3/3 Muxing MP4...")
    mux(video, clips, offsets)
    print(f"Done: {OUTPUT.name}")


if __name__ == "__main__":
    asyncio.run(main())
