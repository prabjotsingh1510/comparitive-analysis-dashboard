"""Build scatter plot JSON from all channel per-unit product data."""
import json, os

def num(v):
    try: return float(v) if v not in (None, '', '-', u'\u2014', 'N/A') else 0.0
    except: return 0.0

skus = []

# ── AMAZON (amz_final.json has pre-computed per-unit fields) ──────────────
with open('amz_final.json') as f:
    amz = json.load(f)
for p in amz.get('products', []):
    units = num(p.get('units'))
    if units <= 0:
        continue
    name = str(p.get('key') or p.get('disp') or '')[:40].strip()
    skus.append({
        'name':     name,
        'channel':  'Amazon',
        'cm2_u':    round(num(p.get('cm2_u')), 1),
        'ebitda_u': round(num(p.get('ebitda_u')), 1),
        'units':    int(units),
        'netrev':   round(num(p.get('netrev_t')), 0),
        'quad':     p.get('quad', 'loss'),
    })

# ── WEBSITE (website_D_full.json) ────────────────────────────────────────
with open('website_D_full.json') as f:
    web = json.load(f)
web_prods = web.get('products', [])
for p in web_prods:
    units = num(p.get('units'))
    if units <= 0:
        continue
    name = str(p.get('code') or p.get('name') or p.get('key') or '')[:40].strip()
    skus.append({
        'name':     name,
        'channel':  'Website',
        'cm2_u':    round(num(p.get('cm2_u')), 1),
        'ebitda_u': round(num(p.get('ebitda_u')), 1),
        'units':    int(units),
        'netrev':   round(num(p.get('netrev_t') or p.get('rev_gst')), 0),
        'quad':     p.get('quad', 'loss'),
    })

# ── FIRSTCRY (inject_channel_data.py produces fc products, check new_D_data.json or all_channel_data.json) ──
# Use raw data from all_channel_data.json with correct per-unit calculation
with open('all_channel_data.json') as f:
    all_d = json.load(f)

fc_raw = all_d.get('firstcry', [])
for p in fc_raw:
    units = num(p.get('Units (3 months)'))
    if units <= 0:
        continue
    name = str(p.get('ProductName') or p.get('VendorStyleCode') or '')[:40].strip()
    cm2_t  = num(p.get('CM2'))
    ebitda_t = num(p.get('EBITDA'))
    netrev_t = num(p.get('Total Net Revenue') or p.get('Net Revenue without GST'))
    cm2_u    = cm2_t / units
    ebitda_u = ebitda_t / units
    quad = 'star' if cm2_u > 0 and ebitda_u > 0 else ('overhead' if cm2_u > 0 else 'loss')
    skus.append({
        'name':     name,
        'channel':  'FirstCry',
        'cm2_u':    round(cm2_u, 1),
        'ebitda_u': round(ebitda_u, 1),
        'units':    int(units),
        'netrev':   round(netrev_t, 0),
        'quad':     quad,
    })

# ── BLINKIT (bl_fixed.json or all_channel_data.json) ──────────────────────
bl_raw = all_d.get('blinkit', [])
for p in bl_raw:
    units = num(p.get('Units (3 months)'))
    if units <= 0:
        continue
    name = str(p.get('item_name') or p.get('P. Breakdown') or '')[:40].strip()
    cm2_t    = num(p.get('CM2'))
    ebitda_t = num(p.get('EBITDA'))
    netrev_t = num(p.get('Net Revenue without GST'))
    cm2_u    = cm2_t / units
    ebitda_u = ebitda_t / units
    quad = 'star' if cm2_u > 0 and ebitda_u > 0 else ('overhead' if cm2_u > 0 else 'loss')
    skus.append({
        'name':     name,
        'channel':  'Blinkit',
        'cm2_u':    round(cm2_u, 1),
        'ebitda_u': round(ebitda_u, 1),
        'units':    int(units),
        'netrev':   round(netrev_t, 0),
        'quad':     quad,
    })

# ── Summary ───────────────────────────────────────────────────────────────
from collections import Counter
ch_counts = Counter(s['channel'] for s in skus)
quad_counts = Counter(s['quad'] for s in skus)
print('Total SKUs:', len(skus))
print('Per channel:', dict(ch_counts))
print('Per quadrant:', dict(quad_counts))
cm2s   = [s['cm2_u']    for s in skus]
ebitdas = [s['ebitda_u'] for s in skus]
units   = [s['units']    for s in skus]
print(f'CM2/u range:    {min(cm2s):.1f} to {max(cm2s):.1f}')
print(f'EBITDA/u range: {min(ebitdas):.1f} to {max(ebitdas):.1f}')
print(f'Units range:    {min(units)} to {max(units)}')
print()
print('Sample Amazon:')
for s in [x for x in skus if x['channel']=='Amazon'][:5]:
    print(f"  {s['name']}: cm2={s['cm2_u']}, ebitda={s['ebitda_u']}, units={s['units']}, quad={s['quad']}")
print('Sample Website:')
for s in [x for x in skus if x['channel']=='Website'][:5]:
    print(f"  {s['name']}: cm2={s['cm2_u']}, ebitda={s['ebitda_u']}, units={s['units']}, quad={s['quad']}")

with open('scatter_data.json', 'w', encoding='utf-8') as f:
    json.dump(skus, f, ensure_ascii=False)
print('\nSaved scatter_data.json with', len(skus), 'SKUs')
