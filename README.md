# Green Home Crown

Fan game by a holder. Not affiliated with any token, studio, or official Bober project.

**Play online:** https://ccosma1.github.io/green-home-crown/

Splash: **GREEN HOME CROWN · Summer stays.**  
Tag: Fan game by a holder.  
CTA: More games · [Green Home Games](https://ccosma1.github.io/green-home-games/)

A mobile-first **stage defense + build-between-waves** in the browser. Hold the Crown through feast-raiders. Prompt 0 ships **L1–5 Summer Dawn** only.

No install. No wallet. No login. No gacha. No PvP. No build timers.

## Local

Run `START.bat` or open `index.html` in a browser.

## How to play

1. **FACE THE SUMMER**, then pick a level. L1 is unlocked; beat a level to open the next.
2. **Build phase** — tap a pad to place **Sling Nest** or **Feast Drum**. **Oak Gate** only goes on the blue **gate pad** at the choke bend. Tap a berry bush once for wood. Tap a building again to upgrade (once).
3. **START WAVE** — enemies walk the bent meadow road toward the Crown (5 hearts). They stop to melee a live Gate until it breaks. You cannot place during a wave.
4. Clear every wave to win. Crown HP ≤ 0 → **Retry** (soft save).
5. **L1** teaches Nest then Gate. **Skip** is always on screen and auto-places a Nest so you cannot softlock.

### Buildings

| Building | Role | Cost |
|---|---|---|
| Sling Nest | Single-target ranged DPS | 14 wood |
| Oak Gate | Enemies melee the Gate until it breaks, then pass | 10 wood |
| Feast Drum | Cooldown AoE thump + 0.35s stagger | 16 wood |

### Enemies

| Unit | Role |
|---|---|
| Field Rat | HP 1, fast |
| Picnic Bandit | HP 3, medium |
| Meadow Brute (L5) | HP 10, slow. Slam telegraph ≥ 0.45s |

Wood drops from clears. Tiny costs. No shop maze. No job cards.

L5 clear plays a skippable cartoon picnic-truck cameo.

## Soft save

Key `green-home-crown-v1`: unlocked level, wood, stars, tutDone, mute.

**New game** wipes unlocks, wood, and tutorial. Splash **FACE THE SUMMER** goes straight to the level map — no history slideshow.

## GitHub Pages

Live at **https://ccosma1.github.io/green-home-crown/**

Repo slant: `green-home-crown`

`.nojekyll` is included so GitHub does not run Jekyll on the assets.

## Files

- `index.html` — the game (HTML, CSS, canvas JS)
- `assets/splash.jpg` — title art
- `assets/cameo-picnic.jpg` — L5 picnic-truck cameo
- `assets/sprites/` — keyed buildings, enemies, Bober, Crown
- `assets/icons/` — original crown-on-grass mark (summer sky, not night purple)
- `scripts/make_icon.py` — regenerates the mark
- `scripts/prep_assets.py` — chroma-key sprites + hub card crop
- `SPINE.md` — campaign acts (document only — not implemented past L5)

## Note

This is a fan game by a holder. It does not connect to a chain, a wallet, or a score server.
It is ads-facing sunny town-defense — not a Lodge colony-sim, not a Dam river-path TD, not an idle MMO.
