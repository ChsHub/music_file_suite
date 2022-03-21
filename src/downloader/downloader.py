from logging import info, exception
from os.path import abspath
from threading import Thread

from persistqueue import SQLiteAckQueue

from src.abstract.abstract_list_model import AbstractListModel
from src.downloader.FileDownload import FileDownload


class Downloader(Thread, AbstractListModel):
    def __init__(self, controller, download_path, queue_path, SelectionVideo, ffmpeg_path):
        Thread.__init__(self, daemon=True)
        AbstractListModel.__init__(self, controller)

        self._counter = -1
        self._ffmpeg_path = ffmpeg_path
        self.download_path = download_path
        self._download_queue = SQLiteAckQueue(path=abspath(queue_path), multithreading=True, auto_commit=True)
        self.get_command = {SelectionVideo.NO_VIDEO.value: '', SelectionVideo.VIDEO.value: 'bestvideo+'}

        self.daemon = True  # Stop thread, when parent thread is terminated
        self.start()  # Start Downloader thread

    # TODO test directory delete
    # TODO handle playlists
    def run(self) -> None:
        """
        Overwrite Thread.run().
        If queue is not empty, download the first element
        """
        try:
            while True:
                info('DOWNLOAD QUEUE SIZE %s' % self._download_queue.size)
                item = self._download_queue.get()
                url, video_command = item

                info('DOWNLOAD: %s' % url)
                self._counter += 1
                current_file = FileDownload(self._ffmpeg_path, url, video_command, self)

                # Save queue
                if current_file.success:
                    self._download_queue.ack(item)
                    self.set_color_ok(self._counter)
                    info('DOWNLOAD QUEUE saved after download %s' % url)
                del current_file
        except Exception as e:
            exception(e)

    def download(self, url: str, video_choice: str) -> None:
        """
        Add new url to the queue
        :param url: Url string
        :param video_choice: Video quality
        """

        url = url.strip()
        video_choice = self.get_command[video_choice]
        if 'youtu' in url:
            self._download_queue.put((url, video_choice))
            info('Added to queue: %s' % url)

    # Notify view

    def set_download_progress(self, percent):
        self._controller.set_progress(self._counter, percent)

    def set_download_title(self, title, url):
        self.update_cell(data=url, column=0, row=self._counter)
        self.update_cell(data=title, column=1, row=self._counter)

    def set_download_size(self, size):
        self.update_cell(data=size, column=3, row=self._counter)

