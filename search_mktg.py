import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Find every mention of mkt_pct, 90.5%, 74.5%, mktg_pct, mkt_pct_nr, mkt_pct_gross
patterns = ['mkt_pct_nr', 'mkt_pct_gross', '90.5', '74.5', '74.51', '90.47',
            'mkt_pct', 'mktg_pct', 'mktg/J.netrev', 'mktg/A.netrev',
            'mktg/J.rev', 'mktg/A.rev', 'w.mkt_pct', 'wf.mkt',
            'Mktg % (Col E)', 'Mktg % (Col AD)', '106.86', '89.76']

for pat in patterns:
    idx = 0
    while True:
        idx = html.find(pat, idx)
        if idx == -1:
            break
        print(f'{pat!r} at {idx}:')
        print('  ' + repr(html[max(0,idx-80):idx+100]))
        print()
        idx += 1
