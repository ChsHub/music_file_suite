from src.controller.generic_controller import GenericController
from src.model.apps.downloader import Downloader
from src.resource.settings import download_path


class ControllerDownloader(GenericController):
    def __init__(self, view, config):
        GenericController.__init__(self, view)
        self._downloader = Downloader(self, download_path, config['Downloader']['queue_path'],
                                      config.SelectionVideo, config.ffmpeg_path)

    # Notify model

    def download(self, url: str, video_choice: str):
        if self._downloader:
            self._submit(self._downloader.download, url, video_choice)
