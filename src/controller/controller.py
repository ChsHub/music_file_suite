# python 3.2+
from concurrent.futures import ThreadPoolExecutor
from logging import exception
from os.path import abspath

from src.model.apps.downloader import Downloader
from src.model.apps.converter import Converter
from src.model.songs.album import Album
from src.resource.ConfigReader import ConfigReader
from src.view.window import Window
from src.resource.settings import download_path

class Controller:

    def __init__(self):
        with ThreadPoolExecutor() as self._executor:
            # Read all strings
            config = ConfigReader()

            self._Album = Album(self)
            self._Converter = Converter(self, config['Converter'])
            self._Downloader = Downloader(self, download_path, abspath(config['Downloader']['queue_path']))
            self._Main_view = Window(self, config['Window'])
            self._Downloader.start() # Start downloader thread
            self._Main_view.MainLoop()

    def _submit(self, *args):
        future = self._executor.submit(*args)
        # called after execution of this task
        future.add_done_callback(self.error_log)

    @staticmethod
    def error_log(future):
        # returns None if no exception occurred
        result = future.exception()
        if result:
            exception(result)

    # +++View+++
    def analyze_files(self, path, files):
        if self._Album:
            self._submit(self._Album.set_files, path, files)

    def set_data(self):
        if self._Album:
            self._submit(self._Album.set_data)

    def set_is_meta(self, is_meta):
        if self._Album:
            self._submit(self._Album.set_is_meta, is_meta)

    def set_is_album(self, is_album):
        if self._Album:
            self._submit(self._Album.set_is_album, is_album)

    def download(self, url):
        if self._Downloader:
            self._submit(self._Downloader.download, url)

    def make_playlist(self):
        if self._Album:
            self._submit(self._Album.make_playlist)

    def edit_song(self, row, column, data):
        if self._Album:
            self._submit(self._Album.edit_song, row, column, data)

    # +++ Converter +++

    def add_convert(self, path, files):
        if self._Converter:
            self._submit(self._Converter.add_job, path, files)

    def start_convert(self, selection):
        if self._Converter:
            self._submit(self._Converter.start_convert, selection)

    # +++ Model +++

    # +++ Downloader +++
    # called: Album -> Controller -> Window
    def set_view(self, data):
        if self._Main_view:
            self._Main_view.set_preview_data(data)

    def set_download_progress(self, id, percent):
        self._Main_view.set_download_progress(id, percent)

    def set_download_title(self, id, title, url):
        self._Main_view.set_download_title(id, title, url)

    # +++ CONVERTER +++

    def set_convert_progress(self, id, percent):
        self._Main_view.set_convert_progress(id, percent)

    def add_convert_line(self, line):
        self._Main_view.add_convert_line(line)

    def update_meta_line(self, row, data):
        if self._Main_view:
            self._Main_view.update_preview_row(row, data)

    def set_meta_color_normal(self, id):
        if self._Main_view:
            self._Main_view.set_meta_color_normal(id)

    def set_meta_color_warning(self, row):
        if self._Main_view:
            self._Main_view.set_meta_color_warning(row)

    def set_meta_color_ok(self, row):
        if self._Main_view:
            self._Main_view.set_meta_color_ok(row)
