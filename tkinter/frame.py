# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

root = Tk()
root.bind("<Escape>", exit)

root.title("window title")
root.geometry("640x320+0+0")
root.resizable(False, False)

frame1=Frame(root, relief="solid", bd=2)
frame1.pack(side="left", fill="both", expand=True)

frame2=Frame(root, relief="solid", bd=2)
frame2.pack(side="right", fill="both", expand=True)

button1=Button(frame1, text="프레임1")
button1.pack(side="right")

button2=Button(frame2, text="프레임2")
button2.pack(side="left")

root.mainloop()
