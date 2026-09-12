#!/usr/bin/env python3
"""Static checks plus a 1D fair-player leak sim for L1-40."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")

MOBS = {
    "rat": {"hp": 1, "spd": 68},
    "bandit": {"hp": 4, "spd": 58},
    "brute": {"hp": 14, "spd": 26},
    "thief": {"hp": 2, "spd": 80},
    "goat": {"hp": 6, "spd": 42},
    "knight": {"hp": 16, "spd": 50},
    "reed": {"hp": 1, "spd": 94},
    "wagon": {"hp": 20, "spd": 36},
}
BOW = {"dmg": [1, 2, 3], "rate": [0.32, 0.28, 0.22], "range": [136, 148, 162], "pierce": [0, 1, 2]}
PAD_T = [0.80, 0.76, 0.56, 0.70]
PATH = 820.0


def must(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("FAIL: " + msg)


def parse_levels() -> list[tuple[str, list[tuple[float, list[str]]]]]:
    block = HTML.split("var LEVELS = [", 1)[1].split("];", 1)[0]
    out: list[tuple[str, list[tuple[float, list[str]]]]] = []
    for chunk in block.split("{ name:")[1:]:
        name = chunk.split('"', 2)[1]
        waves: list[tuple[float, list[str]]] = []
        for wm in re.finditer(r"\{ gap: ([0-9.]+), list: \[([^\]]+)\] \}", chunk):
            kinds = [x.strip().strip('"') for x in wm.group(2).split(",") if x.strip()]
            waves.append((float(wm.group(1)), kinds))
        out.append((name, waves))
    return out


def swarmify(levels: list[tuple[str, list[tuple[float, list[str]]]]]) -> list:
    packed = []
    for li, (name, waves) in enumerate(levels):
        nw = []
        for wi, (gap, kinds) in enumerate(waves):
            fodder = [k for k in kinds if k in ("rat", "reed") or (li >= 10 and k == "thief")]
            if not fodder:
                fodder = ["rat"] if li < 10 else ["reed"]
            if li == 0 and wi == 0:
                target = 8
            elif li < 3:
                target = 10 + li
            elif li < 5:
                target = 12 + li
            elif li < 7:
                target = 16 + li
            elif li < 10:
                target = 26 + li
            elif li < 15:
                target = 24 + (li - 10) * 3
            elif li < 20:
                target = 36 + (li - 15) * 4
            elif li < 25:
                target = 50 + (li - 20) * 2
            elif li < 32:
                target = 60 + (li - 25) * 2
            else:
                target = 74 + (li - 32) * 2
            lst = list(kinds)
            j = 0
            while len(lst) < target:
                lst.append(fodder[j % len(fodder)])
                j += 1
            boss = any(k in lst for k in ("wagon", "knight", "brute"))
            base = (
                0.30 if li < 3 else
                (0.26 if li < 5 else
                 (0.20 if li < 7 else
                  (0.16 if li < 10 else
                   (0.16 if li < 15 else
                    (0.14 if li < 20 else
                     (0.13 if li < 25 else
                      (0.12 if li < 32 else 0.11)))))))
            )
            g = max(0.28, min(0.42, gap)) if boss else base
            nw.append((g, lst))
        packed.append((name, nw))
    return packed


def live_n(li: int) -> int:
    n = 1
    if li >= 2:
        n = 2
    if li >= 5:
        n = 3
    if li >= 14:
        n = 4
    return n


def ranks_for(li: int, n: int) -> list[int]:
    if li < 5:
        return [0] * n
    if li < 10:
        return [1] + [0] * (n - 1)
    if li < 15:
        return [1] * n
    if li < 20:
        return [2] + [1] * (n - 1)
    return [2] * n


def mob_hp(kind: str, li: int) -> int:
    hp = MOBS[kind]["hp"]
    if li >= 7:
        if kind == "rat":
            hp += 1
        if kind == "thief":
            hp += 2
        if kind == "bandit":
            hp += 3
        if kind == "goat":
            hp += 5
        if kind == "brute":
            hp += 6
        if kind == "knight":
            hp += 6
    if li >= 10:
        if kind == "reed":
            hp += 1
        if kind == "thief":
            hp += 1
        if kind == "bandit":
            hp += 2
        if kind == "goat":
            hp += 3
        if kind == "knight":
            hp += 8
        if kind == "brute":
            hp += 6
    if li >= 14:
        if kind == "reed":
            hp += 1
        if kind == "wagon":
            hp += 10
        if kind == "knight":
            hp += 8
        if kind == "goat":
            hp += 3
        if kind == "bandit":
            hp += 2
        if kind == "brute":
            hp += 8
        if kind == "thief":
            hp += 1
    if li >= 20:
        if kind == "wagon":
            hp += 10
        if kind == "knight":
            hp += 8
        if kind == "goat":
            hp += 4
        if kind == "brute":
            hp += 10
        if kind == "reed":
            hp += 1
    if li >= 25:
        if kind == "reed":
            hp += 1
        if kind == "wagon":
            hp += 8
        if kind == "knight":
            hp += 6
        if kind == "goat":
            hp += 3
        if kind == "brute":
            hp += 8
        if kind == "bandit":
            hp += 2
        if kind == "thief":
            hp += 1
    if li >= 32:
        if kind == "reed":
            hp += 1
        if kind == "wagon":
            hp += 8
        if kind == "knight":
            hp += 6
        if kind == "goat":
            hp += 3
        if kind == "brute":
            hp += 8
    return hp


def simulate(waves: list[tuple[float, list[str]]], ranks: list[int], li: int = 0) -> int:
    pads = [{"d": PATH * PAD_T[i], "cd": 0.0, "r": ranks[i]} for i in range(len(ranks))]
    enemies: list[dict] = []
    leaks = 0
    wi = 0
    spawn_i = 0
    spawn_t = 0.15
    dt = 1 / 30
    guard = 0
    while guard < 20000:
        guard += 1
        if wi >= len(waves) and not enemies:
            break
        if wi < len(waves):
            gap, lst = waves[wi]
            spawn_t -= dt
            if spawn_i < len(lst) and spawn_t <= 0:
                k = lst[spawn_i]
                m = MOBS[k]
                enemies.append({"hp": mob_hp(k, li), "spd": m["spd"], "d": 0.0, "kind": k})
                spawn_i += 1
                spawn_t = gap
            if spawn_i >= len(lst) and not enemies:
                wi += 1
                spawn_i = 0
                spawn_t = 0.15
                continue
        for e in enemies:
            e["d"] += e["spd"] * dt
        leaked = [e for e in enemies if e["d"] >= PATH]
        leaks += len(leaked)
        enemies = [e for e in enemies if e["d"] < PATH and e["hp"] > 0]
        for p in pads:
            p["cd"] -= dt
            rng = BOW["range"][p["r"]]
            rnk = p["r"]
            in_rng = [e for e in enemies if abs(e["d"] - p["d"]) <= rng]
            in_rng.sort(key=lambda e: abs(e["d"] - p["d"]))
            if p["cd"] <= 0 and in_rng:
                hits = BOW["pierce"][rnk] + 1
                dmg = BOW["dmg"][rnk]
                for e in in_rng[:hits]:
                    e["hp"] -= dmg
                p["cd"] = BOW["rate"][rnk]
        enemies = [e for e in enemies if e["hp"] > 0]
    return leaks


def main() -> None:
    low = HTML.lower()
    must("kingshot" not in low, "Kingshot")
    must("Oak Gate" not in HTML and "Feast Drum" not in HTML, "old buildings")
    must("beginClear" in HTML and "finishWin" in HTML, "smooth clear")
    must("scoop" in HTML and "Scoop coins, then Next" in HTML, "scoop hold")
    must("pushOffLane" in HTML, "pads off path")
    must("reed" in HTML and "wagon" in HTML, "Act III enemies")
    must("live === 1" in HTML or "livePadCount" in HTML, "1-pad Royal Guard")
    must("wood: 50" in HTML, "L1 one T1 wood")
    must("cost: [50, 90, 160]" in HTML, "tower prices")
    must("Math.min(LEVELS.length" in HTML, "unlock to campaign length")
    must("Crown Road" in HTML and "Summer Claim" in HTML, "L16-20")
    must("Crown March" in HTML and "Feast Storm" in HTML, "L21-22")
    must("Tin Claim" in HTML and "Banner War" in HTML, "L23-24")
    must("Summer Crown" in HTML, "L25")
    must("Gate Dust" in HTML and "Capital Stand" in HTML, "L26 and L40")
    must("STAR_CAP" in HTML and "STAR_CAP = 100" in HTML, "stars toward 100")
    must("Feast shop" not in HTML and "btn-shop" not in HTML, "shop UI gone")
    must("COSMETICS" not in HTML and "scarePlace" not in HTML, "shop data gone")
    must(HTML.count("{ gap:") >= 220, "L1-40 waves")
    must("sepia" not in HTML, "king glow")
    must("dropCoin" in HTML and "tickCoins" in HTML, "coin pickups")
    must("snapCoinPos" in HTML, "reachable coins")
    must("hopH" in HTML, "bouncy coins")
    must("64 * sc" in HTML, "bigger scoop")
    must("swarmify" in HTML, "more NPCs")
    must("showBuddyTip" in HTML and "TIPS" in HTML, "buddy tips")
    must("IM.city" in HTML, "capital city")
    must("last.x + 18 * sc" in HTML, "city gate sits on path end")
    must("city = { x: last.x" in HTML, "city follows path terminus")
    must("{ nx: 0.70, ny: 0.905 }" in HTML, "path ends at castle gate")
    must(".card .meta" in HTML, "crossbow card meta")
    must("flex-direction: row" in HTML, "crossbow icon beside cost")
    must("btn-reset" in HTML, "reset on map")
    must("LIVE_CAP" in HTML and "swarmify" in HTML, "hundreds swarm")
    must("startStick" in HTML, "king drag")
    must("armies fire harder" in HTML, "Royal Guard army buff")
    must("stride" in HTML, "walk cycle")
    must("var rim" not in HTML, "color rims still present")
    must("drawMobFallback" in HTML, "creature fallbacks")
    must("Ride over gold coins" in HTML, "coin tip")
    must((ROOT / "assets/sprites/reed.png").is_file(), "reed.png")
    must((ROOT / "assets/sprites/wagon.png").is_file(), "wagon.png")
    must("spd: 80" in HTML, "thieves slowed")
    must("level >= 5) liveN = 3" in HTML, "L6 third pad")
    must("bober.cd = royal ? 0.48 : 0.62" in HTML, "king still slow")
    must("function mobHp" in HTML, "scaled mob HP")
    must("target = 26 + li" in HTML, "mid-act denser swarm")
    must("li < 7 ? 0.20" in HTML, "L8 gap tighten")
    must("lv >= 25" in HTML, "L26+ HP scale")
    must("startMagnet" in HTML and "tickMagnet" in HTML and "batchCoins" in HTML, "Next coin magnet")
    must('phase === "magnet"' in HTML, "magnet phase")
    must("c.fly" in HTML and "Gold flies to the King" in HTML, "coins arc to king")
    must("startMagnet" in HTML and "coins = []" not in HTML[HTML.find("function beginClear"):HTML.find("function finishWin")], "Next does not dump coins")
    levels = parse_levels()
    must(len(levels) == 40, "40 levels")
    packed = swarmify(levels)
    for li, (name, waves) in enumerate(packed):
        n = live_n(li)
        leaks = simulate(waves, ranks_for(li, n), li)
        hearts = 4 if li < 2 else 3
        must(leaks < hearts, "L%s %s leaks %s hearts (cap %s)" % (li + 1, name, leaks, hearts))
        if li == 5:
            must(leaks <= 1, "L6 Knife Guests too leaky: %s" % leaks)
            must(simulate(waves, [0, 0], li) <= 1, "L6 not clearable with 2 T1")
        if li >= 9:
            must(simulate(waves, [], li) >= hearts, "naked king-less L%s still too easy" % (li + 1))
        if li >= 7:
            t1 = simulate(waves, [0] * n, li)
            must(t1 >= hearts, "L%s T1-only still too easy: leaks %s" % (li + 1, t1))
        if li == 24:
            must(leaks <= 1, "L25 too leaky: %s" % leaks)
            must(any("brute" in lst or "wagon" in lst for _g, lst in waves), "L25 siege")
        if li == 39:
            must(leaks <= 1, "L40 finale too leaky: %s" % leaks)
            must(any("brute" in lst or "wagon" in lst for _g, lst in waves), "L40 siege")
    print("playtest ok")


if __name__ == "__main__":
    main()
