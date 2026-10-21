---
name: run-cursor-studio
description: Run, build, regenerate, preview, screenshot and test Cursor Studio (Windows .cur/.ani cursor sets, the web selector page, and the PowerShell installer). Use when asked to run or screenshot the selector, preview or filter sets, validate cursor files, regenerate the selector page, build a cursor set, or check the Windows installer scripts.
---

Cursor Studio is Python-generated Windows cursor sets (`Sets/`, 24 sets x 7 styles: A, B, C, C2 plus the Gemini Originals GA, GB, GC), a static web selector (`index.html`, identical copy `Selector.html`, served by GitHub Pages) and a Windows-only PowerShell/WinForms installer (`App/`). Everything is driven through one script: `.claude/skills/run-cursor-studio/driver.py` (run from the repo root). Output (screenshots, server log, temp builds) goes to `/tmp/cursor-studio-run/`, never into the repo.

## Prerequisites

Python 3 with `pillow`, `numpy` and `playwright` (already present in the container), and the preinstalled Chromium under `/opt/pw-browsers` (the driver globs for it; never run `playwright install`).

```bash
python3 -c "import PIL, numpy, playwright; print('python deps ok')"
ls /opt/pw-browsers/chromium-*/chrome-linux/chrome
```

PowerShell (only for checking `App/*.ps1`; the installer GUI itself is Windows-only and cannot be run here). `powershell` is not in Ubuntu's apt, so install it as a dotnet tool:

```bash
sudo apt-get install -y dotnet-sdk-8.0
dotnet tool install --global PowerShell --version 7.4.6
export PATH=$PATH:/root/.dotnet/tools
pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'
```

## Run (agent path)

Drive the selector page: serves the repo root on a free port with `python3 -m http.server`, opens `index.html` in headless Chromium, and takes 6 screenshots while exercising the UI: all sets, franchise filter, Mark a style + open "My list", hover a card (live-test dock shows that cursor), open the 17-pointer modal. Prints card counts, the marked line, the modal image size and any console/page/HTTP errors (exit 1 if there are any).

```bash
python3 .claude/skills/run-cursor-studio/driver.py shot
python3 .claude/skills/run-cursor-studio/driver.py shot --filter Simp
```

Expected: `cards: 168 | sets: 24`, `filter "Pok": sets = 2 | cards = 14`, `after Mark: button = Marked | list count = 1`, `board modal: ... | img 620x332`, `console/page errors: 0`.

Screenshots -> `/tmp/cursor-studio-run/{1-all,2-filter,3-marked-list,4-hover,5-board-modal,6-gemini}.png`. Look at them (Read tool) to confirm the page really rendered: cards show previews, the dock shows the hovered cursor, the modal shows the 17-pointer board.

To keep the server up for manual poking (`shot` starts and stops its own if none is running):

```bash
python3 .claude/skills/run-cursor-studio/driver.py serve
python3 .claude/skills/run-cursor-studio/driver.py stop
```

| command | what it does |
|---|---|
| `shot [--filter TEXT]` | headless-Chromium walkthrough of index.html, screenshots + error report |
| `serve` / `stop` | background http.server on a free port (state in `/tmp/cursor-studio-run/server.json`) |
| `validate` | runs `Generator/v2/validate.py`: structurally parses every `.cur` (ICONDIR, sizes, hotspots, PNG/DIB frames) and `.ani` (RIFF/ACON, anih frame count, embedded cursors) in `Sets/` |
| `rebuild-selector` | runs `make_selector.py` (catalog.json + selector_template.html -> Selector.html + index.html), checks the two are byte-identical and that git sees no change |
| `build-gem <set>` | builds the three Gemini Originals styles (GA, GB, GC) of one set into `/tmp/cursor-studio-run/build-gem/` and validates them (about 1.5 min) |
| `build-one <set>` | builds one set (4 styles) into `/tmp/cursor-studio-run/build/` (not the repo) and validates the output |
| `ps-check [--selftest]` | parses `App/*.ps1` with the PowerShell parser; `--selftest` also runs `CursorStudio.SelfTest.ps1` against a registry stub |

## Test

Validate all committed cursor files (about 5,712 files, seconds):

```bash
python3 .claude/skills/run-cursor-studio/driver.py validate
```

Expected: `OK: 168 styles, 2856 .cur and 2856 .ani files are structurally valid`.

Rebuild the selector page and confirm it reproduces the committed one:

```bash
python3 .claude/skills/run-cursor-studio/driver.py rebuild-selector
```

Expected: `Selector.html == index.html: True` and `(clean: rebuild reproduced the committed page)`. If you edited `catalog.json` or `selector_template.html` the git status line will instead list the changed files, which is what you want to commit.

Build a single set into a temp dir and validate it (takes about 2 minutes on 4 cores, 136 files):

```bash
python3 .claude/skills/run-cursor-studio/driver.py build-one 10-Blish
```

Expected: four `{'set': '10-Blish', 'key': ...}` lines (A, B, C, C2 only; use `build-gem` for GA/GB/GC), `built into /tmp/cursor-studio-run/build`, `validated 136 built files`. Do not run `Generator/v2/build24.py` directly for a quick check: it writes into the tracked `Sets/` and `Previews/` and rewrites `catalog.json`, and a full run takes about 30 minutes. `build-one` skips the catalog rewrite and the previews it writes also go to the temp dir.

Windows installer scripts (parse check and logic self-test, about 25 s; needs `pwsh` from Prerequisites):

```bash
python3 .claude/skills/run-cursor-studio/driver.py ps-check --selftest
```

Expected: `0 parse errors` for each of the three scripts and `ALL CHECKS PASSED (336 installs)`.

## Gotchas

- **`E: Unable to locate package powershell`** - Ubuntu 24.04's apt has no PowerShell and the GitHub releases page returns 403 through the proxy. Install it as a dotnet tool from nuget (see Prerequisites).
- **`dotnet tool install --global PowerShell` (no version) fails with "Settings file 'DotnetToolSettings.xml' was not found in the package"** - the newest package is not a tool package. Pin `--version 7.4.6`.
- **`pwsh: command not found` after install** - dotnet tools live in `/root/.dotnet/tools`, which is not on PATH by default; `export PATH=$PATH:/root/.dotnet/tools` (the driver's `ps-check` also looks there).
- **One `404 (File not found)` in the browser console for `/favicon.ico`** - the page has no favicon; harmless. The driver ignores the generic "Failed to load resource" console line and reports any other failed or 4xx request by URL.
- **The installer GUI (`CursorStudio.ps1` WinForms, `Launch-CursorStudio.bat`) cannot run on Linux** - only the parse check and the registry-stub self-test are possible here.
