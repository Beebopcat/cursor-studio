"""Builds the exportable package: CursorStudio-Package.zip (everything: cursors, previews, apps, docs, source).

usage: python3 package.py [output-dir]      (default: CursorSets/Dist)
Also writes one small zip per set (CursorStudio-<set>.zip) for people who only want one set.
"""
import os, sys, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
out = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, 'Dist')
os.makedirs(out, exist_ok=True)
SKIP = {'Dist', '__pycache__'}


def walk(base):
    for d, dirs, files in os.walk(base):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in files:
            yield os.path.join(d, f)


full = os.path.join(out, 'CursorStudio-Package.zip')
with zipfile.ZipFile(full, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in walk(ROOT):
        z.write(f, os.path.join('CursorSets', os.path.relpath(f, ROOT)))
print(full, os.path.getsize(full) // 2**20, 'MB')
if '--per-set' in sys.argv:
    for s in sorted(os.listdir(os.path.join(ROOT, 'Sets'))):
        p = os.path.join(out, f'CursorStudio-{s}.zip')
        with zipfile.ZipFile(p, 'w', zipfile.ZIP_DEFLATED) as z:
            for f in walk(os.path.join(ROOT, 'Sets', s)):
                z.write(f, os.path.join('CursorSets', os.path.relpath(f, ROOT)))
        print(p, os.path.getsize(p) // 2**10, 'KB')
