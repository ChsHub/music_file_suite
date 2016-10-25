from tkinter import Button


class StandardButton(Button):
    def __init__(self, text, master, callback, padx, pady, color):
        super().__init__(master=master, width=20, height=2, bg=color, padx=padx,
                      pady=pady, text=text, command=callback)