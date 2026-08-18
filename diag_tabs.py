import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Find all nav buttons (Website section tabs)
print('=== NAV BUTTONS (Website tabs) ===')
for m in re.finditer(r'data-tab="([^"]+)"', html):
    start = max(0, m.start()-60)
    snippet = html[start:m.end()+60]
    print(f'  data-tab={m.group(1)!r}  |  ...{snippet.strip()[:80]}...')

print()

# 2. Find show() function - what it does when a tab is clicked
print('=== show() function ===')
idx = html.find('function show(id)')
if idx != -1:
    print(html[idx:idx+400])
else:
    print('function show() NOT FOUND')

print()

# 3. Find renderers dict
print('=== renderers dict ===')
idx2 = html.find('const renderers=')
if idx2 == -1:
    idx2 = html.find('const renderers =')
if idx2 != -1:
    print(html[idx2:idx2+400])
else:
    # look for s2:renderS2
    idx3 = html.find('s2:renderS2')
    if idx3 == -1:
        idx3 = html.find('s2:')
    if idx3 != -1:
        print(html[max(0,idx3-50):idx3+400])
    else:
        print('renderers dict pattern not found')

print()

# 4. Check renderS2 exists
print('=== renderS2 presence ===')
if 'function renderS2(' in html:
    idx4 = html.find('function renderS2(')
    print('renderS2 found at:', idx4)
    print(html[idx4:idx4+100])
else:
    print('renderS2 NOT FOUND in html')

print()

# 5. Check sections s1-s6 exist
print('=== Section IDs ===')
for sid in ['s1','s2','s3','s4','s5','s6']:
    count = html.count(f'id="{sid}"')
    print(f'  id="{sid}" count: {count}')

print()

# 6. Check the chan-subnav buttons for Amazon/FC/BL
print('=== chan-subnav buttons ===')
for m in re.finditer(r'class="chan-subnav".*?</div>', html, re.DOTALL):
    snippet = m.group(0)[:300]
    print(snippet)
    print('---')
    break  # just first one
