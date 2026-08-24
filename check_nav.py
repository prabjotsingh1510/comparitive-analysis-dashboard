with open('index.html', encoding='utf-8') as f:
    html = f.read()

import re
# Show chan-switch buttons
idx = html.find('aria-label="Sales channel"')
print('Chan switch area:')
print(html[idx:idx+600])
print()
print('File size:', len(html))
print()
# Check for existing insights
for keyword in ['insights', 'mktgspend', 'chan-insights']:
    found = html.find(keyword)
    print(f'{keyword!r} at: {found}')
