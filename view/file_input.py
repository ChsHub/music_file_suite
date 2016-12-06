import logging
from tkinter.filedialog import askdirectory

import lib.utility.os_interface as os
import lib.utility.path_str as path_str
from paths import file_path
from standard_input import StandardInput
from texts import text_file_input
from os_interface import save_input

class FileInput(StandardInput):


    def __init__(self, master, color, controller_callback):
        super().__init__(master, color, controller_callback, text_file_input)
        self._get_path(file_path)

    def _callback(self):

        path = askdirectory()

        if path == "":
            return
        path = path_str.get_clean_path(path)
        logging.info("path: " + path)

        save_input(os.get_absolute_path("/resource"), "paths.py","file_path", path)
        self._get_path(path)

