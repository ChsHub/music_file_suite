from tkinter import Label, W
from colors import color_background

class StandardLabel(Label):


    def __init__(self, text, master, padx=10, pady=10, color=color_background):
        if not master:
            raise ValueError
        super().__init__(master=master, height=2, bg=color, padx=padx,
                         pady=pady, text=text, anchor=W)

    # TODO delete
    def _create_label_packed(self, master, text, padx, pady, color):
        if not master:
            raise ValueError

        b = StandardLabel(text, master, padx, pady, color)
        b.pack(anchor=W)