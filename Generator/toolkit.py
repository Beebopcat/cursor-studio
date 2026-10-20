"""Rendering toolkit: supersampled vector-ish drawing with gradient shading.

All drawing coordinates are in a 32x32 "cursor unit" space; the canvas renders at
8x (256px) and is downsampled to the final cursor sizes (32/48/64) with LANCZOS.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

K = 8
S = 32 * K


def hexc(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))


def lighten(c, t):
    return mix(c, (255, 255, 255, c[3]), t)


def darken(c, t):
    return mix(c, (0, 0, 0, c[3]), t)


def with_alpha(c, a):
    return (c[0], c[1], c[2], int(a))


class Canvas:
    def __init__(self):
        self.img = Image.new('RGBA', (S, S), (0, 0, 0, 0))

    # ---- masks -------------------------------------------------------
    @staticmethod
    def _m():
        return Image.new('L', (S, S), 0)

    def m_poly(self, pts):
        m = self._m()
        ImageDraw.Draw(m).polygon([(x * K, y * K) for x, y in pts], fill=255)
        return m

    def m_ellipse(self, cx, cy, rx, ry=None):
        ry = rx if ry is None else ry
        m = self._m()
        ImageDraw.Draw(m).ellipse([(cx - rx) * K, (cy - ry) * K, (cx + rx) * K, (cy + ry) * K], fill=255)
        return m

    def m_rrect(self, x0, y0, x1, y1, r):
        m = self._m()
        ImageDraw.Draw(m).rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=r * K, fill=255)
        return m

    def m_line(self, pts, w, round_ends=True):
        m = self._m()
        d = ImageDraw.Draw(m)
        p = [(x * K, y * K) for x, y in pts]
        d.line(p, fill=255, width=max(1, int(w * K)), joint='curve')
        if round_ends:
            r = w * K / 2
            for x, y in (p[0], p[-1]):
                d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        return m

    def m_arc(self, cx, cy, r, a0, a1, w):
        m = self._m()
        ImageDraw.Draw(m).arc([(cx - r) * K, (cy - r) * K, (cx + r) * K, (cy + r) * K], a0, a1,
                              fill=255, width=max(1, int(w * K)))
        return m

    @staticmethod
    def union(*ms):
        out = ms[0]
        for m in ms[1:]:
            out = ImageChops.lighter(out, m)
        return out

    # ---- painting ----------------------------------------------------
    def _gradient(self, mask, top, bot, mode='v', shift=0.0):
        bb = mask.getbbox()
        if not bb:
            return None
        x0, y0, x1, y1 = bb
        w, h = x1 - x0, y1 - y0
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        if mode == 'v':
            t = yy / max(1, h - 1)
        elif mode == 'd':
            t = (xx / max(1, w - 1) * 0.45 + yy / max(1, h - 1) * 0.55)
        elif mode == 'r':  # radial highlight from upper-left
            cx, cy = w * 0.36, h * 0.30
            t = np.sqrt(((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2) * 1.35
        else:
            t = yy / max(1, h - 1)
        t = np.clip(t + shift, 0, 1)[..., None]
        a = np.array(top, np.float32)
        b = np.array(bot, np.float32)
        arr = a + (b - a) * t
        g = Image.fromarray(arr.astype(np.uint8), 'RGBA')
        full = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        full.paste(g, (x0, y0))
        return full

    def paint(self, mask, color, alpha=1.0):
        layer = Image.new('RGBA', (S, S), color)
        if alpha < 1:
            mask = mask.point(lambda v: int(v * alpha))
        self.img.alpha_composite(Image.composite(layer, Image.new('RGBA', (S, S), (0, 0, 0, 0)), mask))

    def paint_grad(self, mask, top, bot, mode='v', shift=0.0, alpha=1.0):
        g = self._gradient(mask, top, bot, mode, shift)
        if g is None:
            return
        if alpha < 1:
            mask = mask.point(lambda v: int(v * alpha))
        self.img.alpha_composite(Image.composite(g, Image.new('RGBA', (S, S), (0, 0, 0, 0)), mask))

    @staticmethod
    def _grow(mask, px):
        px = int(round(px))
        if px <= 0:
            return mask
        k = px * 2 + 1
        return mask.filter(ImageFilter.MaxFilter(k if k % 2 else k + 1))

    @staticmethod
    def _shift(mask, dx, dy):
        return ImageChops.offset(mask, int(dx), int(dy))

    def shape(self, mask, top, bot, outline=None, ow=0.9, mode='v', hi=0.55, shade=0.0, shadow=True, halo=None):
        """Outlined, shaded, specular-edged shape."""
        if shadow:
            sh = self._grow(mask, ow * K)
            sh = self._shift(sh, int(0.9 * K), int(1.1 * K)).filter(ImageFilter.GaussianBlur(0.8 * K))
            self.paint(sh, (0, 0, 0, 255), 0.30)
        if halo is not None and outline is not None:
            self.paint(self._grow(mask, (ow + 0.75) * K), halo)
        if outline is not None:
            self.paint(self._grow(mask, ow * K), outline)
        self.paint_grad(mask, top, bot, mode)
        if hi > 0:
            inner = ImageChops.subtract(mask, self._shift(mask, int(0.9 * K), int(0.9 * K)))
            inner = ImageChops.multiply(inner, mask)
            self.paint(inner.filter(ImageFilter.GaussianBlur(0.25 * K)), (255, 255, 255, 255), hi)
        if shade > 0:
            rim = ImageChops.subtract(mask, self._shift(mask, -int(1.0 * K), -int(1.0 * K)))
            self.paint(ImageChops.multiply(rim, mask).filter(ImageFilter.GaussianBlur(0.3 * K)),
                       (0, 0, 0, 255), shade)

    # conveniences ------------------------------------------------------
    def poly(self, pts, top, bot, outline=None, **kw):
        self.shape(self.m_poly(pts), top, bot, outline, **kw)

    def ell(self, cx, cy, rx, ry, top, bot, outline=None, **kw):
        self.shape(self.m_ellipse(cx, cy, rx, ry), top, bot, outline, **kw)

    def rr(self, x0, y0, x1, y1, r, top, bot, outline=None, **kw):
        self.shape(self.m_rrect(x0, y0, x1, y1, r), top, bot, outline, **kw)

    def stroke(self, pts, w, color, outline=None, ow=0.7, alpha=1.0):
        m = self.m_line(pts, w)
        if outline is not None:
            self.paint(self._grow(m, ow * K), outline)
        self.paint(m, color, alpha)

    def glow(self, cx, cy, r, color, strength=0.8):
        m = self.m_ellipse(cx, cy, r * 0.55)
        m = m.filter(ImageFilter.GaussianBlur(r * K * 0.22))
        self.paint(m, color, strength)

    def sparkle(self, cx, cy, r, color, t=1.0):
        r = r * t
        if r <= 0.05:
            return
        a = r * 0.22
        pts = [(cx, cy - r), (cx + a, cy - a), (cx + r, cy), (cx + a, cy + a),
               (cx, cy + r), (cx - a, cy + a), (cx - r, cy), (cx - a, cy - a)]
        self.paint(self.m_poly(pts), color)
        self.paint(self.m_ellipse(cx, cy, a * 1.1), (255, 255, 255, 255))

    def star(self, cx, cy, r, color, n=5, inner=0.5, rot=-90):
        pts = []
        for i in range(n * 2):
            rr_ = r if i % 2 == 0 else r * inner
            a = math.radians(rot + i * 180 / n)
            pts.append((cx + rr_ * math.cos(a), cy + rr_ * math.sin(a)))
        self.paint(self.m_poly(pts), color)

    def finish(self, size):
        return self.img.resize((size, size), Image.LANCZOS)


def rot(pts, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def tri(t):
    """0..1 -> smooth 0..1..0"""
    return 0.5 - 0.5 * math.cos(2 * math.pi * t)
