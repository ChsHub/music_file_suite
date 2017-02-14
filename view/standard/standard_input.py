from tkinter import Entry, LEFT,YES, X, RIGHT, StringVar, NO, TOP

from standard_button import StandardButton
from standard_frame import StandardFrame


class StandardInput(StandardFrame):
    _entry = None
    _controller_callback = None

    def __init__(self, master, color, controller_callback, text, expand=NO, side=TOP):
        super().__init__(master, side=side, borderwidth=1, expand=expand)

        self._controller_callback = controller_callback
        self._entry = Entry(self, width=50)
        self._entry.pack(side=LEFT, expand=YES, fill=X)

        StandardButton(text, self, self._callback, 0, 0, color, side=RIGHT)

    def _callback(self):
        input = self._entry.get()
        self._controller_callback(input)

    def _get_path(self, path):
        path_text = StringVar()
        path_text.set(path)
        self._entry.config(textvariable=path_text)
        self._controller_callback(path)
