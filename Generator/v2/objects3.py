"""Extra pointer objects for the 24-set roster."""
import math
from toolkit import K, Canvas, tri
from objects import OBJECTS, ARROWS, axis, _ell_axis


def rrpoly(x0, y0, x1, y1, r, n=5):
    pts = []
    for (cx, cy, a0) in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _rot(pts, deg, s=1.0, at=(2.5, 2.5)):
    a = math.radians(deg)
    return [(at[0] + (x * math.cos(a) - y * math.sin(a)) * s, at[1] + (x * math.sin(a) + y * math.cos(a)) * s) for x, y in pts]


def spear(c, t, s=1.0, head='gem'):
    hd = c.m_poly(axis([(0, 0), (3, -2.5), (7.5, -2.0), (9.2, 0), (7.5, 2.0), (3, 2.5)], s))
    guard = c.m_poly(axis([(8.4, -4.4), (9.6, -1.2), (11.2, -1.2), (11.2, 1.2), (9.6, 1.2), (8.4, 4.4), (10.6, 4.0), (12, 1.4), (12, -1.4), (10.6, -4.0)], s))
    shaft = c.m_poly(axis([(11, -.95), (26.5, -.95), (26.5, .95), (11, .95)], s))
    butt = _ell_axis(c, 27.4, 0, 1.5, 1.5, s)
    ridge = c.m_poly(axis([(1.5, -.3), (8.5, -.3), (8.5, .3), (1.5, .3)], s))
    return [(shaft, 'dark'), (hd, head), (ridge, 'white'), (guard, 'trim'), (butt, 'gem')]


def glaive(c, t):
    return spear(c, t, 1.0, 'gem')


def lance(c, t):
    return spear(c, t, 1.0, 'body')


def greatsword(c, t, s=1.05, skull=False):
    bl = c.m_poly(axis([(0, 0), (3.2, -3.2), (16.5, -3.2), (16.5, 0), (3.2, 0)], s))
    br = c.m_poly(axis([(0, 0), (3.2, 0), (16.5, 0), (16.5, 3.2), (3.2, 3.2)], s))
    rune = c.m_poly(axis([(4, -.5), (15, -.5), (15, .5), (4, .5)], s))
    guard = c.m_poly(axis([(16, -6.6), (17.2, -2.5), (18.6, -6.2), (19.2, -2.2), (19.2, 2.2), (18.6, 6.2), (17.2, 2.5), (16, 6.6)], s))
    grip = c.m_poly(axis([(19, -1.4), (24.5, -1.4), (24.5, 1.4), (19, 1.4)], s))
    pom = _ell_axis(c, 25.8, 0, 2.0, 2.0, s)
    parts = [(bl, 'body'), (br, 'body2'), (rune, 'gem'), (grip, 'dark'), (guard, 'trim'), (pom, 'gem')]
    if skull:
        parts.append((_ell_axis(c, 17.6, 0, 2.6, 2.3, s), 'white'))
        parts.append((Canvas.union(_ell_axis(c, 17.4, -.9, .6, .6, s), _ell_axis(c, 17.4, .9, .6, .6, s)), 'gem'))
    return parts


def runeblade(c, t):
    return greatsword(c, t, 1.05, True)


def staff(c, t, s=1.0):
    shaft = c.m_poly(axis([(5, -.9), (27, -.9), (27, .9), (5, .9)], s))
    ring = c.m_poly(axis([(-.2 + 4.2 * math.cos(a) + 4.0, 4.2 * math.sin(a)) for a in [i * math.pi / 14 for i in range(29)]], s))
    hole = c.m_poly(axis([(5.8 + 3.3 * math.cos(a), 3.3 * math.sin(a)) for a in [i * math.pi / 14 for i in range(29)]], s))
    from PIL import ImageChops
    cres = ImageChops.subtract(ring, hole)
    gem = _ell_axis(c, 8.6, 0, 1.6, 1.6, s)
    wrap = c.m_poly(axis([(12, -1.2), (13.2, -1.2), (13.2, 1.2), (12, 1.2)], s))
    return [(shaft, 'dark'), (cres, 'trim'), (wrap, 'white'), (gem, 'gem')]


def _hand_local(bumps=3):
    """hand pointing up, fingertip at origin (units ~ cursor px)."""
    ox, oy = 12.3, -4.0
    sh = lambda pts: [(x - ox, y - oy) for x, y in pts]
    finger = sh(rrpoly(10.2, -4.0, 14.4, 18, 2.1))
    palm = sh(rrpoly(7.4, 15.2, 25.4, 27, 4.2))
    bx = [(14.0, 12.4, 17.4, 19.5), (17.2, 13.5, 20.6, 20.2), (20.4, 14.9, 23.8, 21.2)][:bumps]
    kn = [sh(rrpoly(a, b, c_, d, 1.7)) for a, b, c_, d in bx]
    th = sh([(6.2 + 3.9 * math.cos(math.radians(a)) * math.cos(.5) - 2.3 * math.sin(math.radians(a)) * math.sin(.5),
              19.6 + 3.9 * math.cos(math.radians(a)) * math.sin(.5) + 2.3 * math.sin(math.radians(a)) * math.cos(.5)) for a in range(0, 360, 15)])
    cuff = sh(rrpoly(7.8, 24.4, 25.0, 28.6, 1.3))
    joints = [sh([(10.4, 3.2), (14.2, 3.2), (14.2, 4.0), (10.4, 4.0)]), sh([(10.4, 9.5), (14.2, 9.5), (14.2, 10.3), (10.4, 10.3)])]
    return finger, palm, kn, th, cuff, joints


def gauntlet(c, t, plated=True, bumps=3, s=.74):
    tap = .5 * math.sin(t * 2 * math.pi)
    f, palm, kn, th, cuff, joints = _hand_local(bumps)
    R = lambda pts: c.m_poly(_rot(pts, -45, s, (2.4 - tap * .3, 2.4 - tap * .3)))
    body = Canvas.union(R(f), R(palm), *[R(k) for k in kn])
    parts = [(R(th), 'body2'), (body, 'body'), (R(cuff), 'trim')]
    if plated:
        parts.append((Canvas.union(*[R(j) for j in joints]), 'dark'))
        parts.append((Canvas.union(*[R(k) for k in kn]), 'trim'))
    return parts


def cartoonhand(c, t):
    return gauntlet(c, t, plated=False, bumps=2)


def brush(c, t):
    m = c.m_poly([(2, 2), (19.5, 6.4), (12.6, 10.8), (27.6, 25.2), (25.2, 27.6), (10.8, 12.6), (6.4, 19.5)])
    tip = c.m_poly([(2, 2), (13, 5), (5, 13)])
    return [(m, 'body'), (tip, 'trim')]


def boltptr(c, t):
    m = c.m_poly([(2, 2), (16, 8.6), (11.6, 10.6), (22.5, 17.4), (18.4, 18.8), (27.5, 27.5), (13.2, 19.8), (17.2, 17.8), (6.6, 12.2), (10.6, 10.4)])
    base = c.m_poly([(20.5, 22.4), (27.5, 27.5), (22.4, 20.5)])
    return [(m, 'body'), (base, 'dark')]


def rodptr(c, t, s=1.0):
    body = c.m_poly(axis([(0.6, -2.1), (24, -2.1), (24, 2.1), (0.6, 2.1)], s))
    tipm = _ell_axis(c, 1.2, 0, 1.6, 2.1, s)
    bands = Canvas.union(*[c.m_poly(axis([(x, -2.2), (x + 1.4, -2.2), (x + 1.4, 2.2), (x, 2.2)], s)) for x in (6, 12, 18)])
    return [(Canvas.union(body, tipm), 'body'), (bands, 'gem')]


def emitter(c, t, s=1.0):
    body = c.m_poly(axis([(4, -1.9), (24, -1.6), (24, 1.6), (4, 1.9)], s))
    cone = c.m_poly(axis([(0, 0), (4.2, -1.9), (4.2, 1.9)], s))
    ring = c.m_poly(axis([(8, -2.2), (9.6, -2.2), (9.6, 2.2), (8, 2.2)], s))
    led = _ell_axis(c, 14, 0, 1.0, 1.0, s)
    return [(body, 'dark'), (cone, 'gem'), (ring, 'trim'), (led, 'accent')]


def mini(c, t):
    pts = [(2 + (x - 2) * .62, 2 + (y - 2) * .62) for x, y in ARROWS['classic']]
    return [(c.m_poly(pts), 'body')]


OBJECTS.update(dict(spear=lance, glaive=glaive, greatsword=greatsword, runeblade=runeblade, staff=staff, gauntlet=gauntlet,
                    cartoonhand=cartoonhand, brush=brush, boltptr=boltptr, rodptr=rodptr, emitter=emitter, mini=mini))
