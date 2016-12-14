from tkinter import END

from standard_input import StandardInput
from texts import text_download_input


class DownloadInput(StandardInput):
    def __init__(self, master, color, callback):
        super().__init__(master, color, callback, text_download_input)

    def _callback(self):

        super()._callback()
        self._entry.delete(0, END)