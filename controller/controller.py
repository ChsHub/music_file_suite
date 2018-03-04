from utility.threadPoolExecutor import ThreadPoolExecutor  # TODO use concurrent.futures
# from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from logging import info
from model.model import Model
from view.window import Window


# python 3.2+


class Controller:
    Main_view = None
    _Main_model = None

    def __init__(self):
        self.executor = ThreadPoolExecutor()

        self._Main_model = Model(self)
        self.Main_view = Window(self)

    def submit(self, *args):  # TODO ERROR
        self.executor.submit(*args)  # .result())

    # +++View+++
    def analyze_files(self, file_path):
        if self._Main_model:
            self.submit(self._Main_model.analyze_files, file_path)

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

    def convert_all(self, path):
        if self._Main_model:
            self.submit(self._Main_model.convert_file, path)

    def make_playlist(self):
        if self._Main_model:
            self.submit(self._Main_model.make_playlist)

    # +++Model+++

    # called: Model -> Album -> Controller -> Window
    def set_view(self, data, type):
        if self.Main_view:
            self.Main_view.set_preview_data(data, type)

    def set_download_progress(self, percent):
        self.Main_view.set_download_progress(percent)
