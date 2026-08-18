content = open('index.html', encoding='utf-8').read()

# Find where D_AMZ, D_FC, D_BL are defined
for var in ['D_AMZ', 'D_FC', 'D_BL', 'aprW', 'buildAmazonD', 'buildFCd', 'buildBLD']:
    idx = content.find(var)
    if idx != -1:
        snippet = content[idx:idx+300]
        with open(f'var_{var}.txt', 'w', encoding='utf-8') as f:
            f.write(snippet)
        print(f'{var} found at {idx}')
    else:
        print(f'{var} NOT found')
