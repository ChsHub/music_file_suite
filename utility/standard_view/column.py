from tkinter import TOP, Frame, SOLID

from colors import color_background
from standard_frame import StandardFrame


class Column(Frame):
    def __init__(self, master, padx=10, pady=10):
        Frame.__init__(self, master=master, padx=padx, pady=pady, width=300, height=300, bg=color_background, bd=0,
                       relief=SOLID)

    def get_parent(self):
        if len(self.winfo_children()) % 2 == 0:
            return self
        else:
            return StandardFrame(self, TOP, padx=0)
