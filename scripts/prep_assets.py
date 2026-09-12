#!/usr/bin/env python3
"""Chroma-key sprite JPGs to PNG and crop a hub card from splash."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPR = ROOT / "assets" / "sprites"
HUB = ROOT / "assets" / "hub-card.jpg"

SPRITES = (
    "bober.jpg",
    "crown.jpg",
    "fence.jpg",
    "sling.jpg",
    "sap.jpg",
    "gate.jpg",
    "drum.jpg",
    "king-horse.jpg",
    "bow.jpg",
    "ballista.jpg",
    "thief.jpg",
    "goat.jpg",
    "knight.jpg",
    "reed.jpg",
    "wagon.jpg",
    "city.jpg",
    "buddy.jpg",
    "rat.jpg",
    "bandit.jpg",
    "brute.jpg",
    "berry.jpg",
)


def is_green(r: int, g: int, b: int) -> bool:
    return g >= 140 and g > r + 28 and g > b + 18 and r < 170 and b < 170


def is_city_sage(r: int, g: int, b: int) -> bool:
    """City art uses a yellow-sage chroma the generic key misses."""
    dr, dg, db = r - 156, g - 178, b - 64
    return dr * dr + dg * dg + db * db <= 32 * 32


def key_city_sage(im: Image.Image) -> Image.Image:
    """Flood-fill sage from the edges so castle lawn/dirt stay opaque."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    seen = bytearray(w * h)
    stack = []

    def seed(x: int, y: int) -> None:
        i = y * w + x
        if seen[i]:
            return
        r, g, b, _a = px[x, y]
        if is_city_sage(r, g, b):
            seen[i] = 1
            stack.append((x, y))

    for x in range(w):
        seed(x, 0)
        seed(x, h - 1)
    for y in range(h):
        seed(0, y)
        seed(w - 1, y)
    while stack:
        x, y = stack.pop()
        px[x, y] = (0, 0, 0, 0)
        if x > 0:
            seed(x - 1, y)
        if x + 1 < w:
            seed(x + 1, y)
        if y > 0:
            seed(x, y - 1)
        if y + 1 < h:
            seed(x, y + 1)
    # Soften leftover sage fringe on the cut
    fringe = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if not is_city_sage(r, g, b):
                continue
            edge = (
                (x and px[x - 1, y][3] == 0)
                or (x + 1 < w and px[x + 1, y][3] == 0)
                or (y and px[x, y - 1][3] == 0)
                or (y + 1 < h and px[x, y + 1][3] == 0)
            )
            if edge:
                fringe.append((x, y))
    for x, y in fringe:
        px[x, y] = (0, 0, 0, 0)
    return im


def key_file(src: Path) -> None:
    im = Image.open(src).convert("RGBA")
    if src.name == "city.jpg":
        im = key_city_sage(im)
    px = im.load()
    w, h = im.size
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if src.name != "city.jpg" and is_green(r, g, b):
                px[x, y] = (0, 0, 0, 0)
                continue
            if x < minx:
                minx = x
            if y < miny:
                miny = y
            if x > maxx:
                maxx = x
            if y > maxy:
                maxy = y
    if maxx <= minx:
        im.save(src.with_suffix(".png"))
        return
    pad = max(4, int(min(w, h) * 0.03))
    box = (
        max(0, minx - pad),
        max(0, miny - pad),
        min(w, maxx + 1 + pad),
        min(h, maxy + 1 + pad),
    )
    im.crop(box).save(src.with_suffix(".png"))


def crop_hub() -> None:
    splash = ROOT / "assets" / "splash.jpg"
    im = Image.open(splash).convert("RGB")
    w, h = im.size
    side = min(w, int(h * 0.62))
    left = max(0, (w - side) // 2)
    top = max(0, int(h * 0.28))
    if top + side > h:
        top = h - side
    im.crop((left, top, left + side, top + side)).resize((512, 512), Image.Resampling.LANCZOS).save(
        HUB, quality=86
    )


def main() -> None:
    for name in SPRITES:
        key_file(SPR / name)
        print("keyed", name)
    crop_hub()
    print("hub", HUB)


if __name__ == "__main__":
    main()
