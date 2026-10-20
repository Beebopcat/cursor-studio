"""Builds every cursor set: static .cur, animated .ani, Install.inf, previews, catalog."""
import json, os, struct, sys, io, shutil, time
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from roles import ROLES, FILE_NAMES, render_role
from sets import SETS

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Sets'))
SIZES = (32, 48, 64)
FRAMES = 12
STATIC_T = 0.3
FAST = {'Wait', 'AppStarting'}
HOT = {k: h for k, _, h in ROLES}


# -------------------------------------------------------------- file writers
def _dib(img):
    w, h = img.size
    px = img.convert('RGBA').load()
    xor = bytearray()
    row_mask = ((w + 31) // 32) * 4
    andm = bytearray()
    for y in range(h - 1, -1, -1):
        bits = 0
        mrow = bytearray(row_mask)
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                r = g = b = 0
                mrow[x // 8] |= 0x80 >> (x % 8)
            xor += bytes((b, g, r, a))
        andm += mrow
    hdr = struct.pack('<IiiHHIIiiII', 40, w, h * 2, 1, 32, 0, len(xor) + len(andm), 0, 0, 0, 0)
    return hdr + bytes(xor) + bytes(andm)


def make_cur(images, hotspot):
    """images: {size: RGBA image}; hotspot in 32-unit space."""
    sizes = sorted(images)
    blobs = [_dib(images[s]) for s in sizes]
    out = struct.pack('<HHH', 0, 2, len(sizes))
    off = 6 + 16 * len(sizes)
    for s, b in zip(sizes, blobs):
        hx = min(s - 1, int(round(hotspot[0] * s / 32)))
        hy = min(s - 1, int(round(hotspot[1] * s / 32)))
        out += struct.pack('<BBBBHHII', s if s < 256 else 0, s if s < 256 else 0, 0, 0, hx, hy, len(b), off)
        off += len(b)
    return out + b''.join(blobs)


def _chunk(tag, data):
    c = tag + struct.pack('<I', len(data)) + data
    return c + (b'\0' if len(data) % 2 else b'')


def make_ani(cur_frames, jiffies, title, author):
    n = len(cur_frames)
    anih = struct.pack('<IIIIIIIII', 36, n, n, 0, 0, 0, 1, jiffies, 1)
    info = b'INFO' + _chunk(b'INAM', title.encode('latin-1', 'replace') + b'\0') + \
        _chunk(b'IART', author.encode('latin-1', 'replace') + b'\0')
    fram = b'fram' + b''.join(_chunk(b'icon', f) for f in cur_frames)
    body = b'ACON' + _chunk(b'LIST', info) + _chunk(b'anih', anih) + \
        _chunk(b'rate', struct.pack('<%dI' % n, *([jiffies] * n))) + _chunk(b'LIST', fram)
    return b'RIFF' + struct.pack('<I', len(body)) + body


def make_inf(set_name, variant, ext):
    label = f'{set_name} ({variant})'
    names = [FILE_NAMES[k] + ext for k, _, _ in ROLES]
    strings = '\n'.join(f'{k.lower()} = "{FILE_NAMES[k]}{ext}"' for k, _, _ in ROLES)
    scheme = ','.join(f'%10%\\%CUR_DIR%\\%{k.lower()}%' for k, _, _ in ROLES)
    return f'''; {label} - Windows 11 cursor scheme. Right-click this file > Install.
; (Installs to C:\\Windows\\Cursors and needs administrator approval. The Cursor Studio app does not.)
[Version]
signature="$CHICAGO$"

[DefaultInstall]
CopyFiles = Scheme.Cur
AddReg    = Scheme.Reg

[DestinationDirs]
Scheme.Cur = 10,"%CUR_DIR%"

[Scheme.Reg]
HKCU,"Control Panel\\Cursors\\Schemes","%SCHEME_NAME%",,"{scheme}"

[Scheme.Cur]
''' + '\n'.join(names) + f'''

[Strings]
CUR_DIR = "Cursors\\{label}"
SCHEME_NAME = "{label}"
{strings}
'''.replace('\n', '\r\n')


# ------------------------------------------------------------------ previews
def _font(sz):
    try:
        return ImageFont.load_default(sz)
    except Exception:
        return ImageFont.load_default()


def sheet(icons, title, subtitle, light=False):
    """icons: list of (label, 64px RGBA). 6 columns x 3 rows."""
    cols, cw, ch = 6, 132, 124
    rows = 3
    W, H = cols * cw + 24, rows * ch + 86
    bg = (30, 33, 46) if not light else (240, 242, 248)
    img = Image.new('RGBA', (W, H), bg + (255,))
    d = ImageDraw.Draw(img)
    fg = (240, 244, 255) if not light else (30, 33, 46)
    d.text((18, 12), title, font=_font(22), fill=fg)
    d.text((18, 42), subtitle, font=_font(12), fill=(150, 160, 190) if not light else (90, 96, 120))
    for i, (label, im) in enumerate(icons):
        x, y = 12 + (i % cols) * cw, 74 + (i // cols) * ch
        tile = (42, 46, 64) if not light else (255, 255, 255)
        d.rounded_rectangle([x + 4, y + 4, x + cw - 6, y + ch - 6], radius=12, fill=tile + (255,))
        img.alpha_composite(im.resize((72, 72), Image.LANCZOS), (x + (cw - 72) // 2 - 1, y + 10))
        fs = 11 if len(label) < 18 else 9
        tw = d.textlength(label, font=_font(fs))
        d.text((x + (cw - tw) // 2 - 1, y + ch - 30), label, font=_font(fs), fill=(185, 194, 220) if not light else (80, 86, 110))
    return img


# -------------------------------------------------------------------- build
def build_set(item):
    st = item['style']
    name, slug, fr = item['name'], item['slug'], item['franchise']
    base = os.path.join(OUT, fr, slug)
    for v in ('Static', 'Animated'):
        os.makedirs(os.path.join(base, v), exist_ok=True)
    static_icons, anim_frames64 = [], []
    for role, friendly, hot in ROLES:
        fname = FILE_NAMES[role]
        s_imgs = render_role(st, role, STATIC_T, SIZES)
        with open(os.path.join(base, 'Static', fname + '.cur'), 'wb') as f:
            f.write(make_cur(s_imgs, hot))
        static_icons.append((friendly, s_imgs[64]))
        frames = []
        curs = []
        for i in range(FRAMES):
            imgs = render_role(st, role, i / FRAMES, SIZES)
            curs.append(make_cur(imgs, hot))
            frames.append(imgs[64])
        jif = 4 if role in FAST else 6
        with open(os.path.join(base, 'Animated', fname + '.ani'), 'wb') as f:
            f.write(make_ani(curs, jif, f'{name} - {friendly}', 'Cursor Studio'))
        anim_frames64.append((friendly, frames))
    for v, ext in (('Static', '.cur'), ('Animated', '.ani')):
        with open(os.path.join(base, v, 'Install.inf'), 'wb') as f:
            f.write(make_inf(name, v, ext).encode('ascii'))
    sub = item['blurb']
    sheet(static_icons, name, sub).convert('RGB').save(os.path.join(base, 'preview-static.png'))
    sheet(static_icons, name, sub, light=True).convert('RGB').save(os.path.join(base, 'preview-static-light.png'))
    gif = []
    for i in range(FRAMES):
        gif.append(sheet([(lab, fr_[i]) for lab, fr_ in anim_frames64], name, sub + '  (animated)').convert('RGB'))
    gif[0].save(os.path.join(base, 'preview-animated.gif'), save_all=True, append_images=gif[1:], duration=85, loop=0, optimize=False,
                palette=Image.ADAPTIVE)
    meta = dict(franchise=fr, slug=slug, name=name, blurb=sub,
                path=f'Sets/{fr}/{slug}', roles=[dict(registry=k, label=n, file=FILE_NAMES[k]) for k, n, _ in ROLES])
    with open(os.path.join(base, 'set.json'), 'w') as f:
        json.dump(meta, f, indent=2)
    return meta


if __name__ == '__main__':
    only = sys.argv[1:]
    items = [s for s in SETS if not only or s['slug'] in only]
    t0 = time.time()
    if not only:
        shutil.rmtree(OUT, ignore_errors=True)
    with Pool(4) as p:
        metas = p.map(build_set, items, chunksize=1)
    if not only:
        cat = dict(version=1, roles=[dict(registry=k, label=n) for k, n, _ in ROLES],
                   sets=[{k: v for k, v in m.items() if k != 'roles'} for m in metas])
        with open(os.path.join(os.path.dirname(OUT), 'catalog.json'), 'w') as f:
            json.dump(cat, f, indent=2)
    print('done', len(items), 'sets in', round(time.time() - t0), 's')
