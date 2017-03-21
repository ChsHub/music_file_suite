from tkinter import LEFT, TOP, BOTH
from standard_frame import StandardFrame


class Column(StandardFrame):
    def __init__(self, master):
        super().__init__(master, side=LEFT, fill=BOTH)

    def get_parent(self):
        if len(self.winfo_children()) % 2 == 0:
            return self
        else:
            return StandardFrame(self, TOP, padx=0)
