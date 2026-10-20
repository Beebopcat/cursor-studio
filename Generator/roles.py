"""The 17 Windows pointer roles. Every role is drawn from a SetStyle + animation phase t."""
import math
from PIL import ImageChops, ImageFilter
from toolkit import *
from emblems import EMBLEMS

# Registry value name -> (friendly name, hotspot in 32-unit space)
ROLES = [
    ('Arrow',       'Normal Select',       (2, 2)),
    ('Help',        'Help Select',         (2, 2)),
    ('AppStarting', 'Working In Background', (2, 2)),
    ('Wait',        'Busy',                (16, 16)),
    ('Crosshair',   'Precision Select',    (16, 16)),
    ('IBeam',       'Text Select',         (16, 16)),
    ('NWPen',       'Handwriting',         (3, 29)),
    ('No',          'Unavailable',         (16, 16)),
    ('SizeNS',      'Vertical Resize',     (16, 16)),
    ('SizeWE',      'Horizontal Resize',   (16, 16)),
    ('SizeNWSE',    'Diagonal Resize 1',   (16, 16)),
    ('SizeNESW',    'Diagonal Resize 2',   (16, 16)),
    ('SizeAll',     'Move',                (16, 16)),
    ('UpArrow',     'Alternate Select',    (16, 2)),
    ('Hand',        'Link Select',         (11, 2)),
    ('Pin',         'Location Select',     (16, 29)),
    ('Person',      'Person Select',       (2, 2)),
]
FILE_NAMES = {k: f'{i + 1:02d}-{n.replace(" ", "")}' for i, (k, n, _) in enumerate(ROLES)}

POINTERS = {
    'classic': [(2, 2), (2, 24.5), (7.6, 19.2), (11.4, 28), (15.2, 26.4), (11.4, 17.8), (18.6, 17.6)],
    'sleek':   [(2, 2), (4, 25.5), (8.4, 19.2), (11.2, 27.5), (14, 26.2), (10.8, 18.2), (17.5, 16.6)],
    'shard':   [(2, 2), (2.6, 23), (7.2, 17.6), (10.2, 28), (13.8, 26.4), (10.6, 16.4), (17.8, 15.2)],
    'blunt':   [(2, 2), (2, 25), (8, 20.4), (11.6, 27.6), (15.6, 25.8), (12, 19.2), (19, 18.6)],
    'wing':    [(2, 2), (2, 24), (6.6, 20.6), (9.4, 27.2), (14, 25.6), (11.2, 18.8), (18, 17.4)],
}


class Style:
    """Per-set look: palette, pointer variant, emblem selection per role."""

    def __init__(self, pal, pointer, emblem, rounded=0, emblem_by_role=None, plate=True, bars='gem'):
        self.p = pal
        self.pointer = pointer
        self.emblem = emblem
        self.rounded = rounded
        self.ebr = emblem_by_role or {}
        self.plate = plate

    def em(self, role):
        return EMBLEMS[self.ebr.get(role, self.emblem)]


def _round(c, m, px):
    if not px:
        return m
    px = int(min(px, 0.75) * K)
    k = px * 2 + 1
    return m.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))


def _shimmer(c, mask, t, ang=1.0, width=3.2, alpha=.38, span=(-6, 38)):
    x = span[0] + (span[1] - span[0]) * t
    band = c.m_line([(x - 8 * ang, 0), (x + 8 * ang, 32)], width)
    c.paint(ImageChops.multiply(band, mask), (255, 255, 255, 255), alpha)


def pointer(c, st, t):
    p = st.p
    pts = POINTERS[st.pointer]
    m = _round(c, c.m_poly(pts), st.rounded)
    c.shape(m, p['pt'], p['pb'], p['ol'], ow=1.0, mode='d', hi=.65, shade=.25, halo=p['halo'])
    # inset bevel panel
    cx = sum(x for x, _ in pts) / len(pts)
    cy = sum(y for _, y in pts) / len(pts)
    inner = [(cx + (x - cx) * .56, cy + (y - cy) * .56 + 0.4) for x, y in pts]
    im = ImageChops.multiply(_round(c, c.m_poly(inner), st.rounded * .5), m)
    c.paint_grad(im, darken(p['pb'], .1), lighten(p['pb'], .25), mode='v', alpha=.55)
    # accent trim along the leading edge
    edge = c.m_line([(pts[0][0] + .2, pts[0][1] + 1.2), (pts[1][0] + .2, pts[1][1] - 1.0)], .9)
    c.paint(ImageChops.multiply(edge, m), p['acc'], .95)
    _shimmer(c, m, t)
    return m


def plate(c, st, cx, cy, r):
    p = st.p
    c.ell(cx, cy, r, r, lighten(p['plate'], .15), darken(p['plate'], .2), p['ol'], ow=.8, mode='r', hi=.4)
    c.paint(c.m_arc(cx, cy, r - .45, 0, 360, .5), p['acc'], .9)


def charm(c, st, role, t, cx, cy, r):
    if st.plate:
        plate(c, st, cx, cy, r + 1.0)
    st.em(role)(c, cx, cy, r, t, st.p)


def spinner(c, st, cx, cy, r, t, n=8, dot=.85):
    head = t * n
    for i in range(n):
        a = math.radians(i * 360 / n - 90)
        f = ((head - i) % n) / n  # 0 = head, ->1 trailing
        s = dot * (1.0 - .55 * f)
        col = mix(st.p['acc2'], st.p['acc'], f)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        c.ell(x, y, s, s, lighten(col, .35), col, st.p['ol'], ow=.35, hi=.3, shadow=False) if f < .75 else \
            c.paint(c.m_ellipse(x, y, s * .8), with_alpha(col, 255), .45)


def qmark(c, cx, cy, s, col):
    c.paint(c.m_arc(cx, cy - 1.4 * s, 1.9 * s, 180, 450, 1.15 * s), col)
    c.paint(c.m_line([(cx, cy + .5 * s), (cx, cy + 1.2 * s)], 1.15 * s, False), col)
    c.paint(c.m_ellipse(cx, cy + 2.7 * s, .72 * s), col)


# ------------------------------------------------------------- role painters
def r_Arrow(c, st, t):
    pointer(c, st, t)
    charm(c, st, 'Arrow', t, 23.6, 23.6, 4.5)


def r_Help(c, st, t):
    pointer(c, st, t)
    p = st.p
    b = 1 + .06 * math.sin(t * 2 * math.pi)
    c.ell(23.8, 23.4, 5.7 * b, 5.7 * b, lighten(p['acc'], .35), darken(p['acc'], .25), p['ol'], ow=.8, mode='r', hi=.6)
    qmark(c, 23.8, 23.4, 1.05, hexc('ffffff'))
    c.sparkle(28.8, 17.6, 2.2, lighten(p['acc2'], .3), .4 + .6 * tri(t))


def r_AppStarting(c, st, t):
    pointer(c, st, t)
    c.ell(23.8, 23.8, 6.4, 6.4, lighten(st.p['plate'], .1), darken(st.p['plate'], .35), st.p['ol'], ow=.7, mode='r', hi=.35)
    spinner(c, st, 23.8, 23.8, 3.9, t, 8, .95)


def r_Wait(c, st, t):
    s = 1 + .035 * math.sin(t * 2 * math.pi)
    c.glow(16, 16, 12, st.p['glow'], .22)
    spinner(c, st, 16, 16, 13.4, t, 12, 1.15)
    st.em('Wait')(c, 16, 16, 9.2 * s, t, st.p)


def r_Crosshair(c, st, t):
    p = st.p
    for (x0, y0, x1, y1) in ((16, 1.5, 16, 10), (16, 22, 16, 30.5), (1.5, 16, 10, 16), (22, 16, 30.5, 16)):
        c.stroke([(x0, y0), (x1, y1)], 1.5, lighten(p['acc'], .4), outline=p['ol'], ow=.65)
    for i in range(4):
        a0 = t * 360 / 2 + i * 90 + 8
        c.paint(c.m_arc(16, 16, 7.4, a0, a0 + 58, 1.35), p['ol'])
        c.paint(c.m_arc(16, 16, 7.4, a0, a0 + 58, .85), mix(p['acc2'], (255, 255, 255, 255), .45))
    pulse = .8 + .5 * tri(t)
    c.ell(16, 16, 1.5 * pulse, 1.5 * pulse, hexc('ffffff'), p['acc'], p['ol'], ow=.6, hi=0, shadow=False)
    st.em('Crosshair')(c, 26.2, 26.2, 3.9, t, p)


def r_IBeam(c, st, t):
    p = st.p
    g = .35 + .4 * tri(t)
    c.glow(16, 16, 10, p['glow'], g * .5)
    beam = c.union(c.m_rrect(14.5, 5.2, 17.5, 26.8, 1.0), c.m_rrect(10.8, 3.2, 21.2, 6.0, 1.2), c.m_rrect(10.8, 26.0, 21.2, 28.8, 1.2))
    c.shape(beam, lighten(p['pt'], .1), p['pb'], p['ol'], ow=.85, mode='v', hi=.7, halo=p['halo'])
    c.paint(c.m_rrect(15.3, 7.0, 16.7, 25.0, .6), p['acc'], .85)
    _shimmer(c, beam, t, 0.6, 3.0, .45)
    st.em('IBeam')(c, 25.4, 9.0, 3.6, t, p)


def r_NWPen(c, st, t):
    p = st.p
    ca, sa = math.cos(math.radians(-45)), math.sin(math.radians(-45))

    def T(pts):
        return [(3.8 + x * ca - y * sa, 28.4 + x * sa + y * ca) for x, y in pts]
    body = c.m_poly(T([(5, -1.9), (25, -1.9), (25, 1.9), (5, 1.9)]))
    nib = c.m_poly(T([(0, 0), (5.6, -1.8), (5.6, 1.8)]))
    c.paint(c.union(body, nib).filter(ImageFilter.GaussianBlur(0)), (0, 0, 0, 0))
    c.shape(c.union(body, nib), p['pt'], p['pb'], p['ol'], ow=.9, mode='v', hi=.6, halo=p['halo'])
    c.paint(ImageChops.multiply(nib, nib), lighten(p['acc'], .1), .0)
    c.shape(nib, hexc('fff2c4'), hexc('c9a24a'), p['ol'], ow=.7, mode='v', hi=.5, shadow=False)
    c.shape(c.m_poly(T([(14, -1.9), (17, -1.9), (17, 1.9), (14, 1.9)])), p['acc'], darken(p['acc'], .25), None, hi=0, shadow=False)
    ex, ey = T([(29.5, 0)])[0]
    c.paint(c.m_line(T([(7, -.2), (25, -.2)]), .7), lighten(p['pt'], .5), .6)
    st.em('NWPen')(c, ex, ey, 4.2, t, p)
    ink = .6 + .4 * tri(t)
    c.glow(3.6, 28.6, 2.6, p['acc'], ink)
    _shimmer(c, body, t, 1.0, 2.2, .35, (-4, 36))


def r_No(c, st, t):
    p = st.p
    s = 1 + .03 * math.sin(t * 2 * math.pi)
    bad = p['bad']
    c.glow(16, 16, 13, bad, .22)
    c.paint(c.m_ellipse(16, 16, 9.6), p['plate'], .85)
    ring = ImageChops.subtract(c.m_ellipse(16, 16, 12.6 * s), c.m_ellipse(16, 16, 9.4 * s))
    slash = c.m_line([(8.3, 8.3), (23.7, 23.7)], 3.0)
    c.shape(c.union(ring, slash), lighten(bad, .35), darken(bad, .3), p['ol'], ow=.9, mode='d', hi=.7, halo=p['halo'])
    sub = Canvas()
    st.em('No')(sub, 16, 16, 5.8, t, p)
    a = sub.img.copy()
    a.putalpha(a.getchannel('A').point(lambda v: int(v * .72)))
    c.img.alpha_composite(a)
    c.shape(slash, lighten(bad, .35), darken(bad, .3), p['ol'], ow=.9, mode='d', hi=.7, shadow=False)


def _dbl_arrow(c, ang, L=14.6, head=6.2, sh=2.1):
    pts = [(-L, 0), (-L + head + .6, -head), (-L + head + .6, -sh), (L - head - .6, -sh), (L - head - .6, -head), (L, 0),
           (L - head - .6, head), (L - head - .6, sh), (-L + head + .6, sh), (-L + head + .6, head)]
    return [(16 + x * math.cos(math.radians(ang)) - y * math.sin(math.radians(ang)),
             16 + x * math.sin(math.radians(ang)) + y * math.cos(math.radians(ang))) for x, y in pts]


def _resize(c, st, role, ang, t):
    p = st.p
    L = 14.6 if ang in (0, 90) else 14.2
    m = c.m_poly(_dbl_arrow(c, ang, L))
    c.shape(m, p['pt'], p['pb'], p['ol'], ow=.95, mode='v' if ang in (0, 90) else 'd', hi=.7, shade=.2, halo=p['halo'])
    _shimmer(c, m, t, 1.0, 3.0, .42, (-6, 38))
    e = c.m_line([(16 - math.cos(math.radians(ang)) * 7, 16 - math.sin(math.radians(ang)) * 7),
                  (16 + math.cos(math.radians(ang)) * 7, 16 + math.sin(math.radians(ang)) * 7)], .9)
    c.paint(ImageChops.multiply(e, m), p['acc'], .0)
    st.em(role)(c, 16, 16, 3.9 + .15 * math.sin(t * 6.283), t, p)


def r_SizeNS(c, st, t): _resize(c, st, 'SizeNS', 90, t)
def r_SizeWE(c, st, t): _resize(c, st, 'SizeWE', 0, t)
def r_SizeNWSE(c, st, t): _resize(c, st, 'SizeNWSE', 45, t)
def r_SizeNESW(c, st, t): _resize(c, st, 'SizeNESW', -45, t)


def r_SizeAll(c, st, t):
    p = st.p
    m = c.union(c.m_poly(_dbl_arrow(c, 0, 14.6, 5.6, 2.0)), c.m_poly(_dbl_arrow(c, 90, 14.6, 5.6, 2.0)))
    c.shape(m, p['pt'], p['pb'], p['ol'], ow=.95, mode='d', hi=.7, shade=.2, halo=p['halo'])
    _shimmer(c, m, t, 1.0, 3.0, .4, (-6, 38))
    c.ell(16, 16, 5.2, 5.2, lighten(p['plate'], .1), darken(p['plate'], .25), p['ol'], ow=.7, mode='r', hi=.4, shadow=False)
    st.em('SizeAll')(c, 16, 16, 4.1, t, p)


def r_UpArrow(c, st, t):
    p = st.p
    m = c.m_poly([(16, 1.2), (26.2, 12.4), (19.8, 12.4), (19.8, 29), (12.2, 29), (12.2, 12.4), (5.8, 12.4)])
    m = _round(c, m, st.rounded * .6)
    c.shape(m, p['pt'], p['pb'], p['ol'], ow=1.0, mode='v', hi=.7, shade=.2, halo=p['halo'])
    _shimmer(c, m, t, 1.0, 3.2, .4, (-6, 38))
    st.em('UpArrow')(c, 16, 21.2, 3.5, t, p)


def r_Hand(c, st, t):
    p = st.p
    tap = 1.0 * math.sin(t * 2 * math.pi)
    parts = [c.m_rrect(9.3, 1.8 + tap * .4, 14.5, 17.5, 2.6),
             c.m_rrect(5.2, 14, 25.8, 27, 5),
             c.m_rrect(14.2, 11.6, 17.8, 19.5, 1.8), c.m_rrect(17.4, 12.6, 21, 20, 1.8), c.m_rrect(20.6, 13.8, 24.2, 21, 1.8),
             c.m_ellipse(5.6, 19.4, 3.4, 2.6)]
    m = c.union(*parts)
    c.shape(m, lighten(p['pt'], .1), p['pb'], p['ol'], ow=1.0, mode='v', hi=.7, shade=.25, halo=p['halo'])
    for x in (17.8, 21.0):
        c.stroke([(x, 14.2), (x, 19.0)], .5, darken(p['pb'], .4), alpha=.8)
    c.stroke([(14.5, 12.5), (14.5, 18)], .5, darken(p['pb'], .4), alpha=.8)
    c.paint(c.m_rrect(5.8, 24.0, 25.2, 27.4, 1.4), p['acc'], .95)
    c.paint(ImageChops.multiply(c.m_rrect(5.8, 24.0, 25.2, 25.0, 0), m), (255, 255, 255, 255), .35)
    _shimmer(c, m, t, 1.0, 3.2, .4, (-6, 38))
    st.em('Hand')(c, 15.6, 21.0, 3.5, t, p)
    c.sparkle(11.9, 1.8 + tap * .4, 2.4, lighten(p['acc2'], .35), .35 + .65 * tri(t))


def r_Pin(c, st, t):
    p = st.p
    ripple = (t % 1)
    for k in (0, .5):
        u = (ripple + k) % 1
        c.paint(c.m_arc(16, 28.6, 2 + u * 7, 0, 360, .6), p['acc'], 1 - u) if False else None
        ring = ImageChops.subtract(c.m_ellipse(16, 28.8, 2 + u * 8, .8 + u * 2.2), c.m_ellipse(16, 28.8, 1.5 + u * 8, .5 + u * 2.2))
        c.paint(ring, p['acc'], .9 * (1 - u))
    m = c.union(c.m_ellipse(16, 12, 9.8), c.m_poly([(7.0, 15.6), (16, 29.2), (25.0, 15.6)]))
    c.shape(m, p['pt'], p['pb'], p['ol'], ow=1.0, mode='r', hi=.7, shade=.25, halo=p['halo'])
    c.ell(16, 12, 6.4, 6.4, lighten(p['plate'], .1), darken(p['plate'], .3), p['ol'], ow=.7, mode='r', hi=.3, shadow=False)
    st.em('Pin')(c, 16, 12, 4.9, t, p)
    _shimmer(c, m, t, 1.0, 3.0, .35, (-6, 38))


def r_Person(c, st, t):
    pointer(c, st, t)
    p = st.p
    c.ell(23.8, 23.6, 6.2, 6.2, lighten(p['acc'], .3), darken(p['acc'], .3), p['ol'], ow=.8, mode='r', hi=.55)
    b = .35 * math.sin(t * 2 * math.pi)
    body = ImageChops.multiply(c.union(c.m_ellipse(23.8, 28.2, 4.6, 3.8)), c.m_ellipse(23.8, 23.6, 5.9))
    c.paint(body, hexc('ffffff'))
    c.ell(23.8, 21.0 + b, 2.0, 2.0, hexc('ffffff'), hexc('e6ecf5'), None, hi=0, shadow=False)


ROLE_FUNCS = {k: globals()['r_' + k] for k, _, _ in ROLES}


def render_role(st, role, t, sizes=(32, 48, 64)):
    c = Canvas()
    ROLE_FUNCS[role](c, st, t)
    return {s: c.finish(s) for s in sizes}
