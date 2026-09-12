#!/usr/bin/env python3
"""Rasterize the Green Home Crown mark from original polygons.

Summer-sky full-bleed square, stout three-point gold crown on a squat
grass oval, cream heart on the band. PIL ImageDraw only.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
MASTER = 1024
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)


def _rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.removeprefix("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


SKY = _rgb("#87C6E8")
GRASS = _rgb("#6B9E3A")
GOLD = _rgb("#F5C400")
CREAM = _rgb("#F4E6C3")
JEWEL = _rgb("#C62828")
TIMBER = _rgb("#5C3A1A")
FUR = _rgb("#8B5A2B")
INK = _rgb("#1A1028")


def _mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


GOLD_LIT = _mix(GOLD, CREAM, 0.42)
GOLD_DIM = _mix(GOLD, TIMBER, 0.34)
GRASS_LIT = _mix(GRASS, GOLD, 0.22)
GRASS_DIM = _mix(GRASS, INK, 0.22)
MOSS = _mix(GRASS, FUR, 0.28)


def _stamp_xy(weight: float, steps: int = 20) -> list[tuple[float, float]]:
    return [
        (math.cos(math.tau * i / steps) * weight, math.sin(math.tau * i / steps) * weight)
        for i in range(steps)
    ]


def _shift(pts: list[tuple[float, float]], dx: float, dy: float) -> list[tuple[float, float]]:
    return [(x + dx, y + dy) for x, y in pts]


def poly(draw: ImageDraw.ImageDraw, pts, fill, ink=None, weight: float = 0) -> None:
    if ink is not None and weight > 0:
        for dx, dy in _stamp_xy(weight):
            draw.polygon(_shift(pts, dx, dy), fill=ink)
    draw.polygon(pts, fill=fill)


def oval(draw: ImageDraw.ImageDraw, box, fill, ink=None, weight: float = 0) -> None:
    l, t, r, b = box
    if ink is not None and weight > 0:
        for dx, dy in _stamp_xy(weight):
            draw.ellipse((l + dx, t + dy, r + dx, b + dy), fill=ink)
    draw.ellipse(box, fill=fill)


def bowed_base(x0: float, x1: float, y: float, sag: float, n: int = 9) -> list[tuple[float, float]]:
    """Downward parabola so the band nestles into the grass oval."""
    pts = []
    for i in range(n):
        u = i / (n - 1)
        pts.append((x0 + (x1 - x0) * u, y + sag * 4.0 * u * (1.0 - u)))
    return pts


def stout_crown() -> list[tuple[float, float]]:
    """Closed 3-merlon crown, wider at the band, small flats on the peaks."""
    cx = 512.0
    band_top = 448.0
    band_bot = 678.0
    x_bot_l, x_bot_r = 138.0, 886.0
    x_top_l, x_top_r = 176.0, 848.0
    left_peak = (292.0, 228.0)
    mid_peak = (cx, 104.0)
    right_peak = (732.0, 228.0)
    valley_l, valley_r = 404.0, 620.0
    side_flat = 18.0
    mid_flat = 22.0

    top = [
        (x_top_l, band_top),
        (left_peak[0] - side_flat, left_peak[1] + 10.0),
        (left_peak[0], left_peak[1]),
        (left_peak[0] + side_flat, left_peak[1] + 10.0),
        (valley_l, band_top),
        (mid_peak[0] - mid_flat, mid_peak[1] + 14.0),
        (mid_peak[0], mid_peak[1]),
        (mid_peak[0] + mid_flat, mid_peak[1] + 14.0),
        (valley_r, band_top),
        (right_peak[0] - side_flat, right_peak[1] + 10.0),
        (right_peak[0], right_peak[1]),
        (right_peak[0] + side_flat, right_peak[1] + 10.0),
        (x_top_r, band_top),
        (x_bot_r, band_bot),
    ]
    base = bowed_base(x_bot_r, x_bot_l, band_bot, sag=30.0)
    return top + base[1:]


def merlon_lit() -> list[list[tuple[float, float]]]:
    """Sun-catch quads along the left slope of each merlon."""
    return [
        [(198.0, 448.0), (274.0, 238.0), (292.0, 228.0), (250.0, 448.0)],
        [(404.0, 448.0), (490.0, 118.0), (512.0, 104.0), (470.0, 448.0)],
        [(620.0, 448.0), (714.0, 238.0), (732.0, 228.0), (690.0, 448.0)],
    ]


def band_dim_wedge() -> list[tuple[float, float]]:
    return [
        (176.0, 448.0),
        (848.0, 448.0),
        (886.0, 678.0),
        (700.0, 698.0),
        (512.0, 708.0),
        (138.0, 678.0),
    ]


def cream_heart(cx: float, cy: float, scale: float, n: int = 40) -> list[tuple[float, float]]:
    pts = []
    for i in range(n):
        th = math.tau * i / n
        x = 16.0 * math.sin(th) ** 3
        y = 13.0 * math.cos(th) - 5.0 * math.cos(2.0 * th) - 2.0 * math.cos(3.0 * th) - math.cos(4.0 * th)
        pts.append((cx + x * scale / 16.0, cy - y * scale / 16.0))
    return pts


def jewel_diamond(cx: float, cy: float, hw: float, hh: float) -> list[tuple[float, float]]:
    return [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]


def paint_mark(size: int) -> Image.Image:
    im = Image.new("RGBA", (MASTER, MASTER), (*SKY, 255))
    d = ImageDraw.Draw(im)

    # Tiny moss knolls peek from behind the crown — ears only, no face.
    oval(d, (102, 402, 198, 508), MOSS, ink=INK, weight=20)
    oval(d, (826, 402, 922, 508), MOSS, ink=INK, weight=20)
    oval(d, (118, 416, 180, 488), GRASS_LIT)
    oval(d, (844, 416, 906, 488), GRASS_LIT)

    oval(d, (58, 598, 966, 978), GRASS, ink=INK, weight=38)
    oval(d, (58, 598, 966, 978), GRASS_DIM)
    oval(d, (150, 628, 700, 868), GRASS_LIT)
    oval(d, (210, 658, 520, 820), _mix(GRASS_LIT, CREAM, 0.18))

    crown = stout_crown()
    poly(d, crown, GOLD, ink=INK, weight=42)
    poly(d, band_dim_wedge(), GOLD_DIM)
    for quad in merlon_lit():
        poly(d, quad, GOLD_LIT)
    # Band plate so the heart sits on metal, not a vertical door slit.
    poly(
        d,
        [(230.0, 500.0), (794.0, 500.0), (818.0, 650.0), (206.0, 650.0)],
        GOLD_DIM,
    )
    poly(
        d,
        [(250.0, 518.0), (774.0, 518.0), (790.0, 632.0), (234.0, 632.0)],
        GOLD,
    )
    poly(
        d,
        [(250.0, 518.0), (430.0, 518.0), (400.0, 632.0), (234.0, 632.0)],
        GOLD_LIT,
    )

    heart = cream_heart(512.0, 568.0, 78.0)
    poly(d, heart, CREAM, ink=INK, weight=14)
    poly(d, cream_heart(500.0, 558.0, 28.0), _mix(CREAM, GOLD, 0.15))

    gem = jewel_diamond(512.0, 168.0, 26.0, 34.0)
    poly(d, gem, JEWEL, ink=INK, weight=12)
    poly(d, jewel_diamond(506.0, 160.0, 10.0, 12.0), _mix(JEWEL, CREAM, 0.45))

    if size != MASTER:
        im = im.resize((size, size), Image.Resampling.LANCZOS)
    return im


def main() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    master = paint_mark(MASTER)

    png_512 = ICON_DIR / "icon-512.png"
    png_192 = ICON_DIR / "icon-192.png"
    ico_path = ICON_DIR / "green-home-crown.ico"

    master.resize((512, 512), Image.Resampling.LANCZOS).save(png_512, format="PNG")
    master.resize((192, 192), Image.Resampling.LANCZOS).save(png_192, format="PNG")

    # Pillow ICO skips any size larger than the first image, so 256 leads.
    by_size = {
        s: master.resize((s, s), Image.Resampling.LANCZOS).convert("RGBA")
        for s in ICO_SIZES
    }
    lead = by_size[max(ICO_SIZES)]
    extras = [by_size[s] for s in ICO_SIZES if s != max(ICO_SIZES)]
    lead.save(
        ico_path,
        format="ICO",
        append_images=extras,
        sizes=[(s, s) for s in ICO_SIZES],
    )
    print(f"wrote {png_192}")
    print(f"wrote {png_512}")
    print(f"wrote {ico_path}")


if __name__ == "__main__":
    main()
