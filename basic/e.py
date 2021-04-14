# -*-coding:utf-8-*-

from tqdm import tqdm
import time

for i in tqdm(range(1, 600), mininterval=0.01):
    time.sleep(0.1)
