from tkinter import LEFT, TOP

from standard_frame import StandardFrame


class Column(StandardFrame):
    def __init__(self, master):
        super().__init__(master, side=LEFT)

    def get_parent(self):
        if len(self.winfo_children()) % 2 == 0:
            return self
        else:
            return StandardFrame(self, TOP, padx=0)
