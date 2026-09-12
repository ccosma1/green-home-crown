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
    must("min(20" in HTML, "unlock to 20")
    must("Crown Road" in HTML and "Summer Claim" in HTML, "L16-20")
    must(HTML.count("{ gap:") >= 110, "L1-20 waves")
    must("sepia" not in HTML, "king glow")
    must("dropCoin" in HTML and "tickCoins" in HTML, "coin pickups")
    must("snapCoinPos" in HTML, "reachable coins")
    must("hopH" in HTML, "bouncy coins")
    must("64 * sc" in HTML, "bigger scoop")
    must("densify" in HTML, "more NPCs")
    must("Ride over gold coins" in HTML, "coin tip")
    must((ROOT / "assets/sprites/reed.png").is_file(), "reed.png")
    must((ROOT / "assets/sprites/wagon.png").is_file(), "wagon.png")
    print("playtest ok")


if __name__ == "__main__":
    main()
