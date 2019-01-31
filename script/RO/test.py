a = {'a':1,'b':2,'c':3}

b = {**a}

b['b'] = 3
print(a,b)