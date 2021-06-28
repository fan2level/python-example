# -*-coding:utf-8-*-

a = 'sample/b.dbc'
o = 'sample/b.a.dbc'
d = None

with open(a, 'rb') as f:
    d = f.read()

with open(o, 'w') as f:
    [f.write(chr(x)) for x in d if x < 127 and x != 0x0d]
