from tkinter import Entry, TOP, LEFT,YES, X, RIGHT, END

from standard_button import StandardButton
from standard_frame import StandardFrame
from texts import text_download_input


class DownloadInput(StandardFrame):
    _entry = None
    _download = None

    def __init__(self, master, color, download):
        super().__init__(master, side=TOP, borderwidth=1)

        self._download = download
        self._entry = Entry(self, width=50)
        self._entry.pack(side=LEFT, expand=YES, fill=X)

        StandardButton(text_download_input, self, self._download_callback, 0, 0, color, side=RIGHT)

    def _download_callback(self):

        url = self._entry.get()
        self._entry.delete(0, END)
        self._download(url)