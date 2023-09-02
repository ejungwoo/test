def add1(a):
    a = a + "1"
    if a!="11111":
        return add1(a)
    else:
        return a
            
a = "111"
print(a[:0])

print(add1(a))
