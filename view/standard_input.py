from tkinter import Entry, TOP, LEFT,YES, X, RIGHT, END

from standard_button import StandardButton
from standard_frame import StandardFrame


class StandardInput(StandardFrame):
    _entry = None
    _controller_callback = None

    def __init__(self, master, color, controller_callback, text):
        super().__init__(master, side=TOP, borderwidth=1)


        self._controller_callback = controller_callback
        self._entry = Entry(self, width=50)
        self._entry.pack(side=LEFT, expand=YES, fill=X)

        StandardButton(text, self, self._callback, 0, 0, color, side=RIGHT)

    def _callback(self):

        input = self._entry.get()
        self._controller_callback(input)