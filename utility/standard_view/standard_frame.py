from tkinter import Frame, W, SOLID, BOTH, YES

from colors import color_background


class StandardFrame(Frame):
    def __init__(self, master, side, padx=10, pady=10, borderwidth=0, relief=SOLID, fill=BOTH,
                 bg=color_background, expand=YES):
        super().__init__(master=master, padx=padx, pady=pady,
                         width=300, height=300, bg=bg, bd=borderwidth, relief=relief)
        self.pack(side=side, anchor=W, fill=fill, expand=expand)
