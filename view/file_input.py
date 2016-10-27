import logging
from tkinter.filedialog import askdirectory, StringVar

import lib.utility.os_interface as os
import lib.utility.path_str as path_str
import resource.saved_input as saved_input
from saved_input import file_path
from standard_input import StandardInput
from texts import text_file_input


class FileInput(StandardInput):
    _file_path_saved_input = os.get_absolute_path(u"/resource")

    def __init__(self, master, color, controller_callback):
        super().__init__(master, color, controller_callback, text_file_input)
        self._get_path(file_path)

    def _callback(self):

        album_dir = askdirectory()

        if album_dir == "":
            return
        album_dir = path_str.get_clean_path(album_dir)
        logging.info("album_dir: " + album_dir)

        self._save_input(album_dir)
        self._get_path(album_dir)

    def _get_path(self, album_dir):
        path_text = StringVar()
        path_text.set(album_dir)
        self._entry.config(textvariable=path_text)
        self._controller_callback(album_dir)

    def _save_input(self, file_path):
        # TODO fail
        try:
            file_path = saved_input.file_path
        except AttributeError as e:
            file_path = None

        data = "# -*- coding: utf8 -*-\nfile_path = u'" + file_path + "'"

        os.write_file_data(path=self._file_path_saved_input,
                           file_name=u"saved_input.py", data=data)
