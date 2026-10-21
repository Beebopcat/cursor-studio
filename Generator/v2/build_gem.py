"""Build the Gemini Originals styles (GA, GB, GC) for the 24 sets: .cur/.ani, previews, card art, catalog entries.

usage: python3 build_gem.py [--out DIR] [--frames N] [slug-or-number ...]
  default writes into Sets/ and Previews/ of the repo and updates catalog.json (idempotent).
"""
import json, os, shutil, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build24 as B
import gemini as G
import gemini_art as GA
from roles import ROLES, FILE_NAMES
from styles24 import SETS24

OUT = B.ROOT


def build_style(job):
    num, code = job
    item = SETS24[num - 1]
    st = G.GemStyle(GA.GemArt(num, code))
    ent = G.catalog_styles(item, B.slugify)['ABC'.index(code)]
    base = os.path.join(OUT, ent['path'])
    prev = os.path.join(OUT, ent['preview'])
    for d in (os.path.join(base, 'Static'), os.path.join(base, 'Animated'), prev):
        os.makedirs(d, exist_ok=True)
    stat64, stat32, anim = {}, {}, {}
    label = ent['scheme']
    for role, friendly, hot in ROLES:
        fn = FILE_NAMES[role]
        hot = G.hotspot_for(st, role, hot)
        s = G.render_role(st, role, B.STATIC_T, (32, 48, 64))
        open(os.path.join(base, 'Static', fn + '.cur'), 'wb').write(B.make_cur(s, hot))
        stat64[role], stat32[role] = s[64], s[32]
        frames, curs = [], []
        for i in range(B.FRAMES):
            im = G.render_role(st, role, i / B.FRAMES, (32, 48, 64))
            curs.append(B.make_cur({32: im[32], 48: im[48]}, hot))
            frames.append(im)
        anim[role] = frames
        open(os.path.join(base, 'Animated', fn + '.ani'), 'wb').write(B.make_ani(curs, 4 if role in B.FAST else 6, f'{label} - {friendly}'))
    for v, ext in (('Static', '.cur'), ('Animated', '.ani')):
        open(os.path.join(base, v, 'Install.inf'), 'wb').write(B.make_inf(label, v, ext).encode('ascii', 'replace'))
    order = [r for r, _, _ in ROLES]
    stat32['Arrow'].save(os.path.join(prev, 'cursor32.png'))
    B.card([stat64[r] for r, _ in B.HERO]).save(os.path.join(prev, 'card.png'), optimize=True)
    B.save_gif([B.card([anim[r][i][64] for r, _ in B.HERO]) for i in range(B.FRAMES)], os.path.join(prev, 'card.gif'))
    B.board([stat64[r] for r in order], [stat32[r] for r in order]).save(os.path.join(prev, 'board.png'), optimize=True)
    B.save_gif([B.board([anim[r][i][64] for r in order], [anim[r][i][32] for r in order]) for i in range(B.FRAMES)], os.path.join(prev, 'board.gif'))
    shutil.copyfile(os.path.join(GA.SRC, '%02d%s_img.jpg' % (num, code)), os.path.join(prev, 'art.jpg'))
    return dict(set=item['slug'], key=ent['key'], mode=st.art.mode)


def update_catalog():
    """Idempotent: every set gets its GA/GB/GC entries after A, B, C, C2."""
    p = os.path.join(B.ROOT, 'catalog.json')
    cat = json.load(open(p))
    for s, item in zip(cat['sets'], SETS24):
        s['styles'] = [x for x in s['styles'] if x.get('source') != 'gemini'] + G.catalog_styles(item, B.slugify)
    json.dump(cat, open(p, 'w'), indent=2)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] == ['--out']:
        OUT = os.path.abspath(args[1]); args = args[2:]
    if args[:1] == ['--frames']:
        B.FRAMES = int(args[1]); args = args[2:]
    sel = [i + 1 for i, s in enumerate(SETS24) if not args or s['slug'] in args or str(s['num']) in args]
    jobs = [(n, c) for n in sel for c in 'ABC']
    t0 = time.time()
    with Pool(4) as p:
        for n, r in enumerate(p.imap_unordered(build_style, jobs), 1):
            print(f'[{n}/{len(jobs)}] {r["set"]} {r["key"]} ({r["mode"]})  {round(time.time() - t0)}s', flush=True)
    if OUT == B.ROOT:
        update_catalog()
    print('done', len(jobs), 'styles in', round(time.time() - t0), 's')
