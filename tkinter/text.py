# -*-coding:utf-8-*-
from tkinter import *
from tkinter import ttk

# https://tkdocs.com/index.html

window = Tk()
window.title("window title")
window.geometry("640x320+0+0")
window.resizable(False, False)

text=Text(window)

text.insert(CURRENT, "안녕하세요.\n")
text.insert("current", "반습니다.")
text.insert(2.1, "갑")

text.pack()

text.tag_add("강조", "1.0", "1.6")
text.tag_config("강조", background="yellow") 
text.tag_remove("강조", "1.1", "1.2")

window.mainloop()
