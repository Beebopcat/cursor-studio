#!/usr/bin/env python3
"""Driver for Cursor Studio: serve/shot the selector page, validate sets, rebuild selector, build one set, check PowerShell app.

Subcommands: serve | stop | shot | validate | rebuild-selector | build-one <set> | ps-check
Outputs go to /tmp/cursor-studio-run (override with CS_OUT); nothing is written inside the repo
except by rebuild-selector (which rewrites the tracked Selector.html/index.html).
"""
import argparse, glob, hashlib, json, os, signal, socket, subprocess, sys, time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
V2 = os.path.join(REPO, 'Generator', 'v2')
OUT = os.environ.get('CS_OUT', '/tmp/cursor-studio-run')
PIDFILE = os.path.join(OUT, 'server.json')
os.makedirs(OUT, exist_ok=True)


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


def server_info():
    try:
        i = json.load(open(PIDFILE)); os.kill(i['pid'], 0); return i
    except Exception:
        return None


def cmd_serve(a):
    i = server_info()
    if i:
        print(f"already serving {i['url']} (pid {i['pid']})"); return 0
    port = a.port or free_port()
    log = open(os.path.join(OUT, 'server.log'), 'w')
    p = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', REPO],
                         stdout=log, stderr=log, start_new_session=True)
    url = f'http://127.0.0.1:{port}/'
    import urllib.request
    for _ in range(50):
        try:
            urllib.request.urlopen(url + 'index.html', timeout=1); break
        except Exception:
            time.sleep(0.2)
    else:
        p.kill(); print('server did not come up, see', log.name); return 1
    json.dump(dict(pid=p.pid, url=url), open(PIDFILE, 'w'))
    print(f'serving {url} (pid {p.pid}); log {log.name}'); return 0


def cmd_stop(a):
    i = server_info()
    if i:
        os.killpg(os.getpgid(i['pid']), signal.SIGTERM); os.remove(PIDFILE); print('stopped', i['url'])
    else:
        print('no server running')
    return 0


def chrome_path():
    base = os.environ.get('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
    c = sorted(glob.glob(os.path.join(base, 'chromium-*', 'chrome-linux*', 'chrome')))
    if not c:
        sys.exit(f'no chromium under {base}; set PLAYWRIGHT_BROWSERS_PATH (do not run playwright install)')
    return c[-1]


def cmd_shot(a):
    from playwright.sync_api import sync_playwright
    started = False
    if not server_info():
        cmd_serve(argparse.Namespace(port=None)); started = True
    url = server_info()['url'] + 'index.html'
    errs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path=chrome_path(), args=['--no-sandbox'])
        pg = br.new_context(viewport={'width': 1280, 'height': 900}).new_page()
        pg.on('console', lambda m: errs.append(f'console.{m.type}: {m.text}') if m.type in ('error', 'warning') and not m.text.startswith('Failed to load resource') else None)  # 404 URLs are reported by the response hook (favicon.ico 404 is not: benign)
        pg.on('pageerror', lambda e: errs.append(f'pageerror: {e}'))
        pg.on('requestfailed', lambda r: errs.append(f'requestfailed: {r.url}'))
        pg.on('response', lambda r: errs.append(f'HTTP {r.status}: {r.url}') if r.status >= 400 else None)
        pg.goto(url, wait_until='load')
        pg.wait_for_selector('article.card')
        pg.wait_for_timeout(800)
        print('cards:', pg.locator('article.card').count(), '| sets:', pg.locator('section.set').count())
        pg.screenshot(path=f'{OUT}/1-all.png'); print('shot', f'{OUT}/1-all.png')
        # filter by franchise chip
        pg.locator('#chips .chip', has_text=a.filter).first.click()
        pg.wait_for_timeout(800)
        print(f'filter "{a.filter}": sets =', pg.locator('section.set').count(), '| cards =', pg.locator('article.card').count())
        pg.screenshot(path=f'{OUT}/2-filter.png'); print('shot', f'{OUT}/2-filter.png')
        # Mark first card, check button text + counter
        pg.locator('article.card .btn.m').first.click()
        print('after Mark: button =', pg.locator('article.card .btn.m').first.inner_text(), '| list count =', pg.locator('#cnt').inner_text())
        pg.locator('#openList').click()
        print('marked line:', [l for l in pg.locator('#lTxt').input_value().split('\n')[1:] if not l.endswith(': -')])
        pg.screenshot(path=f'{OUT}/3-marked-list.png'); print('shot', f'{OUT}/3-marked-list.png')
        pg.keyboard.press('Escape')
        # hover a card -> dock + cursor style
        card = pg.locator('article.card').nth(1)
        card.hover()
        print('hover dock name =', pg.locator('#dockName').inner_text(), '| card cursor css =', card.evaluate('e=>e.style.cursor'))
        pg.screenshot(path=f'{OUT}/4-hover.png'); print('shot', f'{OUT}/4-hover.png')
        # open 17-pointer board modal
        pg.locator('article.card .btn.v').first.click()
        pg.wait_for_function('document.getElementById("bImg").complete && document.getElementById("bImg").naturalWidth>0')
        print('board modal:', pg.locator('#bTitle').inner_text(), '| img', pg.locator('#bImg').evaluate('i=>i.naturalWidth+"x"+i.naturalHeight'))
        print('install cmd:', pg.locator('#bCmd').inner_text())
        pg.screenshot(path=f'{OUT}/5-board-modal.png'); print('shot', f'{OUT}/5-board-modal.png')
        br.close()
    print('console/page errors:', len(errs))
    for e in errs:
        print('  ', e)
    if started:
        cmd_stop(None)
    return 1 if errs else 0


def run(cmd, **kw):
    print('$', ' '.join(cmd)); return subprocess.call(cmd, **kw)


def cmd_validate(a):
    return run([sys.executable, 'validate.py'], cwd=V2)


def digest(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def cmd_rebuild_selector(a):
    rc = run([sys.executable, 'make_selector.py'], cwd=V2)
    s, i = digest(f'{REPO}/Selector.html'), digest(f'{REPO}/index.html')
    print('Selector.html == index.html:', s == i)
    r = subprocess.run(['git', '-C', REPO, 'status', '--short', 'Selector.html', 'index.html'], capture_output=True, text=True).stdout
    print('git status of selector files:', r.strip() or '(clean: rebuild reproduced the committed page)')
    return rc or (0 if s == i else 1)


def cmd_build_one(a):
    """Build one set into OUT/build/ (not the repo): patches build24's output dirs, skips catalog()."""
    code = f'''
import sys, os, time, multiprocessing as mp
mp.set_start_method("fork")
sys.path.insert(0, {V2!r}); sys.path.insert(0, {os.path.dirname(V2)!r})
import build24
dst = {os.path.join(OUT, "build")!r}
build24.SETS_OUT = os.path.join(dst, "Sets"); build24.PREV_OUT = os.path.join(dst, "Previews")
build24.FRAMES = {a.frames}
sel = [i for i, s in enumerate(build24.SETS24) if s["slug"] == {a.set!r} or str(s["num"]) == {a.set!r}]
assert sel, "unknown set " + {a.set!r}
t0 = time.time()
with mp.Pool(4) as p:
    for n, r in enumerate(p.imap_unordered(build24.build_style, [(i, k) for i in sel for k in range(4)]), 1):
        print(n, r, round(time.time() - t0), "s", flush=True)
'''
    rc = subprocess.call([sys.executable, '-c', code])
    if rc == 0:
        print('built into', os.path.join(OUT, 'build'))
        sys.path.insert(0, V2)
        import validate
        n = 0
        for f in glob.glob(os.path.join(OUT, 'build', 'Sets', '*', '*', 'Static', '*.cur')):
            validate.check_cur(open(f, 'rb').read(), f); n += 1
        for f in glob.glob(os.path.join(OUT, 'build', 'Sets', '*', '*', 'Animated', '*.ani')):
            validate.check_ani(open(f, 'rb').read(), f); n += 1
        print('validated', n, 'built files')
    return rc


def cmd_ps_check(a):
    pwsh = subprocess.run('command -v pwsh || ls /root/.dotnet/tools/pwsh', shell=True, capture_output=True, text=True).stdout.split()
    if not pwsh:
        print('pwsh not installed; see SKILL.md Prerequisites'); return 1
    pwsh = pwsh[0]
    parse = ('$t=$null;$e=$null;$n=0;foreach($f in Get-ChildItem App/*.ps1){[void][System.Management.Automation.Language.Parser]::ParseFile($f.FullName,[ref]$t,[ref]$e);$n+=$e.Count;"$($f.Name): $($e.Count) parse errors"};exit [int]($n -gt 0)')
    rc = run([pwsh, '-NoProfile', '-Command', parse], cwd=REPO)
    if a.selftest:
        rc = rc or run([pwsh, '-NoProfile', '-File', 'App/CursorStudio.SelfTest.ps1'], cwd=REPO)
    return rc


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='c', required=True)
    s = sp.add_parser('serve'); s.add_argument('--port', type=int); s.set_defaults(f=cmd_serve)
    sp.add_parser('stop').set_defaults(f=cmd_stop)
    s = sp.add_parser('shot'); s.add_argument('--filter', default='Pok'); s.set_defaults(f=cmd_shot)
    sp.add_parser('validate').set_defaults(f=cmd_validate)
    sp.add_parser('rebuild-selector').set_defaults(f=cmd_rebuild_selector)
    s = sp.add_parser('build-one'); s.add_argument('set', help='slug or number, e.g. 10-Blish or 10'); s.add_argument('--frames', type=int, default=12); s.set_defaults(f=cmd_build_one)
    s = sp.add_parser('ps-check'); s.add_argument('--selftest', action='store_true', help='also run App/CursorStudio.SelfTest.ps1 (~25 s)'); s.set_defaults(f=cmd_ps_check)
    a = ap.parse_args(); sys.exit(a.f(a))


if __name__ == '__main__':
    main()
