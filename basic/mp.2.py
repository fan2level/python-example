# -*-coding:utf-8-*-

import multiprocessing as mp

class A(object):
    def __init__(self):
        with mp.Pool() as pool:
            self.result = pool.map(self.run, range(1,10))
            pool.close()
            pool.join()

    def run(self,i):
        print(f'run...{i}')
        return i*i

if __name__ == '__main__':
    a = A()
    print(a.result)


