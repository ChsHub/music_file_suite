# -*- coding: utf8 -*-
# python-2.7.12


from utility.logger import Logger
from model.converter import Converter
from model.downloader import Downloader
from model.model import Model
from view.window import View


class Controller:
    _Main_view = None
    _Main_model = None

    def __init__(self):
        self._Main_view = View(self)
        self._Main_view.init_gui()

    def analyze_files(self, file_path):
        self._Main_model = Model(self)
        return self._Main_model.analyze_files(file_path)

    def update_view(self, album_names):
        self._Main_view.update_view(album_names)

    def get_data(self):
        return self._Main_model.get_data()

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
