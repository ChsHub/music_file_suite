# -*- coding: utf8 -*-
# python-2.7.12


from converter import Converter

from downloader import Downloader
from model.model import Model
from utility.logger import Logger
from view.window import Window


class Controller:
    _Main_view = None
    _Main_model = None

    def __init__(self):
        self._Main_model = Model(self)
        self._Main_view = Window(self)
        self._Main_view.init_gui()


    def analyze_files(self, file_path):
        self._Main_model.analyze_files(file_path)

    def update_view(self, album_names):
        self._Main_view.update_view(album_names)

    def set_view(self, data):
        self._Main_view.set_preview_data(data)

    def set_data(self):
        return self._Main_model.set_data()

    def download(self, url):
        Downloader(url).start()

    def convert_all(self, path):
        Converter(path).start()


def main():
    logger = Logger()
    # try:
    Controller()

    # logging.error("TEST")
    # except Exception as e:
    #   logging.error(str(e))

    logger.shutdown()


if __name__ == '__main__':
    main()
