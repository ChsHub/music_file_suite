from tkinter import Label, W
from colors import color_background

class StandardLabel(Label):


    def __init__(self, text, master, padx=10, pady=10, color=color_background):
        if not master:
            raise ValueError
        super().__init__(master=master, height=2, bg=color, padx=padx,
                         pady=pady, text=text, anchor=W)