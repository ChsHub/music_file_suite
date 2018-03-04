# -*- coding: utf8 -*-
from logging import info, error
from subprocess import PIPE, Popen
from threading import BoundedSemaphore
from re import findall
from utility.os_interface import get_cwd, change_dir, get_file_count
from tempfile import TemporaryFile
from paths import downloader_command, path_to_download_dir


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

            process = Popen(downloader_command + [url], stdin=None, stdout=PIPE, stderr=None, shell=True)

            # print(type(process.stdout))

            while process.stdout:
                data = str(process.stdout.read(174))
                print(data)
                data = findall(match, data)
                if data:
                    self.__model.set_download_progress(data[-1])
                # lines = data.split("\r")
                # data = lines.pop()
                # for line in lines:
                #    print(line)

            try:
                outs, errs = process.communicate()
            # print(outs)
            # print(errs)
            # print(argv)
            except Exception as e:
                process.kill()
                outs, errs = process.communicate()

            change_dir(os_dir)

        # TODO remove
        if file_count + 1 != get_file_count(path_to_download_dir):
            error("DOWNLOAD: " + url)
        else:
            info("DOWNLOAD: DONE")
