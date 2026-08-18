import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Extract D and check D.recon
m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D = json.loads(m.group(1))

print('=== D.recon ===')
print(json.dumps(D.get('recon', 'MISSING'), indent=2))

print()
print('=== D.periods.jan keys ===')
print(list(D['periods']['jan'].keys()))

print()
print('=== D.periods.apr keys ===')
print(list(D['periods']['apr'].keys()))

print()
# 2. Check for any JS errors: look for undefined field access in renderS2
idx = html.find('function renderS2(')
renderS2_body = html[idx:idx+4000]
print('=== renderS2 body (first 2000 chars) ===')
print(renderS2_body[:2000])

print()
# 3. Check renderChanS2Amazon
idx2 = html.find('function renderChanS2Amazon(')
if idx2 != -1:
    body = html[idx2:idx2+3000]
    print('=== renderChanS2Amazon - fields accessed ===')
    # Find all D. field accesses
    for m2 in re.finditer(r'D\.[A-Za-z_.]+', body):
        print(' ', m2.group(0))
else:
    print('renderChanS2Amazon NOT FOUND')

print()
# 4. Check what D_AMZ.recon looks like
m3 = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
amz = json.loads(m3.group(1))
print('=== D_AMZ.recon ===')
print(json.dumps(amz.get('recon', 'MISSING'), indent=2)[:1000])

print()
# 5. Check renderChanS2Amazon accesses recon.checks specifically
idx3 = html.find('function renderChanS2Amazon(')
if idx3 != -1:
    body = html[idx3:idx3+5000]
    # find r.checks, r.corrections etc
    for field in ['checks', 'corrections', 'rescaled_products', 'asins_excluded',
                  'duplicate_rows', 'excluded_units']:
        if field in body:
            print(f'renderChanS2Amazon uses: {field!r}')
        else:
            print(f'renderChanS2Amazon MISSING: {field!r}')
    print()
    # Check specific data access pattern
    for m4 in re.finditer(r'r\.(corrections|checks|rescaled_products|asins_excluded_no_economics_row)[.\[]', body):
        print('  access:', m4.group(0))
