from tkinter import Frame


class StandardFrame(Frame):
    def __init__(self, master, padx=10, pady=10):
        super().__init__(master=master, padx=padx, pady=pady,
                       width=300, height=300)