import re

lines = """
 DN(IA)=DN(IA)+1D0
   DNXT(IAX)=DNXT(IAX)+1D0      !true
   A1DDXT(IAX)=104D3*DNXT(IAX)+1D0      !true
   """
for line in lines.splitlines():
    print("_______________")
    print(line)
    matchObj = re.search('\dD\d', line)
    print("re.search('\dD\d', line) =    ",matchObj)
    matchObj = re.findall('\dD\D', line)
    print("re.findall('\dD\D', line) =    ",matchObj)
