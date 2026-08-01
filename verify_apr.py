import json

with open('apr_data.json', encoding='utf-8') as f:
    new = json.load(f)

t = new['tot']
print('=== NEW APR TOTALS ===')
print('rev:', t['rev'], 'netrev:', round(t['netrev'],2), 'units:', t['units'])
print('cm2:', round(t['cm2'],2), 'cm2pct:', round(t['cm2pct'],5))
print('ebitda:', round(t['ebitda'],2), 'ebitdapct:', round(t['ebitdapct'],5))
print('mktg:', round(t['mktg'],2), 'oh:', round(t['oh'],2), 'n:', t['n'])
print()
print('quad star:', new['quad']['star'])
print('quad overhead:', new['quad']['overhead'])
print('quad loss:', new['quad']['loss'])
print()
print('grand:', new['grand'])
print('cac:', new['cac'])
print()

print('=== TOP 15 PRODUCTS ===')
for p in sorted(new['products'], key=lambda x: -x['rev'])[:15]:
    print(' ', repr(p['key']), 'units='+str(p['units']),
          'rev='+str(p['rev']),
          'cm2_u='+str(round(p['cm2_u'],2)),
          'cm2pct='+str(round(p['cm2pct'],2))+'%',
          'ebitda_u='+str(round(p['ebitda_u'],2)),
          'quad='+p['quad'])

print()
print('=== CATS ===')
for c in new['cats']:
    print(' ', repr(c['cat']), 'n='+str(c['n']), 'rev='+str(round(c['rev'],2)),
          'units='+str(c['units']), 'cm2='+str(round(c['cm2'],2)),
          'cm2pct='+str(round(c['cm2pct'],2))+'%',
          'ebitda='+str(round(c['ebitda'],2)),
          'ebitdapct='+str(round(c['ebitdapct'],2))+'%')
