# -*- coding: utf8 -*-
# ffmpeg-20161027-bf14393-win64-static

from logging import info
import subprocess
from re import sub
import os_interface as os
from path_str import get_full_path
from paths import converter_command, path_to_convert_dir, path_to_download_dir
from queue_task import QueueTask


class Converter(QueueTask):
    def __init__(self):
        QueueTask.__init__(self)

    def consume_element(self, path):
        # TODO test directory delete
        os_dir = os.get_cwd()
        os.change_dir(path_to_convert_dir)
        files = os.get_dir_list(path_to_download_dir)

        info("Convert: " + str(len(files)) + " files")
        for file_name_old in files:
            file_name_new = get_full_path(path_to_convert_dir, sub(r'[^.]*$', 'mp3', file_name_old))
            file_name_old = get_full_path(path_to_download_dir, file_name_old)

            info("Convert: " + file_name_old)
            if not os.exists(file_name_new):
                command = converter_command.replace("input", file_name_old).replace("output", file_name_new)
                info(command)
                subprocess.call(command, stdin=None, stderr=None, universal_newlines=True, shell=False)

        os.change_dir(os_dir)
        info("Convert: DONE")
