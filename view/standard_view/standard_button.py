from tkinter import Button, LEFT

from view.standard_view.colors import color_button


class StandardButton(Button):
    def __init__(self, text, master, callback, color=color_button, side=LEFT, padx=0, pady=0, width=20, **args):
        super().__init__(master=master, width=width, bg=color, padx=padx, pady=pady,
                         text=text, command=callback, **args)
        self.pack(side=side)
