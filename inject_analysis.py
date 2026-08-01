"""Injects the channel decision analysis tab into index.html."""
import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Add 5th button to chan-switch
OLD_BTN = '<button role="tab" aria-selected="false" data-chan="blinkit">Blinkit</button>'
NEW_BTN = '<button role="tab" aria-selected="false" data-chan="blinkit">Blinkit</button>\n    <button role="tab" aria-selected="false" data-chan="analysis">Channel Analysis</button>'
html = html.replace(OLD_BTN, NEW_BTN, 1)

# 2. Build the analysis panel HTML
PANEL = r'''
<div class="chan-panel" id="chan-analysis" hidden>
<header class="top">
  <div class="top-in">
    <h1>Channel Decision Analysis — Apr–Jun 2026</h1>
    <p class="sub">Six strategic questions answered channel-by-channel using verified unit-economics data. All figures ₹.</p>
  </div>
</header>
<div class="wrap" style="padding-top:26px">
'''

# Q1 block
PANEL += r'''
<!-- ===== Q1 ===== -->
<div class="qa" style="--qac:var(--good);margin-bottom:12px">
  <div class="q">Decision Criteria 1</div>
  <h3>Profitable products channel-wise — EBITDA+ &amp; CM2+</h3>
  <div class="ans">
    <p>A product is only genuinely profitable when <b>both CM2 and EBITDA are positive</b> — meaning it earns above its direct costs <em>and</em> its overhead share.</p>
    <div class="tw" style="margin-top:10px"><table>
      <thead><tr><th>Channel</th><th>Profitable SKUs</th><th>Rev from stars</th><th>% of channel rev</th><th>Combined EBITDA</th><th>Top SKUs (CM2/unit → EBITDA/unit)</th></tr></thead>
      <tbody>
        <tr><td><b>Website</b></td><td>8 of 81</td><td>₹2.56 L</td><td>10.6%</td><td><span class="up">+₹10,283</span></td>
          <td class="muted" style="font-size:11px">SFP+JB (₹230→₹1), FP8+AR+CB (₹275→₹46), SJ+SFP+CB (₹325→₹96), FP3+B3+AR (₹252→₹23)</td></tr>
        <tr><td><b>Amazon</b></td><td>5 of 39</td><td>₹1.58 L</td><td>2.3%</td><td><span class="up">+₹18,311</span></td>
          <td class="muted" style="font-size:11px">FP8+CB (₹338→₹109), MPD+JB (₹459→₹229), SFP+JB (₹355→₹125), FP3+JB (₹425→₹196)</td></tr>
        <tr><td><b>FirstCry</b></td><td>10 of 39</td><td>₹1.56 L</td><td>18.0%</td><td><span class="up">+₹13,359</span></td>
          <td class="muted" style="font-size:11px">FP8+CB (₹404→₹175), FP3 (₹234→₹5), B3+AR (₹335→₹106), SFP+JB (₹320→₹91)</td></tr>
        <tr><td><b>Blinkit</b></td><td>0 of 7</td><td>—</td><td>0%</td><td><span class="down">None</span></td>
          <td class="muted" style="font-size:11px">No product clears EBITDA breakeven this quarter</td></tr>
      </tbody>
    </table></div>
    <p style="margin-top:10px"><b>Pattern:</b> Combos and brush-add-on bundles dominate every profitable list. A single acquisition cost spread over a higher-value basket is what tips these products into the green — the same gross margin stock (≈65–84%) exists on loss-making SKUs too. FirstCry has the highest star-count share (18% of revenue) because its catalogue skews toward combos; Blinkit has zero stars because its double cost structure (marketing + platform margin together absorb 93% of net revenue) leaves no room yet.</p>
  </div>
</div>
'''

# Q2 block
PANEL += r'''
<!-- ===== Q2 ===== -->
<div class="qa" style="--qac:var(--warn);margin-bottom:12px">
  <div class="q">Decision Criteria 2</div>
  <h3>Potential products for improving CM2</h3>
  <div class="ans">
    <p>The <b>overhead-heavy quadrant</b> (CM2+ but EBITDA−) is the clearest improvement opportunity. These products already cover every direct cost — the only thing pulling EBITDA below zero is the flat overhead allocation. Three levers apply: <b>(a) increase volume</b> so fixed overheads spread across more units, <b>(b) raise price</b> to widen CM2/unit, or <b>(c) reduce the overhead allocation</b> by cutting the cost it represents.</p>
    <div class="tw" style="margin-top:10px"><table>
      <thead><tr><th>Channel</th><th>SKU</th><th>CM2/unit</th><th>EBITDA/unit</th><th>Gap to EBITDA breakeven</th><th>Lever</th></tr></thead>
      <tbody>
        <tr><td rowspan="3"><b>Website</b></td>
          <td>FP8+CB</td><td class="n"><span class="up">+₹78</span></td><td class="n"><span class="down">−₹152</span></td><td class="n">₹152/unit</td><td class="muted">Volume or price</td></tr>
        <tr><td>FP8, B8, CB (Little Artist Kit)</td><td class="n"><span class="up">+₹188</span></td><td class="n"><span class="down">−₹42</span></td><td class="n">₹42/unit</td><td class="muted">Closest to breakeven — prioritise volume</td></tr>
        <tr><td>SFP+CB</td><td class="n"><span class="up">+₹55</span></td><td class="n"><span class="down">−₹174</span></td><td class="n">₹174/unit</td><td class="muted">CM2 thin — also look at pricing</td></tr>
        <tr><td rowspan="3"><b>Amazon</b></td>
          <td>SFP+CB</td><td class="n"><span class="up">+₹203</span></td><td class="n"><span class="down">−₹26</span></td><td class="n">₹26/unit</td><td class="muted">Closest to EBITDA+ on Amazon</td></tr>
        <tr><td>FP8 (8-colour Finger Paints)</td><td class="n"><span class="up">+₹220</span></td><td class="n"><span class="down">−₹9</span></td><td class="n">₹9/unit</td><td class="muted">Near-breakeven — volume push justified</td></tr>
        <tr><td>Magic Paint Dust</td><td class="n"><span class="up">+₹15</span></td><td class="n"><span class="down">−₹214</span></td><td class="n">₹214/unit</td><td class="muted">Thin CM2 — pricing fix needed first</td></tr>
        <tr><td rowspan="3"><b>FirstCry</b></td>
          <td>Stamp Kit</td><td class="n"><span class="up">+₹185</span></td><td class="n"><span class="down">−₹44</span></td><td class="n">₹44/unit</td><td class="muted">Volume</td></tr>
        <tr><td>Jumbo Brushes (JB)</td><td class="n"><span class="up">+₹157</span></td><td class="n"><span class="down">−₹72</span></td><td class="n">₹72/unit</td><td class="muted">Volume</td></tr>
        <tr><td>Dessert Party</td><td class="n"><span class="up">+₹171</span></td><td class="n"><span class="down">−₹58</span></td><td class="n">₹58/unit</td><td class="muted">Volume</td></tr>
        <tr><td><b>Blinkit</b></td>
          <td>B8 Crayons</td><td class="n"><span class="up">+₹18</span></td><td class="n"><span class="down">−₹211</span></td><td class="n">₹211/unit</td><td class="muted">CM2 too thin — pricing before volume</td></tr>
      </tbody>
    </table></div>
  </div>
</div>
'''

# Q3 block
PANEL += r'''
<!-- ===== Q3 ===== -->
<div class="qa" style="--qac:var(--crit);margin-bottom:12px">
  <div class="q">Decision Criteria 3</div>
  <h3>Products to discontinue based on current inventory &amp; marketing</h3>
  <div class="ans">
    <p>Discontinue candidates are products where <b>EBITDA loss as a % of revenue is extreme</b> — meaning for every rupee of revenue generated, most or all of it is burned back in losses. The priority is products with (a) very high burn rate AND (b) low inventory-clearing urgency (low volume, not core catalogue).</p>
    <div class="tw" style="margin-top:10px"><table>
      <thead><tr><th>Channel</th><th>Product</th><th>Units</th><th>EBITDA loss</th><th>Loss as % of rev</th><th>Action</th></tr></thead>
      <tbody>
        <tr><td rowspan="3"><b>Website</b></td>
          <td>Activity Pack (Digital Print)</td><td class="n">62</td><td class="n"><span class="down">−₹65,964</span></td><td class="n">1,162%</td>
          <td class="muted">Delist — digital product losing ₹12/rev rupee</td></tr>
        <tr><td>MPD+AR+JB (3-item bundle)</td><td class="n">3</td><td class="n"><span class="down">−₹22,502</span></td><td class="n">400%</td>
          <td class="muted">Delist — 3 units, enormous per-unit loss</td></tr>
        <tr><td>Mini Dessert Party</td><td class="n">26</td><td class="n"><span class="down">−₹37,747</span></td><td class="n">377%</td>
          <td class="muted">Reprice or delist — marketing cost ₹1,306/unit</td></tr>
        <tr><td rowspan="3"><b>Amazon</b></td>
          <td>Mini's Magic Dough Lab</td><td class="n">70</td><td class="n"><span class="down">−₹2.64 L</span></td><td class="n">629%</td>
          <td class="muted">Delist — negative net revenue after discounts</td></tr>
        <tr><td>Glue</td><td class="n">114</td><td class="n"><span class="down">−₹71,070</span></td><td class="n">156%</td>
          <td class="muted">Delist — CM1 negative (loses before any ads)</td></tr>
        <tr><td>Touch &amp; Feel (solo)</td><td class="n">32</td><td class="n"><span class="down">−₹36,819</span></td><td class="n">128%</td>
          <td class="muted">Delist or bundle only — negative net revenue</td></tr>
        <tr><td rowspan="2"><b>FirstCry</b></td>
          <td>Chubby Brushes (CB solo)</td><td class="n">44</td><td class="n"><span class="down">−₹16,087</span></td><td class="n">79%</td>
          <td class="muted">Bundle with paints — solo margin too thin for FC fees</td></tr>
        <tr><td>B8 Crayons (solo)</td><td class="n">67</td><td class="n"><span class="down">−₹24,172</span></td><td class="n">78%</td>
          <td class="muted">Bundle or delist — FC margin eats all gross profit</td></tr>
        <tr><td rowspan="2"><b>Blinkit</b></td>
          <td>Dino Art Kit</td><td class="n">274</td><td class="n"><span class="down">−₹1.01 L</span></td><td class="n">92%</td>
          <td class="muted">Pause ads, clear current inventory then reassess</td></tr>
        <tr><td>Unicorn Art Kit</td><td class="n">228</td><td class="n"><span class="down">−₹83,594</span></td><td class="n">92%</td>
          <td class="muted">Pause ads, clear current inventory then reassess</td></tr>
      </tbody>
    </table></div>
    <p style="margin-top:8px"><b>Inventory rule:</b> if current stock can be cleared in &lt;4 weeks at organic sell-through, stop all paid marketing immediately and let inventory deplete. Only reorder if the economics are fixed (price increase or cost reduction).</p>
  </div>
</div>
'''

# Q4 block
PANEL += r'''
<!-- ===== Q4 ===== -->
<div class="qa" style="--qac:var(--s1);margin-bottom:12px">
  <div class="q">Decision Criteria 4</div>
  <h3>Area of focus — COGS, shipping cost, marketing, increasing revenue</h3>
  <div class="ans">
    <div class="tw" style="margin-top:4px"><table>
      <thead><tr><th>Channel</th><th>Gross margin %</th><th>Marketing as % of net rev</th><th>Platform fee % of net rev</th><th>Shipping % of net rev</th><th>Primary lever</th></tr></thead>
      <tbody>
        <tr><td><b>Website</b></td><td class="n">79%</td><td class="n"><b style="color:var(--crit)">90.5%</b></td><td class="n">—</td><td class="n">18.1%</td>
          <td><b>Marketing efficiency.</b> GM is healthy. Marketing alone exceeds CM1 and is the single reason the channel loses money. CAC/conversion fix is the #1 lever.</td></tr>
        <tr><td><b>Amazon</b></td><td class="n">69%</td><td class="n"><b style="color:var(--crit)">39.3%</b></td><td class="n">—</td><td class="n">~15%*</td>
          <td><b>Marketing + referral fee.</b> Amazon Ads are 39% of net rev. No referral fee is in this workbook — adding it makes the picture materially worse. Fix: cut ad spend on low converters (see Section 5).</td></tr>
        <tr><td><b>FirstCry</b></td><td class="n">64%</td><td class="n">—</td><td class="n"><b style="color:var(--crit)">91.7%</b></td><td class="n">—</td>
          <td><b>Platform margin.</b> FirstCry's own fee absorbs nearly all net revenue. Only combos survive. Fix: push higher-MRP combos, negotiate fee rate, or reduce low-MRP solo SKUs on this channel.</td></tr>
        <tr><td><b>Blinkit</b></td><td class="n">78%</td><td class="n"><b style="color:var(--crit)">45.8%</b></td><td class="n"><b style="color:var(--crit)">42.6%</b></td><td class="n">11.4%</td>
          <td><b>Double cost problem.</b> Marketing (46%) + Blinkit Margin (43%) = 89% of net rev — neither alone explains the loss. Both need to move. Short-term: cut all paid campaigns on loss-making SKUs. Medium-term: renegotiate margin rate or raise sell prices.</td></tr>
      </tbody>
    </table></div>
    <p style="margin-top:8px;font-size:12.5px;color:var(--ink-2)">*Amazon shipping is bundled in FBA fees — estimated from pick-pack + inbound + storage lines.</p>
    <p style="margin-top:8px"><b>COGS note:</b> Gross margin is 64–79% across all channels — COGS is <em>not</em> the primary problem anywhere. Every rupee of improvement in COGS helps, but cutting marketing spend in half delivers 5–10× more EBITDA impact per rupee than a 10% COGS reduction would.</p>
    <p><b>Revenue note:</b> Increasing revenue on loss-making SKUs <em>without</em> fixing unit economics just scales the loss. Revenue growth only helps when the product being scaled is CM2-positive. Use the star/overhead-heavy lists from Q1 and Q2 as the target list for revenue investment.</p>
  </div>
</div>
'''

# Q5 block
PANEL += r'''
<!-- ===== Q5 ===== -->
<div class="qa" style="--qac:var(--s2);margin-bottom:12px">
  <div class="q">Decision Criteria 5</div>
  <h3>Which products to focus on which channel</h3>
  <div class="ans">
    <p>Channel economics differ enough that the right product for Website is not always the right product for Blinkit. The framework: <b>Star products</b> = invest on this channel. <b>Overhead-heavy</b> = worth pushing if you can add volume. <b>Loss-making</b> = do not spend to grow until fixed.</p>
    <div class="tw" style="margin-top:10px"><table>
      <thead><tr><th>Product / Range</th><th>Website</th><th>Amazon</th><th>FirstCry</th><th>Blinkit</th></tr></thead>
      <tbody>
        <tr><td><b>FP8+CB (Finger Paints + Chubby Brushes)</b></td>
          <td><span class="tag" style="--tc:var(--warn)">Overhead-heavy</span></td>
          <td><span class="tag" style="--tc:var(--good)">Star ✓</span></td>
          <td><span class="tag" style="--tc:var(--good)">Star ✓</span></td>
          <td>Not listed</td></tr>
        <tr><td><b>SFP+JB (Starter Pack + Jumbo Brushes)</b></td>
          <td><span class="tag" style="--tc:var(--good)">Star ✓</span></td>
          <td><span class="tag" style="--tc:var(--good)">Star ✓</span></td>
          <td><span class="tag" style="--tc:var(--good)">Star ✓</span></td>
          <td>Not listed</td></tr>
        <tr><td><b>FP8+AR+CB (Masterpiece Set)</b></td>
          <td><span class="tag" style="--tc:var(--good)">Star ✓</span></td>
          <td>Not listed</td>
          <td>Not listed</td>
          <td>Not listed</td></tr>
        <tr><td><b>FP3+B3+AR (Starter Pack combo)</b></td>
          <td><span class="tag" style="--tc:var(--good)">Star ✓</span></td>
          <td>Not listed</td>
          <td>Not listed</td>
          <td>Not listed</td></tr>
        <tr><td><b>SFP+CB (Starter + Chubby Brushes)</b></td>
          <td><span class="tag" style="--tc:var(--warn)">Overhead-heavy</span></td>
          <td><span class="tag" style="--tc:var(--warn)">Overhead-heavy</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td>Not listed</td></tr>
        <tr><td><b>Magic Paint Dust (solo)</b></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--warn)">Overhead-heavy</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td>Not listed</td></tr>
        <tr><td><b>SFP / Starter Finger Paint (solo)</b></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td></tr>
        <tr><td><b>B3 / Playdough (solo)</b></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td></tr>
        <tr><td><b>Sensory Playdough / Dessert Party mini's</b></td>
          <td>Not listed</td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td>
          <td><span class="tag" style="--tc:var(--warn)">Overhead-heavy</span></td>
          <td><span class="tag" style="--tc:var(--crit)">Loss</span></td></tr>
      </tbody>
    </table></div>
    <p style="margin-top:10px"><b>Key insight:</b> <b>SFP+JB is the only product that is Star on Website, Amazon AND FirstCry simultaneously</b> — it is the single safest product to push with marketing budget across channels. FP8+CB is Star on Amazon and FirstCry but only overhead-heavy on Website, suggesting Website pricing or volume needs adjustment. Solo hero SKUs (SFP, Magic Paint Dust, Playdough solo) are loss-making everywhere — the mechanism that rescues them is always the same: bundle with accessories to spread the acquisition cost.</p>
  </div>
</div>
'''

# Q6 block
PANEL += r'''
<!-- ===== Q6 ===== -->
<div class="qa" style="--qac:var(--s1);margin-bottom:12px">
  <div class="q">Decision Criteria 6</div>
  <h3>Marketing effort — if there is a potential product</h3>
  <div class="ans">
    <p>Marketing spend is only justified when the product can <b>convert the traffic into CM2-positive sales</b>. The framework below classifies every product by what marketing action is appropriate.</p>
    <div class="grid2" style="margin-top:10px">
      <div class="prob" style="--pc:var(--good)">
        <h4>Star products — Scale ad spend</h4>
        <p>These are CM2+ and EBITDA+. Every incremental unit sold generates real profit. Increase budget here first. Protect their page quality, reviews and in-stock position. <b>Website:</b> SFP+JB, FP8+AR+CB, SJ+SFP+CB, FP3+B3+AR. <b>Amazon:</b> FP8+CB, MPD+JB, SFP+JB, FP3+JB. <b>FirstCry:</b> FP8+CB, FP3, B3+AR, SFP+JB.</p>
      </div>
      <div class="prob" style="--pc:var(--warn)">
        <h4>Overhead-heavy products — Controlled spend</h4>
        <p>CM2 is positive so marketing <em>is</em> recovering its direct cost — the overhead allocation is the only drag. Run spend at current efficiency but don't scale until volume pushes EBITDA positive. Monitor CM2/unit weekly. <b>Priority near-breakeven on Amazon:</b> FP8 (gap ₹9/unit), SFP+CB (gap ₹26/unit).</p>
      </div>
      <div class="prob" style="--pc:var(--s1)">
        <h4>Loss-making but high-conversion products — Fix page, then spend</h4>
        <p>CM2 is negative but the product page converts well (see Website Section 5). Cutting spend here hides the problem. The fix is pricing or COGS — once CM2/unit turns positive, these are ready for spend. Do not increase spend before that point.</p>
      </div>
      <div class="prob" style="--pc:var(--crit)">
        <h4>Loss-making with low conversion — Cut spend immediately</h4>
        <p>These products lose money AND the traffic they attract does not convert. Every ad rupee spent here amplifies the loss with no upside. Cut or pause all paid marketing. Clear current inventory through organic / markdown. <b>Immediate cuts on Website:</b> Activity Pack, MPD+AR+JB, Mini Dessert Party (solo), Canvas Art Board. <b>Amazon:</b> Magic Dough Lab, Glue, Touch &amp; Feel solo, Preschool Kit. <b>Blinkit:</b> all 6 listed SKUs.</p>
      </div>
    </div>
    <div class="tk" style="--tkc:var(--warn);margin-top:14px">
      <h3>Rule of thumb for new or re-launched products</h3>
      <p>Before committing paid budget to any product, verify: <b>(1)</b> CM1/unit is positive (it earns above COGS + ops cost at full price). <b>(2)</b> CM2/unit is positive at a realistic CAC (₹700 on Website, ₹595–₹700 range). <b>(3)</b> A conversion rate target is set (minimum 3% session→order on Website; 2% session→order on Amazon). If any of these three conditions fail, resolve it before spending on traffic — spending to find the failure costs money and teaches nothing useful.</p>
    </div>
  </div>
</div>
'''

# close the panel
PANEL += r'''
</div><!-- /.wrap -->
</div><!-- /#chan-analysis -->
'''

# 3. Inject the panel into HTML just before the tip div
INJECT_BEFORE = '<div class="tip" id="tip"></div>'
if INJECT_BEFORE not in html:
    print('ERROR: injection anchor not found')
    exit(1)

html = html.replace(INJECT_BEFORE, PANEL + INJECT_BEFORE, 1)
print('Panel injected, length:', len(PANEL))

# 4. Wire up the new channel switch in JS — extend the existing chan-switch handler
# The existing handler already uses:
#   document.querySelectorAll('.chan-panel').forEach(p=>p.hidden = p.id !== 'chan-'+b.dataset.chan);
# So it will automatically show/hide #chan-analysis — no JS change needed.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html written. Final size:', len(html))
