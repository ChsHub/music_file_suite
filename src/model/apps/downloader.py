from logging import info, exception
from re import findall
from subprocess import PIPE, Popen, DEVNULL
from threading import BoundedSemaphore, Thread

from os.path import isfile, join, abspath
from persistqueue import FIFOSQLiteQueue
from utility.encoding import decode
from utility.os_interface import get_cwd, change_dir

from src.resource.paths import downloader_command
from src.resource.settings import download_path


# TODO KILL/STOP
class Downloader(Thread):
    _Controller = None
    _download_queue = FIFOSQLiteQueue(path="./resources/youtube_links", multithreading=True, auto_commit=False)
    _active = True

    def __init__(self, controller):
        super().__init__()
        self._Controller = controller
        self._counter = -1
        self.daemon = True

    def run(self) -> None:
        """
        If queue is not empty, download the first element
        """
        try:
            while self._active:
                info("D QUEUE SIZE" + str(self._download_queue.size))
                url = self._download_queue.get()
                self._handle_download(url)
                self._download_queue.task_done()  # Save queue
        except Exception as e:
            exception(e)

    def download(self, url: str) -> None:
        """
        Put new url into the queue
        :param url:
        """
        if not url:
            return
        url = url.strip()
        self._download_queue.put(url)

    # TODO test directory delete
    # TODO playlists
    def _handle_download(self, url:str) -> bool:
        """
        Download the resource from the url
        :param url: Resource link
        :return: True, if download has been successful
        """

        self._counter += 1
        file_name = ''
        info("DOWNLOAD: " + url)

        os_dir = get_cwd()
        change_dir(download_path)
        process = Popen(downloader_command + [url], stdin=DEVNULL, stdout=PIPE, stderr=PIPE, shell=True)

        while True:

            # err = process.stderr.readlines()
            # if err:
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
                self._Controller.set_download_progress(self._counter, '100%')
        info("Download: DONE")
        return True
