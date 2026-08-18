content = open('index.html', encoding='utf-8').read()

# Find the main channel switch JS
idx = content.find('data-chan')
# Find the JS that handles the channel navigation
chan_js_idx = content.find("data-chan='website'")
if chan_js_idx == -1:
    chan_js_idx = content.find('chanSwitch')
if chan_js_idx == -1:
    # Find the event listener that handles chan switching
    chan_js_idx = content.find('chan-switch')
    
print(f'chan-switch CSS at: {chan_js_idx}')

# Look for where the JS switches channels
for pat in ['chan-panel', 'chan-website', 'chanPanel', 'showChan', 'switchChan']:
    idx2 = content.rfind(pat)
    if idx2 != -1:
        print(f'{pat} last at {idx2}: {repr(content[idx2:idx2+100])}')
    else:
        print(f'{pat} not found')

# Find where the main top nav handles channel switching
# This should be a click handler
click_handler_idx = content.find("data-chan']")
if click_handler_idx == -1:
    click_handler_idx = content.find("dataset.chan")
print(f'dataset.chan handler at: {click_handler_idx}')
if click_handler_idx != -1:
    snippet = content[click_handler_idx-200:click_handler_idx+300]
    with open('chan_handler.txt', 'w', encoding='utf-8') as f:
        f.write(snippet)
    print('Written chan_handler.txt')
