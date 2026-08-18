import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── Confirm renderChanS2FirstCry function signature ─────────────────────────
idx = html.find('function renderChanS2FirstCry(')
body = html[idx:idx+8000]
print('=== renderChanS2FirstCry first 600 chars ===')
print(body[:600])

print()
# ── Confirm renderChanS2Blinkit function signature ──────────────────────────
idx2 = html.find('function renderChanS2Blinkit(')
body2 = html[idx2:idx2+600]
print('=== renderChanS2Blinkit first 600 chars ===')
print(body2)

print()
# ── Confirm setupChannel wiring for amazon/firstcry/blinkit ─────────────────
idx3 = html.find('setupChannel(')
while idx3 != -1:
    snippet = html[idx3:idx3+250]
    print('setupChannel call:', snippet[:250])
    print()
    idx3 = html.find('setupChannel(', idx3+1)

print()
# ── Check exactly what renderChanS5 is called with for amazon ───────────────
# look for a5:
idx4 = html.find("a5:")
if idx4 != -1:
    print('a5 setup:', html[idx4:idx4+300])

# ── Check D_AMZ.wf current value ────────────────────────────────────────────
m = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
amz = json.loads(m.group(1))
print('\nD_AMZ.wf:', amz.get('wf', 'MISSING'))
print('D_AMZ.fun:', amz.get('fun', 'MISSING'))

# ── Check D_BL.wf and D_BL.fun current value ────────────────────────────────
m2 = re.search(r'const D_BL = (\{.*?\});', html, re.DOTALL)
bl = json.loads(m2.group(1))
print('\nD_BL.wf:', bl.get('wf', 'MISSING'))
print('D_BL.fun:', bl.get('fun', 'MISSING'))

# ── Get full renderChanS2FirstCry to see how it uses r ──────────────────────
# look for what r.X it accesses (r = D passed in to renderChanS2FirstCry(D))
print()
print('=== all r.FIELD accesses in renderChanS2FirstCry ===')
seen = set()
for m3 in re.finditer(r'\br\.([\w]+)', body):
    k = m3.group(1)
    if k not in seen:
        seen.add(k)
        print(f'  r.{k}')
