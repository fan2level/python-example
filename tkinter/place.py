# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

root = Tk()
root.title("window title")
root.geometry("640x320+0+0")
root.resizable(False, False)

b1=Button(root, text="(50, 50)")
b2=Button(root, text="(50, 100)")
b3=Button(root, text="(100, 150)")
b4=Button(root, text="(0, 200)")
b5=Button(root, text="(0, 300)")
b6=Button(root, text="(0, 300)")

b1.place(x=50, y=50)
b2.place(x=50, y=100, width=50, height=50)
b3.place(x=100, y=150, bordermode="inside")
b4.place(x=0, y=200, relwidth=0.5)
b5.place(x=0, y=300, relx=0.5)
b6.place(x=0, y=300, relx=0.5, anchor="s")

root.mainloop()
