#from utility.threadPoolExecutor import ThreadPoolExecutor  # TODO use concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from logging import info

from model.apps.converter import Converter
from model.model import Model
from view.window import Window


# python 3.2+


class Controller:
    Main_view = None
    _Main_model = None

    def __init__(self):
        self.executor = ThreadPoolExecutor()

        self._Main_model = Model(self)
        self._Converter = Converter(self)
        self.Main_view = Window(self)

    def submit(self, *args):  # TODO ERROR
        self.executor.submit(*args)  # .result())

    # +++View+++
    def analyze_files(self, path, files):
        if self._Main_model:
            self.submit(self._Main_model.analyze_files, path, files)

    def set_data(self):
        if self._Main_model:
            self.submit(self._Main_model.set_data)

    def set_is_meta(self, is_meta):
        if self._Main_model:
            self.submit(self._Main_model.set_is_meta, is_meta)  # TODO

    def set_is_album(self, is_album):
        if self._Main_model:
            self.submit(self._Main_model.set_is_album, is_album)

    def download(self, url):
        if self._Main_model:
            self.submit(self._Main_model.download_file, url)

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