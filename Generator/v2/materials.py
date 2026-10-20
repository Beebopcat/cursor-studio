"""Render materials. Each material has pre (union-level shadow/outline), part (per-shape shading), post (bloom etc.).

Masks are 'L' images at 8x scale (see toolkit). Units in the helpers below are cursor units (1 unit = 1px at 32px).
"""
import math
import numpy as np
from PIL import Image, ImageChops, ImageFilter, ImageDraw
from toolkit import K, S, Canvas, mix, lighten, darken, with_alpha, tri, hexc

LIGHT_DIR = math.radians(-135)  # light comes from the upper left


def erode(m, u):
    px = int(round(u * K))
    if px <= 0:
        return m
    return m.filter(ImageFilter.MinFilter(px * 2 + 1))


def grow(m, u):
    px = int(round(u * K))
    if px <= 0:
        return m
    return m.filter(ImageFilter.MaxFilter(px * 2 + 1))


def shift(m, dx, dy):
    return ImageChops.offset(m, int(round(dx * K)), int(round(dy * K)))


def blur(m, u):
    return m.filter(ImageFilter.GaussianBlur(u * K))


def sub(a, b):
    return ImageChops.subtract(a, b)


def both(a, b):
    return ImageChops.multiply(a, b)


def either(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = ImageChops.lighter(out, m)
    return out


def role_cols(st, role):
    p = st.p
    if isinstance(role, tuple):
        if role == ('skin',):
            return hexc('ffd7b8'), hexc('d98c68')
        return role
    if role == 'body':
        return p['c1'], p['c2']
    if role == 'body2':
        return mix(p['c1'], p['c2'], .5), darken(p['c2'], .15)
    if role == 'trim':
        return lighten(p['ac'], .35), darken(p['ac'], .3)
    if role == 'dark':
        return lighten(p['plate'], .25), darken(p['plate'], .15)
    if role == 'accent':
        return lighten(p['ac2'], .35), darken(p['ac2'], .25)
    if role == 'gem':
        return lighten(p['glow'], .6), p['glow']
    if role == 'white':
        return (255, 255, 255, 255), mix((255, 255, 255, 255), p['c1'], .3)
    raise KeyError(role)


def stops_fill(c, mask, stops, mode='v', alpha=1.0):
    """Multi-stop gradient. stops = [(t, rgba), ...]"""
    bb = mask.getbbox()
    if not bb:
        return
    x0, y0, x1, y1 = bb
    w, h = x1 - x0, y1 - y0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if mode == 'v':
        t = yy / max(1, h - 1)
    elif mode == 'd':
        t = xx / max(1, w - 1) * .45 + yy / max(1, h - 1) * .55
    else:
        cx, cy = w * .36, h * .30
        t = np.sqrt(((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2) * 1.35
    ts = [s[0] for s in stops]
    arr = np.stack([np.interp(t, ts, [s[1][i] for s in stops]) for i in range(4)], -1)
    g = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    full = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    full.paste(g, (x0, y0))
    if alpha < 1:
        mask = mask.point(lambda v: int(v * alpha))
    c.img.alpha_composite(Image.composite(full, Image.new('RGBA', (S, S), (0, 0, 0, 0)), mask))


def centroid(mask):
    a = np.asarray(mask, dtype=np.float32)
    ys, xs = np.nonzero(a > 127)
    if len(xs) == 0:
        return S / 2, S / 2
    return xs.mean(), ys.mean()


_HATCH = {}


def hatch_mask(spacing=2.4, width=.8):
    key = (spacing, width)
    if key not in _HATCH:
        m = Image.new('L', (S, S), 0)
        d = ImageDraw.Draw(m)
        n = int(S * 2 / (spacing * K))
        for i in range(-n, n):
            x = i * spacing * K
            d.line([(x, S), (x + S, 0)], fill=255, width=int(width * K))
        _HATCH[key] = m
    return _HATCH[key]


def _shadow(c, U, alpha=.3, soft=.8, off=(.9, 1.1), g=1.0):
    sh = shift(grow(U, g), *off)
    if soft:
        sh = blur(sh, soft)
    c.paint(sh, (0, 0, 0, 255), alpha)


def _outline(c, st, U, ow, halo=True, halo_w=.75):
    if halo and st.p.get('halo') is not None:
        c.paint(grow(U, ow + halo_w), st.p['halo'])
    c.paint(grow(U, ow), st.p['ol'])


def _spec_edges(c, mask, a=.55):
    inner = both(sub(mask, shift(mask, .9, .9)), mask)
    c.paint(blur(inner, .25), (255, 255, 255, 255), a)


# ----------------------------------------------------------------- materials
class Gloss:
    def pre(self, c, st, U, t):
        _shadow(c, U)
        _outline(c, st, U, 1.0)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        c.paint(grow(m, .4), darken(bot, .5), .6)
        c.paint_grad(m, lighten(top, .08), bot, 'd')
        _spec_edges(c, m, .6)
        c.paint(blur(both(sub(m, shift(m, -1, -1)), m), .3), (0, 0, 0, 255), .22)

    def post(self, c, st, U, t):
        pass


class Flat:
    hard = (1.2, 1.2)

    def pre(self, c, st, U, t):
        _shadow(c, U, .35, 0, self.hard)
        _outline(c, st, U, 1.25, halo_w=.7)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        c.paint(grow(m, .45), darken(bot, .55))
        c.paint(m, top)
        c.paint(both(sub(m, shift(m, -2.0, -2.0)), m), bot, .92)
        c.paint(both(sub(m, shift(m, 1.0, 1.0)), m), (255, 255, 255, 255), .55)

    def post(self, c, st, U, t):
        pass


class Sticker:
    def pre(self, c, st, U, t):
        _shadow(c, U, .35, 1.0, (.8, 1.2), 2.0)
        c.paint(grow(U, 2.3), st.p['ol'], .9)
        c.paint(grow(U, 1.8), st.p.get('halo') or (255, 255, 255, 255))

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        c.paint(grow(m, .35), darken(bot, .45))
        c.paint_grad(m, top, mix(top, bot, .7), 'v')
        c.paint(both(sub(m, shift(m, -1.2, -1.2)), m), bot, .35)
        bb = m.getbbox()
        if bb:
            x0, y0, x1, y1 = [v / K for v in bb]
            w, h = x1 - x0, y1 - y0
            if w > 4 and h > 4:
                e = Canvas()._m()
                ImageDraw.Draw(e).ellipse([(x0 + w * .14) * K, (y0 + h * .1) * K, (x0 + w * .52) * K, (y0 + h * .3) * K], fill=255)
                c.paint(both(blur(e, .15), m), (255, 255, 255, 255), .55)

    def post(self, c, st, U, t):
        pass


class Neon:
    def pre(self, c, st, U, t):
        c.paint(grow(U, 1.6), st.p['ol'], .92)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        k = st.p['glow'] if role in ('body', 'body2') else lighten(top, .1)
        pl = st.p['plate']
        c.paint_grad(m, mix(pl, (0, 0, 0, 255), .1), mix(pl, (0, 0, 0, 255), .55), 'v')
        c.paint_grad(m, with_alpha(top, 255), with_alpha(bot, 255), 'd', alpha=.16)
        rim = sub(m, erode(m, 1.35))
        c.paint(blur(rim, .7), k, 1.0)
        c.paint(rim, lighten(k, .15))
        c.paint(sub(m, erode(m, .6)), (255, 255, 255, 255), .95)

    def post(self, c, st, U, t):
        rim = sub(U, erode(U, 1.6))
        c.paint(blur(rim, 1.8), st.p['glow'], .65 + .3 * tri(t))


class Metal:
    def pre(self, c, st, U, t):
        _shadow(c, U)
        _outline(c, st, U, 1.0)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        stops = [(0, lighten(top, .55)), (.44, top), (.5, darken(bot, .3)), (1.0, lighten(bot, .22))]
        c.paint(grow(m, .4), darken(bot, .6), .7)
        stops_fill(c, m, stops, 'v')
        c.paint(blur(both(sub(m, shift(m, .9, .9)), m), .2), (255, 255, 255, 255), .75)
        c.paint(blur(both(sub(m, shift(m, -.9, -.9)), m), .2), (0, 0, 0, 255), .38)
        c.paint(sub(m, erode(m, .7)), darken(bot, .5), .25)

    def post(self, c, st, U, t):
        pass


class Facet:
    def pre(self, c, st, U, t):
        _shadow(c, U)
        _outline(c, st, U, 1.0)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        c.paint(grow(m, .4), darken(bot, .5), .6)
        c.paint_grad(m, top, bot, 'v')
        cx, cy = centroid(m)
        n = 7
        off = math.radians(12)
        R = S * 2
        for k in range(n):
            a0 = off + k * 2 * math.pi / n
            a1 = off + (k + 1) * 2 * math.pi / n
            mid = (a0 + a1) / 2
            tone = math.cos(mid - LIGHT_DIR)
            wedge = Canvas()._m()
            ImageDraw.Draw(wedge).polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                                           (cx + R * math.cos(mid), cy + R * math.sin(mid)),
                                           (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=255)
            col = (255, 255, 255, 255) if tone > 0 else (0, 0, 0, 255)
            c.paint(both(wedge, m), col, abs(tone) * (.40 if tone > 0 else .32))
            ln = Canvas()._m()
            ImageDraw.Draw(ln).line([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0))], fill=255, width=int(.3 * K))
            c.paint(both(ln, m), (255, 255, 255, 255), .35)
        _spec_edges(c, m, .7)

    def post(self, c, st, U, t):
        pass


class Gel:
    def pre(self, c, st, U, t):
        _shadow(c, U, .22, 1.0, (.8, 1.2))
        c.paint(grow(U, .95), st.p['ol'], .85)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        c.paint_grad(m, lighten(top, .1), bot, 'r')
        rim = sub(m, erode(m, 1.5))
        c.paint(blur(rim, .6), darken(bot, .5), .5)
        bounce = both(sub(m, shift(m, 0, -1.3)), m)
        c.paint(blur(bounce, .3), lighten(top, .5), .4)
        bb = m.getbbox()
        if bb:
            x0, y0, x1, y1 = [v / K for v in bb]
            w, h = x1 - x0, y1 - y0
            if w > 3.5 and h > 3.5:
                e = Canvas()._m()
                ImageDraw.Draw(e).ellipse([(x0 + w * .16) * K, (y0 + h * .1) * K, (x0 + w * .58) * K, (y0 + h * .32) * K], fill=255)
                c.paint(both(blur(e, .12), m), (255, 255, 255, 255), .8)
                d = Canvas()._m()
                ImageDraw.Draw(d).ellipse([(x0 + w * .64) * K, (y0 + h * .16) * K, (x0 + w * .74) * K, (y0 + h * .26) * K], fill=255)
                c.paint(both(d, m), (255, 255, 255, 255), .7)

    def post(self, c, st, U, t):
        pass


class Ink:
    def pre(self, c, st, U, t):
        _shadow(c, U, .55, 0, (1.3, 1.3))
        _outline(c, st, U, 1.35, halo_w=.7)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        c.paint(grow(m, .5), (10, 8, 12, 255))
        c.paint(m, top)
        band = both(sub(m, shift(m, -3.2, -3.2)), m)
        c.paint(both(hatch_mask(2.3, .75), band), bot, .95)
        c.paint(both(sub(m, shift(m, -1.2, -1.2)), m), bot, .95)
        c.paint(both(sub(m, shift(m, 1.1, 1.1)), m), (255, 255, 255, 255), .6)

    def post(self, c, st, U, t):
        pass


class Pixel(Flat):
    hard = (1.0, 1.0)

    def pre(self, c, st, U, t):
        _shadow(c, U, .45, 0, self.hard)
        c.paint(grow(U, 1.0), st.p['ol'])

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        c.paint(grow(m, .4), darken(bot, .55))
        c.paint(m, top)
        c.paint(both(sub(m, shift(m, -1.6, -1.6)), m), bot)
        c.paint(both(sub(m, shift(m, 1.0, 1.0)), m), lighten(top, .6), .9)


class Paint:
    _noise = None

    def rough(self, m):
        if Paint._noise is None:
            rs = np.random.RandomState(5)
            n = Image.fromarray((rs.rand(S // 4, S // 4) * 255).astype(np.uint8)).resize((S, S), Image.BICUBIC)
            Paint._noise = np.asarray(n, dtype=np.float32) - 128
        a = np.asarray(blur(m, .5), dtype=np.float32) + Paint._noise * .9
        return Image.fromarray(((a > 128) * 255).astype(np.uint8))

    def pre(self, c, st, U, t):
        _shadow(c, U, .3, 1.0, (1.0, 1.2))
        c.paint(self.rough(grow(U, 1.1)), st.p['ol'], .95)

    def part(self, c, st, m, role, t):
        top, bot = role_cols(st, role)
        m = self.rough(m)
        c.paint_grad(m, lighten(top, .1), bot, 'd')
        d = ImageDraw.Draw(st_l := Image.new('L', (S, S), 0))
        rs = np.random.RandomState(abs(hash(role)) % 999)
        for i in range(26):
            x = rs.rand() * S * 1.6 - S * .3
            d.line([(x, 0), (x + S * .9, S * .9)], fill=int(90 + rs.rand() * 120), width=int((.25 + rs.rand() * .5) * K))
        c.paint(both(st_l, m), (255, 255, 255, 255), .28)
        c.paint(both(st_l.transpose(Image.FLIP_LEFT_RIGHT), m), (0, 0, 0, 255), .12)
        _spec_edges(c, m, .55)

    def post(self, c, st, U, t):
        pass


MATERIALS = dict(paint=Paint(), gloss=Gloss(), flat=Flat(), sticker=Sticker(), neon=Neon(), metal=Metal(),
                 facet=Facet(), gel=Gel(), ink=Ink(), pixel=Pixel())


def pixelate(img, sizes=(32, 64), grid=32, colors=14, gb=None):
    a = np.asarray(img, dtype=np.float32) / 255.0
    al = a[..., 3:4]
    prem = a[..., :3] * al
    f = S // grid
    prem = prem.reshape(grid, f, grid, f, 3).mean((1, 3))
    al = al.reshape(grid, f, grid, f, 1).mean((1, 3))
    rgb = np.where(al > 0.01, prem / np.maximum(al, 1e-4), 0)
    mask = (al[..., 0] >= .45)
    q = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), 'RGB').quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    qa = np.asarray(q)
    if gb:
        lum = (qa[..., 0] * .3 + qa[..., 1] * .59 + qa[..., 2] * .11) / 255.0
        idx = np.clip((lum * 4).astype(int), 0, 3)
        qa = np.asarray(gb, dtype=np.uint8)[idx]
    out = np.dstack([qa, (mask * 255).astype(np.uint8)])
    out[~mask] = 0
    base = Image.fromarray(out, 'RGBA')
    res = {}
    for s in sizes:
        res[s] = base if s == grid else base.resize((s, s), Image.NEAREST)
    return res
