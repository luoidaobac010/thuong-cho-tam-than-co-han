"""Capture deterministic screenshots of the visualizer for the LaTeX report."""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

HERE = Path(__file__).parent
APP_URL = (HERE.parent / "index.html").resolve().as_uri()
OUT = HERE.parent / "report" / "img"


async def run_to_end(page):
    await page.evaluate("updateSpeed(0)")
    await page.click("#btnPlay")
    await page.wait_for_function("() => document.getElementById('statusText').textContent.includes('nghiệm')")


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=2)
        await page.goto(APP_URL, wait_until="networkidle")

        await page.screenshot(path=OUT / "01_overview.png")

        await page.select_option("#presetSelect", "test1")
        await run_to_end(page)
        await page.screenshot(path=OUT / "02_test1_solved.png")

        await page.select_option("#presetSelect", "test2")
        for _ in range(9):
            await page.click("#btnStep")
        await page.screenshot(path=OUT / "03_step_mode.png")

        await page.select_option("#presetSelect", "test4")
        await run_to_end(page)
        await page.screenshot(path=OUT / "04_no_solution.png")

        await page.fill("#inputN", "6")
        await page.fill("#inputM", "6")
        await page.dispatch_event("#inputM", "change")
        await run_to_end(page)
        await page.hover("#sol_2_2")
        await page.locator(".stage").screenshot(path=OUT / "05_cross_verify.png")

        await browser.close()
    print("ok")


if __name__ == "__main__":
    asyncio.run(main())
