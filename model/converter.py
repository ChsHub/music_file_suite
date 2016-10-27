# -*- coding: utf8 -*-
# ffmpeg-20161027-bf14393-win64-static

import subprocess
from threading import Thread

import os_interface as os
import path_str
from paths import converter_command, path_to_convert_dir, path_to_download_dir


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

        for file in files:
            new_file = path_str.get_full_path(path_to_convert_dir, file + '.mp3')
            file = path_str.get_full_path(path_to_download_dir, file)
            subprocess.call(converter_command + [file]
                            + [new_file], stdin=None, stdout=None,
                            stderr=None,
                            shell=True)
        os.change_dir(os_dir)
        print("Convert: DONE")
