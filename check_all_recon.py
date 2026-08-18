import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── Check D.periods.apr missing fields ─────────────────────────────────────
m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D = json.loads(m.group(1))

print('=== D.periods.apr missing fields ===')
apr = D['periods']['apr']
jan = D['periods']['jan']
print('apr keys:', sorted(apr.keys()))
print('jan keys:', sorted(jan.keys()))
missing_apr = [k for k in jan.keys() if k not in apr]
print('MISSING from apr:', missing_apr)

print()
# ── Check what renderS2 reads from A (=D.periods.apr) ───────────────────────
idx = html.find('function renderS2(')
body = html[idx:idx+10000]
# find all A. accesses
print('renderS2 A. accesses:')
seen = set()
for m2 in re.finditer(r'\bA\.(\w+)', body):
    k = m2.group(1)
    if k not in seen:
        seen.add(k)
        present = k in apr
        print(f'  A.{k}  ->  {"OK" if present else "MISSING"}')

print()
# ── Check renderChanS2Amazon needed fields ──────────────────────────────────
idx2 = html.find('function renderChanS2Amazon(')
body2 = html[idx2:idx2+6000]
print('renderChanS2Amazon r. accesses (r = D_AMZ):')
m3 = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
amz = json.loads(m3.group(1))
seen2 = set()
for m4 in re.finditer(r'\bD\.(recon|checks|fun|wf|pareto|products|tot|cats|quad|channel|periodLabel)', body2):
    k = m4.group(1)
    if k not in seen2:
        seen2.add(k)
        present = k in amz
        print(f'  D_AMZ.{k}  ->  {"OK" if present else "MISSING"}')

# Also check r. accesses (r = D passed in as param)
for m5 in re.finditer(r'\br\.(recon|checks|corrections|fun|wf|pareto)', body2):
    k = m5.group(1)
    if k not in seen2:
        seen2.add(k)
        print(f'  r.{k} (direct access)')

print()
# ── Check renderChanS2FirstCry ───────────────────────────────────────────────
idx3 = html.find('function renderChanS2FirstCry(')
body3 = html[idx3:idx3+4000]
m6 = re.search(r'const D_FC = (\{.*?\});', html, re.DOTALL)
fc = json.loads(m6.group(1))
print('renderChanS2FirstCry D_FC accesses:')
seen3 = set()
for m7 in re.finditer(r'\bD\.(recon|fun|wf|pareto|tot|products|cats|quad)', body3):
    k = m7.group(1)
    if k not in seen3:
        seen3.add(k)
        present = k in fc
        print(f'  D_FC.{k}  ->  {"OK" if present else "MISSING"}')

print()
# ── Check renderChanS2Blinkit ────────────────────────────────────────────────
idx4 = html.find('function renderChanS2Blinkit(')
body4 = html[idx4:idx4+4000]
m8 = re.search(r'const D_BL = (\{.*?\});', html, re.DOTALL)
bl = json.loads(m8.group(1))
print('renderChanS2Blinkit D_BL accesses:')
seen4 = set()
for m9 in re.finditer(r'\bD\.(recon|fun|wf|pareto|tot|products|cats|quad)', body4):
    k = m9.group(1)
    if k not in seen4:
        seen4.add(k)
        present = k in bl
        print(f'  D_BL.{k}  ->  {"OK" if present else "MISSING"}')
