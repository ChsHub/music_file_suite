import sys
import youtube_dl
from io import StringIO
from threading import Thread
from re import findall
from logging import info, exception

from persistqueue import FIFOSQLiteQueue
from utility.os_interface import get_cwd, change_dir


class Downloader(Thread, StringIO):
    _Controller = None
    _download_queue = None
    _active = True
    _current_url = None

    def __init__(self, controller, download_path, queue_path):
        Thread.__init__(self)
        StringIO.__init__(self)
        self._Controller = controller
        self._counter = -1
        self.daemon = True  # Stop thread, when program is closed
        self._download_path = download_path
        self._download_queue = FIFOSQLiteQueue(path=queue_path, multithreading=True, auto_commit=False)

    # TODO test directory delete
    # TODO playlists
    def run(self) -> None:
        """
        Overwrite Thread.run().
        If queue is not empty, download the first element
        """
        try:
            while self._active:
                info("DOWNLOAD QUEUE SIZE" + str(self._download_queue.size))
                url = self._download_queue.get()

                # Download the url
                self._counter += 1
                self._current_url = url
                with self:
                    try:
                        youtube_dl.main([url, '--no-check-certificate']) # , '-f bestvideo+bestaudio']  # , '-U'
                    except SystemExit as e:
                        info(e)

                # Save queue
                self._download_queue.task_done()

        except Exception as e:
            exception(e)

    def write(self, string):
        """
        Overwrite StringIO write().
        Parses youtube-dl Stdout output (https://stackoverflow.com/a/19345047)
        :param string: Stdout string
        :return: StringIO return value
        """
        # TODO read err and out simultaneously

        line = string.strip()
        info(line)
        progress = findall(r'(\d*\.?\d%)', line)

        if progress:
            self._set_download_progress(self._counter, progress[-1])
        elif line.startswith('[download] Destination: '):
            file_name = line.replace('[download] Destination: ', "")
            self._set_download_title(self._counter, file_name, self._current_url)
        elif line.endswith('has already been downloaded'):
            file_name = line.replace(' has already been downloaded', "").replace('[download] ', '')
            self._set_download_title(self._counter, file_name, self._current_url)

        return super().write(string)

    def __enter__(self):
        info("DOWNLOAD: " + self._current_url)
        # Change cwd to file output directory
        self._os_dir = get_cwd()
        change_dir(self._download_path)
        # Redirect stdout to custom function
        self._old_stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        info("Download: DONE")
        # Reset stdout to normal
        sys.stdout = self._old_stdout
        # Reset cwd to normal
        change_dir(self._os_dir)

    def download(self, url: str) -> None:
        """
        Put new url into the queue
        :param url: Url string
        """
        if not url:
            return
        url = url.strip()
        self._download_queue.put(url)

    def _set_download_progress(self, id, percent):
        self._Controller.set_download_progress(id, percent)

    def _set_download_title(self, id, title, url):
        self._Controller.set_download_title(id, title, url)
