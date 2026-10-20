"""Pointer objects: each returns a list of (mask, role) parts. Tip/hotspot is always near (2, 2)."""
import math
from PIL import ImageDraw
from toolkit import K, S, Canvas, tri

SQ = math.sqrt(.5)


def axis(pts, s=1.0, tip=(2.0, 2.0), ang=45):
    """local (x along the object, y across) -> canvas coords; object points down-right from the tip."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return [(tip[0] + (x * ca - y * sa) * s, tip[1] + (x * sa + y * ca) * s) for x, y in pts]


def _ell_axis(c, cx, cy, rx, ry, s, tip=(2.0, 2.0), ang=45, n=28):
    pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return c.m_poly(axis(pts, s, tip, ang))


ARROWS = {
    'classic': [(2, 2), (2, 24.5), (7.6, 19.2), (11.4, 28), (15.2, 26.4), (11.4, 17.8), (18.6, 17.6)],
    'sleek':   [(2, 2), (4, 25.5), (8.4, 19.2), (11.2, 27.5), (14, 26.2), (10.8, 18.2), (17.5, 16.6)],
    'shard':   [(2, 2), (2.6, 23), (7.2, 17.6), (10.2, 28), (13.8, 26.4), (10.6, 16.4), (17.8, 15.2)],
    'blunt':   [(2, 2), (2, 25), (8, 20.4), (11.6, 27.6), (15.6, 25.8), (12, 19.2), (19, 18.6)],
    'wing':    [(2, 2), (2, 24), (6.6, 20.6), (9.4, 27.2), (14, 25.6), (11.2, 18.8), (18, 17.4)],
    'wisp':    [(2, 2), (2, 25), (4.4, 22.6), (6.6, 26.4), (8.8, 23.4), (11.2, 27.8), (13.4, 24.4), (15.4, 26.4), (12.4, 18.2), (18.8, 17.6)],
}


def _arrow(name):
    def f(c, t):
        return [(c.m_poly(ARROWS[name]), 'body')]
    return f


def sword(c, t, s=1.12):
    blade_l = c.m_poly(axis([(0, 0), (2.8, -2.5), (16, -2.5), (16, 0), (2.8, 0)], s))
    blade_r = c.m_poly(axis([(0, 0), (2.8, 0), (16, 0), (16, 2.5), (2.8, 2.5)], s))
    fuller = c.m_poly(axis([(3.5, -.45), (14.5, -.45), (14.5, .45), (3.5, .45)], s))
    guard = c.m_poly(axis([(15.6, -5.4), (17.8, -5.4), (17.8, 5.4), (15.6, 5.4)], s))
    grip = c.m_poly(axis([(17.8, -1.4), (23.5, -1.4), (23.5, 1.4), (17.8, 1.4)], s))
    pommel = _ell_axis(c, 25, 0, 1.9, 1.9, s)
    return [(blade_l, 'body'), (blade_r, 'body2'), (grip, 'dark'), (guard, 'trim'), (pommel, 'gem'), (fuller, 'body2')]


def dagger(c, t, s=1.1):
    l = c.m_poly(axis([(0, 0), (3, -2.5), (9, -2.9), (15, -1.5), (15, 0), (0, 0)], s))
    r = c.m_poly(axis([(0, 0), (15, 0), (15, 1.5), (9, 2.9), (3, 2.5)], s))
    guard = c.m_poly(axis([(15, -3.4), (16.8, -3.4), (16.8, 3.4), (15, 3.4)], s))
    grip = c.m_poly(axis([(16.8, -1.1), (22, -1.1), (22, 1.1), (16.8, 1.1)], s))
    pommel = _ell_axis(c, 23.2, 0, 1.6, 1.6, s)
    return [(l, 'body'), (r, 'body2'), (grip, 'dark'), (guard, 'trim'), (pommel, 'gem')]


def feather(c, t, s=1.15):
    n = 9
    L = 22.0
    top, bot = [(0, 0)], []
    for i in range(1, n + 1):
        x = L * i / n
        w = 4.9 * (math.sin(math.pi * min(1, (x / L) * 1.05)) ** .75) * (1 if i % 2 else .78) + .3
        top.append((x, -w))
        bot.append((x, w * .82 * (1 if i % 2 == 0 else .8)))
    top.append((L, 0))
    vane = c.m_poly(axis(top + bot[::-1], s))
    half = c.m_poly(axis([(0, 0)] + [(x, y * .0) for x, y in top[1:]] + [(L, 0)] + [(x, y) for x, y in bot[::-1]], s))
    shaft = c.m_poly(axis([(-.2, -.35), (L + 3.5, -.45), (L + 3.5, .45), (-.2, .35)], s))
    return [(vane, 'body'), (half, 'body2'), (shaft, 'dark')]


def leaf(c, t, s=1.1):
    L = 21.0
    up = [(0, 0), (3, -3.3), (8, -5.0), (14, -4.4), (19, -2.0), (L, 0)]
    dn = [(0, 0), (3, 3.3), (8, 5.0), (14, 4.4), (19, 2.0), (L, 0)]
    a = c.m_poly(axis(up, s))
    b = c.m_poly(axis(dn, s))
    stem = c.m_poly(axis([(L - 1, -.5), (L + 4, -.5), (L + 4, .5), (L - 1, .5)], s))
    return [(a, 'body'), (b, 'body2'), (stem, 'dark')]


def hat(c, t, s=1.4):
    tilt = math.sin(t * 2 * math.pi) * .5
    cone = c.m_poly(axis([(0, 0), (3.5, -2.8 + tilt * .3), (7.5, -5.2), (11.2, -6.3), (12, 0), (11.2, 6.3), (7.5, 5.2), (3.5, 2.8 - tilt * .3)], s))
    brim = _ell_axis(c, 12.2, 0, 1.7, 7.6, s)
    band = c.m_poly(axis([(9.2, -5.9), (11.6, -6.4), (11.6, 6.4), (9.2, 5.9)], s))
    return [(brim, 'white'), (cone, 'body'), (band, 'trim')]


def round_mask(c, m, u):
    from PIL import ImageFilter
    px = int(min(u, .75) * K)
    k = px * 2 + 1
    return m.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))


def drip(c, t):
    base = c.m_poly(ARROWS['blunt'])
    blobs = [c.m_ellipse(5.2, 24.3, 1.9, 2.6), c.m_ellipse(10.4, 27.4, 2.0, 3.0), c.m_ellipse(15.0, 25.2, 1.7, 2.3),
             c.m_ellipse(16.8, 19.5, 1.9, 1.9), c.m_ellipse(6.0, 14, 1.7, 1.7)]
    m = base
    for b in blobs:
        m = Canvas.union(m, b)
    return [(round_mask(c, m, .7), 'body')]


def banner(c, t):
    wave = lambda x: math.sin((x * .32) - t * 2 * math.pi) * 1.1
    xs = [3.6, 8, 12.5, 17, 21.5]
    top = [(x, 3.4 + wave(x) * (x - 3.6) / 18) for x in xs]
    bot = [(x, 16.4 + wave(x) * (x - 3.6) / 18) for x in xs[::-1]]
    notch = [(17.5, 9.9 + wave(17.5) * .7)]
    flag = c.m_poly(top + [(top[-1][0] - 3.4, 9.9 + wave(19) * .8)] + bot)
    pole = c.m_rrect(1.5, 1.2, 3.6, 29.5, .9)
    fin = c.m_ellipse(2.55, 1.6, 1.9, 1.9)
    return [(pole, 'dark'), (flag, 'body'), (fin, 'trim')]


def spike(c, t):
    base = c.m_poly(ARROWS['classic'])
    spikes = []
    ex, ey, fx, fy = 2, 2, 18.6, 17.6
    dx, dy = fx - ex, fy - ey
    ln = math.hypot(dx, dy)
    nx, ny = dy / ln, -dx / ln
    for u in (.2, .45, .7):
        px, py = ex + dx * u, ey + dy * u
        spikes.append(c.m_poly([(px - dx / ln * 1.9, py - dy / ln * 1.9), (px + nx * 4.2 - dx / ln * .2, py + ny * 4.2 - dy / ln * .2), (px + dx / ln * 1.9, py + dy / ln * 1.9)]))
    lx = []
    for v in (8, 14, 20):
        lx.append(c.m_poly([(2, v - 1.9), (-1.2, v + .4), (2, v + 1.9)]))
    return [(Canvas.union(base, *spikes), 'body')]


def wand(c, t, s=1.0):
    shaft = c.m_poly(axis([(2, -1.2), (26, -1.0), (26, 1.0), (2, 1.2)], s, tip=(3.4, 3.4)))
    c1 = c.m_poly(axis([(9, -1.8), (10.6, -1.8), (10.6, 1.8), (9, 1.8)], s, tip=(3.4, 3.4)))
    c2 = c.m_poly(axis([(14, -1.8), (15.6, -1.8), (15.6, 1.8), (14, 1.8)], s, tip=(3.4, 3.4)))
    pts = []
    for i in range(10):
        r = 4.6 if i % 2 == 0 else 2.0
        a = math.radians(-90 + i * 36 - 45 + 45)
        pts.append((3.4 + r * math.cos(a), 3.4 + r * math.sin(a)))
    star = c.m_poly(pts)
    return [(shaft, 'dark'), (c1, 'trim'), (c2, 'trim'), (star, 'gem')]


OBJECTS = dict(classic=_arrow('classic'), sleek=_arrow('sleek'), shard=_arrow('shard'), blunt=_arrow('blunt'),
               wing=_arrow('wing'), wisp=_arrow('wisp'), sword=sword, dagger=dagger, feather=feather, leaf=leaf,
               hat=hat, drip=drip, banner=banner, spike=spike, wand=wand)
