content = open('index.html', encoding='utf-8').read()

# Check Q1 area
idx = content.find('Profitable SKUs')
if idx == -1:
    print('Q1 header not found!')
else:
    snippet = content[idx-300:idx+1000]
    with open('q1_check.txt', 'w', encoding='utf-8') as f:
        f.write(snippet)
    print('Written to q1_check.txt')

# Also check nav buttons
nav_idx = content.find('chan-switch')
snippet2 = content[nav_idx:nav_idx+600]
with open('nav_check.txt', 'w', encoding='utf-8') as f:
    f.write(snippet2)
print('Nav check written')

# Check if metrics is gone
if 'chan-metrics' in content:
    print('WARNING: chan-metrics still in HTML!')
elif 'Important Metrics' in content:
    print('WARNING: Important Metrics text still in HTML!')
else:
    print('OK: Important Metrics tab removed')

if 'chan-mktgspend' in content:
    print('OK: mktgspend panel present')
else:
    print('WARNING: mktgspend panel missing!')
