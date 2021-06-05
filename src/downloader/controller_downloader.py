from src.abstract.abstract_controller import AbstractController
from src.downloader.downloader import Downloader
from src.resource.settings import download_path


class ControllerDownloader(AbstractController):
    def __init__(self, view, config):
        AbstractController.__init__(self, view)
        self._downloader = Downloader(self, download_path, config['Downloader']['queue_path'],
                                      config.SelectionVideo, config.ffmpeg_path)

    # Notify model

    def download(self, url: str, video_choice: str):
        if self._downloader:
            self._submit(self._downloader.download, url, video_choice)
