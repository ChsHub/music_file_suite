# -*- coding: utf8 -*-
from logging import info
from re import findall
from subprocess import PIPE, Popen, DEVNULL
from threading import BoundedSemaphore
from shlex import quote

from utility.encoding import decode
from utility.os_interface import get_cwd, change_dir, get_file_count
from utility.os_interface import rename_file, remove_file_ending
from utility.utilities import get_file_type

from src.resource.paths import downloader_command, path_to_download_dir


# TODO KILL/STOP
class Downloader:
    _Controller = None

    def __init__(self, controller):
        self._Controller = controller
        self._Download_sem = BoundedSemaphore(value=1)

    # TODO test directory delete
    def consume_element(self, url):

        match = r'(\d*\.?\d%)'

        with self._Download_sem:
            info("DOWNLOAD: " + url)
            os_dir = get_cwd()
            file_count = get_file_count(path_to_download_dir)

            change_dir(path_to_download_dir)
            process = Popen(downloader_command + [url], stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL, shell=True)

            file_name = ""
            for line in process.stdout:
                if "Destination: " in decode(line):
                    file_name = decode(line).split("Destination: ")[-1]
                    break

            data = '0%'
            while data:
                data = findall(match, data)
                if data:
                    self._Controller.set_download_progress(data[-1])
                try:
                    data = decode(process.stdout.read(108))
                except Exception as e:
                    pass
                print(data)

            # TODO playlists
            rename_file(path=".",
                        old_file=file_name,
                        new_file=remove_file_ending(file_name)[:-12] + get_file_type(file_name))
            change_dir(os_dir)

        info("FINISH DOWNLOAD")
