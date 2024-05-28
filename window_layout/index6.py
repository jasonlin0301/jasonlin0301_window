import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("林宣安_0528作業")

        fm = Frame(self)
        Button(fm, text='TOP').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='CENTER').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='Bottom').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='LEFT').pack(side=LEFT)
        Button(fm, text='This is Center Button').pack(side=LEFT)
        Button(fm, text='Right').pack(side=LEFT)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()