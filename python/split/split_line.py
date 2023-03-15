#string_with_lines = "Hello"
string_with_lines = """Hello
World
Python"""

lines = string_with_lines.split('\n')
for i in range(len(lines)):
    lines[i] = ' * ' + lines[i]
result = '\n'.join(lines)
print(result)

