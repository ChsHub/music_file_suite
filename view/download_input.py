from tkinter import Entry, LEFT
from standard_button import StandardButton


class DownloadInput:


    def __init__(self, master, color):
        Entry(master, width=50).pack()
        StandardButton("Download", master, self._download_callback, 0, 0, color).pack(side=LEFT)

    def _download_callback(self):
        return