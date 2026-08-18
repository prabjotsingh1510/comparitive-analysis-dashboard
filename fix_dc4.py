content = open('index.html', encoding='utf-8').read()

# Find and replace the entire DC4 tbody
old_dc4_tbody = '''<tbody>
        <tr><td><b>Website</b></td><td class="n">79.1%%</td><td class="n"><b style="color:var(--crit)">90.5%%</b></td><td class="n">&mdash;</td><td class="n">~71.4%*</td>
          <td><b>Marketing efficiency.</b> GM is healthy at 79.1%. Marketing alone exceeds CM1 and is the single reason the channel loses money. CAC/conversion fix is the #1 lever.</td></tr>
        <tr><td><b>Amazon</b></td><td class="n">77.7%%</td><td class="n"><b style="color:var(--crit)">28.7%%</b></td><td class="n">&mdash;</td><td class="n">~15%*</td>
          <td><b>Marketing + referral fee.</b> Amazon Ads are 28.7% of net rev. Fix: cut ad spend on low converters (see Section 5).</td></tr>
        <tr><td><b>FirstCry</b></td><td class="n">67.5%%</td><td class="n">&mdash;</td><td class="n"><b style="color:var(--crit)">39.0%%</b></td><td class="n">&mdash;</td>
          <td><b>Platform margin, then overheads.</b> Gross margin is strong and CM2 stays positive on most SKUs &mdash; FirstCry&apos;s fee (39.0% of net revenue) is the single biggest lever. Fix: bundle low-MRP solo SKUs to spread the overhead allocation.</td></tr>
        <tr><td><b>Blinkit</b></td><td class="n">77.6%%</td><td class="n"><b style="color:var(--crit)">45.8%%</b></td><td class="n"><b style="color:var(--crit)">42.6%%</b></td><td class="n">~100.0%*</td>
          <td><b>Double cost problem.</b> Marketing (45.8%) + Blinkit Margin (42.6%) = 88.4% of net rev. Short-term: cut all paid campaigns on loss-making SKUs. Medium-term: renegotiate margin rate or raise sell prices.</td></tr>
      </tbody>'''

new_dc4_tbody = '''<tbody>
        <tr><td><b>Website</b></td><td class="n">79.1%</td><td class="n"><b style="color:var(--crit)">90.5%</b></td><td class="n">&mdash;</td><td class="n">~17.0%</td>
          <td><b>Marketing efficiency.</b> GM is healthy at 79.1%. Total marketing spend (₹18.04 L) is 90.5% of net revenue — many loss-making SKUs have marketing costs exceeding their revenue per unit. CAC/conversion fix is the #1 lever.</td></tr>
        <tr><td><b>Amazon</b></td><td class="n">77.7%</td><td class="n"><b style="color:var(--crit)">28.7%</b></td><td class="n">&mdash;</td><td class="n">~17.1%*</td>
          <td><b>Marketing + referral fee.</b> Amazon Ads are 28.7% of net rev. Fix: cut ad spend on low converters (see Section 5).</td></tr>
        <tr><td><b>FirstCry</b></td><td class="n">67.5%</td><td class="n">&mdash;</td><td class="n"><b style="color:var(--crit)">39.0%</b></td><td class="n">&mdash;</td>
          <td><b>Platform margin, then overheads.</b> Gross margin is strong and CM2 stays positive on most SKUs &mdash; FirstCry&apos;s fee (39.0% of net revenue) is the single biggest lever. Fix: bundle low-MRP solo SKUs to spread the overhead allocation.</td></tr>
        <tr><td><b>Blinkit</b></td><td class="n">77.6%</td><td class="n"><b style="color:var(--crit)">45.8%</b></td><td class="n"><b style="color:var(--crit)">42.6%</b></td><td class="n">~11.4%</td>
          <td><b>Double cost problem.</b> Marketing (45.8%) + Blinkit Margin (42.6%) = 88.4% of net rev. Short-term: cut all paid campaigns on loss-making SKUs. Medium-term: renegotiate margin rate or raise sell prices.</td></tr>
      </tbody>'''

if old_dc4_tbody in content:
    content = content.replace(old_dc4_tbody, new_dc4_tbody)
    print("DC4 table replaced successfully")
else:
    print("Exact match not found, trying fallback...")
    # Try to fix just the shipping and %% issues
    fixes = [
        ('79.1%%', '79.1%'),
        ('90.5%%', '90.5%'),
        ('28.7%%', '28.7%'),
        ('67.5%%', '67.5%'),
        ('39.0%%', '39.0%'),
        ('77.6%%', '77.6%'),
        ('45.8%%', '45.8%'),
        ('42.6%%', '42.6%'),
        ('~71.4%*</td>', '~17.0%</td>'),
        ('~100.0%*</td>', '~11.4%</td>'),
        ('~15%*</td>', '~17.1%*</td>'),
    ]
    for old, new in fixes:
        count = content.count(old)
        if count:
            content = content.replace(old, new)
            print(f"  Fixed: {repr(old)} -> {repr(new)} ({count}x)")
        else:
            print(f"  NOT FOUND: {repr(old)}")

# Also update the footnote
old_note = '*Amazon shipping is bundled in FBA fees — estimated from pick-pack + inbound + storage lines.'
new_note = '*Amazon shipping estimated from FBA pick-pack + inbound + storage lines (~17.1% of net rev). Website shipping = actual shipping to customer (17.0%). Blinkit shipping (11.4%) is separate from Blinkit Margin.'
if old_note in content:
    content = content.replace(old_note, new_note)
    print("Updated footnote")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")
