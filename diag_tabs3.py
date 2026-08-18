import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── Website D: check renderS2 required fields ──────────────────────────────
m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D = json.loads(m.group(1))

print('=== Website D.periods.apr keys ===')
apr = D['periods']['apr']
print(list(apr.keys()))
print()

# renderS2 needs: D.periods.jan.cac, D.periods.apr.cac
# D.periods.jan.grand, D.periods.apr.grand
# D.periods.jan.products (find(...))
# D.recon.jan, D.recon.apr
# D.bridge, D.flips
# D.periods.jan.tot, D.periods.apr.tot
# D.s5 (for s5 section)
# D.facts

required_d = ['cac','grand','new_rev','new_units','swings']
for k in required_d:
    in_jan = k in D['periods']['jan']
    in_apr = k in D['periods']['apr']
    print(f'  D.periods.jan.{k}: {"OK" if in_jan else "MISSING"}')
    print(f'  D.periods.apr.{k}: {"OK" if in_apr else "MISSING"}')

print()
# Check D.s5
print('D.s5 present:', 's5' in D)
if 's5' in D:
    print('D.s5 keys:', list(D['s5'].keys()))
    print('D.s5.apr keys:', list(D['s5']['apr'].keys()) if 'apr' in D['s5'] else 'MISSING')

print()
# Check D.bridge, D.flips
print('D.bridge present:', 'bridge' in D, '- len:', len(D.get('bridge',[])))
print('D.flips present:', 'flips' in D, '- len:', len(D.get('flips',[])))
print('D.facts present:', 'facts' in D)

print()
# ── Amazon: renderChanS2Amazon needs D_AMZ.recon ──────────────────────────
m2 = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
amz = json.loads(m2.group(1))
print('=== D_AMZ keys ===')
print(list(amz.keys()))
print('D_AMZ.recon:', amz.get('recon', 'MISSING'))

print()
# ── Check renderS2 for D.periods.apr.cac usage ─────────────────────────────
idx = html.find('function renderS2(')
renderS2_body = html[idx:idx+8000]
# find all A. and J. field accesses
for m3 in re.finditer(r'[JAj]\.(?:cac|grand|new_rev|new_units|swings|products)', renderS2_body):
    print('renderS2 accesses:', m3.group(0))

print()
# ── Check renderChanS2Amazon for exact field accesses ──────────────────────
idx2 = html.find('function renderChanS2Amazon(')
body2 = html[idx2:idx2+5000]
print('=== renderChanS2Amazon recon accesses ===')
for m4 in re.finditer(r'r\.(recon|checks|corrections|rescaled_products|asins_excluded_no_economics_row|duplicate_rows_dropped|excluded_units_total)[.\[]?', body2):
    print(' ', m4.group(0)[:60])
