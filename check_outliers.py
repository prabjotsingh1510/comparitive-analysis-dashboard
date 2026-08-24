import json
with open('scatter_data.json', encoding='utf-8') as f:
    skus = json.load(f)

cm2s = sorted([s['cm2_u'] for s in skus])
edas = sorted([s['ebitda_u'] for s in skus])
print('CM2 extremes:', cm2s[:5], '...', cm2s[-5:])
print('EBITDA extremes:', edas[:5], '...', edas[-5:])
print()
for s in skus:
    if s['cm2_u'] < -500 or s['ebitda_u'] < -500:
        msg = 'OUTLIER ch=%s name=%s cm2=%.0f ebitda=%.0f units=%d' % (
            s['channel'], s['name'][:30], s['cm2_u'], s['ebitda_u'], s['units'])
        print(msg)
