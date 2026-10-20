"""Emblems for the 24-set roster (Gemini concept list). Same signature as emblems.py."""
import math
from PIL import ImageChops, ImageDraw
from toolkit import *
from emblems import EMBLEMS, _pt, _ow

TAU = 2 * math.pi


def _poly_rot(pts, cx, cy, deg):
    a = math.radians(deg)
    return [(cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a), cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)) for x, y in pts]


def _gem(c, pts, top, bot, ol, r, hi=.6, shadow=False):
    c.poly(pts, top, bot, ol, ow=_ow(r) * .8, hi=hi, shadow=shadow)


def mothercrystal(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.15, hexc('7fe0ff'), .35 + .25 * tri(t))
    for side, ang in ((-1, -22), (1, 22)):
        base = [P(side * .42, -.55), P(side * .62, -.15), P(side * .5, .75), P(side * .25, .75), P(side * .22, -.15)]
        _gem(c, _poly_rot(base, *P(side * .42, .4), ang), hexc('b9f2ff'), hexc('2a6fd0'), hexc('0b2560'), r)
    main = [P(0, -1.1), P(.32, -.55), P(.28, .85), P(0, 1.0), P(-.28, .85), P(-.32, -.55)]
    _gem(c, main, hexc('f4feff'), hexc('3a8fe8'), hexc('0b2560'), r, .7, True)
    c.paint(c.m_poly([P(0, -1.1), P(.32, -.55), P(0, -.3), P(-.32, -.55)]), hexc('ffffff'), .7)
    c.paint(c.m_poly([P(0, -.3), P(.32, -.55), P(.28, .85), P(0, 1.0)]), hexc('1d4fb8'), .35)
    for i in range(3):
        a = t * TAU + i * TAU / 3
        x, y = cx + math.cos(a) * r * 1.0, cy + math.sin(a) * r * .45
        _gem(c, [(x, y - r * .2), (x + r * .1, y), (x, y + r * .2), (x - r * .1, y)], hexc('ffffff'), hexc('7fe0ff'), hexc('0b2560'), r * .5, .3)


def moonface(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.2, hexc('a050ff'), .45)
    moon = ImageChops.subtract(c.m_ellipse(cx, cy, r * .98), c.m_ellipse(*P(.5, -.25), r * .82))
    c.shape(moon, hexc('d9a8ff'), hexc('5a1aa8'), hexc('1a0533'), ow=_ow(r), mode='r', hi=.6)
    grin = c.m_arc(*P(-.25, .05), r * .45, 30, 120, r * .1)
    c.paint(ImageChops.multiply(grin, moon), hexc('1a0533'))
    b = .7 + .3 * tri(t)
    c.glow(*P(-.55, -.25), r * .3, hexc('ff2a3a'), b)
    c.ell(*P(-.55, -.25), r * .14, r * .11, hexc('ffd0d0'), hexc('ff2a3a'), hexc('2a0508'), ow=_ow(r) * .4, hi=0, shadow=False)
    c.sparkle(*P(.55, -.55), r * .35, hexc('ffe9ff'), .4 + .6 * tri(t))
    c.sparkle(*P(.6, .45), r * .25, hexc('ffe9ff'), .4 + .6 * tri((t + .5) % 1))


def meteor(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    fl = .08 * math.sin(t * TAU * 2)
    for k, (col, sc) in enumerate(((hexc('ff3a10'), 1.0), (hexc('ff8a20'), .78), (hexc('ffe27a'), .55))):
        tail = [P(.2 * sc - .25, -.45 * sc + .15), P(1.05 + fl, -1.05 - fl), P(.45 * sc - .1, .2 * sc + .1)]
        c.poly(tail, lighten(col, .2), col, None, hi=0, shadow=False)
    c.glow(*P(-.25, .25), r * .8, hexc('ff5a1a'), .7)
    c.ell(*P(-.25, .25), r * .55, r * .55, hexc('8a3020'), hexc('2a0a06'), hexc('120402'), ow=_ow(r), mode='r', hi=.3)
    for a in (20, 140, 260):
        aa = math.radians(a + t * 60)
        c.stroke([P(-.25, .25), (cx + (-.25 + .4 * math.cos(aa)) * r, cy + (.25 + .4 * math.sin(aa)) * r)], r * .07, hexc('ffb040'))


def helm(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.15, hexc('5ad8ff'), .3 + .25 * tri(t))
    spikes = []
    for i, ux in enumerate((-.75, -.4, 0, .4, .75)):
        h = (-1.15 if ux == 0 else -.95 if abs(ux) < .5 else -.75)
        spikes.append([P(ux - .14, -.35), P(ux, h), P(ux + .14, -.35)])
    for sp in spikes:
        c.poly(sp, hexc('c8d4e6'), hexc('3a4660'), hexc('080c18'), ow=_ow(r) * .8, hi=.4, shadow=False)
    shell = [P(-.85, -.4), P(.85, -.4), P(.8, .45), P(.42, 1.0), P(.15, .55), P(-.15, .55), P(-.42, 1.0), P(-.8, .45)]
    c.poly(shell, hexc('b8c6dc'), hexc('2a3448'), hexc('080c18'), ow=_ow(r), hi=.6)
    c.rr(*P(-.6, -.05), *P(.6, .2), r * .08, hexc('04080f'), hexc('04080f'), None, hi=0, shadow=False)
    b = .7 + .3 * tri(t)
    for ex in (-.32, .32):
        c.glow(*P(ex, .08), r * .3, hexc('5ad8ff'), b)
        c.paint(c.m_ellipse(*P(ex, .08), r * .1, r * .06), hexc('e8ffff'))


def hearthstone(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.ell(cx, cy, r, r * .9, hexc('ffe27a'), hexc('a06a10'), hexc('2a1805'), ow=_ow(r), mode='r', hi=.6)
    c.ell(cx, cy, r * .78, r * .7, hexc('6a7aa0'), hexc('1a2440'), hexc('2a1805'), ow=_ow(r) * .5, mode='r', hi=.3, shadow=False)
    for i in range(3):
        a0 = -t * 360 + i * 120
        for k, rr in enumerate((.55, .35)):
            c.paint(c.m_arc(cx, cy, r * rr, a0 + k * 40, a0 + k * 40 + 100, r * .12), hexc('6ad8ff' if k else '2a8aff'), .95)
    c.glow(cx, cy, r * .3, hexc('aaf0ff'), .9)


def eyevines(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    for k in range(3):
        a = math.radians(k * 120 + 40 + 10 * math.sin(t * TAU))
        pts = [(cx + math.cos(a + d * .3) * r * (.6 + d * .45), cy + math.sin(a + d * .3) * r * (.6 + d * .45)) for d in (0, .5, 1)]
        c.stroke(pts, r * .12, hexc('5aff7a'), outline=hexc('0a3a14'), ow=.35)
        c.ell(*pts[-1], r * .12, r * .12, hexc('c8ffb0'), hexc('3ac05a'), hexc('0a3a14'), ow=.3, hi=.4, shadow=False)
    eye = [P(-1, 0), P(-.5, -.5), P(0, -.62), P(.5, -.5), P(1, 0), P(.5, .5), P(0, .62), P(-.5, .5)]
    c.poly(eye, hexc('ffe9a8'), hexc('c48a1a'), hexc('2a1805'), ow=_ow(r), hi=.6)
    c.ell(cx, cy, r * .4, r * .4, hexc('e0b0ff'), hexc('6a2ad0'), hexc('1a0533'), ow=_ow(r) * .6, mode='r', hi=.5, shadow=False)
    c.ell(cx, cy, r * .16, r * .26 * (.6 + .4 * tri(t)), hexc('1a0533'), hexc('1a0533'), None, hi=0, shadow=False)
    c.paint(c.m_ellipse(*P(-.12, -.15), r * .08), hexc('ffffff'))


def canister(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.rr(*P(-.7, -.45), *P(.7, 1.0), r * .2, hexc('b06aff'), hexc('4a1a8a'), hexc('12052a'), ow=_ow(r), hi=.6)
    c.rr(*P(-.72, .05), *P(.72, .45), r * .05, hexc('ffe14a'), hexc('d0a010'), hexc('12052a'), ow=_ow(r) * .5, hi=.3, shadow=False)
    c.rr(*P(-.8, -.65), *P(.8, -.38), r * .1, hexc('d9b6ff'), hexc('6a3ab0'), hexc('12052a'), ow=_ow(r) * .8, hi=.5, shadow=False)
    goo = c.union(c.m_ellipse(*P(0, -.7), r * .55, r * .3), c.m_ellipse(*P(-.45, -.45), r * .14, r * (.35 + .1 * tri(t))), c.m_ellipse(*P(.3, -.5), r * .12, r * .3))
    c.shape(goo, hexc('c8ff6a'), hexc('2f9a14'), hexc('0a3a05'), ow=_ow(r) * .7, mode='r', hi=.6, shadow=False)
    c.paint(c.m_ellipse(*P(-.1, .25), r * .14), hexc('3a2005'))


def flamingo(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    bob = .05 * math.sin(t * TAU)
    for lx in (-.1, .1):
        c.stroke([P(lx, .35), P(lx + .02, 1.1)], r * .07, hexc('e05a8a'), outline=hexc('4a0a2a'), ow=.25)
    c.ell(*P(.05, .2 + bob), r * .6, r * .36, hexc('ffb0d0'), hexc('e0508e'), hexc('4a0a2a'), ow=_ow(r), mode='r', hi=.6)
    c.stroke([P(-.4, .1 + bob), P(-.6, -.35 + bob), P(-.3, -.75 + bob)], r * .14, hexc('ff8ab8'), outline=hexc('4a0a2a'), ow=.35)
    c.ell(*P(-.25, -.8 + bob), r * .2, r * .18, hexc('ffb0d0'), hexc('e0508e'), hexc('4a0a2a'), ow=_ow(r) * .6, hi=.5, shadow=False)
    c.poly([P(-.1, -.85 + bob), P(.3, -.7 + bob), P(-.05, -.7 + bob)], hexc('ffe27a'), hexc('1a1a1a'), hexc('1a0a0a'), ow=_ow(r) * .4, hi=0, shadow=False)
    c.paint(c.m_ellipse(*P(-.25, -.84 + bob), r * .05), hexc('1a0a0a'))


def apple(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    body = c.union(c.m_ellipse(*P(-.3, .1), r * .62, r * .78), c.m_ellipse(*P(.3, .1), r * .62, r * .78))
    body = ImageChops.subtract(body, c.m_ellipse(*P(.95, .1), r * .38))
    c.shape(body, hexc('ff6a5a'), hexc('a00f1a'), hexc('2a0305'), ow=_ow(r), mode='r', hi=.6)
    bite = ImageChops.multiply(c.m_ellipse(*P(.95, .1), r * .46), c.union(c.m_ellipse(*P(-.3, .1), r * .62, r * .78), c.m_ellipse(*P(.3, .1), r * .62, r * .78)))
    c.paint(ImageChops.subtract(bite, c.m_ellipse(*P(.95, .1), r * .38)), hexc('fff2c8'))
    c.stroke([P(0, -.6), P(.1, -1.0)], r * .1, hexc('5a3010'))
    c.poly([P(.1, -.85), P(.6, -1.05), P(.3, -.7)], hexc('9af07a'), hexc('2a8a3a'), hexc('0a3a14'), ow=_ow(r) * .5, hi=.4, shadow=False)
    c.paint(c.m_ellipse(*P(-.45, -.25), r * .18, r * .12), hexc('ffffff'), .7)
    c.sparkle(*P(-.8, -.7), r * .3, hexc('fff2c8'), .4 + .6 * tri(t))


def charrpaw(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    fur = (hexc('ffb257'), hexc('b8500c'))
    c.ell(*P(0, .35), r * .62, r * .5, fur[0], fur[1], hexc('3a1405'), ow=_ow(r), mode='r', hi=.5)
    c.ell(*P(0, .4), r * .34, r * .26, hexc('5a3a30'), hexc('2a1810'), None, hi=.3, shadow=False)
    for ux, vy in ((-.72, -.15), (-.26, -.6), (.26, -.6), (.72, -.15)):
        c.poly([P(ux - .06, vy - .22), P(ux, vy - .55 - .05 * tri(t)), P(ux + .06, vy - .22)], hexc('f4efe0'), hexc('8a8070'), hexc('1a1410'), ow=_ow(r) * .4, hi=0, shadow=False)
        c.ell(*P(ux, vy), r * .22, r * .28, fur[0], fur[1], hexc('3a1405'), ow=_ow(r) * .9, mode='r', hi=.45, shadow=False)
        c.ell(*P(ux, vy + .03), r * .11, r * .14, hexc('5a3a30'), hexc('2a1810'), None, hi=.3, shadow=False)


def scruffy(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    for s in (-1, 1):
        c.stroke([P(s * .35, -.6), P(s * .55, -1.0)], r * .08, hexc('3a4a5a'))
        c.ell(*P(s * .55, -1.0), r * .1, r * .1, hexc('ff8ad8'), hexc('d0308e'), None, hi=0, shadow=False)
    c.ell(cx, cy, r * .85, r * .75, hexc('7af0e0'), hexc('1a8a8a'), hexc('052a2a'), ow=_ow(r), mode='r', hi=.6)
    c.rr(*P(-.85, .2), *P(.85, .45), r * .08, hexc('ff8ad8'), hexc('c0307e'), hexc('3a0520'), ow=_ow(r) * .5, hi=.4, shadow=False)
    c.ell(cx, cy - r * .1, r * .36, r * .36, hexc('1a2030'), hexc('05080f'), hexc('052a2a'), ow=_ow(r) * .6, hi=0, shadow=False)
    b = .7 + .3 * tri(t)
    c.glow(cx, cy - r * .1, r * .3, hexc('ff5ad0'), b)
    c.paint(c.m_ellipse(cx, cy - r * .1, r * .13), hexc('ffd0f0'))


def blossom(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, hexc('9aff6a'), .3 + .3 * tri(t))
    for k in range(6):
        a = k * 60 + t * 30
        pet = _poly_rot([P(0, -.15), P(.22, -.6), P(0, -1.0), P(-.22, -.6)], cx, cy, a)
        c.poly(pet, hexc('ffe27a'), hexc('3ac05a'), hexc('0a3a14'), ow=_ow(r) * .6, hi=.5, shadow=False)
    c.ell(cx, cy, r * .45, r * .45, hexc('c8ff9a'), hexc('2a8a3a'), hexc('0a3a14'), ow=_ow(r) * .8, mode='r', hi=.6)
    c.stroke([P(.3, -.3), P(.55, -.65)], r * .08, hexc('5a3010'))
    c.sparkle(*P(.6, -.72), r * .3, hexc('fff2a0'), .5 + .5 * tri((t * 3) % 1))


def scarab(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, hexc('43ff9a'), .3 + .25 * tri(t))
    leg = .08 * math.sin(t * TAU * 2)
    for s in (-1, 1):
        for vy in (-.15, .2, .55):
            c.stroke([P(s * .4, vy), P(s * .85, vy - .15 + leg * s)], r * .07, hexc('3a2a10'))
    c.ell(*P(0, .25), r * .55, r * .62, hexc('ffe27a'), hexc('a06a10'), hexc('2a1805'), ow=_ow(r), mode='r', hi=.6)
    c.stroke([P(0, -.3), P(0, .85)], r * .05, hexc('5a3a05'))
    c.ell(*P(0, -.5), r * .32, r * .22, hexc('ffd35a'), hexc('8a5a10'), hexc('2a1805'), ow=_ow(r) * .8, hi=.5, shadow=False)
    c.ell(*P(0, -.82), r * .22, r * .14, hexc('7affb0'), hexc('1a9a5a'), hexc('05200f'), ow=_ow(r) * .5, hi=.5, shadow=False)
    for vy in (.05, .35, .65):
        c.stroke([P(-.45, vy), P(.45, vy)], r * .04, hexc('f4efe0'), alpha=.65)


def commander(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    tag = [P(-.75, -.85), P(.75, -.85), P(.75, .2), P(0, 1.0), P(-.75, .2)]
    hues = ['ff5a4a', 'ffb03a', '6ae05a', '4aa8ff', 'c06aff']
    k = int(t * 5) % 5
    top, bot = hexc(hues[k]), hexc(hues[(k + 1) % 5])
    c.poly(tag, lighten(top, .3), darken(bot, .2), hexc('140a1a'), ow=_ow(r), hi=.6)
    inner = [P(-.5, -.62), P(.5, -.62), P(.5, .1), P(0, .66), P(-.5, .1)]
    c.poly(inner, hexc('ffffff'), lighten(top, .4), None, hi=0, shadow=False)
    c.star(*P(0, -.05), r * .38, darken(top, .1), 5, .45)
    c.glow(cx, cy, r * .9, top, .25)


def polyhedron(c, cx, cy, r, t, p):
    ang = t * 60
    outer = [(cx + r * math.cos(math.radians(ang + i * 60)), cy + r * math.sin(math.radians(ang + i * 60))) for i in range(6)]
    inner = [(cx + r * .5 * math.cos(math.radians(-ang + 30 + i * 120)), cy + r * .5 * math.sin(math.radians(-ang + 30 + i * 120))) for i in range(3)]
    c.glow(cx, cy, r * 1.1, hexc('3ee0ff'), .4)
    c.poly(outer, hexc('3a2a7a'), hexc('0a1030'), hexc('3ee0ff'), ow=_ow(r) * .6, hi=.2)
    for i in range(6):
        for j in range(3):
            c.stroke([outer[i], inner[j]], r * .05, hexc('3ee0ff' if (i + j) % 2 else 'ff5ad0'), alpha=.75)
    c.poly(inner, hexc('ff8ad8'), hexc('8a2a8a'), hexc('3ee0ff'), ow=_ow(r) * .4, hi=.4, shadow=False)
    c.paint(c.m_ellipse(cx, cy, r * .14), hexc('ffffff'))


def bolt(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    pts = [P(.15, -1.05), P(-.6, .1), P(-.05, .1), P(-.3, 1.05), P(.65, -.25), P(.1, -.25), P(.4, -1.05)]
    c.glow(cx, cy, r, hexc('ffe14a'), .35 + .35 * tri(t))
    c.poly(pts, hexc('fff2a0'), hexc('ffb800'), hexc('5a3a00'), ow=_ow(r), hi=.6)
    for k in range(2):
        a = t * TAU + k * math.pi
        c.sparkle(cx + math.cos(a) * r * .9, cy + math.sin(a) * r * .9, r * .25, hexc('ffffff'), .5 + .5 * tri(t))


def gringhost(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    bob = .05 * math.sin(t * TAU)
    body = [P(-.95, .4 + bob), P(-.85, -.3 + bob), P(-.7, -.75 + bob), P(-.45, -.55 + bob), P(-.25, -.95 + bob), P(0, -.62 + bob), P(.25, -.95 + bob),
            P(.45, -.55 + bob), P(.7, -.75 + bob), P(.85, -.3 + bob), P(.95, .4 + bob), P(.6, .85 + bob), P(0, .95 + bob), P(-.6, .85 + bob)]
    c.poly(body, hexc('9a6ae0'), hexc('3a1a7a'), hexc('12052a'), ow=_ow(r), mode='r', hi=.5)
    for ex in (-.38, .38):
        c.poly([P(ex - .22, -.25 + bob), P(ex + .22, -.12 + bob), P(ex, .05 + bob)] if ex < 0 else [P(ex + .22, -.25 + bob), P(ex - .22, -.12 + bob), P(ex, .05 + bob)],
               hexc('ffd0d0'), hexc('ff2a3a'), hexc('2a0508'), ow=_ow(r) * .4, hi=0, shadow=False)
    grin = [P(-.6, .2 + bob), P(.6, .2 + bob), P(.35, .55 + bob), P(-.35, .55 + bob)]
    c.poly(grin, hexc('ffffff'), hexc('e6e0ff'), hexc('12052a'), ow=_ow(r) * .5, hi=0, shadow=False)
    for ux in (-.3, 0, .3):
        c.stroke([P(ux, .22 + bob), P(ux, .5 + bob)], r * .04, hexc('7a6aa0'))


def candle(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    fl = .06 * math.sin(t * TAU * 2)
    c.glow(*P(0, -.6), r * .6, hexc('8a5aff'), .6 + .3 * tri(t))
    c.rr(*P(-.42, -.25), *P(.42, 1.0), r * .2, hexc('ffffff'), hexc('c9c4e0'), hexc('2a1a4a'), ow=_ow(r), hi=.5)
    c.ell(*P(.2, .1), r * .08, r * .2, hexc('e6e0ff'), hexc('c9c4e0'), None, hi=0, shadow=False)
    c.poly([P(-.28 + fl, -.3), P(fl * 2, -1.1), P(.28 + fl, -.3), P(0, -.15)], hexc('d9c8ff'), hexc('6a3aff'), hexc('1a0a4a'), ow=_ow(r) * .6, hi=.5, shadow=False)
    for ex in (-.16, .16):
        c.ell(*P(ex, .3), r * .07, r * .1, hexc('ffd35a'), hexc('d08a10'), None, hi=0, shadow=False)


def fish3(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    w = .1 * math.sin(t * TAU * 2)
    c.poly([P(.55, 0), P(1.05, -.5 + w), P(.9, 0), P(1.05, .5 + w)], hexc('ffb050'), hexc('d0601a'), hexc('3a1405'), ow=_ow(r), hi=.4)
    c.ell(*P(-.1, 0), r * .75, r * .5, hexc('ffc070'), hexc('e0701a'), hexc('3a1405'), ow=_ow(r), mode='r', hi=.6)
    for ux, vy in ((-.6, -.18), (-.38, -.25), (-.48, .02)):
        c.ell(*P(ux, vy), r * .11, r * .11, hexc('ffffff'), hexc('e6e6e6'), hexc('1a0a05'), ow=_ow(r) * .3, hi=0, shadow=False)
        c.paint(c.m_ellipse(*P(ux + .02, vy), r * .05), hexc('1a0a05'))
    c.stroke([P(-.7, .22), P(-.55, .28)], r * .05, hexc('3a1405'))
    c.paint(c.m_ellipse(*P(.15, .05), r * .5, r * .3), hexc('5aff3a'), .18 + .12 * tri(t))


def rod(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, hexc('5aff3a'), .35 + .35 * tri(t))
    body = _poly_rot([P(-.22, -1.0), P(.22, -1.0), P(.22, 1.0), P(-.22, 1.0)], cx, cy, 35)
    c.poly(body, hexc('8a9a8a'), hexc('2a3028'), hexc('0a0f08'), ow=_ow(r), hi=.5)
    for vy in (-.55, 0, .55):
        band = _poly_rot([P(-.24, vy - .08), P(.24, vy - .08), P(.24, vy + .08), P(-.24, vy + .08)], cx, cy, 35)
        c.paint(c.m_poly(band), hexc('b6ff6a'))
    c.glow(*_poly_rot([P(0, -1.0)], cx, cy, 35)[0], r * .35, hexc('b6ff6a'), .9)


def ribbon(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    s = .05 * math.sin(t * TAU)
    pink = (hexc('ffc4dc'), hexc('ff5aa0'), hexc('6a1040'))
    for sx in (-1, 1):
        c.poly([P(sx * .12, -.1), P(sx * (.95 + s), -.65), P(sx * (1.0 + s), .35), P(sx * .12, .1)], *pink, ow=_ow(r), mode='r', hi=.6)
        c.poly([P(sx * .1, .1), P(sx * .45, .95), P(sx * .25, .8), P(sx * .05, .95)], pink[0], pink[1], pink[2], ow=_ow(r) * .7, hi=.4, shadow=False)
    c.ell(cx, cy, r * .25, r * .28, hexc('ffe0ee'), hexc('ff6aa8'), pink[2], ow=_ow(r) * .7, hi=.6, shadow=False)


def angelwing(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    flap = 7 * math.sin(t * TAU)
    root = P(-.85, .75)
    for k in range(4, -1, -1):
        a = math.radians(-62 + k * 21 + flap * (1 - k * .15))
        L = r * (1.95 - k * .22)
        w = r * .25
        n = 18
        pts = []
        for i in range(n):
            u = 2 * math.pi * i / n
            lx, ly = math.cos(u) * L / 2 + L / 2, math.sin(u) * w * (1 - .35 * math.cos(u))
            pts.append((root[0] + lx * math.cos(a) - ly * math.sin(a), root[1] + lx * math.sin(a) + ly * math.cos(a)))
        c.poly(pts, hexc('ffffff'), hexc('c4d6ff'), hexc('3a4a7a'), ow=_ow(r) * .7, hi=.6, shadow=(k == 4))
    c.ell(*P(-.55, .45), r * .38, r * .3, hexc('ffffff'), hexc('dce6ff'), hexc('3a4a7a'), ow=_ow(r) * .7, mode='r', hi=.6, shadow=False)


def macaron(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    cols = [('ffb0d0', 'e0508e'), ('b6f0c8', '3ab070'), ('d9c8ff', '7a5ae0')]
    for i, (a, b) in enumerate(cols):
        y = .55 - i * .55 + (.03 * math.sin(t * TAU + i))
        c.ell(*P(0, y + .12), r * .72, r * .22, hexc(a), hexc(b), darken(hexc(b), .6), ow=_ow(r) * .7, hi=.5, shadow=(i == 0))
        c.rr(*P(-.62, y - .04), *P(.62, y + .08), r * .05, hexc('fff8f0'), hexc('f0e0d0'), None, hi=0, shadow=False)
        c.ell(*P(0, y - .1), r * .72, r * .22, hexc(a), hexc(b), darken(hexc(b), .6), ow=_ow(r) * .7, hi=.6, shadow=False)


def witchhat(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    tip = .1 * math.sin(t * TAU)
    c.ell(*P(0, .62), r * 1.0, r * .3, hexc('7a4ad0'), hexc('2a1060'), hexc('0a0420'), ow=_ow(r), hi=.4)
    c.poly([P(-.55, .6), P(-.2, -.3), P(.1 + tip, -1.0), P(.45 + tip, -.75), P(.15, -.35), P(.55, .6)], hexc('8a5ae0'), hexc('2a1060'), hexc('0a0420'), ow=_ow(r), hi=.5)
    c.rr(*P(-.52, .3), *P(.52, .5), r * .05, hexc('ff8a1a'), hexc('b04a05'), hexc('2a0a02'), ow=_ow(r) * .5, hi=.3, shadow=False)
    moon = ImageChops.subtract(c.m_ellipse(*P(0, .4), r * .16), c.m_ellipse(*P(.08, .36), r * .13))
    c.paint(moon, hexc('fff2a0'))
    c.sparkle(*P(.6, -.6), r * .3, hexc('fff2a0'), .4 + .6 * tri(t))


def dragonwing(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    f = .06 * math.sin(t * TAU)
    pts = [P(-.9, .7), P(-.6, -.2), P(-.1, -.9 - f), P(.9, -1.0 - f), P(.6, -.55), P(.95, -.3), P(.55, -.05), P(.85, .3), P(.35, .3), P(.4, .7)]
    c.glow(cx, cy, r * 1.1, hexc('ff4a2a'), .35)
    c.poly(pts, hexc('ff7a4a'), hexc('8a0a10'), hexc('2a0305'), ow=_ow(r), hi=.5)
    for e in ((.9, -1.0 - f), (.95, -.3), (.85, .3)):
        c.stroke([P(-.9, .7), P(*e)], r * .07, hexc('3a0508'), alpha=.85)


def wingdagger(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    f = 5 * math.sin(t * TAU)
    for s in (-1, 1):
        for k in range(3):
            base = P(s * .15, -.1 + k * .18)
            pts = _poly_rot([base, P(s * (.95 - k * .15), -.55 + k * .2), P(s * (.8 - k * .15), -.25 + k * .2)], *base, s * f)
            c.poly(pts, hexc('f0e0c0'), hexc('8a6a40'), hexc('2a1a08'), ow=_ow(r) * .6, hi=.4, shadow=False)
    c.poly([P(0, -1.05), P(.16, -.6), P(.12, .5), P(0, .62), P(-.12, .5), P(-.16, -.6)], hexc('f4f6ff'), hexc('6a7aa8'), hexc('0a1020'), ow=_ow(r) * .8, hi=.6)
    c.rr(*P(-.38, .45), *P(.38, .58), r * .04, hexc('ff5a4a'), hexc('a01014'), hexc('2a0305'), ow=_ow(r) * .4, hi=.3, shadow=False)
    c.rr(*P(-.08, .58), *P(.08, .95), r * .03, hexc('3a2a18'), hexc('1a1008'), None, hi=0, shadow=False)


def holyorb(c, cx, cy, r, t, p):
    c.glow(cx, cy, r * 1.25, hexc('ffe27a'), .55 + .3 * tri(t))
    for k in range(8):
        a = math.radians(k * 45 + t * 45)
        c.stroke([(cx + math.cos(a) * r * .6, cy + math.sin(a) * r * .6), (cx + math.cos(a) * r * 1.05, cy + math.sin(a) * r * 1.05)], r * .1, hexc('fff2a0'), alpha=.9)
    c.ell(cx, cy, r * .58, r * .58, hexc('ffffff'), hexc('ffc04a'), hexc('8a5a05'), ow=_ow(r) * .7, mode='r', hi=.6)


def vcrystal(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, hexc('c070ff'), .35 + .3 * tri(t))
    body = [P(0, -1.12), P(.6, -.32), P(.42, .5), P(0, 1.1), P(-.42, .5), P(-.6, -.32)]
    c.poly(body, hexc('f0d8ff'), hexc('6a2ad0'), hexc('1a0533'), ow=_ow(r), hi=.6)
    c.paint(c.m_poly([P(0, -1.12), P(.6, -.32), P(0, -.1), P(-.6, -.32)]), hexc('ffffff'), .6)
    c.paint(c.m_poly([P(0, -.1), P(.6, -.32), P(.42, .5), P(0, 1.1)]), hexc('3a0a8a'), .4)
    for i in range(3):
        a = t * TAU + i * TAU / 3
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r * .5
        c.sparkle(x, y, r * .25, hexc('e0b0ff'), 1)


def ballbolt(c, cx, cy, r, t, p):
    EMBLEMS['monsterball'](c, cx, cy, r, t, p)


def golemhead(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, hexc('3ee0ff'), .35)
    c.ell(cx, cy, r * .9, r * .82, hexc('f4ecd8'), hexc('a08860'), hexc('2a1a08'), ow=_ow(r), mode='r', hi=.6)
    c.rr(*P(-.95, -.2), *P(.95, .1), r * .08, hexc('ffe27a'), hexc('a06a10'), hexc('2a1805'), ow=_ow(r) * .5, hi=.4, shadow=False)
    c.rr(*P(-.6, -.15), *P(.6, .05), r * .05, hexc('04101a'), hexc('04101a'), None, hi=0, shadow=False)
    b = .7 + .3 * tri(t)
    scan = -.45 + .9 * tri(t)
    c.glow(*P(scan, -.05), r * .3, hexc('3ee0ff'), b)
    c.paint(c.m_rrect(*P(scan - .14, -.12), *P(scan + .14, .02), r * .03), hexc('d8ffff'))


EMBLEMS.update(dict(mothercrystal=mothercrystal, moonface=moonface, meteor=meteor, helm=helm, hearthstone=hearthstone,
                    eyevines=eyevines, canister=canister, flamingo=flamingo, apple=apple, charrpaw=charrpaw, scruffy=scruffy,
                    blossom=blossom, scarab=scarab, commander=commander, polyhedron=polyhedron, bolt=bolt, gringhost=gringhost,
                    candle=candle, fish3=fish3, rod=rod, ribbon=ribbon, angelwing=angelwing, macaron=macaron, witchhat=witchhat,
                    dragonwing=dragonwing, wingdagger=wingdagger, holyorb=holyorb, vcrystal=vcrystal, golemhead=golemhead))
