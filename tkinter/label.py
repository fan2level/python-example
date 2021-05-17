# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

root = Tk()

root.title("Label")
root.geometry("640x320+0+0")
root.resizable(False, False)
root.bind("<Escape>", exit)

label = Label(root, text="라벨")
label.pack()
label2= Label(root, text="label2", width=10, height=5, fg="red", relief="solid")
label2.pack()

root.mainloop()
