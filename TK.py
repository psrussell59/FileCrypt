from tkinter import *


class Root(Tk):
    def __init__(self, name):
        super(Root, self).__init__()
        self.title(name)
        self.geometry("450x215+200+100")
        self.maxsize(width=450, height=215)
