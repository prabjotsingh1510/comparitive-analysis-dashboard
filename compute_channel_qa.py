"""
Computes the data needed to answer the 6 channel-level questions
using numbers already in the dashboard (website) + Amazon/FirstCry/Blinkit data objects.
"""
import json, re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Extract D (website)
m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
D = json.loads(m.group(1))

# Extract D_AMZ
m2 = re.search(r'const D_AMZ = (\{.*?\});', html, re.DOTALL)
AMZ = json.loads(m2.group(1))

# Extract D_FC
m3 = re.search(r'const D_FC = (\{.*?\});', html, re.DOTALL)
FC = json.loads(m3.group(1))

# Extract D_BL
m4 = re.search(r'const D_BL = (\{.*?\});', html, re.DOTALL)
BL = json.loads(m4.group(1))

print("=== ALL CHANNELS PARSED OK ===\n")

# ── Per-channel summary ──────────────────────────────────────────────────────
channels = [
    ('Website (Apr-Jun)', D['periods']['apr']['tot'], D['periods']['apr']['products'], D['periods']['apr']['cats']),
    ('Amazon',  AMZ['tot'], AMZ['products'], AMZ['cats']),
    ('FirstCry', FC['tot'], FC['products'], FC['cats']),
    ('Blinkit',  BL['tot'], BL['products'], BL['cats']),
]

for name, tot, prods, cats in channels:
    print(f"--- {name} ---")
    gmpct_val = tot.get('gmpct', tot.get('gm', 0) / tot.get('netrev', 1))
    if gmpct_val > 1: gmpct_val = gmpct_val / 100  # already pct
    print(f"  rev={tot['rev']:.0f}, units={tot['units']}, gm%={gmpct_val*100:.1f}%")
    print(f"  cm2={tot['cm2']:.0f} ({tot['cm2pct']:.1f}%), ebitda={tot['ebitda']:.0f} ({tot['ebitdapct']:.1f}%)")
    n_star = sum(1 for p in prods if p['quad']=='star')
    n_oh   = sum(1 for p in prods if p['quad']=='overhead')
    n_loss = sum(1 for p in prods if p['quad']=='loss')
    print(f"  star={n_star}, overhead={n_oh}, loss={n_loss}, total={len(prods)}")
    # top combo cat
    combo_cats = [c for c in cats if 'combo' in c['cat'].lower() or c['cat']=='Combo']
    if combo_cats:
        cc = combo_cats[0]
        print(f"  Combo cat: rev={cc['rev']:.0f}, cm2pct={cc['cm2pct']:.1f}%")
    print()

# ── Q1: Profitable products by channel (EBITDA+/CM2+) ───────────────────────
print("=== Q1: PROFITABLE PRODUCTS (EBITDA+ and CM2+) ===")
for name, tot, prods, cats in channels:
    stars = [p for p in prods if p['quad']=='star']
    star_rev = sum(p.get('rev',p.get('rev_t',0)) for p in stars)
    star_ebitda = sum(p.get('ebitda_t',p.get('ebitda_u',0)*p.get('units',1)) for p in stars)
    pct_rev = star_rev/tot['rev']*100 if tot['rev'] else 0
    print(f"  {name}: {len(stars)} profitable SKUs, rev={star_rev:.0f} ({pct_rev:.1f}% of channel), ebitda=+{star_ebitda:.0f}")
    def get_rev(p): return p.get('rev', p.get('rev_t', 0))
    for p in sorted(stars, key=lambda x:-get_rev(x))[:4]:
        print(f"    - {p.get('key',p.get('disp','?'))[:35]}: CM2={p.get('cm2_u',0):.0f}/u, EBITDA={p.get('ebitda_u',0):.0f}/u")
    print()

# ── Q2: Products with CM2+ potential (CM2+ but EBITDA-) ─────────────────────
print("=== Q2: POTENTIAL PRODUCTS TO IMPROVE CM2 (overhead-heavy = CM2+ but EBITDA-) ===")
for name, tot, prods, cats in channels:
    ohs = [p for p in prods if p['quad']=='overhead']
    oh_rev = sum(p.get('rev',p.get('rev_t',0)) for p in ohs)
    print(f"  {name}: {len(ohs)} overhead-heavy SKUs, rev={oh_rev:.0f}")
    def get_rev(p): return p.get('rev', p.get('rev_t', 0))
    for p in sorted(ohs, key=lambda x:-get_rev(x))[:4]:
        cm2_u = p.get('cm2_u', 0)
        ebitda_u = p.get('ebitda_u', 0)
        gap = abs(ebitda_u)
        print(f"    - {p.get('key',p.get('disp','?'))[:35]}: CM2=+{cm2_u:.0f}/u, EBITDA={ebitda_u:.0f}/u, gap={gap:.0f}/u")
    print()

# ── Q3: Products to discontinue ─────────────────────────────────────────────
print("=== Q3: PRODUCTS TO DISCONTINUE (CM2- and high burn relative to revenue) ===")
for name, tot, prods, cats in channels:
    losers = [p for p in prods if p['quad']=='loss']
    scored = []
    for p in losers:
        rev = p.get('rev', p.get('rev_t', 0))
        ebitda = p.get('ebitda_t', p.get('ebitda_u',0)*p.get('units',1))
        if rev > 0:
            burn_rate = abs(ebitda)/rev
            scored.append((p, burn_rate, rev, ebitda))
    scored.sort(key=lambda x:-x[1])
    print(f"  {name}: {len(losers)} loss-making SKUs")
    for p, br, rev, ebitda in scored[:4]:
        print(f"    - {p.get('key',p.get('disp','?'))[:35]}: EBITDA={ebitda:.0f}, burn={br*100:.0f}% of rev, units={p.get('units',0)}")
    print()

# ── Q4: Areas of focus — COGS, shipping, marketing, revenue ─────────────────
print("=== Q4: AREAS OF FOCUS — COGS / SHIPPING / MARKETING / REVENUE ===")
# Website
W_apr = D['periods']['apr']
W_jan = D['periods']['jan']
w_prods = W_apr['products']
w_tot   = W_apr['tot']
w_nr    = w_tot['netrev']
w_mktg  = w_tot['mktg']
w_ship  = sum(p.get('ship_u',0)*p['units'] for p in w_prods)
w_cogs  = w_nr - sum(p.get('gm_u',0)*p['units'] for p in w_prods)  # approximation
w_rev   = w_tot['rev']
print(f"  Website Apr-Jun:")
print(f"    Marketing: {w_mktg:.0f} = {w_mktg/w_nr*100:.1f}% of net rev")
print(f"    Shipping:  {w_ship:.0f} = {w_ship/w_nr*100:.1f}% of net rev")
print(f"    GM%: {w_tot['gm']/w_nr*100:.1f}%")

amz_tot = AMZ['tot']
print(f"  Amazon:")
print(f"    Marketing: {amz_tot['mktg']:.0f} = {amz_tot['mktg']/amz_tot['netrev']*100:.1f}% of net rev")
print(f"    GM%: {amz_tot['gmpct']*100:.1f}%")

fc_tot = FC['tot']
print(f"  FirstCry:")
print(f"    Firstcry Margin: {fc_tot['fcm']:.0f} = {fc_tot['fcm']/fc_tot['netrev']*100:.1f}% of net rev")
print(f"    GM%: {fc_tot['gmpct']*100:.1f}%")

bl_tot = BL['tot']
# BL marketing
bl_mktg = sum(p.get('mktg_u',0)*p['units'] for p in BL['products'])
bl_blmargin = sum(p.get('blmargin_u',0)*p['units'] for p in BL['products'])
print(f"  Blinkit:")
print(f"    Marketing: {bl_mktg:.0f} = {bl_mktg/bl_tot['netrev']*100:.1f}% of net rev")
print(f"    Blinkit Margin: {bl_blmargin:.0f} = {bl_blmargin/bl_tot['netrev']*100:.1f}% of net rev")
print(f"    GM%: {bl_tot['gmpct']*100:.1f}%")
print()

# ── Q5: Which products to focus on which channel ────────────────────────────
print("=== Q5: WHICH PRODUCTS TO FOCUS ON WHICH CHANNEL ===")
# Stars on each channel
for name, tot, prods, cats in channels:
    stars = sorted([p for p in prods if p['quad']=='star'], key=lambda x:-x.get('rev',x.get('rev_t',0)))
    ohs   = sorted([p for p in prods if p['quad']=='overhead'], key=lambda x:-x.get('rev',x.get('rev_t',0)))[:3]
    print(f"  {name} STARS: {[p.get('key',p.get('disp'))[:30] for p in stars]}")
    print(f"  {name} NEAR-STAR (overhead): {[p.get('key',p.get('disp'))[:30] for p in ohs]}")
    print()

# ── Q6: Marketing effort for potential products ──────────────────────────────
print("=== Q6: MARKETING EFFORT FOR POTENTIAL PRODUCTS ===")
# Potential = CM2+, EBITDA- (overhead-heavy) — these are CM2-healthy but overhead eats them
# increasing volume (not more mktg per unit) is the fix
for name, tot, prods, cats in channels:
    ohs = sorted([p for p in prods if p['quad']=='overhead'], key=lambda x:-x.get('rev',x.get('rev_t',0)))
    print(f"  {name}: overhead-heavy products (CM2+ — marketing is working; scale volume or reduce OH):")
    for p in ohs[:4]:
        rev = p.get('rev', p.get('rev_t', 0))
        print(f"    {p.get('key',p.get('disp','?'))[:35]}: rev={rev:.0f}, cm2_u={p.get('cm2_u',0):.0f}, oh_gap={abs(p.get('ebitda_u',0)):.0f}/u below ebitda breakeven")
    print()
