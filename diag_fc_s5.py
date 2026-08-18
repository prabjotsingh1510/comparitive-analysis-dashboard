import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Find how f5 is wired
idx = html.find("f5:")
print('=== f5 wiring ===')
print(html[idx:idx+300])
print()

# 2. Find firstcryWfStages - what fields it reads from D.wf
idx2 = html.find('function firstcryWfStages(')
body_wf = html[idx2:idx2+2000]
print('=== firstcryWfStages body ===')
print(body_wf[:1000])
print()

# 3. Check D_FC.wf
m = re.search(r'const D_FC = (\{.*?\});', html, re.DOTALL)
fc = json.loads(m.group(1))
print('=== D_FC.wf ===')
print(fc.get('wf', 'MISSING'))
print()
print('=== D_FC.fun ===')
print(fc.get('fun', 'MISSING'))
print()

# 4. What fields does firstcryWfStages read from w=D.wf?
print('=== firstcryWfStages w. accesses ===')
seen = set()
for m2 in re.finditer(r'\bw\.([\w]+)', body_wf):
    k = m2.group(1)
    if k not in seen:
        seen.add(k)
        wf = fc.get('wf', {})
        present = isinstance(wf, dict) and k in wf
        print(f'  w.{k}: {"OK" if present else "MISSING"}')

# 5. What does renderChanS5 read from D for funnelMode='none'?
idx3 = html.find('function renderChanS5(')
body_s5 = html[idx3:idx3+6000]
print()
print('=== renderChanS5 D. field accesses ===')
seen2 = set()
for m3 in re.finditer(r'\bD\.([\w]+)', body_s5):
    k = m3.group(1)
    if k not in seen2:
        seen2.add(k)
        present = k in fc
        print(f'  D.{k}: {"OK" if present else "MISSING in D_FC"}')

# 6. Also check opts fields for firstcry
print()
print('=== opts fields used in renderChanS5 ===')
seen3 = set()
for m4 in re.finditer(r'\bopts\.([\w]+)', body_s5):
    k = m4.group(1)
    if k not in seen3:
        seen3.add(k)
        print(f'  opts.{k}')
