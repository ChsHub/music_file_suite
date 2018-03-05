# -*- coding: utf8 -*-
from logging import info, error
from subprocess import PIPE, Popen
from threading import BoundedSemaphore
from re import findall
from utility.os_interface import get_cwd, change_dir, get_file_count
from utility.encoding import decode
from tempfile import TemporaryFile
from resource.paths import downloader_command, path_to_download_dir

# TODO KILL/STOP
class Downloader:
    __model = None

    def __init__(self, model):
        self.__model = model
        self.download_sem = BoundedSemaphore(value=1)

    # TODO test directory delete
    def consume_element(self, url):

        match = r'(\d*\.?\d%)'

        with self.download_sem:
            info("DOWNLOAD: " + url)
            os_dir = get_cwd()
            file_count = get_file_count(path_to_download_dir)

            change_dir(path_to_download_dir)

            process = Popen(downloader_command + [url], stdin=None, stdout=PIPE, stderr=None, shell=False)

            # process.stdout = StdOutput()
            # err, out = process.communicate()
            # return

            data = '0%'
            while data:
                data = findall(match, data)
                if data:
                    self.__model.set_download_progress(data[-1])
                data = decode(process.stdout.read(108))
                print(data)

            change_dir(os_dir)

        info("FINISH DOWNLOAD")