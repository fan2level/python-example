# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

window = Tk()
window.bind("<Escape>", exit)

window.title("window title")
window.geometry("640x320+0+0")
window.resizable(False, False)

width=1

def drawing(event):
    if width>0:
        x1=event.x-1
        y1=event.y-1
        x2=event.x+1
        y2=event.y+1
        canvas.create_oval(x1, y1, x2, y2, fill="blue", width=width)

def scroll(event):
    global width
    if event.delta==120:
        width+=1
    if event.delta==-120:
        width-=1
    label.config(text=str(width))

canvas=Canvas(window, relief="solid", bd=2)
canvas.pack(expand=True, fill="both")
canvas.bind("<B1-Motion>", drawing)
canvas.bind("<MouseWheel>", scroll)

label=Label(window, text=str(width))
label.pack()

window.mainloop()
