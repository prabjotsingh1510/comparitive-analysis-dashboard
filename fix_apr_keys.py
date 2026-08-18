import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D = json.loads(m.group(1))

jan_prods = D['periods']['jan']['products']
apr_prods = D['periods']['apr']['products']

# Build normalised lookup: strip all apostrophe/quote variants and dashes
def normalise(s):
    return (s
        .replace('\u2013', '-')   # en-dash -> hyphen
        .replace('\u2014', '-')   # em-dash -> hyphen
        .replace('\u2018', "'")   # left single quote -> apostrophe
        .replace('\u2019', "'")   # right single quote -> apostrophe
        .replace('\u201c', '"')   # left double quote
        .replace('\u201d', '"')   # right double quote
        .strip()
    )

# Build a map from normalised jan k -> original jan k
jan_norm_map = {}
for p in jan_prods:
    jan_norm_map[normalise(p['k'])] = p['k']

# Fix apr product keys where they don't match jan but would after normalisation
fixed = 0
for p in apr_prods:
    norm_k = normalise(p['k'])
    if p['k'] not in {jp['k'] for jp in jan_prods} and norm_k in jan_norm_map:
        old_k = p['k']
        new_k = jan_norm_map[norm_k]
        print(f'Fixing key:')
        print(f'  OLD: {old_k!r}')
        print(f'  NEW: {new_k!r}')
        p['k'] = new_k
        fixed += 1

print(f'\nFixed {fixed} apr product keys.')

# Write back
new_js = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
start_tok = 'const D = {'
idx_s = html.find(start_tok)
depth, i = 0, idx_s + len('const D = ')
while i < len(html):
    c = html[i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0: idx_e = i + 1; break
    i += 1
s = html.find(';', idx_e)
if s != -1 and s < idx_e + 3: idx_e = s + 1

new_block = 'const D = ' + new_js + ';'
html = html[:idx_s] + new_block + html[idx_e:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Written. Size:', len(html))

# Verify the 3 products now resolve
m2 = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D2 = json.loads(m2.group(1))
amap2 = {p['k']: p for p in D2['periods']['apr']['products']}
top10 = sorted(D2['periods']['jan']['products'], key=lambda x: -x['rev'])[:10]
print('\n=== Verification: top 10 Jan, Apr lookup ===')
for p in top10:
    a = amap2.get(p['k'])
    print(f'  {p["key"]!r:20s}  jan_rev={p["rev"]:>10,.0f}  apr_rev={""+str(round(a["rev"],0)) if a else "STILL MISSING":>10}')
