# -*-coding:utf-8-*-

import unicodedata
 
# format print string...
def fps(string, width, align='<', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF") for c in string))
    return {
        '>': lambda s: fill * count + s,
        '<': lambda s: s + fill * count,
        '^': lambda s: fill * (count / 2)
                       + s
                       + fill * (count / 2 + count % 2)
            }[align](string)

print(fps('aaa', 10, '>'))
print(fps('aaa', 10, '>'))
print(fps('aaaaaaa', 10, '>'))
print(fps('한글', 10, '>'))

# from tqdm import tqdm
# import time

# for i in tqdm(range(1, 600), mininterval=0.01):
#     time.sleep(0.1)

