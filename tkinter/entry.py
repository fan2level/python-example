# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

root = Tk()
root.title("Entry")
root.geometry("640x320+0+0")
root.resizable(False, False)
root.bind("<Escape>", exit)

def calc(event):
    label.config(text="결과="+str(eval(entry.get())))

entry = Entry(root)
entry.bind("<Return>", calc)
entry.pack()

label=Label(root, bg="gray")
label.pack()

root.mainloop()
