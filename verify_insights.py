import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

errors = []

# 1. All data objects parse
for var in ['D', 'D_AMZ', 'D_FC', 'D_BL']:
    m = re.search('const ' + var + r' = (\{.*?\});', html, re.DOTALL)
    try:
        json.loads(m.group(1))
        print(f'{var}: parse OK')
    except Exception as e:
        errors.append(f'{var} parse error: {e}')

# 2. Insights tab DOM elements present
for eid in ['chan-insights', 'vis-A', 'vis-A-chart', 'vis-B-chart',
            'vis-C-chart', 'vis-D-chart', 'vis-E-chart',
            'vis-F-chart', 'vis-G-chart', 'vis-H-table', 'vis-I-chart']:
    if 'id="'+eid+'"' not in html:
        errors.append(f'DOM element id="{eid}" MISSING')

print('DOM elements: OK' if not [e for e in errors if 'DOM' in e] else 'DOM issues!')

# 3. Nav button present
if 'data-chan="insights"' in html:
    print('Nav button: OK')
else:
    errors.append('Nav button MISSING')

# 4. JS functions present
for fn in ['renderVisA', 'renderVisB', 'renderVisC', 'renderVisD',
           'renderVisE', 'renderVisF', 'renderVisG', 'renderVisH',
           'renderVisI', 'setupInsightsControls', 'renderInsights']:
    if 'function '+fn not in html:
        errors.append(f'JS function {fn} MISSING')
print('JS functions: OK' if not [e for e in errors if 'JS' in e] else 'JS issues!')

# 5. Existing tabs unchanged
for tid in ['s1','s2','s3','s4','s5','s6','a1','a2','f2','b2']:
    if 'id="'+tid+'"' not in html:
        errors.append(f'Existing tab "{tid}" MISSING')
print('Existing tabs: OK')

# 6. Existing renderers unchanged
for fn in ['renderS1','renderS2','renderS3','renderS4','renderS5','renderS6',
           'renderChanS1','renderChanS2Amazon','renderChanS5','renderChanS6']:
    if 'function '+fn not in html:
        errors.append(f'Existing renderer {fn} MISSING')
print('Existing renderers: OK')

# 7. CSS classes added
for cls in ['ins-grid2', 'ins-section', 'matrix-tag', 'matrix-cell']:
    if cls not in html:
        errors.append(f'CSS class {cls} MISSING')
print('CSS classes: OK')

print()
if errors:
    print('ERRORS:')
    for e in errors: print(' ', e)
else:
    print('ALL CHECKS PASSED')
print('File size:', len(html))
