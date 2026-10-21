# Cursor Studio: hand-off notes

This file is for anyone, human or AI agent, who picks the project up to revise it. Read this file and
`Generator/v2/styles24.py` first.

## What it is
- **24 Windows 11 cursor sets**, each in **7 styles**:
  - **A**: relic or weapon.
  - **B**: mascot.
  - **C**: gauntlet, HUD or pixel.
  - **C2**: a second Style C variant.
  - **GA, GB, GC - Gemini Originals**: the owner's Gemini-designed art (Gemini designs A, B, C), see "Gemini Originals" below.
- That makes **168 styles** (96 procedural + 72 Gemini). Each style has all **17 Windows pointer roles** as **static `.cur`** and **animated `.ani`** files.
- The roster and the A/B/C concept names follow the Gemini "Cursor Studio" proposal the owner approved.
- All artwork is drawn by code: original, procedurally drawn fan homage. No game assets are included.
  The franchise names are trademarks of their owners, and the package is meant for personal desktop use.
- Owner requests so far (latest first): Gemini cursor art integrated as styles GA/GB/GC; dark theme on every surface (selector, install guide, previews, installer); all A, B and C styles; the hat removed from the chocobo (it has only its crest
  feathers); Style C expanded with one more Style C set (C2) for every set; a full exportable package.

## Layout
```
CursorSets/
  catalog.json                   24 sets x 7 styles: labels, blurbs, scheme names, paths (built by build24.py)
  Sets/<NN-Set>/<Key-Label>/
      Static/   01-NormalSelect.cur ... 17-PersonSelect.cur + Install.inf
      Animated/ 01-NormalSelect.ani ... 17-PersonSelect.ani + Install.inf
  Previews/<NN-Set>/<Key>/       card.png/.gif (3 hero pointers), board.png/.gif (all 17), cursor32.png
  Selector.html, index.html         browser selector (dark theme only): hover-to-test pointers, animated/static, mark styles
  App/                           Windows installer (PowerShell + WinForms, dark mode, no admin; 7 style radios A B C C2 / GA GB GC)
      Launch-CursorStudio.bat, CursorStudio.ps1 (GUI + CLI), CursorStudio.Core.ps1 (logic), CursorStudio.SelfTest.ps1
  Docs/Install-Guide.html|.png|.pdf   illustrated install steps (app, Mouse Properties, INF)
  Generator/                     Python source that renders everything
      toolkit.py      8x supersampled canvas, gradients, glow, sparkle, shapes
      emblems.py, v2/emblems2.py, v2/emblems3.py   themed emblem painters (crystal, chocobo, helm, scarab, ...)
      roles.py        role list, hotspots, file names (shared)
      v2/materials.py render materials: gloss, flat, sticker, neon, metal, facet, gel, ink, pixel, paint
      v2/objects.py, v2/objects3.py   pointer objects: sword, spear, glaive, greatsword, runeblade, staff,
                      gauntlet, cartoonhand, brush, boltptr, rodptr, emitter, feather, hat, drip, banner, ...
      v2/fx.py        loop animations: glint, motes, embers, snow, bubbles, wisps, drips, eyes
      v2/roles2.py    the 17 role painters, built from material + object + emblem + fx
      v2/styles24.py  THE CATALOG: the 96 style definitions (palette, material, pointer, emblem, fx)
      v2/build24.py   production build (files, INF, previews, catalog)
      v2/gemini_art.py, gemini.py, build_gem.py, gemini_src/, gemini_meta.json   Gemini Originals (GA, GB, GC)
      v2/make_selector.py, make_guide.py, v2/validate.py, v2/package.py
```

## Gemini Originals (GA, GB, GC)
Structure choice: the catalog, installer and selector all key a style by a free-form string (`C2` already exists), so the three
Gemini designs per set are three more styles with keys `GA` (Gemini A), `GB` (Gemini B) and `GC` (Gemini C), shown in the
selector under a "G - Gemini Originals" sub-heading. This keeps one-style-per-key and needs no schema change; catalog entries carry
`source: "gemini"`, `art` (card art path) and `hot` (hotspot). Style folders: `Sets/<set>/GA-<Gemini title>/` etc.
- Sources: `Generator/v2/gemini_src/NNX_cur32.png` (32x32 sprite) and `NNX_img.jpg` (220x150 card art), NN = set 01..24, X = A/B/C;
  `gemini_meta.json` = titles, descriptions and accent colours from the Gemini selector page. The Gemini roster matches the 24
  Cursor Studio sets one to one (same order; only punctuation differs, e.g. "&" vs "and").
- `gemini_art.py`: cleans the sprite (drops the faint panel rectangle Gemini left at alpha 15-50), finds the hotspot (centre of the
  opaque pixels nearest the top-left corner), mattes the object out of the card art (background model + colour/luminance distance,
  feathered alpha, colour un-mixing, frame lines removed, region guided by the sprite silhouette) and decides per variant:
  `cutout` (48/64 px from the card art laid out exactly like the sprite) or `upscale` (sprite LANCZOS + unsharp) when the cutout
  does not match the sprite (IoU < 0.45) or the art is cropped by the card edge. `FORCE` overrides single variants.
- `gemini.py`: `GemStyle` (a `Style2` with a palette from the accent colour, materials metal / gloss / neon for A / B / C and the
  Gemini art as the emblem) and `render_role`. Normal Select = the sprite plus animation (accent glow pulse under, shimmer or motes
  over, from fx.py). Help, Working in Background and Person = sprite plus the roles2 badge. All other roles are the roles2 painters
  with the Gemini art as emblem. Hotspots: sprite tip for those four pointer roles, the standard `ROLES` hotspot for the rest.
- `build_gem.py [--out DIR] [--frames N] [sets...]` builds files, previews (`card`, `board`, `cursor32`, `art.jpg`) and updates
  `catalog.json`; `build24.catalog()` also emits the Gemini entries so a full `build24.py` run keeps them.
- Known limit: Gemini drew most of the A and C objects horizontally (tip pointing right), so a sprite's top-left "tip" (the
  hotspot, as specified) is often the back of the object. Rotating those sprites up-left would be a design change for the owner to approve.

## Rebuild
Requirements: Python 3.10+, `pip install pillow numpy`. Use ffmpeg only if you want videos.
```
cd CursorSets/Generator/v2
python3 build24.py            # the 96 procedural styles, about 30 min on 4 cores (add --previews-only to redo only Previews/)
python3 build_gem.py          # the 72 Gemini Originals styles, about 20 min on 4 cores
python3 build24.py 02 13      # only sets 02 and 13 (number or slug)
python3 validate.py           # structural check of every .cur/.ani
python3 make_selector.py      # refresh Selector.html from catalog.json
python3 ../make_guide.py      # refresh Docs/Install-Guide.html, .png and .pdf (dark, needs playwright + chromium)
python3 package.py            # Dist/CursorStudio-Package.zip (add --per-set for one zip per set)
pwsh ../../App/CursorStudio.SelfTest.ps1   # installer logic against a registry stub (any OS)
```

## How to revise a style
1. Find the entry in `v2/styles24.py`. It is one `S(key, label, blurb, palette, material, pointer, emblem, fx, charm, ebr)` call.
   - `palette`: `P(c1, c2, ol, ac, ac2, glow, plate, bad, halo)`. c1 and c2 are the body gradient, `ol` is the outline,
     `ac`/`ac2` are trim and accent, `glow` is the glow colour, `plate` is the dark backing and `bad` is the "Unavailable" red.
     `px(name)` is the pixel-art version of a palette (no halo). `gb=GB` forces the 4-shade handheld green.
   - `material`: one of gloss, flat, sticker, neon, metal, facet, gel, ink, pixel or paint (see materials.py).
   - `pointer`: a key of `OBJECTS` (objects.py / objects3.py). `mini` is a small arrow used with `charm='mascot'`.
   - `emblem`: a key of `EMBLEMS`, drawn on the badge, the Busy pointer and the resize arrows.
     `ebr` maps a role to an emblem (for example `E('chocobo', 'wheel')` uses the wheel for Busy, Pin and Move).
   - `charm`: True draws a badge on the Normal pointer; False means no badge (use it for object pointers);
     `'mascot'` draws a big emblem beside a mini arrow; `'flag'` draws the emblem on the banner object.
2. Rebuild that set (`python3 build24.py <NN>`), check `Previews/<NN-Set>/<Key>/board.png`,
   then run `validate.py`, `make_selector.py` and the self-test.

To add an emblem, write `def name(c, cx, cy, r, t, p)` in `emblems3.py`, drawn inside radius r and periodic
in t (0..1), then register it in the `EMBLEMS.update(...)` call. To add a pointer object, return
`[(mask, role), ...]` with the tip at (2, 2) and register it in `OBJECTS`.
Roles are body, body2, trim, dark, accent, gem and white, or a tuple of colours.

## File format notes
- `.cur`: ICONDIR type 2. The 32 px image is a classic 32-bit BGRA DIB with an AND mask. The 48 and 64 px images are PNG-compressed
  (Windows Vista and later). The hotspot is scaled per size from `roles.ROLES`.
- `.ani`: RIFF/ACON with anih (flags = AF_ICON), rate, and LIST/fram of 12 `icon` chunks. Each chunk is a .cur holding 32 px (DIB)
  and 48 px (PNG). Rate is 6 jiffies (100 ms) per frame, or 4 jiffies for Busy and Working in Background.
- `Install.inf` copies to `%WINDIR%\Cursors\<scheme>` and registers `HKCU\Control Panel\Cursors\Schemes`.
  It needs admin rights. The PowerShell app does not: it copies to `%LOCALAPPDATA%\CursorStudio\Installed`,
  writes the 17 `HKCU\Control Panel\Cursors` values and the scheme, then calls `SystemParametersInfo(SPI_SETCURSORS)`.

## Known limits and open items
- Dark theme: selector (dark only, no light mode), install guide (HTML/PNG/PDF), previews (both desktop strips on the board are dark), installer (was already dark).
- Everything was built and checked on Linux. The files are validated structurally and the installer logic is unit-tested
  against a registry stub. **The WinForms window, the real registry writes, and Windows' handling of PNG frames inside
  `.ani` have not been run on a Windows machine.** If animated pointers look blank on some PC, rebuild with
  `make_cur` writing DIBs for every size (one-line change in `build24.py`).
- At 32 px the gauntlet pointers read as a gloved fist pointing up-left. They are worth a hand-tuned pass.
- The art is procedural vector art, not painted illustration. For a painterly upgrade, swap an emblem painter for
  a hand-made 256 px PNG sprite (load it with Pillow and composite it in the emblem function) and keep the pipeline.
