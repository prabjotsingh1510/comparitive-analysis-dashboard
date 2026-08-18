content = open('index.html', encoding='utf-8').read()
idx = content.find('Decision Criteria 4')
with open('dc4_final.txt', 'w', encoding='utf-8') as f:
    f.write(content[idx:idx+2500])
print("Written")
