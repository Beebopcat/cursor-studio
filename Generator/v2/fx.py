"""Animation effects drawn over a pointer object. All periodic in t."""
import math
import numpy as np
from PIL import ImageChops
from toolkit import K, tri, lighten, mix
from materials import both, blur

_R = np.random.RandomState(11).rand(10, 4).tolist()


def _box(U):
    bb = U.getbbox()
    if not bb:
        return 2, 2, 26, 26
    return [v / K for v in bb]


def shimmer(c, st, U, t, width=3.0, alpha=.4, hard=False):
    x = -6 + 44 * t
    band = c.m_line([(x - 8, 0), (x + 8, 32)], width, False)
    c.paint(both(band, U), (255, 255, 255, 255), alpha)


def run(c, st, t, U, spinner_free=True):
    fx = st.fx
    p = st.p
    x0, y0, x1, y1 = _box(U)
    if fx in ('glint', 'rays'):
        if st.material not in ('neon',):
            shimmer(c, st, U, t, 3.0 if fx == 'glint' else 2.2, .42 if st.material != 'flat' else .55)
        return
    n = 5
    for i in range(n):
        a, b, ph, sz = _R[i]
        u = (t + ph) % 1
        bx = x0 + (x1 - x0) * a
        by = y0 + (y1 - y0) * b
        if fx == 'motes':
            x, y, r = bx + u * 3, by - u * 4, 1.5 * math.sin(math.pi * u)
            c.sparkle(x, y, r + .01, lighten(p['glow'], .45))
        elif fx == 'embers':
            x, y, r = bx + math.sin(u * 6 + i) * 1.2, by - u * 7, 1.0 * (1 - u) + .15
            c.paint(c.m_ellipse(x, y, r), mix(p['ac2'], p['ac'], u), .95)
            c.glow(x, y, r * 3, p['ac'], .4 * (1 - u))
        elif fx == 'snow':
            x, y, r = bx - u * 3 + math.sin(u * 5 + i), by + u * 5 - 2, .8 + .35 * (i % 2)
            c.paint(c.m_ellipse(x, y, r), (255, 255, 255, 255), .95 * math.sin(math.pi * u))
        elif fx == 'bubbles':
            x, y, r = bx + math.sin(u * 5 + i) * 1.1, by - u * 6, .7 + .65 * u
            c.ell(x, y, r, r, lighten(p['c1'], .7), p['c1'], p['ol'], ow=.3, hi=.7, shadow=False) if u < .95 else None
        elif fx == 'wisps':
            x, y, r = bx + math.sin(u * 4 + i) * 1.6, by - u * 7, .9 + 1.4 * u
            c.glow(x, y, r * 2.2, p['glow'], .85 * (1 - u))
        elif fx == 'drips':
            x, y = x0 + 3 + i * 3.4, y1 - 2 + u * 3
            c.paint(c.m_ellipse(x, y, .8, 1.1 + u * .4), p['c1'], .9 * (1 - u))
        elif fx == 'eyes':
            if i < 2:
                gl = tri((t * 2 + i * .4) % 1)
                c.glow(x0 + (x1 - x0) * (.35 + .3 * i), y0 + (y1 - y0) * .35, 2.0, p['glow'], .5 * gl)
