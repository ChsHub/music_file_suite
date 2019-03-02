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

        if not url:
            return

        # with self._Download_sem:
        self._counter += 1
        self._Controller.set_download_progress(self._counter, '0%')
        info("DOWNLOAD: " + url)
        os_dir = get_cwd()

        change_dir(path_to_download_dir)
        process = Popen(downloader_command + [url], stdin=DEVNULL, stdout=PIPE, stderr=PIPE, shell=True)


        while True:

            #err = process.stderr.readlines()
            #if err:
            #    self._Controller.set_download_progress(self._counter, 'Error: update youtube-dl version')
            #    error(str(err))
            #    return # TODO use async to read err and out simultaneously

            symbol = b''
            char = True
            while (not char in [b'\r', b'\n']) and char:
                char = process.stdout.read(1)
                symbol += char


            line0 = decode(symbol)
            if not line0:
                break
            line0 = line0.strip()
            print(line0)

            progress = findall(r'(\d*\.?\d%)', line0)
            if progress:
                self._Controller.set_download_progress(self._counter, progress[-1])
            elif line0.startswith('[download] Destination: '):
                line0 = line0.replace('[download] Destination: ', "")
                self._Controller.set_download_title(self._counter, line0)

        change_dir(os_dir)
        self._Controller.set_download_progress(self._counter, '100%')
        info("Download: DONE")
