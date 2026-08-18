import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

def load_var(var):
    m = re.search('const ' + var + r' = (\{.*?\});', html, re.DOTALL)
    return json.loads(m.group(1))

D_AMZ = load_var('D_AMZ')
D_FC  = load_var('D_FC')
D_BL  = load_var('D_BL')

# ── Find renderChanS5 and see what fields it accesses on D ──────────────────
idx = html.find('function renderChanS5(')
body_s5 = html[idx:idx+8000]

print('=== renderChanS5 D. field accesses ===')
seen = set()
for m2 in re.finditer(r'\bD\.([\w.]+)', body_s5):
    k = m2.group(1).split('.')[0]
    if k not in seen:
        seen.add(k)
        print(f'  D.{k}')

print()
print('=== renderChanS5 opts. field accesses ===')
seen2 = set()
for m3 in re.finditer(r'\bopts\.([\w]+)', body_s5):
    k = m3.group(1)
    if k not in seen2:
        seen2.add(k)
        print(f'  opts.{k}')

print()
# ── Check D_AMZ fields needed by renderChanS5 ──────────────────────────────
print('=== D_AMZ keys vs renderChanS5 needs ===')
for k in ['wf','fun','tot','products','pareto','recon']:
    present = k in D_AMZ
    print(f'  D_AMZ.{k}: {"OK" if present else "MISSING"}')

# Check D_AMZ.fun sub-fields
print()
print('D_AMZ.fun:', D_AMZ.get('fun', 'MISSING'))

# Check D_AMZ.wf sub-fields
print()
print('D_AMZ.wf:', 'OK' if 'wf' in D_AMZ else 'MISSING')
if 'wf' in D_AMZ:
    print(' wf keys:', list(D_AMZ['wf'].keys()))

print()
# ── Check what amazonWfStages reads from D.wf ──────────────────────────────
idx2 = html.find('function amazonWfStages(')
body_amz_wf = html[idx2:idx2+2000]
print('=== amazonWfStages D.wf field accesses ===')
seen3 = set()
for m4 in re.finditer(r'\bw\.([\w]+)', body_amz_wf):
    k = m4.group(1)
    if k not in seen3:
        seen3.add(k)
        wf = D_AMZ.get('wf', {})
        present = k in wf
        print(f'  w.{k}: {"OK" if present else "MISSING (wf has: " + str(list(wf.keys())) + ")"}')

print()
# ── Check Blinkit ─────────────────────────────────────────────────────────
print('=== D_BL keys vs renderChanS5 needs ===')
for k in ['wf','fun','tot','products']:
    present = k in D_BL
    print(f'  D_BL.{k}: {"OK" if present else "MISSING"}')

print()
# ── Check blinkitWfStages reads from D.wf ──────────────────────────────────
idx3 = html.find('function blinkitWfStages(')
body_bl_wf = html[idx3:idx3+2000]
print('=== blinkitWfStages D.wf field accesses ===')
seen4 = set()
for m5 in re.finditer(r'\bw\.([\w]+)', body_bl_wf):
    k = m5.group(1)
    if k not in seen4:
        seen4.add(k)
        wf = D_BL.get('wf', {})
        present = k in wf
        print(f'  w.{k}: {"OK" if present else "MISSING (wf has: " + str(list(wf.keys())) + ")"}')

print()
# ── Check FirstCry renderChanS2FirstCry ─────────────────────────────────────
print('=== renderChanS2FirstCry full body scan ===')
idx4 = html.find('function renderChanS2FirstCry(')
body_fc = html[idx4:idx4+6000]

# Find all field accesses on r (=D_FC passed in)
print('r. accesses (r = D_FC):')
seen5 = set()
for m6 in re.finditer(r'\br\.([\w.]+)', body_fc):
    k = m6.group(1).split('.')[0]
    if k not in seen5:
        seen5.add(k)
        present = k in D_FC.get('recon', {})
        fc_top  = k in D_FC
        print(f'  r.{k}: D_FC.{k}={"OK" if fc_top else "MISSING"}  D_FC.recon.{k}={"OK" if present else "MISSING"}')

print()
# Print D_FC.recon
print('D_FC.recon:', json.dumps(D_FC.get('recon', 'MISSING'), indent=2)[:500])

print()
# Check what EXACT sub-fields renderChanS2FirstCry uses on r.recon
print('renderChanS2FirstCry accesses on r.recon.*:')
for m7 in re.finditer(r'\br\.recon\.([\w.]+)', body_fc):
    k = m7.group(1)
    rc = D_FC.get('recon', {})
    val = rc.get(k, 'MISSING')
    print(f'  r.recon.{k}: {repr(val)[:80]}')

# Also check r.units_check_vs_rto_pivot fields
print()
print('r.units_check_vs_rto_pivot.* accesses:')
for m8 in re.finditer(r'\br\.units_check_vs_rto_pivot\.([\w]+)', body_fc):
    k = m8.group(1)
    ucheck = D_FC.get('recon', {}).get('units_check_vs_rto_pivot', {})
    print(f'  .{k}: {"OK - "+str(ucheck.get(k)) if k in ucheck else "MISSING from D_FC.recon.units_check_vs_rto_pivot"}')
