import string

def pos_to_char(pos):
    return chr(pos + 97)

def char_position(letter):
    return ord(letter) - 97

#string.ascii_lowercase.index('a')

for i in range(26):
    ap = pos_to_char(i)
    i2 = char_position(ap)
    i3 = string.ascii_lowercase.index(ap)
    print(i, ap, i2, i3)
