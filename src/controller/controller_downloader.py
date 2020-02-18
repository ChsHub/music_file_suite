from src.controller.generic_controller import GenericController
from src.model.apps.downloader import Downloader
from src.resource.settings import download_path


class ControllerDownloader(GenericController):
    def __init__(self, view, config):
        GenericController.__init__(self)
        self._view = view

        self._downloader = Downloader(self, download_path, config['Downloader']['queue_path'],
                                      config.SelectionVideo, config.ffmpeg_path)

    # Notify model

    def download(self, url: str, video_choice: str):
        if self._downloader:
            self._submit(self._downloader.download, url, video_choice)

    # Notify view

    def set_download_progress(self, id, percent):
        self._view.set_download_progress(id, percent)

    def set_download_title(self, id, title, url):
        self._view.set_download_title(id, title, url)

    def set_download_size(self, id, size):
        self._view.set_download_size(id, size)

    def set_finished_color(self, row):
        self._view.set_finished_color(row)
