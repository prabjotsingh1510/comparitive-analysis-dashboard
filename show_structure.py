f = open('index.html', encoding='utf-8')
html = f.read()
f.close()
print('Size:', len(html))

# Show channel buttons
idx = html.find('role="tablist" aria-label="Sales channel"')
print('\n=== CHANNEL BUTTONS ===')
print(html[idx:idx+500])

# Show analysis panel opening
idx2 = html.find('id="chan-analysis"')
print('\n=== ANALYSIS PANEL OPENING ===')
print(html[idx2:idx2+400])

# Show first Q heading
idx3 = html.find('Decision Criteria 1')
print('\n=== Q1 HEADING ===')
print(html[idx3-50:idx3+200])
