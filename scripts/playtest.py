#!/usr/bin/env python3
"""Static + numeric checks for Prompt 0d slice."""

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
    must("Stick Fence" not in HTML, "Stick Fence still in UI")
    must("Sap Bowl" not in HTML, "Sap Bowl still in UI")
    must("Oak Gate" in HTML and "Feast Drum" in HTML and "Sling Nest" in HTML, "new trio")
    must("A short history" not in HTML, "history overlay still present")
    must('SAVE_KEY = "green-home-crown-v1"' in HTML, "save key")
    must("FACE THE SUMMER" in HTML, "splash CTA")
    must("Fan game by a holder." in HTML, "tag")
    must("https://ccosma1.github.io/green-home-games/" in HTML, "hub link")
    must("tutDone" in HTML, "tutorial persist")
    must("skipTut" in HTML and "btn-skip" in HTML, "Skip control")
    must("samplePath" in HTML, "bent path sampler")
    must("TELE = 0.62" in HTML, "brute telegraph")
    must("min-height: 55dvh" in HTML, "stage ≥55% viewport")
    must("canPlaceNow" in HTML, "mid-fight place gate")
    must("filmSeen" in HTML, "chapter film persist")
    must("Wipe run?" in HTML, "wipe behind pause")
    must("id=\"btn-new\"" not in HTML, "splash New game still present")
    must("id=\"btn-win-map\"" not in HTML, "twin win Map still present")
    must("king-horse" in HTML, "king horse sprite")
    must("Opens later" in HTML, "locked pad tip")
    must("gacha" not in low and "alliance" not in low, "no gacha/alliances")
    must(HTML.count("{ gap:") >= 5, "waves present")

    must((ROOT / "assets/sprites/gate.png").is_file(), "missing gate.png")
    must((ROOT / "assets/sprites/drum.png").is_file(), "missing drum.png")
    must((ROOT / "assets/sprites/king-horse.png").is_file(), "missing king-horse.png")
    for n in range(1, 11):
        must((ROOT / ("assets/film/f%d.jpg" % n)).is_file(), "missing film f%d" % n)
    must(0.62 >= 0.45, "telegraph floor")

    print("playtest ok")


if __name__ == "__main__":
    main()
