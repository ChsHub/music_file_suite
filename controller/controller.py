from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

from model.model import Model
from window import Window


# python 3.2+


class Controller:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=cpu_count() * 2)
        self._Main_model = Model(self)
        self._Main_view = Window(self)
        self._Main_view.start()
        self.executor.shutdown()

    def analyze_files(self, file_path):
        self.executor.submit(self._Main_model.analyze_files, file_path)

    def set_data(self):
        if self._Main_model:
            return self._Main_model.set_data()

    def update_view(self, is_album):
        if self._Main_view:
            self.executor.submit(self._Main_model.update_view, is_album)

    # called: Model -> Album -> Controller -> Window
    def set_view(self, data):
        if self._Main_view:
            self._Main_view.set_preview_data(data)

    def download(self, url):
        self.executor.submit(self._Main_model.download_file, url)

    def convert_all(self, path):
        self.executor.submit(self._Main_model.convert_file, path)
