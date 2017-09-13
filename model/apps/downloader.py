# -*- coding: utf8 -*-
from logging import info, error
from subprocess import call
from threading import BoundedSemaphore

from utility.os_interface import get_cwd, change_dir, get_file_count

from paths import downloader_command, path_to_download_dir


class Downloader:
    def __init__(self):
        self.download_sem = BoundedSemaphore(value=1)

    # TODO test directory delete
    def consume_element(self, url):

        with self.download_sem:
            info("DOWNLOAD: " + url)
            os_dir = get_cwd()
            file_count = get_file_count(path_to_download_dir)

            change_dir(path_to_download_dir)
            call(downloader_command + [url], stdin=None, stdout=None, stderr=None, shell=True)
            change_dir(os_dir)

            if file_count + 1 != get_file_count(path_to_download_dir):
                error("DOWNLOAD: " + url)
            else:
                info("DOWNLOAD: DONE")
