import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D = json.loads(m.group(1))

jan_prods = D['periods']['jan']['products']
apr_prods = D['periods']['apr']['products']

# Build apr map keyed by p.k
amap = {p['k']: p for p in apr_prods}

# top 10 jan by revenue
top10 = sorted(jan_prods, key=lambda x: -x['rev'])[:10]

print('=== Top 10 Jan products — key lookup in Apr ===')
for p in top10:
    a = amap.get(p['k'])
    print(f'  key={p["k"]!r}')
    print(f'    jan rev={p["rev"]:,.0f}   apr found={"YES rev="+str(round(a["rev"],0)) if a else "NO"}')
    if not a:
        # Try to find it by matching just the first part of k (before ||)
        short_key = p['k'].split('||')[0]
        candidates = [ak for ak in amap if ak.split('||')[0] == short_key]
        print(f'    -> candidates by short key {short_key!r}: {candidates}')
    print()
