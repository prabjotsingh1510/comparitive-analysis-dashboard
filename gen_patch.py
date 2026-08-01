"""
Reads full_replacement.json and index.html,
patches D.periods.apr, D.bridge, D.flips, D.recon, the s5 apr wf,
D.facts star_both and persistent_loss, and D.recon.
Writes updated index.html.
"""
import json, re

with open('full_replacement.json', encoding='utf-8') as f:
    rep = json.load(f)

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── Helper: compact JSON serialiser that matches JS style ───────────────────
def js(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

# ═══════════════════════════════════════════════════════════════════════════
# 1.  Replace D.periods.apr  (the entire value of "apr":{...} inside D)
# ═══════════════════════════════════════════════════════════════════════════
apr_json = js(rep['apr_period'])
# The key in the JS object is "apr":{...},
# followed by "},"  (closing periods then comma then "bridge")
# We need to locate the exact span.  Use the known stable anchor strings.
APR_START = '"apr":{"label":"Apr\u2013Jun 2026"'
# Find start
idx_start = html.find(APR_START)
if idx_start == -1:
    print("ERROR: could not find apr start marker")
    exit(1)

# Walk forward matching braces to find the end of the apr object
depth = 0
i = idx_start + len('"apr":')  # start at the {
while i < len(html):
    c = html[i]
    if c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            idx_end = i + 1
            break
    i += 1

old_apr_block = html[idx_start:idx_end]
new_apr_block = '"apr":' + apr_json
print(f'APR block: old={len(old_apr_block)} chars -> new={len(new_apr_block)} chars')
html = html[:idx_start] + new_apr_block + html[idx_end:]

# ═══════════════════════════════════════════════════════════════════════════
# 2.  Replace D.bridge
# ═══════════════════════════════════════════════════════════════════════════
bridge_json = js(rep['bridge'])
BRIDGE_START = '"bridge":['
idx_b = html.find(BRIDGE_START)
if idx_b == -1:
    print("ERROR: bridge not found")
    exit(1)
depth = 0
i = idx_b + len('"bridge":')
while i < len(html):
    c = html[i]
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            idx_b_end = i + 1
            break
    i += 1
old_bridge = html[idx_b:idx_b_end]
new_bridge = '"bridge":' + bridge_json
print(f'BRIDGE: old={len(old_bridge)} -> new={len(new_bridge)}')
html = html[:idx_b] + new_bridge + html[idx_b_end:]

# ═══════════════════════════════════════════════════════════════════════════
# 3.  Replace D.flips
# ═══════════════════════════════════════════════════════════════════════════
flips_json = js(rep['flips'])
FLIPS_START = '"flips":['
idx_f = html.find(FLIPS_START)
if idx_f == -1:
    print("ERROR: flips not found")
    exit(1)
depth = 0
i = idx_f + len('"flips":')
while i < len(html):
    c = html[i]
    if c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            idx_f_end = i + 1
            break
    i += 1
old_flips = html[idx_f:idx_f_end]
new_flips = '"flips":' + flips_json
print(f'FLIPS: old={len(old_flips)} -> new={len(new_flips)}')
html = html[:idx_f] + new_flips + html[idx_f_end:]

# ═══════════════════════════════════════════════════════════════════════════
# 4.  Replace D.recon (the whole object)
# ═══════════════════════════════════════════════════════════════════════════
recon_json = js(rep['recon'])
RECON_START = '"recon":{"jan":{'
idx_r = html.find(RECON_START)
if idx_r == -1:
    print("ERROR: recon not found")
    exit(1)
depth = 0
i = idx_r + len('"recon":')
while i < len(html):
    c = html[i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            idx_r_end = i + 1
            break
    i += 1
old_recon = html[idx_r:idx_r_end]
new_recon = '"recon":' + recon_json
print(f'RECON: old={len(old_recon)} -> new={len(new_recon)}')
html = html[:idx_r] + new_recon + html[idx_r_end:]

# ═══════════════════════════════════════════════════════════════════════════
# 5.  Replace the apr waterfall inside D.s5.apr.wf
# ═══════════════════════════════════════════════════════════════════════════
apr_wf_json = js(rep['apr_wf'])
# Find  "apr":{"wf":{...}  inside s5
WF_ANCHOR = '"apr":{"wf":{"gross":'
idx_wf = html.find(WF_ANCHOR)
if idx_wf == -1:
    print("ERROR: apr wf anchor not found")
    exit(1)
# The wf object is the inner {}
i = idx_wf + len('"apr":{"wf":')  # points to the { of wf
depth = 0
while i < len(html):
    c = html[i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            idx_wf_end = i + 1
            break
    i += 1
old_wf = html[idx_wf + len('"apr":{"wf":'):idx_wf_end]
new_wf_block = '"apr":{"wf":' + apr_wf_json
print(f'APR WF: old wf obj={len(old_wf)} chars')
html = html[:idx_wf] + new_wf_block + html[idx_wf_end:]

# ═══════════════════════════════════════════════════════════════════════════
# 6.  Update D.facts.star_both and persistent_loss
# ═══════════════════════════════════════════════════════════════════════════
sb_json = js(rep['star_both'])
PL_json = js(rep['persistent_loss'])

STAR_BOTH_START = '"star_both":['
idx_sb = html.find(STAR_BOTH_START)
if idx_sb != -1:
    depth = 0
    i = idx_sb + len('"star_both":')
    while i < len(html):
        c = html[i]
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                idx_sb_end = i + 1
                break
        i += 1
    old_sb = html[idx_sb:idx_sb_end]
    new_sb = '"star_both":' + sb_json
    print(f'STAR_BOTH: old={len(old_sb)} -> new={len(new_sb)}')
    html = html[:idx_sb] + new_sb + html[idx_sb_end:]
else:
    print("WARNING: star_both not found")

PERS_LOSS_START = '"persistent_loss":['
idx_pl = html.find(PERS_LOSS_START)
if idx_pl != -1:
    depth = 0
    i = idx_pl + len('"persistent_loss":')
    while i < len(html):
        c = html[i]
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                idx_pl_end = i + 1
                break
        i += 1
    old_pl = html[idx_pl:idx_pl_end]
    new_pl = '"persistent_loss":' + PL_json
    print(f'PERSISTENT_LOSS: old={len(old_pl)} -> new={len(new_pl)}')
    html = html[:idx_pl] + new_pl + html[idx_pl_end:]
else:
    print("WARNING: persistent_loss not found")

# ═══════════════════════════════════════════════════════════════════════════
# 7.  Update star_both_revshare fact
# ═══════════════════════════════════════════════════════════════════════════
# recompute: star_both rev / (jan_rev + apr_rev) * 100
combined_rev = 2614540.52 + rep['apr_period']['tot']['rev']
star_both_rev = sum(s['rev'] for s in rep['star_both'])
new_share = star_both_rev / combined_rev * 100
OLD_SHARE_PAT = r'"star_both_revshare":[0-9.]+'
new_share_str = f'"star_both_revshare":{round(new_share,10)}'
m = re.search(OLD_SHARE_PAT, html)
if m:
    print(f'STAR_BOTH_REVSHARE: old={m.group()} -> new={new_share_str}')
    html = html[:m.start()] + new_share_str + html[m.end():]
else:
    print("WARNING: star_both_revshare not found")

# ═══════════════════════════════════════════════════════════════════════════
# 8.  Update facts.mpd, facts.pd, facts.ck etc from persistent_loss list
# ═══════════════════════════════════════════════════════════════════════════
# Load full_replacement persistent_loss entries
pl = {p['key']: p for p in rep['persistent_loss']}

# Helper to update a named fact sub-object
def update_fact_key(html_str, fact_key, new_ebitda, new_jcm2p, new_acm2p):
    # pattern: "mpd":{"key":"magic paint dust","jrev":...,"arev":...,"rev":...,"ebitda":...
    # We update: ebitda, jcm2p, acm2p
    # Find the fact block
    start_pat = f'"{fact_key}":{{"key":'
    idx = html_str.find(start_pat)
    if idx == -1:
        return html_str, False
    # find end of this object
    depth = 0
    i = idx + len(f'"{fact_key}":')
    while i < len(html_str):
        c = html_str[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                idx_end = i + 1
                break
        i += 1
    old_block = html_str[idx:idx_end]
    # Update ebitda
    new_block = re.sub(r'"ebitda":-?[0-9.]+', f'"ebitda":{round(new_ebitda,5)}', old_block)
    # Update jcm2p
    new_block = re.sub(r'"jcm2p":-?[0-9.]+', f'"jcm2p":{round(new_jcm2p,2)}', new_block)
    # Update acm2p
    new_block = re.sub(r'"acm2p":-?[0-9.]+', f'"acm2p":{round(new_acm2p,5)}', new_block)
    return html_str[:idx] + new_block + html_str[idx_end:], old_block != new_block

# Also update rev for each fact
def update_fact_rev(html_str, fact_key, new_rev):
    start_pat = f'"{fact_key}":{{"key":'
    idx = html_str.find(start_pat)
    if idx == -1:
        return html_str
    depth = 0
    i = idx + len(f'"{fact_key}":')
    while i < len(html_str):
        c = html_str[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                idx_end = i + 1
                break
        i += 1
    old_block = html_str[idx:idx_end]
    new_block = re.sub(r'"rev":[0-9.]+', f'"rev":{round(new_rev,2)}', old_block, count=1)
    return html_str[:idx] + new_block + html_str[idx_end:]

# Map fact keys to persistent_loss product keys
fact_map = {
    'mpd': 'magic paint dust',
    'pd': 'Playdough',
    'ck': 'Canvas Kit',
    'act': 'Activity Pack',
    'mdp': 'Mini Dessert Party',
    'sr': 'SR',
    'abc': 'ABC Kit',
}

for fact_k, prod_key in fact_map.items():
    if prod_key in pl:
        p = pl[prod_key]
        html, changed = update_fact_key(html, fact_k, p['ebitda'], p['jcm2p'], p['acm2p'])
        if changed:
            print(f'Updated fact.{fact_k} ({prod_key}): ebitda={p["ebitda"]:.2f}')
        html = update_fact_rev(html, fact_k, p['rev'])

# ═══════════════════════════════════════════════════════════════════════════
# 9.  Update top3_burn fact
# ═══════════════════════════════════════════════════════════════════════════
top3_keys = ['magic paint dust', 'Playdough', 'Canvas Kit']
top3_burn = sum(pl[k]['ebitda'] for k in top3_keys if k in pl)
TOP3_PAT = r'"top3_burn":-?[0-9.]+'
m = re.search(TOP3_PAT, html)
if m:
    new_top3 = f'"top3_burn":{round(top3_burn, 10)}'
    print(f'TOP3_BURN: old={m.group()} -> new={new_top3}')
    html = html[:m.start()] + new_top3 + html[m.end():]
else:
    print("WARNING: top3_burn not found")

# ═══════════════════════════════════════════════════════════════════════════
# Write output
# ═══════════════════════════════════════════════════════════════════════════
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('\nindex.html written successfully.')
print(f'Final file size: {len(html):,} bytes')
