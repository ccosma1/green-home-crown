#!/usr/bin/env python3
"""Static checks for Prompt 3 fewer-pads slice."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def must(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("FAIL: " + msg)


def main() -> None:
    low = HTML.lower()
    must("kingshot" not in low, "Kingshot")
    must("Oak Gate" not in HTML and "Feast Drum" not in HTML, "old buildings")
    must("beginClear" in HTML and "finishWin" in HTML, "smooth clear")
    must("pushOffLane" in HTML, "pads off path")
    must("reed" in HTML and "wagon" in HTML, "Act III enemies")
    must("live === 1" in HTML or "livePadCount" in HTML, "1-pad Royal Guard")
    must("wood: 12" in HTML, "L1 one T1 wood")
    must("min(15" in HTML, "unlock to 15")
    must(HTML.count("{ gap:") >= 80, "longer L1-15 waves")
    must("sepia" not in HTML, "king glow")
    must((ROOT / "assets/sprites/reed.png").is_file(), "reed.png")
    must((ROOT / "assets/sprites/wagon.png").is_file(), "wagon.png")
    print("playtest ok")


if __name__ == "__main__":
    main()
