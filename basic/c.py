# -*-coding:utf-8-*-
import os
import time

a = [1,2,3,4,5,6]
print(a[1:5])
print(a[:])

# sorting
print(sorted("hello"))
print(sorted([5,2,3,7,5]))

adic = {3:1, 2:2, 1:4}
print(sorted(adic))
print(sorted(adic.items(), key=lambda x: x[1]))
print(sorted(range(1,10), reverse=True))
