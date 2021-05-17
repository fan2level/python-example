# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

root = Tk()
root.title("window title")
root.geometry("640x320+0+0")
root.resizable(False, False)

b1=Button(root, text="top")
b1_1=Button(root, text="top-1")

b2=Button(root, text="bottom")
b2_1=Button(root, text="bottom-1")

b3=Button(root, text="left")
b3_1=Button(root, text="left-1")

b4=Button(root, text="right")
b4_1=Button(root, text="right-1")

b5=Button(root, text="center", bg="red")

b1.pack(side="top")
b1_1.pack(side="top", fill="x")

b2.pack(side="bottom")
b2_1.pack(side="bottom", anchor="e")

b3.pack(side="left")
b3_1.pack(side="left", fill="y")

b4.pack(side="right")
b4_1.pack(side="right", anchor="s")

b5.pack(expand=True, fill="both")

root.mainloop()
