#!/usr/bin/env python3
"""Render the homepage tutorial GIF with Playwright + ffmpeg.

Loads the built English landing page, injects tools/tutorial_overlay.js and
captures one deterministic frame per step of window.__seek(f), then assembles
an optimized palette GIF into assets/tutorial.gif.
"""
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'claude-code-session-viewer' / 'index.html'
OVERLAY = Path(__file__).resolve().parent / 'tutorial_overlay.js'
FRAMES = Path('/tmp/ccviewer-tutorial-frames')
OUT = ROOT / 'assets' / 'tutorial.gif'

FPS = 10
TOTAL = 150
OPEN_AT = 68          # first frame of the viewer; dialog is fading out here
WIDTH = 880           # output GIF width (page captured at 960x600 @2x)


def capture():
    FRAMES.mkdir(parents=True, exist_ok=True)
    for old in FRAMES.glob('f_*.png'):
        old.unlink()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 960, 'height': 600}, device_scale_factor=2)
        page.goto(PAGE.as_uri())
        page.wait_for_timeout(2200)  # fonts + landing fade-in animations
        page.add_script_tag(path=str(OVERLAY))
        for f in range(TOTAL):
            if f == OPEN_AT:
                page.evaluate('window.__tutOpenDemo()')
                page.wait_for_timeout(400)
            page.evaluate(f'window.__seek({f})')
            page.screenshot(path=str(FRAMES / f'f_{f:03d}.png'), clip={'x': 0, 'y': 0, 'width': 960, 'height': 600})
        browser.close()


def assemble():
    vf = (
        f'scale={WIDTH}:-2:flags=lanczos,split[a][b];'
        '[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4'
    )
    subprocess.run(
        ['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS),
         '-i', str(FRAMES / 'f_%03d.png'), '-vf', vf, '-loop', '0', str(OUT)],
        check=True,
    )


def main():
    if not PAGE.exists():
        sys.exit('Built page missing — run: python3 claude-code-session-viewer/build.py')
    capture()
    assemble()
    size = OUT.stat().st_size / 1024 / 1024
    print(f'{OUT} — {len(list(FRAMES.glob("f_*.png")))} frames @ {FPS}fps, {size:.2f} MB')
    if size > 4:
        print('WARNING: over 4 MB — consider fewer colors / lower fps')


if __name__ == '__main__':
    main()
