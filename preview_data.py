import json, sys

with open('extracted_data.json', encoding='utf-8') as f:
    d = json.load(f)

out = open('data_preview.txt', 'w', encoding='utf-8')

# Print Raw Data - Website columns
ws = d['Raw Data - Website']
out.write('=== RAW DATA - WEBSITE (first 10 rows) ===\n')
for r in ws[:10]:
    out.write(f'Row {r["row"]}: {r["data"][:30]}\n')

out.write('\n=== RAW DATA - AMAZON (first 10 rows) ===\n')
for r in d['Raw Data - Amazon'][:10]:
    out.write(f'Row {r["row"]}: {r["data"][:30]}\n')

out.write('\n=== RAW DATA - FIRSTCRY (first 10 rows) ===\n')
for r in d['Raw Data - FirstCry'][:10]:
    out.write(f'Row {r["row"]}: {r["data"][:30]}\n')

out.write('\n=== RAW DATA - BLINKIT (first 10 rows) ===\n')
for r in d['Raw Data - Blinkit'][:10]:
    out.write(f'Row {r["row"]}: {r["data"][:30]}\n')

out.write('\n=== CHANNEL MATRICES ===\n')
for r in d['Channel Matrices']:
    out.write(f'Row {r["row"]}: {r["data"][:20]}\n')

out.write('\n=== MARKETING EFFICIENCY ===\n')
for r in d['Marketing Efficiency']:
    out.write(f'Row {r["row"]}: {r["data"][:20]}\n')

out.write('\n=== EXECUTIVE DASHBOARD ===\n')
for r in d['Executive Dashboard']:
    out.write(f'Row {r["row"]}: {r["data"][:20]}\n')

out.close()
print("Done")
