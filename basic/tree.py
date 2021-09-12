#-*-coding:utf-8-*-

class Node(object):
    def __init__(self, data):
        self.data = data
        self.__child = list()

    def add(self, data):
        self.__child.append(data)

    def get(self, data):
        return next((x for x in self.__child if x == data), None)
    
    def children(self):
        return self.__child

class LinkedList(object):
    def __init__(self):
        self.root = None

    def _printitems(self, child, indent):
        print(f"{'':<{indent}}{child.data}")
        for item in child.children():
            self._printitems(item, indent+2)

    def printitems(self):
        self._printitems(self.root, 0)
        
if __name__ == '__main__':
    tree = LinkedList()
    one = Node(1)
    tree.root = one
    two = Node(2)
    three = Node(3)
    four = Node(4)
    
    one.add(two)
    one.add(three)
    three.add(four)

    tree.printitems()
