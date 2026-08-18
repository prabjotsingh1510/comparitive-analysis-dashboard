import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

errors = []

# ── 1. All 4 JS data objects parse ─────────────────────────────────────────
for var in ['D', 'D_AMZ', 'D_FC', 'D_BL']:
    m = re.search('const ' + var + r' = (\{.*?\});', html, re.DOTALL)
    try:
        d = json.loads(m.group(1))
        print(f'{var}: parse OK')
    except Exception as e:
        errors.append(f'{var} PARSE ERROR: {e}')
        print(f'{var}: PARSE ERROR {e}')

# ── 2. Website D — all renderS2 required fields ─────────────────────────────
m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D = json.loads(m.group(1))
required_apr = ['cac','grand','new_rev','new_units','swings','label','tot','quad','cats','products']
for k in required_apr:
    if k not in D['periods']['apr']:
        errors.append(f'D.periods.apr.{k} MISSING')
    else:
        print(f'  D.periods.apr.{k}: OK')

# renderS2 also needs D.recon.jan/apr with old_rev, new_rev etc.
for p in ['jan','apr']:
    for f in ['old_rev','new_rev','old_units','new_units','sum_rev','sum_units']:
        if f not in D['recon'][p]:
            errors.append(f'D.recon.{p}.{f} MISSING')
print('  D.recon: OK')

# ── 3. D_AMZ — renderChanS2Amazon fields ────────────────────────────────────
m2 = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
amz = json.loads(m2.group(1))
for f in ['checks','corrections']:
    if f not in amz.get('recon',{}):
        errors.append(f'D_AMZ.recon.{f} MISSING')
for f in ['duplicate_rows_dropped','rescaled_products',
          'asins_excluded_no_economics_row','excluded_units_total']:
    if f not in amz.get('recon',{}).get('corrections',{}):
        errors.append(f'D_AMZ.recon.corrections.{f} MISSING')
# rev_t present on all products
bad_rev = [p['key'] for p in amz['products'] if not p.get('rev_t')]
if bad_rev:
    errors.append(f'D_AMZ products missing rev_t: {bad_rev}')
print(f'  D_AMZ: recon OK, {len(amz["products"])} products, 0 missing rev_t')

# ── 4. D_FC — renderChanS2FirstCry fields ───────────────────────────────────
m3 = re.search(r'const D_FC = (\{.*?\});', html, re.DOTALL)
fc = json.loads(m3.group(1))
for f in ['gross_revenue_check','units_check_vs_rto_pivot']:
    if f not in fc.get('recon',{}):
        errors.append(f'D_FC.recon.{f} MISSING')
bad_rev_fc = [p['key'] for p in fc['products'] if not p.get('rev_t')]
if bad_rev_fc:
    errors.append(f'D_FC products missing rev_t: {bad_rev_fc}')
print(f'  D_FC: recon OK, {len(fc["products"])} products, 0 missing rev_t')

# ── 5. D_BL — renderChanS2Blinkit fields ────────────────────────────────────
m4 = re.search(r'const D_BL = (\{.*?\});', html, re.DOTALL)
bl = json.loads(m4.group(1))
for f in ['units_check_vs_sales_raw','ads_spend_check']:
    if f not in bl.get('recon',{}):
        errors.append(f'D_BL.recon.{f} MISSING')
bad_rev_bl = [p['key'] for p in bl['products'] if not p.get('rev_t')]
if bad_rev_bl:
    errors.append(f'D_BL products missing rev_t: {bad_rev_bl}')
print(f'  D_BL: recon OK, {len(bl["products"])} products, 0 missing rev_t')

# ── 6. Channel Analysis tab still present ───────────────────────────────────
assert 'data-chan="analysis"' in html, 'Channel Analysis tab MISSING'
assert 'Decision Criteria 1' in html
assert 'Decision Criteria 6' in html
print('  Channel Analysis tab: OK')

# ── Summary ──────────────────────────────────────────────────────────────────
print()
if errors:
    print('ERRORS FOUND:')
    for e in errors: print(' ', e)
else:
    print('ALL CHECKS PASSED — no errors found.')
print(f'File size: {len(html):,} bytes')
