# -*-coding:utf-8-*-
import os
import glob
import time

print(os.listdir('.'))

print(glob.glob('./*'))

# f-strings
num = 1000000000
print(f'{num:,}')
