import re, json

with open("index.html", 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const D = (\{.*?\});\n', html)
data = json.loads(m.group(1))

with open("website_D_full.json", 'w', encoding='utf-8') as f:
    json.dump(data, f)

print("recon.jan:", json.dumps(data['recon']['jan'], indent=1))
print("recon.apr:", json.dumps(data['recon']['apr'], indent=1))
print("\nperiods.jan.grand:", json.dumps(data['periods']['jan']['grand'], indent=1))
print("periods.apr.grand:", json.dumps(data['periods']['apr']['grand'], indent=1))
print("\nperiods.jan.cac:", data['periods']['jan']['cac'])
print("periods.apr.cac:", data['periods']['apr']['cac'])
print("periods.jan.new_rev:", data['periods']['jan']['new_rev'], "new_units:", data['periods']['jan']['new_units'])
print("periods.apr.new_rev:", data['periods']['apr']['new_rev'], "new_units:", data['periods']['apr']['new_units'])
print("\nswings[0] jan sample:", json.dumps(data['periods']['jan']['swings'][0], indent=1))
print("swings count jan:", len(data['periods']['jan']['swings']), "apr:", len(data['periods']['apr']['swings']))
print("\nproducts[0] sample (jan):", json.dumps(data['periods']['jan']['products'][0], indent=1))
