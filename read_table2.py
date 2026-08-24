import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

start = html.find('<h2>Per-Product Breakdown</h2>')
table_start = html.find('<div class="tw"><table>', start)
table_end = html.find('</table></div>', table_start) + len('</table></div>')

section = html[start:table_end]

# Extract all rows
rows = re.findall(r'<tr>\s*(.*?)\s*</tr>', section, re.DOTALL)
print(f'Total rows found: {len(rows)} (1 header + data rows)')

# Parse data rows
products = []
for row in rows[1:]:  # skip header
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    if not cells:
        continue
    # Clean HTML
    def clean(s):
        s = re.sub(r'<[^>]+>', '', s).strip()
        s = s.replace('₹', '').replace(',', '').replace('/u', '').strip()
        return s

    name = clean(cells[0]) if len(cells) > 0 else ''
    units = clean(cells[1]) if len(cells) > 1 else ''
    rev_gst = clean(cells[2]) if len(cells) > 2 else ''
    rev_nogst = clean(cells[3]) if len(cells) > 3 else ''
    mktg = clean(cells[4]) if len(cells) > 4 else ''
    mktg_pct_gst = clean(cells[5]) if len(cells) > 5 else ''
    mktg_pct_nogst = clean(cells[6]) if len(cells) > 6 else ''
    cm2 = clean(cells[7]) if len(cells) > 7 else ''

    # Parse numbers
    try: rev_gst_n = float(rev_gst)
    except: rev_gst_n = 0
    try: units_n = int(units)
    except: units_n = 0
    try: mktg_n = float(mktg)
    except: mktg_n = 0
    try: cm2_n = float(cm2)
    except: cm2_n = 0

    products.append({
        'name': name,
        'units': units_n,
        'rev_gst': rev_gst_n,
        'mktg': mktg_n,
        'cm2_u': cm2_n,
        'mktg_pct_nogst': mktg_pct_nogst,
    })
    print(f"  {name!r:35s} units={units_n:4d}  rev={rev_gst_n:>10,.0f}  cm2={cm2_n:>6.0f}/u  mktg={mktg_n:>10,.0f}")

print(f'\nTotal products: {len(products)}')

# Check the min/max CM2 for colour scale
cm2_vals = [p['cm2_u'] for p in products if p['cm2_u'] != 0]
print(f'CM2/u range: {min(cm2_vals):.0f} to {max(cm2_vals):.0f}')
print(f'Max revenue: {max(p["rev_gst"] for p in products):,.0f}')

# Show table_start and table_end positions
print()
print('table_start:', table_start)
print('table_end:', table_end)
print('section_start (h2):', start)
