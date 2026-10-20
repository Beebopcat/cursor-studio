"""Themed emblem painters. Each draws inside a unit circle centred on (cx, cy) with radius r.

Signature: emblem(c, cx, cy, r, t, p) where t in [0,1) is the loop phase and p the palette.
All animation is periodic in t so the .ani loops seamlessly.
"""
import math
from PIL import ImageChops
from toolkit import *

TAU = 2 * math.pi


def _pt(cx, cy, r):
    return lambda u, v: (cx + u * r, cy + v * r)


def _ow(r):
    return max(0.55, r * 0.11)


# ---------------------------------------------------------------- FFXIV
def crystal(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, p['glow'], 0.35 + 0.25 * tri(t))
    top = hexc('f2ffff'); mid = hexc('7fd8ff'); bot = hexc('2f6fd6')
    body = [P(0, -1.12), P(.66, -.32), P(.46, .5), P(0, 1.1), P(-.46, .5), P(-.66, -.32)]
    c.poly(body, mid, bot, hexc('0f2a66'), ow=_ow(r), hi=.6)
    c.paint(c.m_poly([P(0, -1.12), P(.66, -.32), P(0, -.1), P(-.66, -.32)]), top, .85)
    c.paint(c.m_poly([P(0, -.1), P(.66, -.32), P(.46, .5), P(0, 1.1)]), hexc('1d4fb8'), .45)
    c.paint(c.m_poly([P(0, -.1), P(-.66, -.32), P(-.46, .5), P(0, 1.1)]), hexc('bff0ff'), .35)
    c.stroke([P(0, -.1), P(0, 1.1)], .06 * r, hexc('ffffff'), alpha=.5)
    a = t * TAU
    c.sparkle(cx + r * .95 * math.cos(a), cy + r * .8 * math.sin(a) - r * .1, r * .5, hexc('fff6c0'), 0.4 + 0.6 * tri((t * 2) % 1))


def chocobo(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    w = math.sin(t * TAU) * 6
    for ang, ln in ((-28 + w, .8), (4 + w * .6, 1.0), (32 + w * .3, .8)):
        a = math.radians(ang - 90)
        base = P(-.1, -.5)
        tip = (base[0] + math.cos(a) * ln * r, base[1] + math.sin(a) * ln * r)
        n = (-math.sin(a) * .22 * r, math.cos(a) * .22 * r)
        c.poly([(base[0] + n[0], base[1] + n[1]), tip, (base[0] - n[0], base[1] - n[1])],
               hexc('ffe27a'), hexc('f2b01e'), hexc('7a4a05'), ow=_ow(r) * .9, hi=.3, shadow=False)
    c.poly([P(.55, .05), P(1.12, .3), P(.55, .55)], hexc('ffb347'), hexc('e06a14'), hexc('6b2d05'), ow=_ow(r), hi=.4, shadow=False)
    c.ell(*P(-.05, .1), r * .85, r * .8, hexc('fff0a0'), hexc('f4b92a'), hexc('7a4a05'), ow=_ow(r), mode='r', hi=.6)
    c.ell(*P(.22, .0), r * .17, r * .2, hexc('1b1020'), hexc('1b1020'), shadow=False, hi=0)
    c.paint(c.m_ellipse(*P(.26, -.07), r * .06), (255, 255, 255, 255))
    c.paint(c.m_ellipse(*P(.3, .38), r * .16), hexc('ff9a8a'), .55)


def voidmoon(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.2, p['glow'], .55)
    c.ell(cx, cy, r, r, hexc('3a1670'), hexc('070212'), hexc('b57cff'), ow=_ow(r) * .9, mode='r', hi=.2)
    for i in range(3):
        a0 = t * 360 + i * 120
        c.paint(c.m_arc(cx, cy, r * .62, a0, a0 + 70, r * .13), hexc('d29bff'), .8)
    moon = ImageChops.subtract(c.m_ellipse(*P(-.12, 0), r * .7), c.m_ellipse(*P(.18, -.12), r * .6))
    c.shape(moon, hexc('ffffff'), hexc('b9c4e8'), None, hi=0, shadow=False)
    c.sparkle(*P(.5, -.35), r * .4, hexc('ffe9ff'), .5 + .5 * tri(t))
    c.sparkle(*P(.35, .5), r * .3, hexc('ffe9ff'), .5 + .5 * tri((t + .5) % 1))


# ------------------------------------------------------------------ WoW
def stormwind(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    sh = [P(-.85, -.88), P(.85, -.88), P(.85, .12), P(0, 1.08), P(-.85, .12)]
    c.poly(sh, hexc('4f8dff'), hexc('12307e'), hexc('06143a'), ow=_ow(r), hi=.5)
    c.poly([P(-.7, -.74), P(.7, -.74), P(.7, .08), P(0, .9), P(-.7, .08)], hexc('2f63d9'), hexc('0e2a74'), hexc('f4c542'), ow=_ow(r) * .55, hi=.2, shadow=False)
    c.poly([P(-.09, -.7), P(.09, -.7), P(.09, .35), P(0, .5), P(-.09, .35)], hexc('ffffff'), hexc('b8c4d8'), hexc('2a3550'), ow=_ow(r) * .45, hi=0, shadow=False)
    c.poly([P(-.42, -.14), P(.42, -.14), P(.42, .0), P(-.42, .0)], hexc('ffe27a'), hexc('d49a14'), hexc('5a3a05'), ow=_ow(r) * .45, hi=.3, shadow=False)
    c.ell(*P(0, -.78), r * .13, r * .13, hexc('ffe27a'), hexc('d49a14'), hexc('5a3a05'), ow=_ow(r) * .4, hi=0, shadow=False)
    x = -1.0 + 2.0 * ((t * 1.4) % 1)
    band = c.m_line([P(x - .4, -1), P(x + .2, 1.1)], r * .22)
    c.paint(ImageChops.multiply(band, c.m_poly(sh)), (255, 255, 255, 255), .35)


def orgrimmar(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    for i in range(7):
        a = math.radians(i * 360 / 7 - 90 + 12)
        b = (cx + math.cos(a) * r * .55, cy + math.sin(a) * r * .55)
        tip = (cx + math.cos(a) * r * 1.12, cy + math.sin(a) * r * 1.12)
        n = (-math.sin(a) * r * .2, math.cos(a) * r * .2)
        c.poly([(b[0] + n[0], b[1] + n[1]), tip, (b[0] - n[0], b[1] - n[1])], hexc('c9c2b8'), hexc('4a433d'), hexc('140c0a'), ow=_ow(r) * .8, hi=.4, shadow=False)
    c.ell(cx, cy, r * .78, r * .78, hexc('6b5a52'), hexc('1a1210'), hexc('0c0605'), ow=_ow(r), mode='r', hi=.45)
    c.ell(cx, cy, r * .5, r * .5, hexc('d6a24b'), hexc('6b3e0f'), hexc('230f03'), ow=_ow(r) * .6, mode='r', hi=.5, shadow=False)
    pulse = .55 + .45 * tri(t)
    c.glow(cx, cy, r * .45, hexc('ff3b20'), pulse)
    c.ell(cx, cy, r * .24, r * .24, hexc('ff9a50'), hexc('c4140c'), hexc('330503'), ow=_ow(r) * .4, hi=.4, shadow=False)


def frostbound(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, p['glow'], .3 + .3 * tri(t))
    for k in range(3):
        a = math.radians(k * 60 + 90)
        c.stroke([(cx - math.cos(a) * r * .95, cy - math.sin(a) * r * .95), (cx + math.cos(a) * r * .95, cy + math.sin(a) * r * .95)],
                 r * .13, hexc('d8f6ff'), outline=hexc('1d4a8a'), ow=_ow(r) * .5)
    blade = [P(0, -1.1), P(.2, -.5), P(.2, .45), P(0, .62), P(-.2, .45), P(-.2, -.5)]
    c.poly(blade, hexc('ffffff'), hexc('5db8ff'), hexc('0b2a66'), ow=_ow(r), hi=.7)
    c.paint(c.m_poly([P(0, -1.1), P(.2, -.5), P(.2, .45), P(0, .62)]), hexc('2d7dd2'), .35)
    c.poly([P(-.5, .5), P(.5, .5), P(.5, .68), P(-.5, .68)], hexc('9fb0c8'), hexc('3b4a64'), hexc('0a1020'), ow=_ow(r) * .5, hi=.4, shadow=False)
    c.poly([P(-.1, .68), P(.1, .68), P(.1, 1.05), P(-.1, 1.05)], hexc('3a4a66'), hexc('161e30'), hexc('05080f'), ow=_ow(r) * .5, hi=.2, shadow=False)
    c.paint(c.m_poly([P(0, -.2), P(.07, -.05), P(0, .1), P(-.07, -.05)]), hexc('ffffff'), .5 + .5 * tri(t))
    c.sparkle(*P(.8, -.6), r * .38, hexc('ffffff'), .4 + .6 * tri((t * 2) % 1))


# ----------------------------------------------------------- Goosebumps
def monsterblood(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    wob = math.sin(t * TAU) * .05
    c.glow(cx, cy, r * 1.15, hexc('7dff3a'), .35)
    blob = c.union(c.m_ellipse(*P(0, .2), r * (.95 + wob), r * (.7 - wob)),
                   c.m_ellipse(*P(-.35, -.2), r * .5), c.m_ellipse(*P(.4, -.1), r * .55),
                   c.m_rrect(*P(-.6, .3), *P(-.4, 1.1), r * .1), c.m_ellipse(*P(-.5, 1.05), r * .13, r * .17))
    c.shape(blob, hexc('b6ff5a'), hexc('2c9a12'), hexc('0d3b06'), ow=_ow(r), mode='r', hi=.6)
    c.paint(c.m_ellipse(*P(-.4, -.3), r * .2, r * .11), (255, 255, 255, 255), .75)
    for i, (bx, ph) in enumerate(((-.1, 0), (.35, .33), (.6, .66))):
        u = (t + ph) % 1
        c.ell(*P(bx, .5 - u * 1.2), r * (.1 + .08 * (i % 2)), r * (.1 + .08 * (i % 2)), hexc('e8ffc8'), hexc('8aea4a'), hexc('1c5a0b'), ow=_ow(r) * .35, hi=.8, shadow=False)
    c.paint(c.m_ellipse(*P(.1, .45), r * .1, r * .13), hexc('1d4a0a'), .0)


def lawngnome(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    w = math.sin(t * TAU) * .06
    c.poly([P(-.5, .1), P(.5, .1), P(.62, .5), P(.3, 1.08), P(0, 1.15), P(-.3, 1.08), P(-.62, .5)], hexc('ffffff'), hexc('c6c2bd'), hexc('2b2420'), ow=_ow(r) * .9, hi=.5)
    c.ell(*P(0, .25), r * .52, r * .42, hexc('ffd0b0'), hexc('d98c68'), hexc('4a2214'), ow=_ow(r) * .8, mode='r', hi=.5, shadow=False)
    c.poly([P(-.8 + w, .12), P(0 + w * 2, -1.18), P(.8 + w, .12)], hexc('ff5a4a'), hexc('a80f14'), hexc('2c0305'), ow=_ow(r), hi=.55)
    c.rr(*P(-.8, .0), *P(.8, .2), r * .1, hexc('ffffff'), hexc('c9c4be'), hexc('2b2420'), ow=_ow(r) * .6, hi=.3, shadow=False)
    c.ell(*P(0, .34), r * .2, r * .17, hexc('ffa9a0'), hexc('d9534a'), hexc('4a1410'), ow=_ow(r) * .5, hi=.6, shadow=False)
    glint = .6 + .4 * tri(t)
    for ex in (-.25, .25):
        c.ell(*P(ex, .2), r * .1, r * .08, hexc('ffffff'), hexc('dddddd'), hexc('1a0a08'), ow=_ow(r) * .3, hi=0, shadow=False)
        c.paint(c.m_ellipse(*P(ex, .2), r * .045), hexc('ff2a1a'), glint)


# ---------------------------------------------------------------- GW2
def golem_blish(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.15, hexc('3ee0ff'), .4)
    for i in range(3):
        a0 = t * 360 + i * 120
        c.paint(c.m_arc(cx, cy, r * .98, a0, a0 + 62, r * .15), hexc('6af0ff'), .9)
    c.stroke([P(0, -.7), P(0, -1.0)], r * .1, hexc('2a2f3a'))
    c.ell(*P(0, -1.0), r * .12, r * .12, hexc('7af6ff'), hexc('1bb7d6'), None, hi=0, shadow=False)
    c.rr(*P(-.62, -.72), *P(.62, .62), r * .2, hexc('e6c394'), hexc('8a5c2e'), hexc('2e1a0a'), ow=_ow(r), hi=.55)
    c.rr(*P(-.48, -.3), *P(.48, .06), r * .1, hexc('1a2230'), hexc('070b12'), None, hi=0, shadow=False)
    b = .75 + .25 * tri(t)
    for ex in (-.25, .25):
        c.glow(*P(ex, -.12), r * .3, hexc('3ee0ff'), b * .8)
        c.rr(*P(ex - .14, -.2), *P(ex + .14, -.04), r * .04, hexc('d4fdff'), hexc('34d6ff'), None, hi=0, shadow=False)
    c.rr(*P(-.34, .26), *P(.34, .46), r * .05, hexc('5a3c1e'), hexc('2e1a0a'), None, hi=0, shadow=False)
    for ux in (-.5, .5):
        c.paint(c.m_ellipse(*P(ux, -.58), r * .06), hexc('fff0cf'), .9)


def asura_taimi(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    flick = math.sin(t * TAU) * .06
    for s in (-1, 1):
        c.poly([P(s * .55, -.1), P(s * (1.1 + flick), -.78), P(s * .85, .25)], hexc('d9b6ff'), hexc('8250c8'), hexc('2c0f55'), ow=_ow(r), hi=.4, shadow=False)
    c.poly([P(-.25, -.75), P(0, -1.12 - flick), P(.25, -.75)], hexc('7be7ff'), hexc('2a8fcf'), hexc('0a2f55'), ow=_ow(r) * .8, hi=.4, shadow=False)
    c.ell(cx, cy + r * .12, r * .66, r * .78, hexc('f0d4ff'), hexc('a76fe0'), hexc('2c0f55'), ow=_ow(r), mode='r', hi=.6)
    c.rr(*P(-.62, -.42), *P(.62, -.22), r * .1, hexc('4a3a6a'), hexc('1e1536'), None, hi=0, shadow=False)
    for ex in (-.3, .3):
        c.ell(*P(ex, -.32), r * .27, r * .24, hexc('e8fdff'), hexc('49c9f0'), hexc('0e2a4a'), ow=_ow(r) * .7, mode='r', hi=.6, shadow=False)
    c.paint(c.m_ellipse(*P(-.3, -.32), r * .07), hexc('ffffff'), .5 + .5 * tri(t))
    c.paint(c.m_ellipse(*P(.3, -.32), r * .07), hexc('ffffff'), .5 + .5 * tri((t + .5) % 1))
    c.stroke([P(-.2, .38), P(0, .5), P(.2, .38)], r * .09, hexc('3a1a66'))
    c.ell(*P(0, .08), r * .07, r * .06, hexc('7a40c0'), hexc('7a40c0'), hi=0, shadow=False)


def charr_tybalt(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    tw = math.sin(t * TAU) * .05
    for s in (-1, 1):
        c.poly([P(s * .5, -.55), P(s * (.98 + tw), -1.15), P(s * .78, -.3)], hexc('5a463c'), hexc('1a110c'), hexc('0a0504'), ow=_ow(r) * .8, hi=.4, shadow=False)
        c.poly([P(s * .55, -.4), P(s * (.55 + tw), -.95), P(s * .22, -.55)], hexc('ff9a3c'), hexc('c4570c'), hexc('401a04'), ow=_ow(r) * .7, hi=.3, shadow=False)
    c.poly([P(-.85, -.2), P(-.5, -.62), P(.5, -.62), P(.85, -.2), P(.7, .6), P(.3, .95), P(-.3, .95), P(-.7, .6)], hexc('ffb257'), hexc('c4570c'), hexc('401a04'), ow=_ow(r), hi=.55)
    c.rr(*P(-.62, -.5), *P(.62, -.28), r * .1, hexc('6a5040'), hexc('2a1c14'), hexc('0a0504'), ow=_ow(r) * .5, hi=.3, shadow=False)
    for ex in (-.3, .3):
        c.ell(*P(ex, -.39), r * .15, r * .15, hexc('d9f6ff'), hexc('5a9fd0'), hexc('0a1a2a'), ow=_ow(r) * .4, hi=.5, shadow=False)
    for ex in (-.3, .3):
        c.ell(*P(ex, -.02), r * .13, r * .09, hexc('fff2a0'), hexc('f0b800'), hexc('2a1400'), ow=_ow(r) * .4, hi=0, shadow=False)
        c.paint(c.m_rrect(*P(ex - .025, -.09), *P(ex + .025, .05), 0), hexc('120a05'))
    c.poly([P(-.16, .2), P(.16, .2), P(0, .36)], hexc('ff9a9a'), hexc('c04a50'), hexc('3a0a10'), ow=_ow(r) * .4, hi=0, shadow=False)
    c.stroke([P(.42, -.1), P(.6, .35)], r * .06, hexc('7a2a10'), alpha=.9)
    c.stroke([P(-.15, .5), P(0, .4), P(.15, .5)], r * .06, hexc('401a04'))


def sylvari_canach(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    for s in (-1, 1):
        c.poly([P(s * .15, -.2), P(s * 1.0, .95), P(s * .85, 1.05), P(s * .05, .05)], hexc('f4f7ff'), hexc('8a9ab5'), hexc('141a28'), ow=_ow(r) * .6, hi=.5, shadow=False)
    hood = [P(0, -1.12), P(.75, -.5), P(.82, .35), P(.5, .85), P(-.5, .85), P(-.82, .35), P(-.75, -.5)]
    c.poly(hood, hexc('4db36a'), hexc('0f4a2a'), hexc('04170c'), ow=_ow(r), hi=.55)
    for ux, vy, w in ((-.55, -.35, -1), (.55, -.35, 1), (0, -.85, 0)):
        c.poly([P(ux, vy), P(ux + w * .25, vy - .3), P(ux + w * .05, vy + .15)], hexc('9cf0a8'), hexc('2f9a50'), None, hi=0, shadow=False)
    c.ell(*P(0, .22), r * .5, r * .5, hexc('0b2418'), hexc('02100a'), None, hi=0, shadow=False)
    c.ell(*P(0, .26), r * .38, r * .38, hexc('d8ffd4'), hexc('7fd68a'), None, hi=.3, shadow=False, mode='r')
    b = .7 + .3 * tri(t)
    for ex in (-.16, .16):
        c.glow(*P(ex, .2), r * .22, hexc('9affb0'), b)
        c.paint(c.m_ellipse(*P(ex, .2), r * .07), hexc('0e3a1c'))
    c.paint(c.m_poly([P(-.35, .55), P(.35, .55), P(0, .85)]), hexc('0f4a2a'))


def lich_joko(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, hexc('43ff9a'), .3 + .2 * tri(t))
    neme = [P(-.55, -.9), P(.55, -.9), P(.98, .85), P(.52, .95), P(.52, .1), P(-.52, .1), P(-.52, .95), P(-.98, .85)]
    c.poly(neme, hexc('ffe27a'), hexc('b07a14'), hexc('3a2005'), ow=_ow(r), hi=.6)
    for i in range(4):
        y = -.55 + i * .28
        c.stroke([P(-.56 + i * .02, y), P(-.7 - i * .06, y + .2)], r * .08, hexc('2a5fc8'))
        c.stroke([P(.56 - i * .02, y), P(.7 + i * .06, y + .2)], r * .08, hexc('2a5fc8'))
    c.ell(*P(0, -.05), r * .52, r * .62, hexc('f4efe0'), hexc('b8ad94'), hexc('2c261c'), ow=_ow(r) * .8, mode='r', hi=.5, shadow=False)
    f = .7 + .3 * tri(t)
    for ex in (-.2, .2):
        c.ell(*P(ex, -.1), r * .14, r * .17, hexc('0a1a10'), hexc('02080a'), None, hi=0, shadow=False)
        c.glow(*P(ex, -.1), r * .2, hexc('43ff9a'), f)
        c.paint(c.m_ellipse(*P(ex, -.1), r * .06), hexc('d8ffe8'))
    c.poly([P(0, .08), P(.07, .24), P(-.07, .24)], hexc('1a1a14'), hexc('1a1a14'), hi=0, shadow=False)
    for ux in (-.18, -.06, .06, .18):
        c.paint(c.m_rrect(*P(ux - .03, .34), *P(ux + .03, .5), 0), hexc('3a3328'))
    c.poly([P(-.5, -.92), P(0, -1.2), P(.5, -.92), P(0, -.78)], hexc('ffe27a'), hexc('d19a1a'), hexc('3a2005'), ow=_ow(r) * .6, hi=.5, shadow=False)
    c.ell(*P(0, -.98), r * .09, r * .09, hexc('9affc4'), hexc('1f9a5a'), hexc('04170c'), ow=_ow(r) * .3, hi=.6, shadow=False)


# ------------------------------------------------------------- Pokemon-ish
def monsterball(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    base = c.m_ellipse(cx, cy, r)
    c.shape(base, hexc('ff7a6a'), hexc('a80f1c'), hexc('1a0a12'), ow=_ow(r), mode='r', hi=.6)
    lower = ImageChops.multiply(base, c.m_rrect(*P(-1.2, .0), *P(1.2, 1.2), 0))
    c.paint_grad(lower, hexc('ffffff'), hexc('b5bfd6'), mode='r')
    c.paint(ImageChops.multiply(base, c.m_rrect(*P(-1.2, -.12), *P(1.2, .12), 0)), hexc('1a0a12'))
    c.ell(cx, cy, r * .34, r * .34, hexc('ffffff'), hexc('c9d2e6'), hexc('1a0a12'), ow=_ow(r) * .9, mode='r', hi=.5, shadow=False)
    c.paint(c.m_ellipse(cx, cy, r * .16), hexc('ffffff'), .4 + .6 * tri(t))
    c.glow(cx, cy, r * .3, hexc('ff5a5a'), .6 * tri(t))
    c.paint(c.m_ellipse(*P(-.45, -.5), r * .22, r * .12), (255, 255, 255, 255), .7)


def ghostling(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    bob = math.sin(t * TAU) * .06
    for i, (ux, ph) in enumerate(((-.8, 0), (.85, .5))):
        u = (t + ph) % 1
        c.glow(*P(ux, .5 - u * 1.2), r * .26, hexc('b06bff'), .7 * (1 - u))
    body = [P(-.78, .0 + bob), P(-.55, -.7 + bob), P(0, -.98 + bob), P(.55, -.7 + bob), P(.78, 0 + bob),
            P(.78, .9 + bob), P(.52, .72 + bob), P(.26, .96 + bob), P(0, .74 + bob), P(-.26, .96 + bob), P(-.52, .72 + bob), P(-.78, .9 + bob)]
    c.poly(body, hexc('ffffff'), hexc('b9a2ea'), hexc('2a124f'), ow=_ow(r), mode='r', hi=.7)
    for ex in (-.3, .3):
        c.ell(*P(ex, -.12 + bob), r * .15, r * .21, hexc('2a124f'), hexc('0e0420'), None, hi=0, shadow=False)
        c.paint(c.m_ellipse(*P(ex - .04, -.2 + bob), r * .05), (255, 255, 255, 255))
    c.poly([P(-.14, .22 + bob), P(.14, .22 + bob), P(.1, .6 + bob + .05 * tri(t)), P(-.1, .6 + bob + .05 * tri(t))],
           hexc('ff7aa8'), hexc('d93a78'), hexc('4a0a2a'), ow=_ow(r) * .4, hi=.4, shadow=False)
    c.paint(c.m_ellipse(*P(-.52, .15 + bob), r * .12, r * .08), hexc('ff9ac0'), .6)
    c.paint(c.m_ellipse(*P(.52, .15 + bob), r * .12, r * .08), hexc('ff9ac0'), .6)


# -------------------------------------------------------------- Simpsons
def donut(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    dough = ImageChops.subtract(c.m_ellipse(cx, cy, r, r * .85), c.m_ellipse(cx, cy - r * .02, r * .26, r * .22))
    c.shape(dough, hexc('f6c17a'), hexc('b86a22'), hexc('4a2208'), ow=_ow(r), hi=.4)
    icing = ImageChops.subtract(c.m_ellipse(cx, cy - r * .1, r * .9, r * .72), c.m_ellipse(cx, cy - r * .08, r * .3, r * .24))
    c.shape(icing, hexc('ff9ad0'), hexc('e0408e'), hexc('7a1450'), ow=_ow(r) * .5, mode='r', hi=.65, shadow=False)
    cols = [hexc('ffe14a'), hexc('4ac8ff'), hexc('ffffff'), hexc('7aff6a'), hexc('ff5a5a'), hexc('ffffff')]
    spots = [(-.6, -.2, 20), (-.2, -.5, -30), (.35, -.5, 40), (.65, -.15, -15), (.55, .22, 55), (-.1, .38, 10),
             (-.5, .22, -50), (.15, -.2, 70), (.25, .28, -35), (-.28, -.15, 35)]
    for i, (ux, vy, ang) in enumerate(spots):
        a = math.radians(ang)
        d = (math.cos(a) * r * .11, math.sin(a) * r * .11)
        x, y = P(ux, vy)
        c.stroke([(x - d[0], y - d[1]), (x + d[0], y + d[1])], r * .1, cols[i % 6], outline=hexc('5a1040'), ow=.25)
    x = -1.0 + 2.0 * t
    band = c.m_line([P(x - .3, -1), P(x + .2, 1)], r * .18)
    c.paint(ImageChops.multiply(band, icing), (255, 255, 255, 255), .4)


def nuclear(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    pulse = .5 + .5 * tri(t)
    c.glow(cx, cy, r * 1.25, hexc('5aff3a'), .35 + .35 * pulse)
    c.ell(cx, cy, r, r, hexc('fff56a'), hexc('d6a800'), hexc('1a1a08'), ow=_ow(r), mode='r', hi=.5)
    sect = c._m()
    from PIL import ImageDraw
    d = ImageDraw.Draw(sect)
    rot0 = t * 360 * 0  # keep upright; glow animates instead
    for k in range(3):
        a0 = -90 - 30 + k * 120 + rot0
        d.pieslice([(cx - r * .8) * K, (cy - r * .8) * K, (cx + r * .8) * K, (cy + r * .8) * K], a0 + 0, a0 + 60, fill=255)
    sect = ImageChops.subtract(sect, c.m_ellipse(cx, cy, r * .22))
    c.paint(sect, hexc('15180a'))
    c.paint(c.m_ellipse(cx, cy, r * .13), hexc('15180a'))
    c.paint(c.m_ellipse(*P(-.45, -.55), r * .18, r * .1), (255, 255, 255, 255), .6)
    c.sparkle(*P(.7, -.7), r * .35, hexc('b6ff6a'), .3 + .7 * tri((t * 2) % 1))


# ------------------------------------------------------------------ Cute
def friend(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    sway = math.sin(t * TAU) * .05
    for s in (-1, 1):
        c.ell(*P(s * .45, -.78 + (sway if s > 0 else -sway)), r * .22, r * .5, hexc('ffffff'), hexc('f3dce6'), hexc('6a3a58'), ow=_ow(r) * .8, hi=.4, shadow=False)
        c.ell(*P(s * .45, -.74), r * .09, r * .3, hexc('ffc4dc'), hexc('ff9ac0'), None, hi=0, shadow=False)
    c.ell(*P(0, .12), r * .95, r * .82, hexc('ffffff'), hexc('f3dce6'), hexc('6a3a58'), ow=_ow(r), mode='r', hi=.6)
    blink = 1.0 if not (0.82 < t < 0.92) else 0.15
    for ex in (-.4, .4):
        c.ell(*P(ex, .06), r * .1, r * .11 * blink, hexc('3a1f3a'), hexc('1a0a1a'), None, hi=0, shadow=False)
    c.ell(*P(0, .26), r * .09, r * .06, hexc('ffb84a'), hexc('f08a1a'), hexc('6a3a05'), ow=_ow(r) * .3, hi=0, shadow=False)
    for ex in (-.62, .62):
        c.paint(c.m_ellipse(*P(ex, .3), r * .15, r * .1), hexc('ffa0c4'), .65)
    bow = [P(.28, -.52), P(.75, -.8), P(.75, -.2)]
    c.poly(bow, hexc('ff8ab8'), hexc('e0407e'), hexc('6a1040'), ow=_ow(r) * .6, hi=.5, shadow=False)
    c.poly([P(.28, -.52), P(-.1, -.8), P(-.1, -.2)], hexc('ff8ab8'), hexc('e0407e'), hexc('6a1040'), ow=_ow(r) * .6, hi=.5, shadow=False)
    c.ell(*P(.28, -.52), r * .14, r * .14, hexc('ffd0e4'), hexc('ff6aa4'), hexc('6a1040'), ow=_ow(r) * .4, hi=.5, shadow=False)


def strawberry(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    body = c.union(c.m_ellipse(*P(0, -.15), r * .95, r * .8),
                   c.m_poly([P(-.9, .0), P(.9, .0), P(.45, .85), P(0, 1.1), P(-.45, .85)]))
    c.shape(body, hexc('ff6a7a'), hexc('c4143a'), hexc('4a0414'), ow=_ow(r), mode='r', hi=.6)
    for (ux, vy) in ((-.5, -.3), (0, -.4), (.5, -.3), (-.25, .05), (.25, .05), (-.5, .22), (0, .35), (.5, .22), (-.15, .62), (.2, .62)):
        c.poly([P(ux, vy - .08), P(ux + .05, vy + .03), P(ux - .05, vy + .03)], hexc('fff2a0'), hexc('e0b020'), None, hi=0, shadow=False)
    sw = math.sin(t * TAU) * 6
    for ang in (-60, -20, 20, 60):
        a = math.radians(ang + sw * .4 - 90)
        base = P(0, -.82)
        tip = (base[0] + math.cos(a) * r * .75, base[1] + math.sin(a) * r * .75)
        n = (-math.sin(a) * r * .17, math.cos(a) * r * .17)
        c.poly([(base[0] + n[0], base[1] + n[1]), tip, (base[0] - n[0], base[1] - n[1])], hexc('9af07a'), hexc('2a9a3a'), hexc('0a3a14'), ow=_ow(r) * .6, hi=.4, shadow=False)
    c.paint(c.m_ellipse(*P(-.45, -.4), r * .2, r * .11), (255, 255, 255, 255), .75)
    c.sparkle(*P(.72, -.6), r * .38, hexc('ffffff'), .4 + .6 * tri((t * 2) % 1))


def pawprint(c, cx, cy, r, t, p):
    P = _pt(cx, cy, r)
    c.glow(cx, cy, r * 1.1, hexc('ff8a1a'), .25 + .3 * tri(t))
    pad = [hexc('c58cff'), hexc('6a2ab8')]
    c.ell(*P(0, .38), r * .62, r * .52, hexc('4a4a60'), hexc('15151f'), hexc('06060c'), ow=_ow(r), mode='r', hi=.5)
    c.ell(*P(0, .42), r * .36, r * .28, pad[0], pad[1], None, hi=.4, shadow=False)
    for ux, vy, rx, ry in ((-.78, -.1, .22, .3), (-.28, -.62, .22, .3), (.28, -.62, .22, .3), (.78, -.1, .22, .3)):
        c.ell(*P(ux, vy), r * rx, r * ry, hexc('4a4a60'), hexc('15151f'), hexc('06060c'), ow=_ow(r) * .9, mode='r', hi=.45, shadow=False)
        c.ell(*P(ux, vy + .02), r * rx * .55, r * ry * .55, pad[0], pad[1], None, hi=.3, shadow=False)
    c.sparkle(*P(.85, -.75), r * .34, hexc('ffb14a'), .4 + .6 * tri((t * 2) % 1))


EMBLEMS = {f.__name__: f for f in (
    crystal, chocobo, voidmoon, stormwind, orgrimmar, frostbound, monsterblood, lawngnome,
    golem_blish, asura_taimi, charr_tybalt, sylvari_canach, lich_joko,
    monsterball, ghostling, donut, nuclear, friend, strawberry, pawprint)}
