from logging import info
from re import findall
from subprocess import PIPE, Popen, DEVNULL
from threading import BoundedSemaphore

from utility.encoding import decode
from utility.os_interface import get_cwd, change_dir

from src.resource.paths import downloader_command, path_to_download_dir


# TODO KILL/STOP
class Downloader:
    _Controller = None

    def __init__(self, controller):
        self._Controller = controller
        self._Download_sem = BoundedSemaphore(value=1)
        self._counter = 0

    # TODO test directory delete
    # TODO playlists
    def consume_element(self, url):

        with self._Download_sem:
            info("DOWNLOAD: " + url)
            os_dir = get_cwd()

            change_dir(path_to_download_dir)
            process = Popen(downloader_command + [url], stdin=DEVNULL, stdout=PIPE, stderr=PIPE, shell=True)

            for line in process.stdout:
                line = decode(line)
                progress = findall(r'(\d*\.?\d%)', line)
                if progress:
                    self._Controller.set_download_progress(self._counter, progress[-1])

            change_dir(os_dir)

            self._Controller.set_download_progress(self._counter, '100%')
            self._counter += 1

        info("Download: DONE")
