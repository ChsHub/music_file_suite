import logging
from tkinter import TOP, LEFT
from tkinter.filedialog import askdirectory

import lib.utility.os_interface as os
import lib.utility.path_str as path_str
from standard_button import StandardButton
from standard_frame import StandardFrame
from standard_label import StandardLabel


class FileInput(StandardFrame):

    _file_label = None
    _file_path_saved_input = os.get_absolute_path(u"/resource")
    analyze_files = None

    def __init__(self, master, album_dir, color, analyze_files):
        super().__init__(master=master, side=TOP, borderwidth=1)


        self.analyze_files = analyze_files
        self._file_label = StandardLabel(album_dir, self, 0, 0, color)
        self._file_label.pack(side=LEFT)
        StandardButton("Open File", self, self._open_file_callback, 0, 0, color).pack(side=LEFT)


    #### CALLBACK ####

    def _open_file_callback(self):
        album_dir = askdirectory()

        if album_dir == "":
            return
        album_dir = path_str.get_clean_path(album_dir)

        logging.info("album_dir: " + album_dir)

        self._file_label.config(text=album_dir)
        self._save_input(album_dir)
        self.analyze_files(album_dir)

    #### WRITE FILE ####

    def _save_input(self, file_path):
        data = "# -*- coding: utf8 -*-\nfile_path = u'" + file_path + "'"

        os.write_file_data(path=self._file_path_saved_input,
                           file_name=u"saved_input.py", data=data)
