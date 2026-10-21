"""Writes Selector.html and its identical copy index.html (the browser selector app, served by GitHub Pages) from catalog.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
cat = json.load(open(os.path.join(ROOT, 'catalog.json')))
cat = dict(sets=[dict(num=s['num'], group=s['group'], slug=s['slug'], name=s['name'],
                      styles=[{k: st[k] for k in ('key', 'label', 'blurb', 'material', 'pointer', 'preview')} for st in s['styles']]) for s in cat['sets']])
page = open(os.path.join(HERE, 'selector_template.html'), encoding='utf-8').read().replace('/*CAT*/{}', json.dumps(cat, ensure_ascii=False))
for name in ('Selector.html', 'index.html'):
    open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(page)
print('Selector.html + index.html', len(page) // 1024, 'KB')
