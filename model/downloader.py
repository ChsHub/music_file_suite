# -*- coding: utf8 -*-
import subprocess
from threading import Thread
import os_interface as os
from paths import path_to_youtube_dl, path_to_download_dir

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

class Downloader(Thread):
    _url = None
    def __init__(self, url):
        Thread.__init__(self)
        self._url = url

    def run(self):
        # TODO test directory delete
        os_dir = os.get_cwd()
        os.change_dir(path_to_download_dir)
        subprocess.call([path_to_youtube_dl, '--no-check-certificate', self._url], stdin=None, stdout=None, stderr=None,
                        shell=True)
        #os.change_dir(os_dir)
        print("DOWNLOAD: DONE")
