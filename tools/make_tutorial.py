#!/usr/bin/env python3
"""Render the homepage tutorial GIF with Playwright + ffmpeg.

Loads the built English landing page, injects tools/tutorial_overlay.js,
feeds it the official sample (assets/example-session.jsonl) via
window.__tutDemo, and captures one deterministic frame per step of
window.__seek(f). Assembles an optimized palette GIF into
assets/tutorial.gif (plays once — step buttons on the page let viewers
review) plus 8 static step frames as assets/tutorial-step{1..8}.webp.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'claude-code-session-viewer' / 'index.html'
OVERLAY = Path(__file__).resolve().parent / 'tutorial_overlay.js'
SAMPLE = ROOT / 'assets' / 'example-session.jsonl'
FRAMES = Path('/tmp/ccviewer-tutorial-frames')
OUT = ROOT / 'assets' / 'tutorial.gif'

FPS = 10
TOTAL = 225          # 150 logical frames x 1.5 slowdown = 22.5 s
OPEN_AT = 110        # real frame where the viewer demo session is loaded (behind the dialog)
WIDTH = 880          # output width (page captured at 960x600 @2x)
STEPS = [41, 57, 80, 107, 140, 161, 182, 207]  # real frames exported as tutorial-step{N}.webp


def capture():
    FRAMES.mkdir(parents=True, exist_ok=True)
    for old in FRAMES.glob('f_*.png'):
        old.unlink()
    demo = SAMPLE.read_text(encoding='utf-8')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 960, 'height': 600}, device_scale_factor=2)
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(2200)  # fonts + landing fade-in animations
        page.evaluate('t => window.__tutDemo = t', demo)
        page.add_script_tag(path=str(OVERLAY))
        assert page.evaluate('window.__tutTotal') == TOTAL, 'overlay timeline and TOTAL drifted apart'
        for f in range(TOTAL):
            if f == OPEN_AT:
                page.evaluate('window.__tutOpenDemo()')
                page.wait_for_timeout(400)
            page.evaluate(f'window.__seek({f})')
            page.screenshot(path=str(FRAMES / f'f_{f:03d}.png'), clip={'x': 0, 'y': 0, 'width': 960, 'height': 600})
        browser.close()


def assemble():
    # -loop -1: no Netscape loop block -> the GIF plays once, then rests on the
    # final viewer state. The page offers step buttons + replay instead of looping.
    vf = (
        f'scale={WIDTH}:-2:flags=lanczos,split[a][b];'
        '[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4'
    )
    subprocess.run(
        ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
         '-i', str(FRAMES / 'f_%03d.png'), '-vf', vf, '-loop', '-1', str(OUT)],
        check=True,
    )


def export_steps():
    for n, f in enumerate(STEPS, 1):
        img = Image.open(FRAMES / f'f_{f:03d}.png').convert('RGB')
        w, h = img.size
        img = img.resize((WIDTH, round(h * WIDTH / w)), Image.LANCZOS)
        out = ROOT / 'assets' / f'tutorial-step{n}.webp'
        img.save(out, 'WEBP', quality=80, method=6)
        print(f'{out.name}: {out.stat().st_size / 1024:.0f} KB')


def main():
    if not PAGE.exists():
        sys.exit('Built page missing — run: python3 claude-code-session-viewer/build.py')
    if not SAMPLE.exists():
        sys.exit('Sample missing — assets/example-session.jsonl')
    capture()
    assemble()
    export_steps()
    size = OUT.stat().st_size / 1024 / 1024
    print(f'{OUT} — {TOTAL} frames @ {FPS}fps, {size:.2f} MB')
    if size > 4:
        print('WARNING: over 4 MB — consider fewer colors / lower fps')


if __name__ == '__main__':
    main()
