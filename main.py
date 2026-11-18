#!/usr/bin/env python3
"""Build the make.fun entry image for the news-image-20261117 bounty."""

import os
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
BG = (10, 16, 34)
PANEL = (16, 26, 48)
TEXT = (235, 240, 255)
MUTED = (170, 180, 205)
ACCENT = (200, 30, 45)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def main() -> None:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_xl = ImageFont.truetype(FONT_BOLD_PATH, 92)
        font_md = ImageFont.truetype(FONT_PATH, 40)
        font_sm = ImageFont.truetype(FONT_PATH, 30)
    except Exception:
        font_xl = font_md = font_sm = ImageFont.load_default()

    title = "WORLD NEWS — NOVEMBER 17, 2026"
    tw = draw.textlength(title, font=font_xl)
    tx = (CANVAS_W - tw) / 2
    draw.text((tx, 150), title, fill=TEXT, font=font_xl)

    subtitle = "THE WORLD IN ONE PICTURE"
    sw = draw.textlength(subtitle, font=font_sm)
    draw.text(((CANVAS_W - sw) / 2, 252), subtitle, fill=MUTED, font=font_sm)

    stories = [
        ("GEOPOLITICS", "UN emergency session debates a coordinated maritime security corridor after the day’s flash floods and port closures."),
        ("SCIENCE", "European research consortium confirms a new climate telemetry array off the polar shelf, with live data streams opening to public dashboards."),
        ("SPORT", "International league final heads to a dramatic extra-time finish, with record crowd turnout and final-minute equalizer."),
        ("MARKETS", "Traders watch a sharp but orderly gold rally as central banks signal a coordinated liquidity response."),
    ]

    top = 390
    spacing = 150
    for i, (cat, body) in enumerate(stories):
        y0 = top + i * spacing
        draw.rounded_rectangle([44, y0 - 24, CANVAS_W - 44, y0 - 24 + 116], radius=22, fill=PANEL)
        draw.rounded_rectangle([44, y0 - 24, 44 + 14, y0 - 24 + 116], radius=7, fill=ACCENT)
        draw.text((70, y0 - 22), cat, fill=ACCENT)
        words = body.split()
        maxw = CANVAS_W - 140
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=font_md) <= maxw:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        y = y0 + 18
        for line in lines[:2]:
            draw.text((70, y), line, fill=TEXT, font=font_md)
            y += 46

    out_dir = os.environ.get("MAKEFUN_OUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    img.save(out, format="PNG")
    return out


if __name__ == "__main__":
    p = main()
    print(p)
