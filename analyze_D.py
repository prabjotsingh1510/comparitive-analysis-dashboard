content = open('index.html', encoding='utf-8').read()

# Find the script section
script_idx = content.find('<script>')
if script_idx == -1:
    print('No script tag found')
else:
    # Find const D
    d_idx = content.find('const D = {', script_idx)
    print(f'Script starts at: {script_idx}')
    print(f'const D at: {d_idx}')
    
    # Find where D ends
    # It's a JSON object followed by semicolon
    # Let's find 'const D = {' and then count braces
    pos = d_idx + len('const D = ')
    depth = 0
    in_string = False
    escape = False
    i = pos
    while i < len(content):
        c = content[i]
        if escape:
            escape = False
        elif c == '\\' and in_string:
            escape = True
        elif c == '"' and not escape:
            in_string = not in_string
        elif not in_string:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    d_end = i + 1
                    break
        i += 1
    
    print(f'D object ends at: {d_end}')
    # Print snippet after D
    with open('after_D.txt', 'w', encoding='utf-8') as f:
        f.write(content[d_end:d_end+2000])
    print('Written after_D.txt')
    
    # Also write the structure of D (first 2000 chars)
    with open('D_structure.txt', 'w', encoding='utf-8') as f:
        f.write(content[d_idx:d_idx+3000])
    print('Written D_structure.txt')
