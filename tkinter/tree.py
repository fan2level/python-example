from tkinter import *
from tkinter import ttk

root = Tk()

tree = ttk.Treeview(root, columns=['one','two'])
tree.pack()

# 첫번째 행은 고정 #0

tree.heading('#0', text='id')
tree.heading('one', text='one')
tree.heading('two', text='two')
pt = tree.insert('', 'end', text='aaa', values=['일일','22'])
tree.insert(pt, 'end', text='bbb', values=['11',22])
tree.insert('', 'end', text='ccc', values=[33,44])

root.mainloop()
