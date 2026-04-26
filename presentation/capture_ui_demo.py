"""
capture_ui_demo.py — Capture real Streamlit UI screenshots via Playwright.

Launches wiki_query.py with WIKI_DEMO_MODE=1 and navigates through:

  ERROR SCENARIO — Invalid Settings
  1. Settings page (blank) — scrolls full page
  2. Settings page (model filled, API key empty) — clicks submit
  3. Validation error revealed — scrolls to show the error alert

  HAPPY PATH
  4. Settings page (both fields filled) — scrolls to submit
  5. Wiki confirmation (37 pages) — scrolls full page list
  6. Chat page (empty) — scrolls sidebar + main
  7. Chat — question typed
  8. Chat — self-attention answer — scrolls to reveal answer + token metrics

  ERROR SCENARIO — Query Not Found
  9. Chat — out-of-scope query typed
  10. Chat — not-found response — scrolls to reveal full message

Each scene scrolls from top to the relevant content so nothing is cut off.
"""
from __future__ import annotations

import io
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image
from moviepy import ImageClip, concatenate_videoclips
from playwright.sync_api import sync_playwright, Page, TimeoutError as PWTimeout

HERE = Path(__file__).parent
ROOT = HERE.parent
UI_OUT = HERE / "ui-demo.mp4"

W, H   = 1280, 720
FPS    = 24
PORT   = 8502
URL    = f"http://localhost:{PORT}"

DEMO_MODEL = "claude-sonnet-4-6"
DEMO_KEY   = "demo-api-key-for-presentation"

SCROLL_STEPS   = 14   # frames in the scroll animation
SCROLL_WAIT_MS = 35   # ms between screenshot captures during scroll


# ── Low-level helpers ─────────────────────────────────────────────────────────

def _frame(page: Page) -> ImageClip:
    """Capture one frame at the current scroll position."""
    data = page.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
    arr  = np.array(Image.open(io.BytesIO(data)).convert("RGB"))
    return arr   # return raw array; wrap in ImageClip at call site


def _shot(page: Page, duration: float) -> ImageClip:
    """Static clip — one screenshot held for `duration` seconds."""
    return ImageClip(_frame(page), duration=duration)


def _max_scroll_y(page: Page) -> int:
    sh = page.evaluate("document.documentElement.scrollHeight")
    return max(0, sh - H)


def _scroll_to(page: Page, y: int) -> None:
    page.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")
    page.wait_for_timeout(SCROLL_WAIT_MS)


def _ready(page: Page, timeout: int = 20) -> None:
    """Wait for Streamlit to finish a rerun (spinner gone, DOM settled)."""
    page.wait_for_selector("[data-testid='stApp']", timeout=timeout * 1000)
    try:
        page.wait_for_selector(
            "[data-testid='stStatusWidget']",
            state="hidden", timeout=6000,
        )
    except PWTimeout:
        pass
    page.wait_for_timeout(500)


def _wait_for_server(max_wait: int = 30) -> None:
    import urllib.request
    deadline = time.time() + max_wait
    while time.time() < deadline:
        try:
            urllib.request.urlopen(URL, timeout=1)
            return
        except Exception:
            time.sleep(0.5)
    raise RuntimeError(f"Streamlit did not start on {URL} within {max_wait}s")


# ── Scroll-sequence builder ───────────────────────────────────────────────────

def _scroll_seq(
    page: Page,
    *,
    from_y: int = 0,
    to_y: int | None = None,        # None → scroll to bottom of page
    hold_top: float   = 1.5,        # seconds to hold at the start position
    hold_bottom: float = 2.0,       # seconds to hold at the end position
    steps: int = SCROLL_STEPS,
) -> list[ImageClip]:
    """
    Return a list of ImageClips that, when concatenated, show the page
    scrolling from `from_y` to `to_y` with pauses at both ends.

    If the distance is negligible (< 80 px), returns a single static clip.
    """
    end_y = to_y if to_y is not None else _max_scroll_y(page)

    # Snap to start
    _scroll_to(page, from_y)
    page.wait_for_timeout(200)

    clips: list[ImageClip] = [_shot(page, hold_top)]

    distance = end_y - from_y
    if distance > 80:
        # Proportional scroll duration: ~0.4s per 200 px, capped 1.0–2.5 s
        scroll_dur = max(1.0, min(2.5, distance / 500))
        frame_dur  = scroll_dur / steps
        for i in range(1, steps + 1):
            y = int(from_y + distance * i / steps)
            _scroll_to(page, y)
            clips.append(ImageClip(_frame(page), duration=frame_dur))
        clips.append(_shot(page, hold_bottom))
    else:
        # Nothing meaningful to scroll — extend the top hold instead
        clips[0] = _shot(page, hold_top + hold_bottom)

    return clips


# ── Main capture ──────────────────────────────────────────────────────────────

def capture(output: Path = UI_OUT) -> Path:
    os.system(f"lsof -ti:{PORT} | xargs kill -9 2>/dev/null; true")
    time.sleep(0.4)

    env  = {**os.environ, "WIKI_DEMO_MODE": "1"}
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run",
            str(ROOT / "wiki_query.py"),
            f"--server.port={PORT}",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--logger.level=error",
        ],
        env=env, cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        _wait_for_server()

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page    = browser.new_page(viewport={"width": W, "height": H})
            clips:  list[ImageClip] = []

            # ── 1. Settings — blank: scroll full page ─────────────────────
            page.goto(URL)
            _ready(page)
            clips.extend(_scroll_seq(page, hold_top=2.5, hold_bottom=2.0))

            # ── 2. ERROR: fill model, leave API key empty, click submit ───
            _scroll_to(page, 0)
            page.locator('input[placeholder="gpt-4o"]').scroll_into_view_if_needed()
            page.locator('input[placeholder="gpt-4o"]').fill(DEMO_MODEL)
            # Intentionally leave API key empty to trigger validation error
            page.wait_for_timeout(300)
            clips.append(_shot(page, 1.5))   # show model filled, key blank
            page.locator(
                '[data-testid="baseButton-primaryFormSubmit"],'
                '[data-testid="baseButton-secondaryFormSubmit"],'
                'button[kind="primaryFormSubmit"]'
            ).first.click()
            _ready(page, timeout=10)

            # ── 3. ERROR: scroll to reveal the validation error alert ─────
            # The st.error() alert renders below the form after the failed submit.
            try:
                page.wait_for_selector('[data-testid="stAlert"]', timeout=6000)
            except PWTimeout:
                pass
            clips.extend(_scroll_seq(page, hold_top=1.0, hold_bottom=3.5))

            # ── 4. Settings — fill both fields correctly, scroll to submit ─
            _scroll_to(page, 0)
            page.locator('input[placeholder="gpt-4o"]').scroll_into_view_if_needed()
            page.locator('input[placeholder="gpt-4o"]').fill(DEMO_MODEL)
            page.locator('input[placeholder="your-provider-api-key"]').scroll_into_view_if_needed()
            page.locator('input[placeholder="your-provider-api-key"]').fill(DEMO_KEY)
            page.wait_for_timeout(300)
            # Scroll from top (shows filled model field) down to submit button
            clips.extend(_scroll_seq(page, hold_top=2.0, hold_bottom=2.5))

            # ── 5. Submit → wiki confirmation: scroll full page list ───────
            page.locator(
                '[data-testid="baseButton-primaryFormSubmit"],'
                '[data-testid="baseButton-secondaryFormSubmit"],'
                'button[kind="primaryFormSubmit"]'
            ).first.click()
            _ready(page, timeout=15)
            clips.extend(_scroll_seq(page, hold_top=2.5, hold_bottom=2.5))

            # ── 6. Start querying → chat page (empty): scroll sidebar+main ─
            _scroll_to(page, 0)
            page.get_by_role("button", name="Start querying", exact=False).click()
            _ready(page, timeout=10)
            clips.extend(_scroll_seq(page, hold_top=2.0, hold_bottom=1.5))

            # ── 7. Happy-path question typed ──────────────────────────────
            # Scroll to bottom so the chat input is clearly visible
            _scroll_to(page, _max_scroll_y(page))
            page.wait_for_timeout(300)
            chat = page.locator('[data-testid="stChatInputTextArea"]')
            chat.fill("What is self-attention?")
            page.wait_for_timeout(400)
            clips.append(_shot(page, 2.5))

            # ── 8. Happy-path answer: scroll top → answer → token metrics ─
            chat.press("Enter")
            _ready(page, timeout=15)
            # Scroll from top (user question) all the way down (answer + metrics)
            clips.extend(_scroll_seq(page, hold_top=1.5, hold_bottom=4.0))

            # ── 9. Not-found question typed ───────────────────────────────
            # Scroll to bottom to show the chat input
            _scroll_to(page, _max_scroll_y(page))
            page.wait_for_timeout(300)
            chat2 = page.locator('[data-testid="stChatInputTextArea"]')
            chat2.fill("What is a diffusion model?")
            page.wait_for_timeout(400)
            clips.append(_shot(page, 2.5))

            # ── 10. Not-found response: scroll top → not-found message ────
            chat2.press("Enter")
            _ready(page, timeout=15)
            clips.extend(_scroll_seq(page, hold_top=1.5, hold_bottom=4.0))

            browser.close()

        video = concatenate_videoclips(clips)
        video.write_videofile(
            str(output), fps=FPS, codec="libx264",
            audio=False, logger=None,
            ffmpeg_params=["-crf", "23", "-preset", "fast"],
        )
        return output

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    out = capture()
    print(f"  ✓ ui-demo.mp4 ({out.stat().st_size // 1024} KB)")
