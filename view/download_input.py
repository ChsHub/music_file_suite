from tkinter import END

from resource.texts import text_download_input
from view.standard_view.standard_input import StandardInput


class DownloadInput(StandardInput):
    def __init__(self, master, color, callback):
        super().__init__(master, color, callback, text_download_input)

    def _callback(self):
        super()._callback()
        self._entry.delete(0, END)
