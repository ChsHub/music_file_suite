from tkinter import END

from standard_input import StandardInput
from texts import text_convert_input


class ConvertInput(StandardInput):
    def __init__(self, master, color, callback):
        super().__init__(master, color, callback, text_convert_input)

    def _callback(self):
        super()._callback()
        self._entry.delete(0, END)
        #self._get_path()