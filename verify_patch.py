import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const D = (\{.*?\});', html, re.DOTALL)
if not m:
    print('ERROR: could not find D = {...}')
    exit(1)

try:
    d = json.loads(m.group(1))
    print('D parses OK')
    t = d['periods']['apr']['tot']
    print('apr units:', t['units'], 'rev:', round(t['rev'],2))
    print('apr cm2:', round(t['cm2'],2), 'cm2pct:', round(t['cm2pct'],2), '%')
    print('apr ebitda:', round(t['ebitda'],2), 'ebitdapct:', round(t['ebitdapct'],2), '%')
    print('apr n:', t['n'], 'mktg:', round(t['mktg'],2))
    print('apr cac:', d['periods']['apr']['cac'])
    g = d['periods']['apr']['grand']
    print('apr grand profit:', g['profit'], 'profit_u:', g['profit_u'])
    print('flips:', len(d['flips']))
    sb = d['facts']['star_both']
    print('star_both:', len(sb), '->', [s['key'] for s in sb])
    print('bridge[6]:', d['bridge'][6])
    print('recon.apr:', d['recon']['apr'])
    wf = d['s5']['apr']['wf']
    print('s5.apr.wf gross:', wf['gross'], 'gm:', round(wf['gm'],2), 'mkt:', round(wf['mkt'],2), 'eb:', round(wf['eb'],2))
    print('star_both_revshare:', d['facts']['star_both_revshare'])
    print('top3_burn:', d['facts']['top3_burn'])
    print('persistent_loss[0]:', d['facts']['persistent_loss'][0])
    # Quad check
    q = d['periods']['apr']['quad']
    print('quads: star='+str(q['star']['n'])+' overhead='+str(q['overhead']['n'])+' loss='+str(q['loss']['n']))
    print('ALL OK')
except json.JSONDecodeError as je:
    print('PARSE ERROR at pos', je.pos, ':', je.msg)
    snippet = m.group(1)[max(0,je.pos-200):je.pos+200]
    print('Context:', repr(snippet))
