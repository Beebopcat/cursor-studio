"""Structural check of every built .cur / .ani file (RIFF/ICONDIR sizes, frame counts, hotspots, image decode)."""
import glob, io, os, struct, sys
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def check_cur(d, where):
    rs, tp, n = struct.unpack('<HHH', d[:6])
    assert rs == 0 and tp == 2 and n >= 1, where
    for i in range(n):
        w, h, _, _, hx, hy, sz, off = struct.unpack('<BBBBHHII', d[6 + 16 * i:22 + 16 * i])
        w = w or 256
        assert off + sz <= len(d) and hx < w and hy < h if h else True, where
        blob = d[off:off + sz]
        if blob[:8] == b'\x89PNG\r\n\x1a\n':
            assert Image.open(io.BytesIO(blob)).size == (w, w), where
        else:
            assert struct.unpack('<I', blob[:4])[0] == 40, where
    return n


def check_ani(d, where):
    assert d[:4] == b'RIFF' and struct.unpack('<I', d[4:8])[0] == len(d) - 8 and d[8:12] == b'ACON', where
    p, frames, anih = 12, 0, None
    while p < len(d):
        tag, sz = d[p:p + 4], struct.unpack('<I', d[p + 4:p + 8])[0]
        body = d[p + 8:p + 8 + sz]
        if tag == b'anih':
            anih = struct.unpack('<9I', body)
        if tag == b'LIST' and body[:4] == b'fram':
            q = 4
            while q < len(body):
                assert body[q:q + 4] == b'icon', where
                s2 = struct.unpack('<I', body[q + 4:q + 8])[0]
                check_cur(body[q + 8:q + 8 + s2], where)
                frames += 1
                q += 8 + s2 + (s2 & 1)
        p += 8 + sz + (sz & 1)
    assert p == len(d) and anih and anih[1] == frames and anih[8] == 1, where
    return frames


if __name__ == '__main__':
    curs = glob.glob(os.path.join(ROOT, 'Sets', '*', '*', 'Static', '*.cur'))
    anis = glob.glob(os.path.join(ROOT, 'Sets', '*', '*', 'Animated', '*.ani'))
    for f in curs:
        check_cur(open(f, 'rb').read(), f)
    for f in anis:
        check_ani(open(f, 'rb').read(), f)
    styles = glob.glob(os.path.join(ROOT, 'Sets', '*', '*'))
    print(f'OK: {len(styles)} styles, {len(curs)} .cur and {len(anis)} .ani files are structurally valid')
    sys.exit(0 if len(curs) == len(anis) == len(styles) * 17 else 1)
