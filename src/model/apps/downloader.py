from logging import info, error
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
        self._counter = -1

    # TODO test directory delete
    # TODO playlists
    def download(self, url):

        with self._Download_sem:
            self._counter += 1
            info("DOWNLOAD: " + url)
            os_dir = get_cwd()

            change_dir(path_to_download_dir)
            process = Popen(downloader_command + [url], stdin=DEVNULL, stdout=PIPE, stderr=PIPE, shell=True)

            line0, line1 = ' ', ''
            while line0 != line1:

                err = process.stderr.readlines()
                if err:
                    self._Controller.set_download_progress(self._counter, 'Error: update youtube-dl version')
                    error(str(err))
                    return
                line1 = line0
                line0 += decode(process.stdout.read(100))
                progress = line0.split('\r')
                if len(progress) > 1:
                    progress, line0 = progress[-2:]
                    print(progress)
                    progress = findall(r'(\d*\.?\d%)', progress)
                    if progress:
                        self._Controller.set_download_progress(self._counter, progress[-1])

            change_dir(os_dir)
            self._Controller.set_download_progress(self._counter, '100%')
            info("Download: DONE")
