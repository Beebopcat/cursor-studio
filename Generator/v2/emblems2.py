import math
from PIL import ImageDraw, ImageChops
from toolkit import *
from emblems import EMBLEMS, _pt, _ow


def wheel(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.ell(cx, cy, r, r, hexc('c88a4a'), hexc('6a3a14'), hexc('2a1405'), ow=_ow(r), mode='r', hi=.5)
    c.ell(cx, cy, r * .72, r * .72, hexc('3a2008'), hexc('3a2008'), None, hi=0, shadow=False)
    for k in range(8):
        a = math.radians(k * 45 + t * 45)
        c.stroke([(cx, cy), (cx + math.cos(a) * r * .8, cy + math.sin(a) * r * .8)], r * .13, hexc('e0a560'), outline=hexc('2a1405'), ow=.3)
    c.ell(cx, cy, r * .24, r * .24, hexc('ffd35a'), hexc('b8801a'), hexc('2a1405'), ow=_ow(r) * .5, hi=.5, shadow=False)


def sunburst(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    for k in range(10):
        a = math.radians(k * 36 + t * 36)
        c.poly([(cx + math.cos(a - .12) * r * .5, cy + math.sin(a - .12) * r * .5), (cx + math.cos(a) * r * 1.12, cy + math.sin(a) * r * 1.12),
                (cx + math.cos(a + .12) * r * .5, cy + math.sin(a + .12) * r * .5)], hexc('fff2b0'), hexc('ffb347'), None, hi=0, shadow=False)
    c.ell(cx, cy, r * .55, r * .55, hexc('fffbe0'), hexc('ffc04a'), hexc('a05a10'), ow=_ow(r) * .8, mode='r', hi=.5)


def gear(c, cx, cy, r, t, p):
    n = 8
    pts = []
    for i in range(n * 4):
        a = math.radians(i * 360 / (n * 4) + t * 360 / n)
        rr = r if (i % 4) in (1, 2) else r * .78
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    m = c.m_poly(pts)
    c.shape(m, hexc('e8c394'), hexc('7a4a1e'), hexc('2a1405'), ow=_ow(r), mode='r', hi=.6)
    c.ell(cx, cy, r * .42, r * .42, hexc('0e2a3a'), hexc('04101a'), hexc('2a1405'), ow=_ow(r) * .5, hi=0, shadow=False)
    c.glow(cx, cy, r * .5, hexc('3ee0ff'), .8)
    c.paint(c.m_ellipse(cx, cy, r * .2), hexc('d8ffff'))


def pumpkin(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.2, hexc('ff8a1a'), .35 + .3 * tri(t))
    for ux in (-.5, 0, .5):
        c.ell(*P(ux, .08), r * (.5 if ux == 0 else .42), r * .78, hexc('ffa640'), hexc('c4560c'), hexc('4a1a04'), ow=_ow(r) * .8, mode='r', hi=.5, shadow=(ux == -.5))
    c.rr(*P(-.08, -.95), *P(.14, -.55), r * .05, hexc('6a8a3a'), hexc('2a4a14'), hexc('0a1a04'), ow=_ow(r) * .5, hi=.2, shadow=False)
    f = .7 + .3 * tri(t)
    for ex in (-.34, .34):
        c.poly([P(ex - .16, -.05), P(ex + .16, -.05), P(ex, -.38)], hexc('fff2a0'), hexc('ffb800'), None, hi=0, shadow=False)
        c.glow(*P(ex, -.15), r * .22, hexc('ffd35a'), f)
    c.poly([P(-.4, .3), P(-.2, .5), P(0, .34), P(.2, .5), P(.4, .3), P(.3, .6), P(0, .72), P(-.3, .6)], hexc('fff2a0'), hexc('ffb800'), hexc('4a1a04'), ow=_ow(r) * .3, hi=0, shadow=False)


def rune(c, cx, cy, r, t, p):
    c.glow(cx, cy, r * 1.1, p['glow'], .5)
    c.paint(c.m_arc(cx, cy, r * .95, 0, 360, r * .14), lighten(p['glow'], .3))
    for i in range(3):
        a0 = t * 360 + i * 120
        c.paint(c.m_arc(cx, cy, r * .62, a0, a0 + 80, r * .13), (255, 255, 255, 255), .9)
    c.stroke([(cx - r * .3, cy - r * .35), (cx + r * .3, cy - r * .35), (cx, cy + r * .45)], r * .13, lighten(p['glow'], .5))
    c.paint(c.m_ellipse(cx, cy, r * .13), (255, 255, 255, 255))


EMBLEMS.update(dict(wheel=wheel, sunburst=sunburst, gear=gear, pumpkin=pumpkin, rune=rune))
