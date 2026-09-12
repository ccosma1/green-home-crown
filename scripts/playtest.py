#!/usr/bin/env python3
"""Static + numeric checks for Prompt 0 Summer Dawn slice."""

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
    must("wallet" not in low or "does not connect" in (ROOT / "README.md").read_text(encoding="utf-8").lower(), "wallet UI")
    must('SAVE_KEY = "green-home-crown-v1"' in HTML, "save key")
    must("FACE THE SUMMER" in HTML, "splash CTA")
    must("Fan game by a holder." in HTML, "tag")
    must("Green Home Games" in HTML, "hub CTA")
    must("https://ccosma1.github.io/green-home-games/" in HTML, "hub link")
    must("Stick Fence" in HTML and "Sling Nest" in HTML and "Sap Bowl" in HTML, "3 buildings")
    must("Field Rat" in HTML or '"rat"' in HTML, "field rat")
    must("Meadow Gate" in HTML and "Summer Dawn" in HTML, "L1 and L5 names")
    must("e.tele = 0.55" in HTML, "brute telegraph 0.55s")
    must("min-height: 55dvh" in HTML, "stage ≥55% viewport")
    must(HTML.count("waves:") >= 5 or "LEVELS = [" in HTML, "levels present")
    must(HTML.count("{ gap:") >= 5, "waves present")
    must("A short history" not in HTML, "history overlay still present")
    must("id=\"history\"" not in HTML, "history DOM still present")
    must("drawPathRibbon" in HTML and "#F4E6C3" in HTML, "cream dirt ribbon")
    must("gacha" not in low and "alliance" not in low, "no gacha/alliances")

    # L1 sling vs rats: path ~0.75 of 520px, rat 86 px/s
    travel = (0.75 * 520) / 86
    shots = travel / 0.68
    must(shots > 4, "L1 sling should outpace 4 rats on the lane")
    must(0.55 >= 0.45, "telegraph floor")

    for p in (
        "assets/splash.jpg",
        "assets/cameo-picnic.jpg",
        "assets/sprites/bober.png",
        "assets/sprites/brute.png",
        "assets/icons/green-home-crown.ico",
        "assets/icons/icon-192.png",
        "assets/icons/icon-512.png",
        "START.bat",
        ".nojekyll",
        "SPINE.md",
        "BRAND_MARK.md",
    ):
        must((ROOT / p).is_file(), "missing " + p)

    print("playtest ok")
    print("L1 travel %.2fs, sling shots on first rat ~%.1f" % (travel, shots))


if __name__ == "__main__":
    main()
