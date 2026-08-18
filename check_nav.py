content = open('index.html', encoding='utf-8').read()

# Check the chan-switch / setupChannel logic
# Find where channels are set up
for pat in ['setupChannel', 'data-chan', 'chan-switch']:
    idx = content.find(pat)
    if idx != -1:
        print(f'{pat} at {idx}: {repr(content[idx:idx+200])}')
    else:
        print(f'{pat} not found')

# Check the nav for mktgspend button
nav_idx = content.find('data-chan="mktgspend"')
print(f'mktgspend nav button at: {nav_idx}')
if nav_idx != -1:
    print(repr(content[nav_idx-50:nav_idx+100]))

# Check if the setupChannel call for mktgspend uses wrong ID
bl_idx = content.find("setupChannel('chan-mktgspend'")
print(f'setupChannel mktgspend at: {bl_idx}')

# Check the main nav buttons
nav_start = content.find('<nav id="chan-switch"')
if nav_start == -1:
    nav_start = content.find('id="chan-switch"')
if nav_start != -1:
    nav_snippet = content[nav_start:nav_start+600]
    with open('nav_snippet.txt', 'w', encoding='utf-8') as f:
        f.write(nav_snippet)
    print('Written nav_snippet.txt')
