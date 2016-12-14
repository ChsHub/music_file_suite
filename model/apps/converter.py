# -*- coding: utf8 -*-
# ffmpeg-20161027-bf14393-win64-static

import subprocess
from threading import Thread
from re import sub
import os_interface as os
import path_str
from paths import converter_command, path_to_convert_dir, path_to_download_dir
import logging

class Converter(Thread):
    _url = None

    def __init__(self, path):
        Thread.__init__(self)
        self._path = path

    def run(self):
        # TODO test directory delete
        os_dir = os.get_cwd()
        os.change_dir(path_to_convert_dir)
        files = os.get_dir_list(path_to_download_dir)

        logging.info("Convert: "+str(len(files))+" files")
        for file_name_old in files:
            file_name_new = path_str.get_full_path(path_to_convert_dir, sub(r'[^.]*$','mp3', file_name_old))
            file_name_old = path_str.get_full_path(path_to_download_dir, file_name_old)

            logging.info("Convert: " + file_name_old)
            if not os.exists(file_name_new):
                subprocess.call(converter_command + [file_name_old]
                            + [file_name_new], stdin=None, stderr=None, universal_newlines=True,
                            shell=False)

        os.change_dir(os_dir)
        print("Convert: DONE")
