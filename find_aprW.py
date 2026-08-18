content = open('index.html', encoding='utf-8').read()

# Find where aprW is defined
idx = content.find('const aprW =')
if idx == -1:
    idx = content.find('aprW =')
if idx != -1:
    snippet = content[idx:idx+500]
    with open('aprW_def.txt', 'w', encoding='utf-8') as f:
        f.write(snippet)
    print(f'aprW found at {idx}')
else:
    print('aprW not found as assignment')

# Find what D.periods uses
idx2 = content.find('D.periods.apr')
if idx2 != -1:
    print(f'D.periods.apr used at {idx2}')
    
# Find buildAprD or similar 
for pat in ['aprW', 'buildWebD', 'D.periods', 'const apr', 'aprData']:
    idx3 = content.find(pat)
    if idx3 != -1:
        print(f'{pat} found at {idx3}: {repr(content[idx3:idx3+80])}')

# Find D_AMZ pattern to understand inter-channel data
idx4 = content.find('const D_AMZ')
idx5 = content.find('const D_FC')
idx6 = content.find('const D_BL')
print(f'D_AMZ at {idx4}, D_FC at {idx5}, D_BL at {idx6}')
