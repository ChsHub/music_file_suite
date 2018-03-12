# python 3.2+
from concurrent.futures import ThreadPoolExecutor
from logging import error
from src.model.apps.downloader import Downloader
from src.model.apps.converter import Converter
from src.model.model import Model
from src.view.window import Window


class Controller:
    Main_view = None
    _Main_model = None
    _Converter = None
    _Downloader = None

    def __init__(self):
        self.executor = ThreadPoolExecutor()

        self._Main_model = Model(self)
        self._Converter = Converter(self)
        self._Downloader = Downloader(self)
        self.Main_view = Window(self)

    def submit(self, *args):
        future = self.executor.submit(*args)
        # called after execution of this task
        future.add_done_callback(self.error_log)

    @staticmethod
    def error_log(future):
        # returns None if no exception occurred
        exception = future.exception()
        if exception:
            error(type(exception))
            error(exception)

    # +++View+++
    def analyze_files(self, path, files):
        if self._Main_model:
            self.submit(self._Main_model.analyze_files, path, files)

    def set_data(self):
        if self._Main_model:
            self.submit(self._Main_model.set_data)

    def set_is_meta(self, is_meta):
        if self._Main_model:
            self.submit(self._Main_model.set_is_meta, is_meta)

    def set_is_album(self, is_album):
        if self._Main_model:
            self.submit(self._Main_model.set_is_album, is_album)

    def download(self, url):
        if self._Downloader:
            self.submit(self._Downloader.consume_element, url)

    def add_convert(self, path, files):
        if self._Converter:
            self.submit(self._Converter.consume_element, path, files)

    def make_playlist(self):
        if self._Main_model:
            self.submit(self._Main_model.make_playlist)

    def start_convert(self, selection):
        if self._Converter:
            self.submit(self._Converter.start_convert, selection)

    # +++Model+++

    # called: Model -> Album -> Controller -> Window
    def set_view(self, data, type):
        if self.Main_view:
            self.Main_view.set_preview_data(data, type)

    def set_download_progress(self, percent):
        self.Main_view.set_download_progress(percent)

    def set_convert_progress(self, id, percent):
        self.Main_view.set_convert_progress(id, percent)

    def add_convert_line(self, line):
        self.Main_view.add_convert_line(line)
