# -*-coding:utf-8-*-

class Node(object):
    def __init__(self, data):
        self.data = data
        self.__next = None

    @property
    def next(self):
        return self.__next
    @next.setter
    def next(self, data):
        self.__next = data

class Data(Node):
    pass

class LinkedList(object):
    def __init__(self):
        self.head = None

    def printitem(self):
        temp = self.head
        while(temp):
            print(temp.data)
            temp = temp.next

if __name__ == '__main__':
    llist = LinkedList()
    one = Data(1)
    second = Data(2)
    third = Data(3)

    llist.head = one
    one.next = second
    second.next = third

    llist.printitem()
