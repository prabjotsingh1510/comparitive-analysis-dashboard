with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Find the start of the Per-Product Breakdown section
start = html.find('<h2>Per-Product Breakdown</h2>')
print('Section start:', start)

# Find the end: the next <h2> tag or end of the containing section
end = html.find('<h2>', start + 10)
print('Next h2 at:', end)
if end == -1:
    # Try finding closing div pattern
    end = html.find('</div>', start + 500) + 6

# Print the full section
section = html[start:end]
print('Section length:', len(section))
print()
print('=== FULL SECTION ===')
print(section[:6000])

# Also check what's around this section (context)
print()
print('=== CONTEXT BEFORE ===')
print(html[max(0,start-400):start])
print()
print('=== WHAT COMES AFTER ===')
print(html[end:end+400])
