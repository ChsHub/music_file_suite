from tkinter import Frame, LEFT,W, SOLID, X, YES
from colors import color_background

class StandardFrame(Frame):

    def __init__(self, master, side, padx=10, pady=10, borderwidth=0, relief=SOLID):
        super().__init__(master=master, padx=padx, pady=pady,
                       width=300, height=300, bg=color_background, bd=borderwidth, relief=relief)
        self.pack(side=side, anchor=W, fill=X, expand=YES)