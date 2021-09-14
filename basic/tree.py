# -*-coding:utf-8-*-

class Tree(object):
    "Generic tree node."
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add(child)
    def __repr__(self):
        return self.name
    def add(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def _search(self, root, name):
        if root.name == name:
            return root
        for child in root.children:
            if self._search(child, name) != None:
                return child
    def search(self, name):
        return self._search(self, name)
    
    def _print(self, tree, indent):
        print(f"{'':<{indent}}{tree}")
        if len(tree.children) == 0:
            return
        for child in tree.children:
            self._print(child, indent+2)
    def printtree(self):
        self._print(self, 0)

if __name__ == '__main__':
    t = Tree('*', [Tree('1'),
                   Tree('2'),
                   Tree('+', [Tree('3'),
                              Tree('4')])])

    t.printtree()
    print()
    print(t.search('2'))
