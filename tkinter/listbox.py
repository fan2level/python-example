# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

root = Tk()
root.bind("<Escape>", exit)

root.title("window title")
root.geometry("640x320+0+0")
root.resizable(False, False)

l = Listbox(root, selectmode="extended", height=0)
l.insert(0, "1번")
l.insert(1, "2번")
l.insert(2, "3번")
l.insert(3, "4번")
l.insert(4, "5번")
l.pack()

root.mainloop()
