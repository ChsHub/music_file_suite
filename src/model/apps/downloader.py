from logging import info
from re import findall
from subprocess import PIPE, Popen, DEVNULL
from threading import BoundedSemaphore

from os.path import isfile, join, abspath
from utility.encoding import decode
from utility.os_interface import get_cwd, change_dir

from src.resource.paths import downloader_command
from src.resource.settings import download_path


# TODO KILL/STOP
class Downloader:
    _Controller = None
    _download_queue = []
    _active = True
    _log_path = abspath('resources/download_queue.log')

    def __init__(self, controller):
        self._Controller = controller
        self._Download_sem = BoundedSemaphore(value=1)
        self._queue_sem = BoundedSemaphore(value=1)
        self._counter = -1

    def _save_queue(self):
        with self._queue_sem:
            with open(self._log_path, mode='w') as f:
                f.write('\n'.join(self._download_queue))

    def load_queue(self):

        with self._queue_sem:
            with open(self._log_path, mode='r') as f:
                for line in f:
                    self._download_queue.append(line.strip())

        for url in self._download_queue:
            self._handle_download(url)

    def download(self, url):
        if not url:
            return
        with self._queue_sem:
            self._download_queue.append(url)
        self._save_queue()
        self._handle_download(url)

    # TODO test directory delete
    # TODO playlists
    def _handle_download(self, url):


        with self._Download_sem:


            self._counter += 1
            file_name = ''
            info("DOWNLOAD: " + url)

            os_dir = get_cwd()
            change_dir(download_path)
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
                info(line0)

                progress = findall(r'(\d*\.?\d%)', line0)
                if progress:
                    self._Controller.set_download_progress(self._counter, progress[-1])
                elif line0.startswith('[download] Destination: '):
                    file_name = line0.replace('[download] Destination: ', "")
                    self._Controller.set_download_title(self._counter, file_name, url)
                elif line0.endswith('has already been downloaded'):
                    file_name = line0.replace(' has already been downloaded', "").replace('[download] ', '')
                    self._Controller.set_download_title(self._counter, file_name, url)

            change_dir(os_dir)
            if file_name:
                if isfile(join(download_path, file_name)):
                    with self._queue_sem:
                        self._download_queue.remove(url)
                    self._Controller.set_download_progress(self._counter, '100%')
            self._save_queue()
            info("Download: DONE")
