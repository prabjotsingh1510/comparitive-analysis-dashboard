content = open('index.html', encoding='utf-8').read()

# Find Decision Criteria 4 in the HTML
idx = content.find('Decision Criteria 4')
if idx == -1:
    idx = content.find('DECISION CRITERIA 4')
if idx == -1:
    idx = content.find('decision criteria 4')

print(f'DC4 found at: {idx}')
if idx != -1:
    with open('dc4_snippet.txt', 'w', encoding='utf-8') as f:
        f.write(content[idx:idx+4000])
    print('Written dc4_snippet.txt')

# Also find where 90.5 is in the HTML (the hard-coded value if any)
idx2 = content.find('90.5')
print(f'90.5 found at: {idx2}')
if idx2 != -1:
    print(repr(content[idx2-100:idx2+100]))

# Find DC4 table
idx3 = content.find('MARKETING AS % OF NET REV')
if idx3 == -1:
    idx3 = content.find('Marketing as % of Net Rev')
print(f'Marketing column header at: {idx3}')
if idx3 != -1:
    print(repr(content[idx3-200:idx3+800]))
