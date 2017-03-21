# -*- coding: utf8 -*-
from subprocess import call
from logging import info
from os_interface import get_cwd, change_dir
from paths import downloader_command, path_to_download_dir
from queue_task import QueueTask


class Downloader(QueueTask):

    def __init__(self):
        QueueTask.__init__(self)

    def consume_element(self, url):
        # TODO test directory delete
        os_dir = get_cwd()
        change_dir(path_to_download_dir)
        info("DOWNLOAD: "+url)
        call(downloader_command + [url], stdin=None, stdout=None, stderr=None,
                        shell=True)
        change_dir(os_dir)
        info("DOWNLOAD: DONE")
        # TODO GUI