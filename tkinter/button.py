# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Button")
root.geometry("640x320+0+0")
root.resizable(False, False)
root.bind("<Escape>", exit)

count = 0
def countUP():
    global count
    count += 1
    label.config(text=str(count))

label = Label(root, text="0")
label.pack()

button = Button(root, text="카운터", overrelief="solid", width=15, command=countUP, repeatdelay=1000, repeatinterval=100)
button.pack()

root.mainloop()
