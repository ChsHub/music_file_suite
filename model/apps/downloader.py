# -*- coding: utf8 -*-
import subprocess
from queue_task import QueueTask
from logging import info
import os_interface as os
from paths import downloader_command, path_to_download_dir


class Downloader(QueueTask):

    def __init__(self):
        QueueTask.__init__(self)


    def consume_element(self, url):
        # TODO test directory delete
        os_dir = os.get_cwd()
        os.change_dir(path_to_download_dir)
        info("DOWNLOAD: "+url)
        subprocess.call(downloader_command + [url], stdin=None, stdout=None, stderr=None,
                        shell=True)
        os.change_dir(os_dir)
        info("DOWNLOAD: DONE")
        # TODO GUI