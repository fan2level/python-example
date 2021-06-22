# -*-coding:utf-8-*-

import os,sys
import multiprocessing as mp

class ClassA(object):
    def __init__(self, p):
        self.p = p

    def __call__(self):
        print(f"p: {self.p}")

if __name__ == '__main__':
    a = ClassA(1)
    print(callable(a))
    a()
