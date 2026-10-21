"""Gemini Originals (styles GA, GB, GC): the owner's Gemini cursor art as full 17-role Cursor Studio styles.

Pointer roles that show the object (Normal, Help, Working in Background, Person) use the Gemini sprite as the pointer;
Help / Working / Person add the engine's own badge (roles2) on top. Every other role is the engine's role painter
(busy ring, I-beam, resize arrows, link hand, ...) in the set's accent colour with the Gemini art as its emblem.
Animation: accent glow pulse + shimmer/motes from fx.py, 12 frames.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from PIL import Image, ImageFilter
import roles2
from roles2 import Style2, ROLE_FUNCS
from roles import ROLES
from toolkit import Canvas, K, S, tri, lighten, darken, mix
from materials import blur
import fx as FX
import gemini_art as GA

KEYS = {'A': 'GA', 'B': 'GB', 'C': 'GC'}
MATERIAL = {'A': 'metal', 'B': 'gloss', 'C': 'neon'}
FX_MODE = {'A': 'glint', 'B': 'motes', 'C': 'rays'}
POINTER_ROLES = {'Arrow', 'Help', 'AppStarting', 'Person'}   # drawn on top of the sprite, hotspot from the sprite tip
BADGED = {'Help', 'AppStarting', 'Person'}
NAME = {}


def _meta(num):
    return GA.META[num - 1]


def palette(accent):
    r, g, b = accent
    acc = (r, g, b, 255)
    dark = darken(acc, .82)
    return dict(c1=lighten(acc, .6), c2=darken(acc, .38), ol=darken(acc, .85), ac=lighten(acc, .15), ac2=lighten(acc, .65),
                glow=acc, plate=dark, bad=(255, 74, 90, 255), halo=None)


def _emblem(art):
    """Emblem painter: the Gemini art (cropped to its silhouette) fitted into radius r."""
    im = art.hires
    bb = im.getbbox()
    crop = im.crop(bb) if bb else im

    def paint(c, cx, cy, r, t, p):
        pulse = 1 + .03 * math.sin(t * 2 * math.pi)
        box = 2 * r * K * pulse
        s = min(box / crop.width, box / crop.height)
        sz = (max(1, int(crop.width * s)), max(1, int(crop.height * s)))
        sp = crop.resize(sz, Image.LANCZOS)
        c.glow(cx, cy, r * 1.35, p['glow'], .25 + .25 * tri(t))
        c.img.alpha_composite(sp, (int(cx * K - sz[0] / 2), int(cy * K - sz[1] / 2)))
    return paint


class GemStyle(Style2):
    def __init__(self, art):
        m = _meta(art.num)
        info = m['styles'][art.code]
        key = KEYS[art.code]
        super().__init__(key, info['title'], info['desc'], palette(m['accent']), MATERIAL[art.code], 'gemini', 'gem',
                         FX_MODE[art.code], False, {})
        self.art = art
        self.accent = tuple(m['accent'])
        self._em = _emblem(art)

    def em(self, role):
        return self._em


def hotspot_for(st, role, default):
    return st.art.hotspot if role in POINTER_ROLES else default


# ---------------------------------------------------------------- pointer layer
def _silhouette(st):
    return st.art.hires.getchannel('A')


def _effects(st, t, size):
    """(under, over) RGBA layers at `size`: accent glow pulse under the sprite, shimmer / motes over it."""
    U = _silhouette(st)
    p = st.p
    cu = Canvas()
    gl = blur(U, 2.4 if size < 64 else 2.8)
    cu.paint(gl, p['glow'], .22 + .30 * tri(t))
    co = Canvas()
    if st.fx == 'motes':
        FX.run(co, st, t, U)
    else:
        FX.shimmer(co, st, U, t, 2.6 if st.fx == 'glint' else 2.0, .30)
    return cu.finish(size), co.finish(size)


def pointer_layer(st, t, size):
    under, over = _effects(st, t, size)
    base = st.art.layer(size)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.alpha_composite(under)
    out.alpha_composite(base)
    # keep the shimmer on the artwork only (motes are allowed to leave the silhouette)
    if st.fx != 'motes':
        a = base.getchannel('A')
        o = over.copy()
        o.putalpha(Image.fromarray((np.array(o.getchannel('A')).astype(np.float32) * np.array(a).astype(np.float32) / 255).astype(np.uint8)))
        over = o
    out.alpha_composite(over)
    return out


# ---------------------------------------------------------------- roles
def _no_pointer(c, st, t):
    return None


def render_role(st, role, t, sizes=(32, 48, 64)):
    if role == 'Arrow':
        return {s: pointer_layer(st, t, s) for s in sizes}
    c = Canvas()
    if role in BADGED:
        orig = roles2.pointer
        roles2.pointer = _no_pointer
        try:
            ROLE_FUNCS[role](c, st, t)
        finally:
            roles2.pointer = orig
        out = {}
        for s in sizes:
            im = pointer_layer(st, t, s)
            im.alpha_composite(c.finish(s))
            out[s] = im
        return out
    ROLE_FUNCS[role](c, st, t)
    return {s: c.finish(s) for s in sizes}


# ---------------------------------------------------------------- catalog helpers
def all_styles():
    """[(set number, [GemStyle GA, GB, GC])] built lazily (cutouts take a few seconds)."""
    out = []
    for n in range(1, 25):
        out.append((n, [GemStyle(GA.GemArt(n, c)) for c in 'ABC']))
    return out


def _hot(num, c):
    a = GA.AIM.load().get('%02d%s' % (num, c))
    return a['tip'] if a else GA.hotspot_of(GA.clean_sprite(os.path.join(GA.SRC, '%02d%s_cur32.png' % (num, c))))


def catalog_styles(set_item, slugify):
    """catalog.json style entries for one set (no image work: names from gemini_meta.json)."""
    m = _meta(set_item['num'])
    res = []
    for c in 'ABC':
        key, info = KEYS[c], m['styles'][c]
        sd = f'{key}-{slugify(info["title"])}'
        res.append(dict(key=key, label=info['title'], blurb=info['desc'], material='gemini', pointer='Gemini sprite',
                        scheme=f'{set_item["name"]} - {key} {info["title"]}',
                        path=f'Sets/{set_item["slug"]}/{sd}', preview=f'Previews/{set_item["slug"]}/{key}',
                        art=f'Previews/{set_item["slug"]}/{key}/art.jpg', source='gemini',
                        hot=list(_hot(set_item['num'], c))))
    return res
