import __future__

class ClassA(object):
    def __init__(self):
        self.index = 0
        self.data = [1,2,3,4,5]
    def __iter__(self):
        self.index = 0
        return self
    def next(self):           # python3: __next__
        if self.index > len(self.data) -1:
            raise StopIteration
        v = self.data[self.index]
        self.index += 1
        return v

if __name__ == '__main__':
    a = ClassA()
    print(type(a.data))
    print(next(a))
