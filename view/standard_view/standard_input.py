from tkinter import Entry, LEFT, YES, X, RIGHT, StringVar, NO, TOP

from view.standard_view.standard_button import StandardButton
from view.standard_view.standard_frame import StandardFrame


class StandardInput(StandardFrame):
    _entry = None
    _controller_callback = None

    def __init__(self, master, color, controller_callback, text, expand=NO, side=TOP):
        super().__init__(master, side=side, borderwidth=1, expand=expand)

        self._controller_callback = controller_callback
        self._entry = Entry(self, width=50)
        self._entry.pack(side=LEFT, expand=YES, fill=X)

        StandardButton(text, self, callback=self._callback, color=color, side=RIGHT)

    def _callback(self):
        self._controller_callback(self._entry.get())

    def _get_path(self, path):
        path_text = StringVar()
        path_text.set(path)
        self._entry.config(textvariable=path_text)
        self._controller_callback(path)
