"""Replace D_AMZ in index.html with the freshly computed amz_new.json."""
import json, re

with open('amz_new.json', encoding='utf-8') as f:
    new_amz = json.load(f)

with open('index.html', encoding='utf-8') as f:
    html = f.read()

new_amz_js = json.dumps(new_amz, ensure_ascii=False, separators=(',', ':'))

# Find D_AMZ = {...};
START = 'const D_AMZ = {'
idx_start = html.find(START)
if idx_start == -1:
    print("ERROR: D_AMZ not found")
    exit(1)

# Walk braces to find end
depth = 0
i = idx_start + len('const D_AMZ = ')
while i < len(html):
    c = html[i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            idx_end = i + 1
            break
    i += 1

# idx_end should point just past the closing }
# The line ends with ';' then newline
# Find the semicolon
semi = html.find(';', idx_end)
if semi != -1 and semi < idx_end + 3:
    idx_end = semi + 1

old_block = html[idx_start:idx_end]
new_block = 'const D_AMZ = ' + new_amz_js + ';'

print(f'Old D_AMZ: {len(old_block):,} chars')
print(f'New D_AMZ: {len(new_block):,} chars')

html = html[:idx_start] + new_block + html[idx_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html written.')
print(f'Final size: {len(html):,} bytes')

# Quick sanity: re-parse
m = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
amz = json.loads(m.group(1))
t = amz['tot']
print(f'\nVerification:')
print(f'  products: {len(amz["products"])}')
print(f'  units: {t["units"]}')
print(f'  rev: {t["rev"]:,.0f}')
print(f'  cm2: {t["cm2"]:,.0f} ({t["cm2pct"]:.2f}%)')
print(f'  ebitda: {t["ebitda"]:,.0f} ({t["ebitdapct"]:.2f}%)')
print(f'  mktg: {t["mktg"]:,.0f}')
print(f'  GM%: {t["gmpct"]*100:.1f}%')
print(f'  stars: {amz["quad"]["star"]["n"]}, overhead: {amz["quad"]["overhead"]["n"]}, loss: {amz["quad"]["loss"]["n"]}')
