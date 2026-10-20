"""v2 roles: same 17 Windows pointer roles, but drawn through a material + pointer object + fx."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import ImageChops, ImageDraw
from toolkit import *
import emblems2  # registers extra emblems
from emblems import EMBLEMS
from roles import ROLES, FILE_NAMES
from materials import MATERIALS, either, both, sub, erode, grow, blur, pixelate
from objects import OBJECTS, round_mask
import objects3, emblems3  # extra pointer objects and emblems
import fx as FX


class Style2:
    def __init__(self, key, label, blurb, p, material, ptr='classic', emblem='crystal', fx='glint', charm=True, ebr=None):
        self.key, self.label, self.blurb, self.p = key, label, blurb, p
        self.material, self.ptr, self.emblem, self.fx, self.charm, self.ebr = material, ptr, emblem, fx, charm, ebr or {}

    def em(self, role):
        return EMBLEMS[self.ebr.get(role, self.emblem)]

    def draw(self, c, parts, t, fxmode='full'):
        mat = MATERIALS[self.material]
        U = either(*[m for m, _ in parts])
        mat.pre(c, self, U, t)
        for m, role in parts:
            mat.part(c, self, m, role, t)
        mat.post(c, self, U, t)
        if fxmode == 'full':
            FX.run(c, self, t, U)
        elif fxmode == 'shimmer' and self.material != 'neon':
            FX.shimmer(c, self, U, t, 3.0, .4)
        return U

    def line(self, c, pts, w, role='trim', ow=.65):
        top, bot = __import__('materials').role_cols(self, role)
        m = c.m_line(pts, w)
        if self.material == 'neon':
            c.paint(blur(m, .9), self.p['glow'], .85)
            c.paint(grow(m, .5), self.p['ol'], .9)
            c.paint(m, lighten(top, .5))
            return
        c.paint(grow(m, ow), self.p['ol'])
        c.paint(m, lighten(top, .25))


def plate(c, st, cx, cy, r):
    p = st.p
    parts = [(c.m_ellipse(cx, cy, r), ('plate',))]
    c.ell(cx, cy, r, r, lighten(p['plate'], .15), darken(p['plate'], .25), p['ol'], ow=.8, mode='r', hi=.35, shadow=False)
    c.paint(c.m_arc(cx, cy, r - .45, 0, 360, .5), p['ac'], .95)


def charm(c, st, role, t, cx, cy, r):
    plate(c, st, cx, cy, r + 1.0)
    st.em(role)(c, cx, cy, r, t, st.p)


def spinner(c, st, cx, cy, r, t, n=8, dot=.85):
    head = t * n
    for i in range(n):
        a = math.radians(i * 360 / n - 90)
        f = ((head - i) % n) / n
        s = dot * (1.0 - .55 * f)
        col = mix(st.p['ac2'], st.p['ac'], f)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        if f < .75:
            c.ell(x, y, s, s, lighten(col, .4), col, st.p['ol'], ow=.35, hi=.3, shadow=False)
        else:
            c.paint(c.m_ellipse(x, y, s * .8), col, .5)


def qmark(c, cx, cy, s, col):
    c.paint(c.m_arc(cx, cy - 1.4 * s, 1.9 * s, 180, 450, 1.15 * s), col)
    c.paint(c.m_line([(cx, cy + .5 * s), (cx, cy + 1.2 * s)], 1.15 * s, False), col)
    c.paint(c.m_ellipse(cx, cy + 2.7 * s, .72 * s), col)


def pointer(c, st, t):
    parts = OBJECTS[st.ptr](c, t)
    return st.draw(c, parts, t)


# ------------------------------------------------------------------ roles
def r_Arrow(c, st, t):
    pointer(c, st, t)
    if st.charm == 'flag':
        wave = math.sin(11.5 * .32 - t * 2 * math.pi) * 1.1 * (11.5 - 3.6) / 18
        st.em('Arrow')(c, 11.4, 9.9 + wave, 3.9, t, st.p)
    elif st.charm == 'mascot':
        b = .4 * math.sin(t * 2 * math.pi)
        st.em('Arrow')(c, 19.6, 19.4 + b, 9.4, t, st.p)
    elif st.charm:
        charm(c, st, 'Arrow', t, 23.6, 23.6, 4.5)


def r_Help(c, st, t):
    pointer(c, st, t)
    b = 1 + .06 * math.sin(t * 2 * math.pi)
    st.draw(c, [(c.m_ellipse(23.8, 23.4, 5.7 * b), 'trim')], t, 'none')
    qmark(c, 23.8, 23.4, 1.05, (255, 255, 255, 255))
    c.sparkle(28.8, 17.6, 2.2, lighten(st.p['ac2'], .3), .4 + .6 * tri(t))


def r_AppStarting(c, st, t):
    pointer(c, st, t)
    c.ell(23.8, 23.8, 6.4, 6.4, lighten(st.p['plate'], .1), darken(st.p['plate'], .35), st.p['ol'], ow=.7, mode='r', hi=.35)
    spinner(c, st, 23.8, 23.8, 3.9, t, 8, .95)


def r_Wait(c, st, t):
    s = 1 + .035 * math.sin(t * 2 * math.pi)
    c.glow(16, 16, 12, st.p['glow'], .2)
    spinner(c, st, 16, 16, 13.4, t, 12, 1.15)
    st.em('Wait')(c, 16, 16, 9.2 * s, t, st.p)


def r_Crosshair(c, st, t):
    for (x0, y0, x1, y1) in ((16, 1.5, 16, 10), (16, 22, 16, 30.5), (1.5, 16, 10, 16), (22, 16, 30.5, 16)):
        st.line(c, [(x0, y0), (x1, y1)], 1.5, 'trim')
    for i in range(4):
        a0 = t * 180 + i * 90 + 8
        c.paint(c.m_arc(16, 16, 7.4, a0, a0 + 58, 1.35), st.p['ol'])
        c.paint(c.m_arc(16, 16, 7.4, a0, a0 + 58, .85), lighten(st.p['ac2'], .45))
    pulse = .8 + .5 * tri(t)
    c.ell(16, 16, 1.5 * pulse, 1.5 * pulse, (255, 255, 255, 255), st.p['ac'], st.p['ol'], ow=.6, hi=0, shadow=False)
    st.em('Crosshair')(c, 26.2, 26.2, 3.9, t, st.p)


def r_IBeam(c, st, t):
    c.glow(16, 16, 10, st.p['glow'], (.35 + .4 * tri(t)) * .5)
    beam = either(c.m_rrect(14.5, 5.2, 17.5, 26.8, 1.0), c.m_rrect(10.8, 3.2, 21.2, 6.0, 1.2), c.m_rrect(10.8, 26.0, 21.2, 28.8, 1.2))
    st.draw(c, [(beam, 'body')], t, 'shimmer')
    st.em('IBeam')(c, 25.4, 9.0, 3.6, t, st.p)


def r_NWPen(c, st, t):
    ca, sa = math.cos(math.radians(-45)), math.sin(math.radians(-45))
    T = lambda pts: [(3.8 + x * ca - y * sa, 28.4 + x * sa + y * ca) for x, y in pts]
    body = c.m_poly(T([(5, -1.9), (25, -1.9), (25, 1.9), (5, 1.9)]))
    nib = c.m_poly(T([(0, 0), (5.6, -1.8), (5.6, 1.8)]))
    band = c.m_poly(T([(14, -1.9), (17, -1.9), (17, 1.9), (14, 1.9)]))
    st.draw(c, [(body, 'body'), (nib, 'white'), (band, 'trim')], t, 'shimmer')
    ex, ey = T([(29.5, 0)])[0]
    st.em('NWPen')(c, ex, ey, 4.2, t, st.p)
    c.glow(3.6, 28.6, 2.6, st.p['ac'], .6 + .4 * tri(t))


def r_No(c, st, t):
    p = st.p
    s = 1 + .03 * math.sin(t * 2 * math.pi)
    bad = p['bad']
    c.glow(16, 16, 13, bad, .2)
    c.paint(c.m_ellipse(16, 16, 9.6), p['plate'], .85)
    ring = sub(c.m_ellipse(16, 16, 12.6 * s), c.m_ellipse(16, 16, 9.4 * s))
    slash = c.m_line([(8.3, 8.3), (23.7, 23.7)], 3.0)
    cols = (lighten(bad, .35), darken(bad, .3))
    sub_c = Canvas()
    st.em('No')(sub_c, 16, 16, 5.8, t, p)
    a = sub_c.img.copy()
    a.putalpha(a.getchannel('A').point(lambda v: int(v * .72)))
    c.img.alpha_composite(a)
    st.draw(c, [(either(ring, slash), cols)], t, 'none')


def _dbl_arrow(ang, L=14.6, head=6.2, sh=2.1):
    pts = [(-L, 0), (-L + head + .6, -head), (-L + head + .6, -sh), (L - head - .6, -sh), (L - head - .6, -head), (L, 0),
           (L - head - .6, head), (L - head - .6, sh), (-L + head + .6, sh), (-L + head + .6, head)]
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return [(16 + x * ca - y * sa, 16 + x * sa + y * ca) for x, y in pts]


def _resize(c, st, role, ang, t):
    L = 14.6 if ang in (0, 90) else 14.2
    st.draw(c, [(c.m_poly(_dbl_arrow(ang, L)), 'body')], t, 'shimmer')
    st.em(role)(c, 16, 16, 3.9 + .15 * math.sin(t * 6.283), t, st.p)


def r_SizeNS(c, st, t): _resize(c, st, 'SizeNS', 90, t)
def r_SizeWE(c, st, t): _resize(c, st, 'SizeWE', 0, t)
def r_SizeNWSE(c, st, t): _resize(c, st, 'SizeNWSE', 45, t)
def r_SizeNESW(c, st, t): _resize(c, st, 'SizeNESW', -45, t)


def r_SizeAll(c, st, t):
    m = either(c.m_poly(_dbl_arrow(0, 14.6, 5.6, 2.0)), c.m_poly(_dbl_arrow(90, 14.6, 5.6, 2.0)))
    st.draw(c, [(m, 'body')], t, 'shimmer')
    c.ell(16, 16, 5.2, 5.2, lighten(st.p['plate'], .1), darken(st.p['plate'], .25), st.p['ol'], ow=.7, mode='r', hi=.4, shadow=False)
    st.em('SizeAll')(c, 16, 16, 4.1, t, st.p)


def r_UpArrow(c, st, t):
    m = c.m_poly([(16, 1.2), (26.2, 12.4), (19.8, 12.4), (19.8, 29), (12.2, 29), (12.2, 12.4), (5.8, 12.4)])
    st.draw(c, [(m, 'body')], t, 'shimmer')
    st.em('UpArrow')(c, 16, 21.2, 3.5, t, st.p)


def r_Hand(c, st, t):
    tap = math.sin(t * 2 * math.pi)
    th = [(6.2 + 3.9 * math.cos(math.radians(a)) * math.cos(.5) - 2.3 * math.sin(math.radians(a)) * math.sin(.5),
           19.6 + 3.9 * math.cos(math.radians(a)) * math.sin(.5) + 2.3 * math.sin(math.radians(a)) * math.cos(.5)) for a in range(0, 360, 15)]
    parts = [c.m_rrect(10.2, 1.8 + tap * .4, 14.4, 18, 2.1), c.m_rrect(7.4, 15.2, 25.4, 27, 4.2),
             c.m_rrect(14.0, 12.4, 17.4, 19.5, 1.7), c.m_rrect(17.2, 13.5, 20.6, 20.2, 1.7), c.m_rrect(20.4, 14.9, 23.8, 21.2, 1.7),
             c.m_poly(th)]
    cuff = c.m_rrect(7.8, 24.4, 25.0, 27.4, 1.3)
    st.draw(c, [(either(*parts), 'body'), (cuff, 'trim')], t, 'shimmer')
    for x in (17.3, 20.5):
        c.stroke([(x, 14.6), (x, 19.0)], .5, darken(st.p['c2'], .4), alpha=.8)
    st.em('Hand')(c, 15.6, 21.0, 3.5, t, st.p)
    c.sparkle(11.9, 1.8 + tap * .4, 2.4, lighten(st.p['ac2'], .35), .35 + .65 * tri(t))


def r_Pin(c, st, t):
    for k in (0, .5):
        u = (t + k) % 1
        ring = sub(c.m_ellipse(16, 28.8, 2 + u * 8, .8 + u * 2.2), c.m_ellipse(16, 28.8, 1.5 + u * 8, .5 + u * 2.2))
        c.paint(ring, st.p['ac'], .9 * (1 - u))
    m = either(c.m_ellipse(16, 12, 9.8), c.m_poly([(7.0, 15.6), (16, 29.2), (25.0, 15.6)]))
    st.draw(c, [(m, 'body')], t, 'shimmer')
    c.ell(16, 12, 6.4, 6.4, lighten(st.p['plate'], .1), darken(st.p['plate'], .3), st.p['ol'], ow=.7, mode='r', hi=.3, shadow=False)
    st.em('Pin')(c, 16, 12, 4.9, t, st.p)


def r_Person(c, st, t):
    pointer(c, st, t)
    st.draw(c, [(c.m_ellipse(23.8, 23.6, 6.2), 'trim')], t, 'none')
    b = .35 * math.sin(t * 2 * math.pi)
    body = both(c.m_ellipse(23.8, 28.2, 4.6, 3.8), c.m_ellipse(23.8, 23.6, 5.9))
    c.paint(body, (255, 255, 255, 255))
    c.ell(23.8, 21.0 + b, 2.0, 2.0, (255, 255, 255, 255), (230, 236, 245, 255), None, hi=0, shadow=False)


ROLE_FUNCS = {k: globals()['r_' + k] for k, _, _ in ROLES}


def render_role(st, role, t, sizes=(32, 64)):
    c = Canvas()
    ROLE_FUNCS[role](c, st, t)
    if st.material == 'pixel':
        return pixelate(c.img, sizes, gb=st.p.get('gb'))
    return {s: c.finish(s) for s in sizes}
