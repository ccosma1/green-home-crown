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
    "rat.jpg",
    "bandit.jpg",
    "brute.jpg",
    "berry.jpg",
)


def is_green(r: int, g: int, b: int) -> bool:
    return g >= 140 and g > r + 28 and g > b + 18 and r < 170 and b < 170


def key_file(src: Path) -> None:
    im = Image.open(src).convert("RGBA")
    px = im.load()
    w, h = im.size
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b, _a = px[x, y]
            if is_green(r, g, b):
                px[x, y] = (0, 0, 0, 0)
            else:
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
