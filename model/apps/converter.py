# -*- coding: utf8 -*-
# ffmpeg-20161027-bf14393-win64-static

from logging import info
from re import sub
from subprocess import call

from utility.os_interface import exists, get_cwd, get_dir_list, make_directory, change_dir
from utility.path_str import get_full_path
from paths import converter_command
from queue_task import QueueTask
from subprocess import PIPE, run


class Converter(QueueTask):
    def __init__(self):
        QueueTask.__init__(self)

    def consume_element(self, path):
        os_dir = get_cwd()
        path_to_convert_dir = get_full_path(path, "CONVERTED")

        make_directory(path_to_convert_dir)
        change_dir(path_to_convert_dir)
        files = get_dir_list(path)

        info("Convert: " + str(len(files)) + " files")
        for file_name_old in files:
            file_name_new = get_full_path(path=path_to_convert_dir, file_name=sub(r'[^.]*$', 'mp3', file_name_old))
            file_name_old = get_full_path(path=path, file_name=file_name_old)

            info("Convert: " + file_name_old)
            if not exists(file_name_new):

                command = converter_command.replace("input", file_name_old)
                command = command.replace("output", file_name_new)

                call(command, stdout=None, stderr=None, shell=False)
               # info(result.returncode, result.stdout, result.stderr)

        change_dir(os_dir)
        info("Convert: DONE")
