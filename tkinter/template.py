# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

root = Tk()
root.title("root title")
root.geometry("640x320+0+0")
root.resizable(False, False)

root.bind("<Escape>", exit)

root.mainloop()
