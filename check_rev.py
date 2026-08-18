import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

for var in ['D_AMZ', 'D_FC', 'D_BL']:
    m = re.search('const ' + var + r' = (\{.*?\});', html, re.DOTALL)
    d = json.loads(m.group(1))
    print(f'\n=== {var}: {len(d["products"])} products ===')
    print(f'  tot.rev = {d["tot"]["rev"]:,.0f}')
    for p in sorted(d['products'], key=lambda x: -x.get('rev_t',0))[:8]:
        print(f'  {p["key"]!r:30s} rev_t={p.get("rev_t",0):>12,.0f}  units={p.get("units",0):>5}  mrp={p.get("mrp",0):>6}')
