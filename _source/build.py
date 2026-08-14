#!/usr/bin/env python3
"""Static build for the Nordic Steam Co. demo storefront.

Pages live in src/pages/*.html and hold only the <main> content plus a
one-line front matter comment. Header/footer come from src/partials.
Product cards are generated from the PRODUCTS list below so the grids on
the homepage, shop and cart stay in sync — the same job the WooCommerce
loop does in the real build.
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site')

PRODUCTS = [
    dict(slug='aurora-barrel-6', name='Aurora 6-Person Outdoor Barrel Sauna — Red Cedar',
         cat='Outdoor Saunas', price=6499.00, was=7199.00, img='p-barrel.svg',
         rating=4.9, reviews=68, badge='Best seller', stock='In stock — ships in 5–7 business days'),
    dict(slug='fjord-cabin-4', name='Fjord 4-Person Indoor Cabin Sauna Kit',
         cat='Indoor Sauna Kits', price=4899.00, was=None, img='p-cabin.svg',
         rating=4.8, reviews=41, badge=None, stock='In stock — ships in 3–5 business days'),
    dict(slug='solstice-infrared-2', name='Solstice 2-Person Full-Spectrum Infrared Sauna',
         cat='Infrared Saunas', price=3749.00, was=4199.00, img='p-infrared.svg',
         rating=4.7, reviews=112, badge='Sale', stock='In stock — ships in 2–4 business days'),
    dict(slug='kelvin-9kw-heater', name='Kelvin 9kW Electric Sauna Heater with Stone Set',
         cat='Sauna Heaters', price=1149.00, was=None, img='p-heater.svg',
         rating=4.8, reviews=57, badge=None, stock='In stock — ships next business day'),
    dict(slug='glacier-plunge', name='Glacier Cold Plunge Tub with 1HP Chiller',
         cat='Cold Plunge', price=5299.00, was=None, img='p-plunge.svg',
         rating=4.9, reviews=34, badge='New', stock='In stock — ships in 7–10 business days'),
    dict(slug='vaporpro-12kw', name='VaporPro 12kW Commercial Steam Generator',
         cat='Steam Generators', price=2299.00, was=2599.00, img='p-steam.svg',
         rating=4.6, reviews=23, badge='Sale', stock='In stock — ships in 3–5 business days'),
    dict(slug='cedar-glass-door', name='Cedar Sauna Door — Full Glass, Bronze Tint',
         cat='Doors & Windows', price=1049.00, was=None, img='p-door.svg',
         rating=4.8, reviews=29, badge=None, stock='In stock — ships in 5–7 business days'),
    dict(slug='nordic-accessory-kit', name='Nordic Accessory Kit — Bucket, Ladle, Thermometer, Timer',
         cat='Accessories', price=189.00, was=229.00, img='p-kit.svg',
         rating=4.7, reviews=186, badge='Sale', stock='In stock — ships next business day'),
]
BY_SLUG = {p['slug']: p for p in PRODUCTS}

STAR_FULL = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21l1.2-6.9-5-4.9 6.9-1z"/></svg>'
STAR_HALF = ('<svg viewBox="0 0 24 24"><defs><linearGradient id="h"><stop offset="50%" stop-color="currentColor"/>'
             '<stop offset="50%" stop-color="#ddd6ce"/></linearGradient></defs>'
             '<path fill="url(#h)" d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21l1.2-6.9-5-4.9 6.9-1z"/></svg>')
STAR_EMPTY = '<svg viewBox="0 0 24 24" fill="#ddd6ce"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21l1.2-6.9-5-4.9 6.9-1z"/></svg>'


def stars(rating, cls=''):
    out = []
    for i in range(1, 6):
        if rating >= i:
            out.append(STAR_FULL)
        elif rating >= i - 0.5:
            out.append(STAR_HALF)
        else:
            out.append(STAR_EMPTY)
    return f'<span class="stars {cls}">' + ''.join(out) + '</span>'


def money(v):
    return '${:,.2f}'.format(v)


def pcard(p):
    badge = ''
    if p['badge']:
        klass = 'sale' if p['badge'] == 'Sale' else ''
        badge = f'<span class="badge {klass}">{p["badge"]}</span>'
    was = f'<s>{money(p["was"])}</s>' if p['was'] else ''
    js_name = html.escape(p['name'].replace('—', '-'), quote=True)
    return f'''<div class="pcard">{badge}
  <a class="thumb" href="product.html?p={p['slug']}"><img src="assets/img/{p['img']}" alt="{html.escape(p['name'])}"></a>
  <span class="cat">{html.escape(p['cat'])}</span>
  <h3><a href="product.html?p={p['slug']}">{html.escape(p['name'])}</a></h3>
  <div class="rating-line">{stars(p['rating'])}<span>{p['rating']} ({p['reviews']})</span></div>
  <div class="price">{was}{money(p['price'])}</div>
  <div class="acts">
    <button class="btn" onclick="addToCart('{js_name}', {p['price']})">Add to cart</button>
    <button class="icobtn" title="Add to wishlist" onclick="toggleWish('{js_name}')">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.8 5.6a5.2 5.2 0 0 0-7.4 0L12 7l-1.4-1.4a5.2 5.2 0 1 0-7.4 7.4L12 21.4l8.8-8.4a5.2 5.2 0 0 0 0-7.4z"/></svg>
    </button>
  </div>
</div>'''


def grid(slugs, four=False):
    cls = 'pgrid four' if four else 'pgrid'
    return f'<div class="{cls}">' + ''.join(pcard(BY_SLUG[s]) for s in slugs) + '</div>'


HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/img/logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{schema}
</head>
<body data-page="{page}">
'''


def build():
    header = open(os.path.join(ROOT, 'src/partials/header.html')).read()
    footer = open(os.path.join(ROOT, 'src/partials/footer.html')).read()
    os.makedirs(OUT, exist_ok=True)

    pages_dir = os.path.join(ROOT, 'src/pages')
    built = []
    for fn in sorted(os.listdir(pages_dir)):
        if not fn.endswith('.html'):
            continue
        raw = open(os.path.join(pages_dir, fn)).read()
        m = re.match(r'\s*<!--meta\s*(\{.*?\})\s*-->', raw, re.S)
        meta = json.loads(m.group(1)) if m else {}
        body = raw[m.end():] if m else raw

        # standalone star widgets
        for token, val, cls in [('{{RATING_G}}', 4.8, ''), ('{{RATING_T}}', 4.9, ''),
                                ('{{RATING_S}}', 4.8, ''), ('{{STARS5}}', 5, ''),
                                ('{{STARS45}}', 4.5, ''), ('{{STARS4}}', 4, ''),
                                ('{{STARS3}}', 3, ''), ('{{STARS5LG}}', 5, 'lg'),
                                ('{{STARS48LG}}', 4.8, 'lg')]:
            if token in body:
                body = body.replace(token, stars(val, cls))

        # expand generator tokens
        for token, slugs, four in [
            ('{{GRID_NEW}}', ['aurora-barrel-6', 'glacier-plunge', 'solstice-infrared-2',
                              'kelvin-9kw-heater', 'fjord-cabin-4', 'vaporpro-12kw'], False),
            ('{{GRID_ALL}}', [p['slug'] for p in PRODUCTS], False),
            ('{{GRID_RELATED}}', ['kelvin-9kw-heater', 'cedar-glass-door', 'nordic-accessory-kit'], False),
        ]:
            if token in body:
                body = body.replace(token, grid(slugs, four))

        doc = HEAD.format(
            title=meta.get('title', 'Nordic Steam Co.'),
            desc=meta.get('desc', ''),
            page=meta.get('page', ''),
            schema=meta.get('schema', ''),
        ) + header + '<main>' + body + '</main>' + footer + '\n</body>\n</html>\n'
        open(os.path.join(OUT, fn), 'w').write(doc)
        built.append(fn)

    # copy assets
    os.system(f'rm -rf {OUT}/assets && cp -r {ROOT}/assets {OUT}/assets')
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    print('built %d pages -> %s' % (len(built), OUT))
    print(', '.join(built))


if __name__ == '__main__':
    build()
