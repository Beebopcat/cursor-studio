"""Production build: 24 sets x 4 styles -> Static .cur + Animated .ani + Install.inf + previews + catalog.

usage: python3 build24.py [--frames N] [--previews-only] [slug-or-number ...]
  --previews-only re-renders only Previews/ (card/board png+gif) and leaves Sets/ and catalog.json untouched.
"""
import io, json, os, re, struct, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from PIL import Image, ImageDraw, ImageFont
from roles import ROLES, FILE_NAMES
from roles2 import render_role
from styles24 import SETS24
from build import _dib, _chunk, make_inf

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SETS_OUT = os.path.join(ROOT, 'Sets')
PREV_OUT = os.path.join(ROOT, 'Previews')
FRAMES = 12
PREVIEWS_ONLY = False
STATIC_T = 0.3
FAST = {'Wait', 'AppStarting'}
HERO = [('Arrow', 'Normal'), ('Wait', 'Busy'), ('Hand', 'Link')]
BG = (27, 30, 43)
TILE = (42, 46, 64)
STRIP1 = (18, 20, 28)    # near-black desktop strip
STRIP2 = (62, 67, 90)    # slate desktop strip (dark theme: no light strip)


def slugify(s):
    return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-')


def _png(img):
    b = io.BytesIO()
    img.save(b, 'PNG', optimize=True)
    return b.getvalue()


def make_cur(images, hotspot):
    """32 px as classic 32-bit DIB (universal); larger sizes PNG-compressed (Windows Vista+)."""
    sizes = sorted(images)
    blobs = [_dib(images[s]) if s <= 32 else _png(images[s]) for s in sizes]
    out = struct.pack('<HHH', 0, 2, len(sizes))
    off = 6 + 16 * len(sizes)
    for s, b in zip(sizes, blobs):
        hx = min(s - 1, int(round(hotspot[0] * s / 32)))
        hy = min(s - 1, int(round(hotspot[1] * s / 32)))
        out += struct.pack('<BBBBHHII', s if s < 256 else 0, s if s < 256 else 0, 0, 0, hx, hy, len(b), off)
        off += len(b)
    return out + b''.join(blobs)


def make_ani(cur_frames, jiffies, title, author='Cursor Studio'):
    n = len(cur_frames)
    anih = struct.pack('<IIIIIIIII', 36, n, n, 0, 0, 0, 1, jiffies, 1)
    info = b'INFO' + _chunk(b'INAM', title.encode('latin-1', 'replace') + b'\0') + _chunk(b'IART', author.encode('latin-1') + b'\0')
    fram = b'fram' + b''.join(_chunk(b'icon', f) for f in cur_frames)
    body = b'ACON' + _chunk(b'LIST', info) + _chunk(b'anih', anih) + _chunk(b'rate', struct.pack('<%dI' % n, *([jiffies] * n))) + _chunk(b'LIST', fram)
    return b'RIFF' + struct.pack('<I', len(body)) + body


def font(sz):
    return ImageFont.load_default(sz)


def tiles(img, icons, x0, y0, cols, cell):
    d = ImageDraw.Draw(img)
    for i, im in enumerate(icons):
        x, y = x0 + (i % cols) * cell, y0 + (i // cols) * cell
        d.rounded_rectangle([x, y, x + cell - 6, y + cell - 6], radius=10, fill=TILE)
        img.alpha_composite(im, (x + (cell - 6 - im.width) // 2, y + (cell - 6 - im.height) // 2))


def strips(img, icons32, y0, W):
    d = ImageDraw.Draw(img)
    d.rectangle([12, y0, W - 12, y0 + 42], fill=STRIP1)
    d.rectangle([12, y0 + 46, W - 12, y0 + 88], fill=STRIP2)
    for i, im in enumerate(icons32):
        img.alpha_composite(im, (18 + i * 35, y0 + 5))
        img.alpha_composite(im, (18 + i * 35, y0 + 51))
    return y0 + 94


def card(heroes):
    img = Image.new('RGBA', (264, 96), BG + (255,))
    tiles(img, heroes, 4, 4, 3, 88)
    return img.convert('RGB')


def board(icons64, icons32, title=None):
    W = 620
    img = Image.new('RGBA', (W, 3 * 74 + 110), BG + (255,))
    tiles(img, icons64, 12, 8, 8, 74)
    strips(img, icons32, 3 * 74 + 12, W)
    return img.convert('RGB')


def save_gif(frames, path, dur=85):
    h = frames[0].height
    mosaic = Image.new('RGB', (frames[0].width, h * 3))
    for i in range(3):
        mosaic.paste(frames[i * (len(frames) // 3)], (0, i * h))
    pal = mosaic.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    q[0].save(path, save_all=True, append_images=q[1:], duration=dur, loop=0, disposal=1)


def style_dir(item, st):
    return f'{st.key}-{slugify(st.label)}'


def build_style(job):
    si, k = job
    item = SETS24[si]
    st = item['styles'][k]
    sd = style_dir(item, st)
    base = os.path.join(SETS_OUT, item['slug'], sd)
    prev = os.path.join(PREV_OUT, item['slug'], st.key)
    for d in ((prev,) if PREVIEWS_ONLY else (os.path.join(base, 'Static'), os.path.join(base, 'Animated'), prev)):
        os.makedirs(d, exist_ok=True)
    stat64, stat32, anim = {}, {}, {}
    label = f'{item["name"]} - {st.key} {st.label}'
    for role, friendly, hot in ROLES:
        fn = FILE_NAMES[role]
        s = render_role(st, role, STATIC_T, (32, 48, 64))
        if not PREVIEWS_ONLY:
            open(os.path.join(base, 'Static', fn + '.cur'), 'wb').write(make_cur(s, hot))
        stat64[role], stat32[role] = s[64], s[32]
        frames, curs = [], []
        for i in range(FRAMES):
            im = render_role(st, role, i / FRAMES, (32, 48, 64))
            curs.append(make_cur({32: im[32], 48: im[48]}, hot))
            frames.append(im)
        anim[role] = frames
        if not PREVIEWS_ONLY:
            open(os.path.join(base, 'Animated', fn + '.ani'), 'wb').write(make_ani(curs, 4 if role in FAST else 6, f'{label} - {friendly}'))
    for v, ext in (('Static', '.cur'), ('Animated', '.ani')):
        if not PREVIEWS_ONLY:
            open(os.path.join(base, v, 'Install.inf'), 'wb').write(make_inf(label, v, ext).encode('ascii', 'replace'))
    # previews
    order = [r for r, _, _ in ROLES]
    stat32['Arrow'].save(os.path.join(prev, 'cursor32.png'))
    card([stat64[r] for r, _ in HERO]).save(os.path.join(prev, 'card.png'), optimize=True)
    save_gif([card([anim[r][i][64] for r, _ in HERO]) for i in range(FRAMES)], os.path.join(prev, 'card.gif'))
    board([stat64[r] for r in order], [stat32[r] for r in order]).save(os.path.join(prev, 'board.png'), optimize=True)
    save_gif([board([anim[r][i][64] for r in order], [anim[r][i][32] for r in order]) for i in range(FRAMES)], os.path.join(prev, 'board.gif'))
    return dict(set=item['slug'], key=st.key)


def catalog():
    sets = []
    for item in SETS24:
        styles = []
        for st in item['styles']:
            sd = style_dir(item, st)
            styles.append(dict(key=st.key, label=st.label, blurb=st.blurb, material=st.material, pointer=st.ptr,
                               scheme=f'{item["name"]} - {st.key} {st.label}', path=f'Sets/{item["slug"]}/{sd}',
                               preview=f'Previews/{item["slug"]}/{st.key}'))
        import gemini
        styles += gemini.catalog_styles(item, slugify)
        sets.append(dict(num=item['num'], group=item['group'], slug=item['slug'], name=item['name'], styles=styles))
    roles = [dict(registry=k, label=n, file=FILE_NAMES[k]) for k, n, _ in ROLES]
    json.dump(dict(version=2, roles=roles, sets=sets), open(os.path.join(ROOT, 'catalog.json'), 'w'), indent=2)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] == ['--frames']:
        FRAMES = int(args[1]); args = args[2:]
    if args[:1] == ['--previews-only']:
        PREVIEWS_ONLY = True; args = args[1:]
    sel = [i for i, s in enumerate(SETS24) if not args or s['slug'] in args or str(s['num']) in args]
    jobs = [(i, k) for i in sel for k in range(4)]   # the 3 Gemini styles per set come from build_gem.py
    t0 = time.time()
    with Pool(4) as p:
        for n, r in enumerate(p.imap_unordered(build_style, jobs), 1):
            print(f'[{n}/{len(jobs)}] {r["set"]} {r["key"]}  {round(time.time() - t0)}s', flush=True)
    if not PREVIEWS_ONLY:
        catalog()
    print('done', len(jobs), 'styles in', round(time.time() - t0), 's')
