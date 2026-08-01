import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. D still parses
m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
d = json.loads(m.group(1))
print('D OK, apr units:', d['periods']['apr']['tot']['units'])
print('D OK, apr rev:', d['periods']['apr']['tot']['rev'])
print('D OK, apr cm2pct:', round(d['periods']['apr']['tot']['cm2pct'],2), '%')
print('D OK, apr ebitdapct:', round(d['periods']['apr']['tot']['ebitdapct'],2), '%')
print('D OK, apr cac:', d['periods']['apr']['cac'])

# 2. New button
assert 'data-chan="analysis"' in html, 'analysis button MISSING'
print('Channel Analysis button: OK')

# 3. Panel
assert 'id="chan-analysis"' in html, 'analysis panel MISSING'
print('Channel Analysis panel: OK')

# 4. Six Q headings
for i in range(1, 7):
    needle = 'Decision Criteria ' + str(i)
    assert needle in html, f'{needle} MISSING'
print('All 6 Decision Criteria headings: OK')

# 5. Panel hidden by default
assert 'id="chan-analysis" hidden' in html, 'panel not hidden by default'
print('Panel hidden attribute: OK')

print()
print('All checks passed.')
print('Final file size:', len(html), 'bytes')
