with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Find "Per-Product Breakdown"
idx = html.find('Per-Product Breakdown')
if idx == -1:
    idx = html.find('per-product')
    if idx == -1:
        idx = html.lower().find('per-product')
print('Per-Product Breakdown at:', idx)
if idx != -1:
    print(html[max(0,idx-300):idx+800])
    print()

# Also search for related terms
for term in ['Per Product', 'per product', 'product breakdown', 'Product Breakdown',
             'All products', 'product deep dive', 'renderChanS3', 'renderS3']:
    i = html.find(term)
    if i != -1:
        print(f'{term!r} found at {i}')
        print(html[max(0,i-50):i+200])
        print('---')
