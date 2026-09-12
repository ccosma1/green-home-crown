#!/usr/bin/env python3
"""Static checks for Prompt 2 king-action slice."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def must(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("FAIL: " + msg)


def main() -> None:
    low = HTML.lower()
    must("kingshot" not in low, "forbidden string Kingshot")
    must("Oak Gate" not in HTML, "Oak Gate still in UI")
    must("Feast Drum" not in HTML, "Feast Drum still in UI")
    must("Sling Nest" not in HTML, "Sling Nest still in UI")
    must("Crossbow" in HTML and "Royal Ballista" in HTML, "crossbow tiers")
    must("tickKing" in HTML and "WASD" in HTML, "king move")
    must("royal" in HTML and "All ballistae ready" in HTML, "Royal Guard")
    must("thief" in HTML and "goat" in HTML and "knight" in HTML, "L6-10 enemies")
    must("hp: 2" in HTML and "hp: 6" in HTML and "hp: 18" in HTML, "hardened HP")
    must("crownMax" in HTML, "crown HP 4 then 3")
    must("max-width: 560px" in HTML, "bigger map")
    must("bober.facing" in HTML, "king facing")
    must("pullOntoLane" in HTML, "pads pulled onto lane")
    must("min-height: 55dvh" in HTML, "stage ≥55%")
    must("A short history" not in HTML, "history overlay")
    must("filmSeen" in HTML, "chapter film")
    must("gacha" not in low, "gacha")
    must(HTML.count("{ gap:") >= 10, "L1-10 waves")
    must((ROOT / "assets/sprites/bow.png").is_file(), "bow.png")
    must((ROOT / "assets/sprites/king-horse.png").is_file(), "king-horse")
    must((ROOT / "assets/sprites/thief.png").is_file(), "thief")
    must((ROOT / "assets/sprites/goat.png").is_file(), "goat")
    must((ROOT / "assets/sprites/knight.png").is_file(), "knight")
    print("playtest ok")


if __name__ == "__main__":
    main()
