from utility.threadPoolExecutor import ThreadPoolExecutor # TODO use concurrent.futures
# from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from logging import info
from model.model import Model
from window import Window


# python 3.2+


class Controller:
    def __init__(self):
        with ThreadPoolExecutor(max_workers=cpu_count() * 2) as executor:
            self.executor = executor
            self._Main_model = Model(self)
            self._Main_view = Window(self)
            self._Main_view.start()

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

    def convert_all(self):
        if self._Main_model:
            self.submit(self._Main_model.convert_file)

    # +++Model+++

    # called: Model -> Album -> Controller -> Window
    def set_view(self, data, type):
        if self._Main_view:
            self._Main_view.set_preview_data(data, type)
