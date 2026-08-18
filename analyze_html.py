import re

with open('index.html', encoding='utf-8') as f:
    content = f.read()

# Find nav buttons
nav_buttons = re.findall(r'<button[^>]*onclick=[^>]*>([^<]+)</button>', content)
print('Nav buttons:', nav_buttons)

# Find section ids
sections = re.findall(r'<section[^>]*id="([^"]+)"', content)
print('Sections:', sections)
