with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Find end of blinkit panel
idx2 = html.rfind('</div><!-- /#chan-blinkit -->')
print('chan-blinkit end at:', idx2)
print(repr(html[idx2:idx2+300]))
print()

# Find the <div class="tip" line
idx3 = html.find('<div class="tip"')
print('tip div at:', idx3)
print(repr(html[idx3-50:idx3+100]))
print()

# Find the chan-bar
idx4 = html.find('class="chan-bar"')
print('chan-bar at:', idx4)
print(repr(html[idx4:idx4+600]))
print()

# Find all data-chan buttons
import re
for m in re.finditer(r'data-chan="([^"]+)"', html):
    print('data-chan:', m.group(1), 'at', m.start())
