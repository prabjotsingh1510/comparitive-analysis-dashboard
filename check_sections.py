content = open('index.html', encoding='utf-8').read()

# Find where the JS data object is
idx = content.find('const D = {')
if idx == -1:
    print('JS data not found')
else:
    snippet = content[idx:idx+500]
    with open('js_start.txt', 'w', encoding='utf-8') as f:
        f.write(snippet)
    print('JS data found at index', idx)
    
# Check sections content
for sid in ['s1', 's2', 's3', 'a1', 'a2', 'a3', 'f1', 'b1']:
    idx3 = content.find(f'id="{sid}"')
    if idx3 != -1:
        snippet3 = content[idx3:idx3+150]
        print(f'{sid}: {repr(snippet3[:80])}')

# Check analysis section
anal_idx = content.find('chan-analysis')
snippet4 = content[anal_idx:anal_idx+200]
with open('anal_check.txt', 'w', encoding='utf-8') as f:
    f.write(snippet4)
print('Analysis check written')
