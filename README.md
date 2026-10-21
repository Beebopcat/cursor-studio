# Cursor Studio

[**▶ Live demo: beebopcat.github.io/cursor-studio**](https://beebopcat.github.io/cursor-studio/) - hover any card to try that cursor in your browser.

[![Cursor Studio page with the Animated preview toggle, a live test pointer and the FFXIV Crystal Dawn set cards.](docs/media/01.webp)](https://beebopcat.github.io/cursor-studio/)

**24 Windows 11 cursor sets x 4 styles** - static `.cur` and animated `.ani`, a browser selector, a dark-mode installer, and the procedural generator that renders all 3,264 cursor files.

## Screenshots and video

| | |
|:--:|:--:|
| ![Cursor Studio page with the Animated preview toggle, a live test pointer and the FFXIV Crystal Dawn set cards.](docs/media/01.webp) | ![Crystal Dawn set cards in the Animated preview, each showing 17 pointer thumbnails in styles A, B, C and C2.](docs/media/02.webp) |
| <sub>Cursor Studio page with the Animated preview toggle, a live test pointer and the FFXIV Crystal Dawn set cards.</sub> | <sub>Crystal Dawn set cards in the Animated preview, each showing 17 pointer thumbnails in styles A, B, C and C2.</sub> |
| ![Filtered to FFXIV, showing the Chocobo Caravan set cards with cursor thumbnails under the set heading.](docs/media/03.webp) | ![Scrolled down to FFXIV set 03 Void and Moon and set 04 A Realm Reborn, with their cursor thumbnails.](docs/media/04.webp) |
| <sub>Filtered to FFXIV, showing the Chocobo Caravan set cards with cursor thumbnails under the set heading.</sub> | <sub>Scrolled down to FFXIV set 03 Void and Moon and set 04 A Realm Reborn, with their cursor thumbnails.</sub> |

### Video

[![Cursor Studio page with the Animated preview toggle, a live test pointer and the FFXIV Crystal Dawn set cards.](docs/media/poster.webp)](docs/media/clip.mp4)

*Click the poster to open the short screen recording (docs/media/clip.mp4).*


Every set comes in four styles:
- **A**: relic or weapon.
- **B**: mascot.
- **C**: gauntlet, HUD or pixel.
- **C2**: a second Style C take.

Each style ships all 17 Windows pointers as **static `.cur`** and **animated `.ani`** files.

| # | Set | # | Set |
|---|---|---|---|
| 01 | FFXIV - Crystal Dawn | 13 | GW2 - Canach |
| 02 | FFXIV - Chocobo Caravan | 14 | GW2 - Palawa Joko |
| 03 | FFXIV - Void and Moon | 15 | GW2 - Tyrian Legends Ensemble |
| 04 | FFXIV - A Realm Reborn | 16 | GW2 - Blish and Taimi Magitech |
| 05 | WoW - Frostmourne Icecrown | 17 | GW2 - Canach, Joko and Tybalt |
| 06 | WoW - Ashbringer and Silver Hand | 18 | Pokemon - Kanto Companions |
| 07 | WoW - Dalaran Arcane and Emerald Dream | 19 | Pokemon - Ghost Parade |
| 08 | Goosebumps - Monster Blood | 20 | Simpsons - Springfield Donuts |
| 09 | Goosebumps - Revenge of the Lawn Gnomes | 21 | Simpsons - Nuclear Nightshift |
| 10 | GW2 - Blish | 22 | Sanrio Friends Remastered |
| 11 | GW2 - Tybalt Leftpaw | 23 | Strawberry Dream Bakery |
| 12 | GW2 - Taimi and Scruffy 2.0 | 24 | Spooky Paws |

## Use
- **Browse and test:** open `Selector.html`. Hover a card to use that pointer on the page.
- **Install on Windows 11:** double-click `App/Launch-CursorStudio.bat`. Pick a set, a style, and Animated or Static, then press Apply Now. No admin rights needed.
- **Picture guide:** `Docs/Install-Guide.html` (also `.png` and `.pdf`).
- **Manual:** every `Static/` and `Animated/` folder holds the 17 files plus an `Install.inf`.
- **CLI:** `powershell -ExecutionPolicy Bypass -File App/CursorStudio.ps1 -Set 01-Crystal-Dawn -Style A -Mode Animated -Apply`

## Revise or rebuild
See `HANDOFF.md`. `python3 Generator/v2/package.py` makes the full exportable zip.

## Disclaimer
Independent, personal-use fan project. All artwork is original and procedurally drawn by code; no game or show assets are included. Franchise names (Final Fantasy XIV, World of Warcraft, Goosebumps, Guild Wars 2, Pokemon, The Simpsons, Sanrio) are trademarks of their owners, who do not endorse this project.

## Credits
Built by Casey Shingledecker with Claude Code. Set roster and A/B/C style concepts adapted from a Gemini design proposal.
