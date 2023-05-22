import re

print(re.match('a', 'aba'))
print(re.match('x', 'aba'))

print("========================")

matchObj = re.search('a', 'a')
print(matchObj)

print("========================")

print(re.search('a', 'aba'))
print(re.search('a', 'bbb'))
print(re.search('a', 'baa'))

print("========================4")

matchObj_iter = re.finditer('a', 'baa')
print(matchObj_iter)
for matchObj in matchObj_iter:
    print(matchObj)
