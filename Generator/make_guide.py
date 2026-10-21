"""Generates Docs/Install-Guide.html (self-contained, graphical) from the built Crystal Dawn set."""
import base64, io, os, struct, sys, json
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
from roles import ROLES, FILE_NAMES

_c = json.load(open(os.path.join(ROOT, 'catalog.json')))
DEMO_ST = _c['sets'][0]['styles'][0]
DEMO = os.path.join(ROOT, DEMO_ST['path'])
DEMO_PREV = os.path.join(ROOT, DEMO_ST['preview'])


def read_cur(path, want=32):
    d = open(path, 'rb').read()
    n = struct.unpack('<H', d[4:6])[0]
    for i in range(n):
        w, h, _, _, hx, hy, sz, off = struct.unpack('<BBBBHHII', d[6 + 16 * i:22 + 16 * i])
        if w == want:
            b = d[off:off + sz]
            W, H2 = struct.unpack('<ii', b[4:12]); H = H2 // 2
            xor = b[40:40 + W * H * 4]
            im = Image.new('RGBA', (W, H)); px = im.load()
            for y in range(H):
                for x in range(W):
                    o = ((H - 1 - y) * W + x) * 4
                    px[x, y] = (xor[o + 2], xor[o + 1], xor[o], xor[o + 3])
            return im


def b64png(im, scale=1):
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    bio = io.BytesIO(); im.save(bio, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(bio.getvalue()).decode()


def b64file(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


icons = {k: b64png(read_cur(os.path.join(DEMO, 'Static', FILE_NAMES[k] + '.cur'))) for k, _, _ in ROLES}
cat = _c
prev_static = b64file(os.path.join(DEMO_PREV, 'board.png'), 'image/png')
prev_anim = b64file(os.path.join(DEMO_PREV, 'board.gif'), 'image/gif')

rows = ''.join(
    f'<div class="row{" sel" if k == "Arrow" else ""}"><span>{n}</span><img src="{icons[k]}" width="32" height="32"></div>'
    for k, n, _ in ROLES)

tree = ''
cur = None
for s in cat['sets']:
    if s['group'] != cur:
        cur = s['group']
        tree += f'<div class="tf">{cur.upper().replace("-", " / ")}</div>'
    tree += f'<div class="tn{" on" if s["num"] == 1 else ""}">{s["name"].split(" - ", 1)[-1]}</div>'

HTML = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cursor Studio Install Guide</title>
<style>
:root{{--bg:#0c1020;--pn:#151a2e;--pn2:#232a47;--tx:#eef1fc;--dim:#98a2c4;--ac:#8274ff;--ac2:#47e3ff;--ok:#6edca0;--warn:#ffcf5a;--win:#23252f;--wint:#202225;color-scheme:dark}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--tx);font:16px/1.55 "Segoe UI",system-ui,sans-serif}}
.wrap{{max-width:1040px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:34px;margin:0 0 6px;letter-spacing:-.02em}}h2{{font-size:24px;margin:48px 0 6px}}h3{{margin:0 0 6px;font-size:17px}}
.lead{{color:var(--dim);margin:0 0 24px}}
.tag{{display:inline-block;background:var(--ac);color:#fff;border-radius:99px;padding:2px 12px;font-size:13px;font-weight:600;margin-right:8px}}
.steps{{display:grid;gap:18px}}
.step{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:20px;background:var(--pn);border-radius:16px;padding:18px;align-items:center}}
@media(max-width:760px){{.step{{grid-template-columns:1fr}}}}
.num{{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--ac);color:#fff;font-weight:700;margin-right:8px}}
.badge{{position:absolute;display:grid;place-items:center;width:24px;height:24px;border-radius:50%;background:#ff4f7a;color:#fff;font-weight:700;font-size:13px;box-shadow:0 0 0 3px rgba(255,79,122,.35)}}
.mock{{position:relative;border-radius:10px;overflow:hidden;background:var(--win);color:#e4e7f2;box-shadow:0 10px 30px rgba(0,0,0,.35);font:13px/1.35 "Segoe UI",sans-serif}}
.tb{{background:#181a24;padding:7px 10px;display:flex;justify-content:space-between;font-size:12px;color:#b4bad2}}
.mock.dark{{background:#1a1c28;color:#eef}}.mock.dark .tb{{background:#10121a;color:#aab}}
kbd{{background:#2d3350;border:1px solid #4a5280;border-bottom-width:3px;border-radius:6px;padding:1px 8px;font:600 13px "Segoe UI";color:#eef1fc}}
code{{background:var(--pn2);padding:1px 7px;border-radius:6px;font-size:14px}}
.tabs{{display:flex;gap:2px;padding:8px 10px 0;background:#23252f;font-size:12px}}.tabs span{{padding:5px 9px;border:1px solid #444a66;border-bottom:none;border-radius:4px 4px 0 0;background:#2c2f3c}}.tabs .a{{background:#343848;font-weight:600}}
.body{{background:#2a2d3a;padding:10px 12px;border:1px solid #444a66;margin:0 10px 10px}}
.sel-box{{border:1px solid #666c8a;padding:4px 8px;display:flex;justify-content:space-between;margin:4px 0 8px;background:#1c1e29}}
.list{{border:1px solid #999;height:216px;overflow:hidden;margin:4px 0 8px}}.row{{display:flex;justify-content:space-between;align-items:center;padding:0 8px;height:24px;font-size:12px}}
.row img{{height:22px;width:22px}}.row.sel{{background:#0a64c8;color:#fff}}
.btns{{display:flex;gap:6px;justify-content:flex-end}}.btn{{border:1px solid #666c8a;background:#353a52;color:#e4e7f2;padding:3px 14px;font-size:12px;border-radius:3px}}.btn.p{{border-color:#4aa3ff;box-shadow:0 0 0 1px #4aa3ff}}
.fx{{display:flex;font-size:12px;height:230px}}.fxs{{width:150px;background:#1e2029;border-right:1px solid #3a3f56;padding:8px}}.fxm{{flex:1;padding:8px}}
.f{{display:flex;align-items:center;gap:6px;padding:5px 8px;border-radius:4px}}.f.s{{background:#2f4a78}}.ico{{width:16px;height:12px;background:#f2c14e;border-radius:2px}}
.studio{{display:grid;grid-template-columns:150px 1fr;height:260px;font-size:11px}}.sl{{background:#212434;padding:8px;overflow:hidden}}.tf{{color:#8d97bd;font-weight:600;font-size:9px;margin:5px 4px 1px}}.tn{{padding:2px 6px;border-radius:5px;font-size:10px;white-space:nowrap}}.tn.on{{background:#7a6cff;color:#fff}}
.sr{{padding:8px}}.sr img{{width:100%;border-radius:8px;display:block}}.rad{{display:flex;gap:14px;margin:7px 0;font-weight:600}}.dot{{display:inline-block;width:10px;height:10px;border:2px solid #7a6cff;border-radius:50%;vertical-align:-1px;margin-right:5px}}.dot.on{{background:#7a6cff}}
.db{{display:inline-block;padding:4px 10px;border-radius:5px;background:#2a2e40;font-size:10px;margin-right:4px;font-weight:600}}.db.p{{background:#7a6cff}}
.tip{{background:var(--pn2);border-left:4px solid var(--warn);border-radius:8px;padding:10px 14px;margin:14px 0;font-size:15px}}
.tip.ok{{border-color:var(--ok)}}
table{{width:100%;border-collapse:collapse;font-size:14px}}td,th{{padding:7px 10px;border-bottom:1px solid var(--pn2);text-align:left}}
.tree{{background:var(--pn);border-radius:12px;padding:14px 18px;font:13px/1.5 ui-monospace,Consolas,monospace;overflow:auto;white-space:pre}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}@media(max-width:760px){{.cols{{grid-template-columns:1fr}}}}
.cols img{{width:100%;border-radius:12px}}
@media print{{html,body{{background:#0c1020;-webkit-print-color-adjust:exact;print-color-adjust:exact}}.step,.tip{{break-inside:avoid}}}}
</style></head><body><div class="wrap">
<h1>Cursor Studio - Install Guide</h1>
<p class="lead">Windows 11 - 24 cursor sets x 7 styles (A, B, C, C2 and the three Gemini Originals GA, GB, GC) - every style ships as <b>Animated</b> (<code>.ani</code>) and <b>Static</b> (<code>.cur</code>). Choose the path that suits you:</p>
<p><span class="tag">A</span><b>Cursor Studio app</b> (recommended, one click, no admin) &nbsp; <span class="tag">B</span><b>Manual</b> via Mouse Properties &nbsp; <span class="tag">C</span><b>Right-click Install.inf</b></p>

<h2><span class="tag">A</span>Cursor Studio app - the 60 second route</h2>
<p class="lead">Dark-mode installer included in <code>CursorSets\\App</code>. It copies the cursors into your profile, registers the scheme and applies it instantly. Nothing needs administrator rights.</p>
<div class="steps">
<div class="step"><div><h3><span class="num">1</span>Get the folder</h3><p>Download the repository (<b>Code &rarr; Download ZIP</b>), then right-click the zip and choose <b>Extract All&hellip;</b>. Keep the <code>CursorSets</code> folder together - the app reads the <code>Sets</code> folder next to it.</p></div>
<div class="mock"><div class="tb"><span>Extract Compressed (Zipped) Folders</span><span>x</span></div><div class="fx"><div class="fxs"><div class="f s">Downloads</div><div class="f">Documents</div><div class="f">Desktop</div></div><div class="fxm"><div class="f"><span class="ico"></span>CursorSets</div><div class="f" style="margin-left:22px"><span class="ico"></span>App</div><div class="f" style="margin-left:22px"><span class="ico"></span>Sets</div><div class="f" style="margin-left:22px"><span class="ico"></span>Docs</div></div></div><span class="badge" style="left:152px;top:42px">1</span></div></div>
<div class="step"><div><h3><span class="num">2</span>Launch it</h3><p>Open <code>CursorSets\\App</code> and double-click <b>Launch-CursorStudio.bat</b>. If SmartScreen appears: <b>More info &rarr; Run anyway</b> (the script is plain text you can read).</p></div>
<div class="mock"><div class="tb"><span>App</span><span>x</span></div><div class="fx"><div class="fxs"><div class="f">CursorSets</div><div class="f s">App</div></div><div class="fxm"><div class="f s"><span class="ico" style="background:#9aa"></span>Launch-CursorStudio.bat</div><div class="f"><span class="ico" style="background:#7ab"></span>CursorStudio.ps1</div><div class="f"><span class="ico" style="background:#7ab"></span>CursorStudio.Core.ps1</div></div></div><span class="badge" style="right:10px;top:48px">2</span></div></div>
<div class="step"><div><h3><span class="num">3</span>Pick a set and a style</h3><p>Choose a set in the left list (grouped by franchise), then a style: <b>A</b> relic/weapon, <b>B</b> mascot, <b>C</b> gauntlet/HUD/pixel or <b>C2</b>. The preview shows all 17 pointers. Select <b>Animated (.ani)</b> or <b>Static (.cur)</b> - the preview switches to match.</p></div>
<div class="mock dark"><div class="tb"><span>Cursor Studio</span><span>x</span></div><div class="studio"><div class="sl">{tree}</div><div class="sr"><img src="{prev_anim}"><div class="rad"><span><span class="dot on"></span>Style A</span><span><span class="dot"></span>B</span><span><span class="dot"></span>C</span><span><span class="dot"></span>C2</span></div><div class="rad"><span><span class="dot on"></span>Animated (.ani)</span><span><span class="dot"></span>Static (.cur)</span></div></div></div><span class="badge" style="left:150px;top:70px">3</span><span class="badge" style="left:182px;top:206px">3</span></div></div>
<div class="step"><div><h3><span class="num">4</span>Apply</h3><p><b>Apply Now</b> installs and activates the set immediately. <b>Add to Scheme List</b> only registers it so you can pick it later under <i>Mouse Settings &rarr; Pointers &rarr; Scheme</i>. <b>Restore Windows Default</b> undoes everything.</p></div>
<div class="mock dark"><div class="tb"><span>Cursor Studio</span><span>x</span></div><div style="padding:14px"><div class="rad"><span><span class="dot"></span>Animated (.ani)</span><span><span class="dot on"></span>Static (.cur)</span></div><p style="margin:6px 0 12px;color:#9aa">FFXIV - Crystal Dawn</p><span class="db p">Apply Now</span><span class="db">Add to Scheme List</span><span class="db">Restore Windows Default</span><span class="db">Mouse Settings</span><p style="color:#6edca0;margin-top:14px">Applied: FFXIV - Crystal Dawn (Static). Move your mouse - the new pointers are live.</p></div><span class="badge" style="left:14px;top:84px;display:none">4</span><span class="badge" style="left:6px;top:84px">4</span></div></div>
</div>
<div class="tip ok"><b>Headless / scripted:</b> <code>powershell -ExecutionPolicy Bypass -File CursorStudio.ps1 -Set 01-Crystal-Dawn -Style A -Mode Animated -Apply</code> &nbsp;or&nbsp; <code>-List</code>, <code>-Restore</code>.</div>

<h2><span class="tag">B</span>Manual install - Mouse Properties</h2>
<p class="lead">Works for <b>both</b> <code>.cur</code> and <code>.ani</code>. Repeat step 4 for each pointer, or use the app / the INF to do all 17 at once.</p>
<div class="steps">
<div class="step"><div><h3><span class="num">1</span>Open Mouse Properties</h3><p>Press <kbd>Win</kbd> + <kbd>R</kbd>, type <code>main.cpl</code> and press <kbd>Enter</kbd> (or <code>control mouse</code>).</p></div>
<div class="mock"><div class="tb"><span>Run</span><span>x</span></div><div style="padding:14px 16px"><p style="margin:0 0 10px">Type the name of a program, folder, document, or Internet resource, and Windows will open it for you.</p><div class="sel-box" style="margin-left:34px"><b>main.cpl</b><span>v</span></div><div class="btns"><span class="btn p">OK</span><span class="btn">Cancel</span><span class="btn">Browse...</span></div></div><span class="badge" style="right:52px;top:96px">1</span></div></div>
<div class="step"><div><h3><span class="num">2</span>Pointers tab &rarr; select a role</h3><p>Open the <b>Pointers</b> tab. In <b>Customize</b>, click a role such as <b>Normal Select</b> (the arrow). The 17 roles match the numbered file names <code>01-NormalSelect</code> &hellip; <code>17-PersonSelect</code>.</p></div>
<div class="mock"><div class="tb"><span>Mouse Properties</span><span>x</span></div><div class="tabs"><span>Buttons</span><span class="a">Pointers</span><span>Pointer Options</span><span>Wheel</span></div><div class="body"><b style="font-size:11px">Scheme</b><div class="sel-box"><span>Windows Default (system scheme)</span><span>v</span></div><b style="font-size:11px">Customize:</b><div class="list">{rows}</div></div><span class="badge" style="right:6px;top:176px">2</span></div></div>
<div class="step"><div><h3><span class="num">3</span>Browse&hellip;</h3><p>Click <b>Browse&hellip;</b>. The folder opens at the Windows cursors folder - navigate to your set's <code>Animated</code> or <code>Static</code> folder.</p></div>
<div class="mock"><div class="tb"><span>Mouse Properties</span><span>x</span></div><div class="body" style="margin-top:10px"><div style="display:flex;gap:10px"><div style="flex:1;border:1px solid #666c8a;height:110px;display:grid;place-items:center;font-size:12px;color:#9aa2c4">preview</div><div class="btns" style="flex-direction:column;justify-content:start"><span class="btn">Use Default</span><span class="btn p">Browse...</span></div></div><div class="btns" style="margin-top:20px"><span class="btn">OK</span><span class="btn">Cancel</span><span class="btn">Apply</span></div></div><span class="badge" style="right:20px;top:60px">3</span></div></div>
<div class="step"><div><h3><span class="num">4</span>Pick the file, then Open</h3><p>Choose the matching file (for example <code>01-NormalSelect.ani</code>) and click <b>Open</b>. Animated files preview in the box; <b>.cur</b> files show a still.</p></div>
<div class="mock"><div class="tb"><span>Browse</span><span>x</span></div><div class="fx"><div class="fxs"><div class="f">01-Crystal-Dawn</div><div class="f s">A-Aetherial-Glaive-Relic</div><div class="f">Animated</div></div><div class="fxm"><div class="f s"><span class="ico" style="background:#6ac"></span>01-NormalSelect.ani</div><div class="f"><span class="ico" style="background:#6ac"></span>02-HelpSelect.ani</div><div class="f"><span class="ico" style="background:#6ac"></span>03-WorkingInBackground.ani</div><div class="f"><span class="ico" style="background:#6ac"></span>04-Busy.ani</div></div></div><span class="badge" style="right:12px;top:54px">4</span></div></div>
<div class="step"><div><h3><span class="num">5</span>Save as a scheme, then Apply</h3><p>After all roles are set click <b>Save As&hellip;</b>, name it (for example <i>Crystal Dawn Animated</i>) and press <b>OK</b>. Next time just pick it in the <b>Scheme</b> drop-down and click <b>Apply</b>.</p></div>
<div class="mock"><div class="tb"><span>Save Scheme</span><span>x</span></div><div style="padding:14px 16px"><p style="margin:0 0 8px">Save this cursor scheme as:</p><div class="sel-box"><b>FFXIV - Crystal Dawn (Animated)</b></div><div class="btns"><span class="btn p">OK</span><span class="btn">Cancel</span></div></div><span class="badge" style="right:6px;top:80px">5</span></div></div>
</div>

<h2><span class="tag">C</span>One right-click: Install.inf</h2>
<div class="steps"><div class="step"><div><h3>Register all 17 pointers at once</h3><p>Open the set's <code>Animated</code> or <code>Static</code> folder, right-click <b>Install.inf</b> and choose <b>Install</b> (Windows 11: <i>Show more options &rarr; Install</i>). Approve the admin prompt - it copies the files to <code>C:\\Windows\\Cursors</code>. Then open <code>main.cpl</code> &rarr; Pointers and choose the new scheme in the <b>Scheme</b> list.</p></div>
<div class="mock"><div class="tb"><span>Static</span><span>x</span></div><div style="padding:12px"><div class="f s" style="width:240px">Install.inf</div><div style="background:#2a2d3a;border:1px solid #4a5070;border-radius:8px;width:230px;margin:6px 0 0 60px;padding:6px 0;box-shadow:0 6px 18px rgba(0,0,0,.25);font-size:12px"><div class="f">Open</div><div class="f s">Install</div><div class="f">Edit</div><div class="f">Properties</div></div></div><span class="badge" style="left:226px;top:100px">!</span></div></div></div>

<h2>Switching between Animated and Static</h2>
<div class="cols"><div><img src="{prev_static}" alt="static preview"><p class="lead">Static - 17 crisp <code>.cur</code> pointers.</p></div><div><img src="{prev_anim}" alt="animated preview"><p class="lead">Animated - the same 17 roles as looping <code>.ani</code> pointers.</p></div></div>
<p>In the app, flip the radio button and press <b>Apply Now</b> again. Manually, choose the other scheme in the <b>Scheme</b> drop-down. Each variant is registered as its own scheme (<i>Set Name (Animated)</i> / <i>(Static)</i>).</p>

<h2>Sizes &amp; sharpness</h2>
<div class="tip">Every cursor file contains <b>32, 48 and 64&nbsp;px</b> images, so Windows can pick the closest match for your pointer size and display scale instead of stretching one bitmap. To enlarge pointers: <b>Settings &rarr; Accessibility &rarr; Mouse pointer and touch &rarr; Size</b>.</div>

<h2>Folder map</h2>
<div class="tree">CursorSets/
 catalog.json                     list of all sets
 App/   Launch-CursorStudio.bat   dark-mode installer (PowerShell, no install needed)
        CursorStudio.ps1 / .Core.ps1
 Docs/  Install-Guide.html / .png this sheet
 Sets/
  01-Crystal-Dawn/ ... 24-Spooky-Paws/      24 sets
    A-&lt;name&gt;/ B-&lt;name&gt;/ C-&lt;name&gt;/ C2-&lt;name&gt;/ GA-&lt;name&gt;/ GB-&lt;name&gt;/ GC-&lt;name&gt;/   7 styles per set
      Static/    01-NormalSelect.cur ... 17-PersonSelect.cur + Install.inf
      Animated/  01-NormalSelect.ani ... 17-PersonSelect.ani + Install.inf
 Previews/&lt;set&gt;/&lt;style&gt;/   card.png/.gif, board.png/.gif, cursor32.png (GA/GB/GC also art.jpg)
 Selector.html / index.html          browser selector (dark) with live hover test
 Generator/                        Python source that renders everything (see HANDOFF.md)</div>

<h2>The 17 pointer roles</h2>
<table><tr><th>#</th><th>Windows name</th><th>Registry key</th><th>File</th></tr>
{''.join(f'<tr><td>{i + 1}</td><td>{n}</td><td><code>{k}</code></td><td><code>{FILE_NAMES[k]}</code></td></tr>' for i, (k, n, _) in enumerate(ROLES))}</table>

<h2>Troubleshooting</h2>
<table>
<tr><td><b>Animated pointer does not move</b></td><td>Make sure the slot points to a <code>.ani</code> file. Re-apply the <b>Animated</b> scheme. A few remote-desktop and game-capture tools show static cursors only.</td></tr>
<tr><td><b>Blurry cursor</b></td><td>Set <i>Accessibility &rarr; Mouse pointer size</i> to a step that matches your display scale; every file ships 32/48/64&nbsp;px.</td></tr>
<tr><td><b>Script blocked</b></td><td>Use the <code>.bat</code> launcher (it bypasses the policy for this one run) or run the headless command shown in section A.</td></tr>
<tr><td><b>Go back</b></td><td>Press <b>Restore Windows Default</b>, or in Pointers pick <i>Windows Default</i> from the Scheme list.</td></tr>
</table>
<p class="lead" style="margin-top:28px">Making your own animated pointer? RealWorld Cursor Editor (GIF/strip &rarr; .ani with hotspots) and Custom Cursors Studio (Microsoft Store) both work. The generator in <code>CursorSets/Generator</code> shows how these sets are built.</p>
</div></body></html>'''

os.makedirs(os.path.join(ROOT, 'Docs'), exist_ok=True)
open(os.path.join(ROOT, 'Docs', 'Install-Guide.html'), 'w', encoding='utf-8').write(HTML)
print('guide ok', len(HTML) // 1024, 'KB')


def render_png_pdf():
    import glob
    from playwright.sync_api import sync_playwright
    exe = (glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome') or [None])[0]
    html = os.path.join(ROOT, 'Docs', 'Install-Guide.html')
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': 1100, 'height': 900}, color_scheme='dark')
        pg.goto('file://' + html)
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(ROOT, 'Docs', 'Install-Guide.png'), full_page=True)
        pg.pdf(path=os.path.join(ROOT, 'Docs', 'Install-Guide.pdf'), format='A4', print_background=True, margin=dict(top='10mm', bottom='10mm', left='8mm', right='8mm'))
        b.close()


if '--no-render' not in sys.argv:
    render_png_pdf()
    print('Install-Guide.png + .pdf rendered (dark)')
