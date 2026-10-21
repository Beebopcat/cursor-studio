"""Gemini Originals: re-aim the pointer sprites so the business end points up-left (-135 deg) like a Windows arrow.

gemini_aim.json = per-variant decision table {key: {rotate_deg, flip, tip [x,y] at 32 px, reason, ...}}; produced by
`python3 gemini_aim.py` from the hand-verified HINTS below (PCA principal axis refined by eye).
Optional per-entry "split_x": the sprite holds a pointer (columns < split_x) plus a companion object (kept in place).
Rotation: 4x supersampled bicubic on premultiplied alpha, box downsample; the art is scaled down if it would not fit.
"""
import json, math, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'gemini_aim.json')
SS = 4
TARGET = -135.0


def load():
    try:
        return json.load(open(PATH))
    except OSError:
        return {}


def make_mask(sprite, split):
    """32 px L mask of the pointer component(s) (centroid column < split), grown by 1 px; None without a split."""
    if split is None:
        return None
    al = np.array(sprite)[..., 3] >= 40
    lab = np.zeros(al.shape, int)
    n = 0
    for y0 in range(32):
        for x0 in range(32):
            if al[y0, x0] and not lab[y0, x0]:
                n += 1
                st = [(y0, x0)]
                lab[y0, x0] = n
                while st:
                    y, x = st.pop()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < 32 and 0 <= nx < 32 and al[ny, nx] and not lab[ny, nx]:
                                lab[ny, nx] = n
                                st.append((ny, nx))
    keep = np.zeros(al.shape, bool)
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) >= 6 and xs.mean() < split:
            keep |= lab == i
    m = Image.fromarray((keep * 255).astype(np.uint8))
    from PIL import ImageFilter
    return m.filter(ImageFilter.MaxFilter(3))


def _region(img, size, mask):
    """(pointer, companion) split of an RGBA image at `size` px (companion None without a mask)."""
    if mask is None:
        return img, None
    m = np.array(mask.resize((size, size), Image.BILINEAR if size != 32 else Image.NEAREST)) > 60
    a = np.array(img)
    p, c = a.copy(), a.copy()
    p[~m] = 0
    c[m] = 0
    return Image.fromarray(p, 'RGBA'), Image.fromarray(c, 'RGBA')


def params(sprite, cfg):
    """Transform in 32 px continuous coords: (centre c, dest centre c2, scale k) for a sprite and its aim entry."""
    th = math.radians(cfg['rotate_deg'])
    split = cfg.get('split_x')
    mask = make_mask(sprite, split)
    pointer, _ = _region(sprite, 32, mask)
    al = np.array(pointer.resize((32 * 8, 32 * 8), Image.BILINEAR))[..., 3] >= 128
    ys, xs = np.where(al)
    px = np.stack([(xs + .5) / 8.0, (ys + .5) / 8.0], 1)
    c = np.array([(px[:, 0].min() + px[:, 0].max()) / 2, (px[:, 1].min() + px[:, 1].max()) / 2])
    F = np.diag([-1.0 if cfg.get('flip') else 1.0, 1.0])
    R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    q = (px - c) @ (R @ F).T
    lo, hi = q.min(0), q.max(0)
    w, h = hi - lo
    if split is None:
        k = min(1.0, 29.0 / max(w, 1e-6), 29.0 / max(h, 1e-6))
        c2 = np.array([1.0, 1.0]) - k * lo + 0.0
        # keep the top-left corner of the object 1 px inside the canvas (room for the outline / glow)
        c2 = np.array([1.5, 1.5]) - k * lo
    else:
        ox0, oy0 = px.min(0)
        ox1, oy1 = px.max(0)
        k = min(1.0, (split - 1.0) / max(w, 1e-6), 29.0 / max(h, 1e-6))
        cx = min(max(c[0], 0.5 + k * w / 2), split - 0.5 - k * w / 2)
        cy = min(max(c[1], 1 + k * h / 2), 31 - k * h / 2)
        c2 = np.array([cx, cy]) - k * (lo + hi) / 2
    return c, c2, k, mask


def apply(img, cfg, prm):
    """Rotate/flip the art in `img` (RGBA, square, size N) as configured. 4x supersample, alpha stays crisp."""
    c, c2, k, mask = prm
    n = img.width
    th = math.radians(cfg['rotate_deg'])
    ptr, comp = _region(img, n, mask)
    S = n * SS
    big = ptr.resize((S, S), Image.BICUBIC if n >= S else Image.LANCZOS)
    a = np.array(big).astype(np.float32)
    a[..., :3] *= a[..., 3:4] / 255.0                     # premultiply
    F = np.diag([-1.0 if cfg.get('flip') else 1.0, 1.0])
    R = np.array([[math.cos(-th), -math.sin(-th)], [math.sin(-th), math.cos(-th)]])
    M = F @ R / k                                         # dest offset -> source offset (32 px units, same scale in S px)
    u = S / 32.0
    c4, c24 = c * u, c2 * u
    off = c4 - M @ c24
    coef = (M[0, 0], M[0, 1], off[0], M[1, 0], M[1, 1], off[1])
    bands = [Image.fromarray(a[..., i], 'F').transform((S, S), Image.AFFINE, coef, Image.BICUBIC) for i in range(4)]
    r = np.stack([np.array(b) for b in bands], -1)
    r = np.clip(r, 0, 255)
    r = r.reshape(n, SS, n, SS, 4).mean((1, 3))           # box downsample (premultiplied)
    al = r[..., 3:4]
    rgb = np.where(al > 0.5, r[..., :3] * 255.0 / np.maximum(al, 1e-3), 0)
    out = Image.fromarray(np.clip(np.concatenate([rgb, al], -1) + .5, 0, 255).astype(np.uint8), 'RGBA')
    if comp is not None:
        out.alpha_composite(comp)
    return out


def tip_of(sprite, cfg, mask=None):
    """Tip pixel of an (aimed) 32 px sprite: centre of the opaque pointer pixels nearest the top-left corner."""
    ptr, _ = _region(sprite, 32, mask)
    a = np.array(ptr)[..., 3]
    ys, xs = np.where(a >= 128)
    d = xs + ys
    sel = d <= d.min() + 2
    return [int(min(31, round(xs[sel].mean()))), int(min(31, round(ys[sel].mean())))]


# ------------------------------------------------------------------ decision table generator
# key: (tip direction in image degrees, 0 = right, 90 = down, -90 = up; reason, optional split_x)
HINTS = {
    '01A': (0, 'glaive drawn horizontally, spearhead on the right'),
    '02A': (0, 'plume blade, feathers left, point right'),
    '03A': (180, 'dagger, blade point on the left, hilt stub right'),
    '04A': (180, 'red blade, cream point on the left, tail right'),
    '04B': (45, 'comet: head (business end) lower-right, flame tail up-left; head swung to the tip'),
    '10A': (-90, 'upright ornament, point up'),
    '10B': (45, 'orb on a wand, cyan crystal tip lower-right'),
    '10C': (0, 'arrowhead pointing right'),
    '11A': (-90, 'upright dagger, point up'),
    '11C': (0, 'flame-trailed head, point right'),
    '12C': (0, 'arrowhead pointing right'),
    '13A': (0, 'green blade, point right'),
    '13C': (0, 'tapered spike, point right, glow trail left'),
    '14A': (0, 'staff, point right'),
    '14C': (0, 'spear-like relic, point right'),
    '15A': (-26, 'spear, head up-right, shaft down-left'),
    '16A': (0, 'jewelled scepter, spike on the right'),
    '16C': (0, 'wand with ringed head on the right (head is the business end)'),
    '17A': (0, 'spear, red pommel left, blade right'),
    '17C': (0, 'dark blade, point right'),
    '20A': (0, 'pointing glove, finger right (donut companion stays)', 13),
    '20B': (-10, 'pointing glove, finger right-up (donut companion stays)', 13),
    '20C': (-5, 'pointing glove, finger right (donut companion stays)', 13),
    '21A': (-45, 'green rod, tip upper-right (fish companion stays)', 14),
    '21B': (-50, 'green arrow-rod, tip upper-right (fish companion stays)', 14),
    '21C': (-45, 'slim green rod, tip upper-right (fish companion stays)', 14),
}
KEEP = {
    'B': 'mascot or round emblem: no pointing end, left as drawn',
    'A': 'tip (or business end) already at the upper-left',
    'C': 'tip (or business end) already at the upper-left',
}
KEEP_SPECIAL = {
    '03C': 'round reticle with a short handle: no clear pointing end',
    '01B': 'symmetric crystal drop: no clear pointing end',
    '12A': 'upright mascot figure: no pointing end',
    '15C': 'wing with its spike already at the upper-left',
    '18A': 'bolt point already at the upper-left (pokeball companion)',
    '18B': 'bolt point already at the upper-left (pokeball companion)',
    '18C': 'bolt point already at the upper-left (pokeball companion)',
    '19A': 'Gengar mascot with companion: no pointing end', '19C': 'Gengar mascot with companion: no pointing end',
    '22A': 'bow and wing: no pointing end', '22C': 'bow and wing: no pointing end',
    '23A': 'radish pair: no pointing end', '23C': 'radish pair: no pointing end',
    '24A': 'paw and hat: no pointing end', '24C': 'paw and hat: no pointing end',
    '09A': 'gnome hat tip already at the upper-left',
}


def _wrap(d):
    d = (d + 180) % 360 - 180
    return 180.0 if d == -180 else d


def build_table():
    import gemini_art as GA
    out = {}
    for n in range(1, 25):
        for c in 'ABC':
            nm = '%02d%s' % (n, c)
            spr = GA.clean_sprite(os.path.join(GA.SRC, nm + '_cur32.png'))
            if nm in HINTS:
                h = HINTS[nm]
                hint, reason = h[0], h[1]
                split = h[2] if len(h) > 2 else None
                ptr, _ = _region(spr, 32, make_mask(spr, split))
                ys, xs = np.where(np.array(ptr)[..., 3] >= 128)
                p = np.stack([xs, ys], 1).astype(float)
                w, v = np.linalg.eigh(np.cov((p - p.mean(0)).T))
                ax = v[:, 1]
                hv = np.array([math.cos(math.radians(hint)), math.sin(math.radians(hint))])
                if ax @ hv < 0:
                    ax = -ax
                pca = math.degrees(math.atan2(ax[1], ax[0]))
                phi = pca if abs(_wrap(pca - hint)) <= 25 else hint
                cfg = dict(rotate_deg=round(_wrap(TARGET - phi), 1), flip=False, reason=reason, tip_dir_deg=round(phi, 1),
                           pca_deg=round(pca, 1), pca_elong=round(float(w[1] / max(w[0], .1)), 1))
                if split:
                    cfg['split_x'] = split
                prm = params(spr, cfg)
                # the rotated pointer's own mask: re-derive from the aimed sprite (component split) for companion sprites
                aimed = apply(spr, cfg, prm)
                tip = tip_of(aimed, cfg, make_mask(aimed, split))
            else:
                reason = KEEP_SPECIAL.get(nm) or KEEP[c]
                cfg = dict(rotate_deg=0, flip=False, reason=reason)
                tip = GA.hotspot_of(spr)
            cfg['tip'] = tip
            out[nm] = cfg
    return out


if __name__ == '__main__':
    t = build_table()
    json.dump(t, open(PATH, 'w'), indent=1)
    print(sum(1 for v in t.values() if v['rotate_deg']), 'rotated of', len(t))
