#p1 = "\"string\\n\"\n"
s1 = "1 string\n"
s2 = "2 \nstring"
s3 = """3 string
"""
s4 = """4
string"""
s5 = """5 string"""
s6 = """6 string\n"""
s7 = """7 \nstring"""
s8 = "string"

for ss in [s1,s2,s3,s4,s5,s6,s7,s8]:
  if "\n" in ss or "\r\n" in ss:
    print("multiple line +++++++++++++:",ss)
  else:
    print("NOT multiple line:",ss)
