from logging import info
from tkinter import NO, BOTTOM
from tkinter.filedialog import askdirectory
from utility.os_interface import get_absolute_path
from utility.path_str import get_clean_path
from utility.os_interface import save_input
from standard_view.standard_input import StandardInput
from texts import text_file_input


class FileInput(StandardInput):
    def __init__(self, master, color, controller_callback):
        super().__init__(master, color, controller_callback, text_file_input, expand=NO, side=BOTTOM)

    def _callback(self):
        path = askdirectory()

        if path == "":
            return
        path = get_clean_path(path)
        info("path: " + path)

        save_input(get_absolute_path("/resource"), "paths.py", "file_path", path)
        self._get_path(path)
