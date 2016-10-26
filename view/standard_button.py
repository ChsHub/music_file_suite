from tkinter import Button, LEFT
from colors import color_button

class StandardButton(Button):
    def __init__(self, text, master, callback, padx, pady, color=color_button, side=LEFT):
        super().__init__(master=master, width=20, height=2, bg=color, padx=padx,
                      pady=pady, text=text, command=callback)
        self.pack(side=side)