import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Extract renderChanS3 table row template
idx = html.find('function renderChanS3(')
snippet = html[idx:idx+4000]
print('=== renderChanS3 table row template ===')
# find the tbody innerHTML assignment
ti = snippet.find('tb.innerHTML=')
print(snippet[ti:ti+800])
print()

# 2. Check D_AMZ product fields - first 3 products
m = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
amz = json.loads(m.group(1))
print('=== First 3 D_AMZ products - all fields ===')
for p in amz['products'][:3]:
    print(p)
    print()

# 3. What revenue fields exist?
p0 = amz['products'][0]
print('=== Revenue-related fields in first product ===')
for k, v in p0.items():
    if 'rev' in k.lower() or 'cm2' in k.lower() or 'ebitda' in k.lower():
        print(f'  {k}: {v}')
