"""Gemini Originals: loads the owner's Gemini cursor art and prepares it for the engine.

Inputs (gemini_src/): NNX_cur32.png (32x32 sprite) and NNX_img.jpg (220x150 card art on a dark panel), NN=01..24, X=A/B/C.
gemini_meta.json holds the titles, descriptions and accent colour per set and style (from the owner's Gemini selector page).

Per variant this produces a `GemArt` with
  .sprite     cleaned 32x32 RGBA sprite (stray panel residue removed)
  .hotspot    (x, y) in 32 px space, the tip = top-left-most opaque region of the sprite
  .layer(S)   the pointer art at S px (32: the sprite itself; 48/64: clean cutout of the card art, or the
              upscaled+sharpened sprite when the cutout does not match the sprite well)
  .hires      RGBA image (cutout or upscaled sprite) in a 256 px canvas laid out like the sprite, used as the role badge
  .mode       'cutout' or 'upscale' (decided per variant by comparing the cutout with the sprite)
"""
import json, os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'gemini_src')
META = json.load(open(os.path.join(HERE, 'gemini_meta.json'), encoding='utf-8'))
HI = 256

# per-variant override of the automatic choice: 'cutout' or 'upscale'
FORCE = {'03A': 'upscale', '16C': 'upscale', '05A': 'cutout', '11A': 'cutout'}


def _label(mask):
    """4-connected components of a boolean array (small images only)."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    n = 0
    for y in range(h):
        for x in range(w):
            if mask[y, x] and not lab[y, x]:
                n += 1
                st = [(y, x)]
                lab[y, x] = n
                while st:
                    cy, cx = st.pop()
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n
                            st.append((ny, nx))
    return lab, n


def _grow(m, r):
    im = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * r + 1))
    return np.array(im) > 127


def clean_sprite(path):
    """Drop the faint panel rectangle (alpha 15..50) Gemini left around many sprites, keep real glow next to the body."""
    a = np.array(Image.open(path).convert('RGBA')).copy()
    al = a[..., 3]
    core = _grow(al >= 96, 1)
    al[(al < 96) & ~core] = 0
    al[al < 10] = 0
    a[..., 3] = al
    return Image.fromarray(a, 'RGBA')


def hotspot_of(sprite):
    """Tip of the sprite: centre of the opaque pixels nearest the top-left corner (min x+y region)."""
    a = np.array(sprite)[..., 3]
    ys, xs = np.where(a >= 128)
    d = xs + ys
    sel = d <= d.min() + 2
    return int(round(xs[sel].mean())), int(round(ys[sel].mean()))


def _lin(a, w, h, mn):
    """Min/max over a w x h rectangle (numpy, edge padded)."""
    f = np.minimum if mn else np.maximum
    out = a
    if w > 1:
        p = np.pad(out, ((0, 0), (w // 2, w // 2)), mode='edge')
        out = p[:, 0:out.shape[1]]
        for k in range(1, w):
            out = f(out, p[:, k:k + a.shape[1]])
    if h > 1:
        p = np.pad(out, ((h // 2, h // 2), (0, 0)), mode='edge')
        o2 = p[0:a.shape[0], :]
        for k in range(1, h):
            o2 = f(o2, p[k:k + a.shape[0], :])
        out = o2
    return out


def _open(m, w, h):
    """Binary opening with a w x h rectangle."""
    a = (m * 255).astype(np.uint8)
    return _lin(_lin(a, w, h, True), w, h, False) > 127


FRAMED = {'05A', '05B', '05C', '06A', '06B', '06C', '07A', '07B', '07C', '10A', '11A', '12A'}   # cards drawn inside a panel


def matte(img_path):
    """Cut the object out of the 220x150 card art. Returns (RGBA float array HxWx4 0..255, core mask bool)."""
    im = np.array(Image.open(img_path).convert('RGB')).astype(np.float32)
    framed = os.path.basename(img_path)[:3] in FRAMED
    h, w, _ = im.shape
    ring = np.concatenate([im[:5].reshape(-1, 3), im[-5:].reshape(-1, 3), im[:, :5].reshape(-1, 3), im[:, -5:].reshape(-1, 3)])
    bg0 = np.median(ring, axis=0)
    d0 = np.sqrt(((im - bg0) ** 2).sum(-1))
    fg0 = _grow(d0 > 40, 4)
    # smooth background model: quadratic fit on the background pixels
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    X = np.stack([np.ones_like(xx), xx / w, yy / h, (xx / w) ** 2, (yy / h) ** 2, xx * yy / (w * h)], -1)
    sel = ~fg0
    if sel.sum() > 200:
        bg = np.zeros_like(im)
        for c in range(3):
            coef, *_ = np.linalg.lstsq(X[sel], im[..., c][sel], rcond=None)
            bg[..., c] = X @ coef
    else:
        bg = np.broadcast_to(bg0, im.shape)
    d = np.sqrt(((im - bg) ** 2).sum(-1))
    # alpha ramp from colour distance (feathered), luminance-aware so dark objects survive
    lum = lambda a: a @ np.array([.3, .59, .11], np.float32)
    dl = np.abs(lum(im) - lum(bg))
    dist = np.maximum(d, dl * 1.4)
    alpha = np.clip((dist - 22) / 55, 0, 1)
    core = dist > 45
    # remove frame/panel structure: thin lines vanish under a morphological opening, the object (plus thin parts
    # touching it) is rebuilt from the surviving seeds
    op = np.array(Image.fromarray((core * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(7))) > 127
    seeds = _grow(op, 3) & core if op.sum() > 30 else core
    reg0 = _grow(seeds, 6) & core
    lab, n = _label(reg0)
    keep = np.zeros_like(core)
    areas = sorted(((int((lab == i).sum()), i) for i in range(1, n + 1)), reverse=True)
    big = areas[0][0] if areas else 0
    for ar, i in areas:
        ys, xs = np.where(lab == i)
        bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        frame = ar / float(bw * bh) < .10 and (bw > .6 * w or bh > .6 * h)
        if ar >= max(25, big * .03) and not frame:
            keep |= lab == i
    reg = _grow(keep, 7)
    if framed:
        # the card has a panel: its border remnants are straight horizontal/vertical lines of 4 px or less
        body = _grow(_open(keep, 5, 5), 2)
        lines = (_open(keep, 15, 1) | _open(keep, 1, 15)) & ~body
        reg &= ~_grow(lines, 2) | body
    alpha = alpha * reg
    # un-mix colours from the background so glow edges do not carry dark fringes
    a3 = np.clip(alpha, 1e-3, 1)[..., None]
    fgc = np.clip((im - (1 - a3) * bg) / a3, 0, 255)
    out = np.concatenate([fgc, (alpha * 255)[..., None]], -1)
    return out, keep, seeds


def _bbox(mask):
    ys, xs = np.where(mask)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def _fit(core, sprite):
    """Similarity transform art px -> sprite 32-space (scale, tx, ty) from the object bboxes."""
    ax0, ay0, ax1, ay1 = _bbox(core)
    sa = np.array(sprite)[..., 3] >= 100
    sx0, sy0, sx1, sy1 = _bbox(sa)
    s = max(sx1 - sx0, 1) / max(ax1 - ax0, 1) if (ax1 - ax0) >= (ay1 - ay0) else max(sy1 - sy0, 1) / max(ay1 - ay0, 1)
    tx = (sx0 + sx1) / 2 - s * (ax0 + ax1) / 2
    ty = (sy0 + sy1) / 2 - s * (ay0 + ay1) / 2
    return s, tx, ty


def _guide(cut, core, sprite, tf):
    """Keep only art that lies near the sprite's silhouette (mapped back into art space): drops leftover panel lines."""
    s, tx, ty = tf
    h, w = core.shape
    sp = sprite.getchannel('A').point(lambda v: 255 if v >= 60 else 0)
    n = int(round(32 / s))
    g = Image.new('L', (w, h), 0)
    g.paste(sp.resize((n, n), Image.BILINEAR), (int(round(-tx / s)), int(round(-ty / s))))
    r = int(max(4, min(30, 1.0 / s)))
    g = np.array(g.filter(ImageFilter.MaxFilter(2 * r + 1 if r < 15 else 31))) > 100
    cut = cut.copy()
    cut[..., 3] *= g
    return cut, core & g


def _render(cut, tf, size, extra=0):
    """Place the cutout on a size x size RGBA canvas using the art->sprite transform (premultiplied resample)."""
    s, tx, ty = tf
    f = size / 32.0
    sc = s * f
    h, w = cut.shape[:2]
    pm = cut.copy()
    pm[..., :3] *= pm[..., 3:4] / 255.0
    big = Image.fromarray(np.clip(pm, 0, 255).astype(np.uint8), 'RGBA')
    nw, nh = max(1, int(round(w * sc))), max(1, int(round(h * sc)))
    r = big.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    canvas.paste(r, (int(round(tx * f)), int(round(ty * f))))
    a = np.array(canvas).astype(np.float32)
    al = a[..., 3:4]
    a[..., :3] = np.where(al > 0, a[..., :3] * 255.0 / np.maximum(al, 1), 0)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def _upscale(sprite, size):
    r = sprite.resize((size, size), Image.LANCZOS)
    return r.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=2))


def _iou(a, b):
    a, b = a >= 110, b >= 110
    u = (a | b).sum()
    return (a & b).sum() / u if u else 0


class GemArt:
    def __init__(self, num, code):
        self.num, self.code = num, code
        self.name = '%02d%s' % (num, code)
        self.sprite = clean_sprite(os.path.join(SRC, self.name + '_cur32.png'))
        self.hotspot = hotspot_of(self.sprite)
        self.cut, core, seeds = matte(os.path.join(SRC, self.name + '_img.jpg'))
        h, w = core.shape
        self.tf = _fit(core, self.sprite)
        self.cut, core = _guide(self.cut, core, self.sprite, self.tf)
        self.tf = _fit(core, self.sprite)
        bx0, by0, bx1, by1 = _bbox(seeds & core)
        self.cropped = bx0 <= 1 or by0 <= 1 or bx1 >= w - 1 or by1 >= h - 1
        c32 = _render(self.cut, self.tf, 32)
        self.iou = _iou(np.array(c32)[..., 3], np.array(self.sprite)[..., 3])
        self.mode = FORCE.get(self.name) or ('cutout' if (self.iou >= .45 and not self.cropped) else 'upscale')
        self._cache = {}

    def layer(self, size):
        """Pointer art at `size` px as RGBA (the 32 px one is the Gemini sprite untouched)."""
        if size == 32:
            return self.sprite
        if size not in self._cache:
            self._cache[size] = _render(self.cut, self.tf, size) if self.mode == 'cutout' else _upscale(self.sprite, size)
        return self._cache[size]

    @property
    def hires(self):
        return self.layer(HI)


def all_variants():
    for n in range(1, 25):
        for c in 'ABC':
            yield GemArt(n, c)
