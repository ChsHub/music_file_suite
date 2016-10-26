# -*- coding: utf8 -*-
# python-2.7.12


import datetime
import logging
import utility.os_interface as os
from model.downloader import Downloader
from model.model import Model
from view.view import View
_max_count_logfiles = 10


class Controller:
    _Main_view = None
    _Main_model = None

    def __init__(self):
        self._Main_view = View(self)
        self._Main_view.init_gui()

    def analyze_files(self, file_path, is_album):
        self._Main_model = Model(self)
        return self._Main_model.analyze_files(file_path, is_album)

    def update_view(self, album_names):
        self._Main_view.update_view(album_names)

    def get_data(self, is_album):
        return self._Main_model.get_data(is_album)

    def set_data(self, is_album):
        return self._Main_model.set_data(is_album)

    def download(self, url):

        Downloader(url).start()


def get_log_name():
    return 'log_files/' + str(datetime.datetime.now()).replace(':', '_').replace('.', '_') + '.log'


def init_logging():
    # Delete old log files
    logging_path = os.get_cwd() + '/log_files'
    dir_list = os.get_dir_list(logging_path)

    while len(dir_list) > _max_count_logfiles:
        os.delete_file(logging_path, dir_list.pop(0))

    # WRITE Log
    logging.basicConfig(handlers=[logging.FileHandler(get_log_name(), 'w', 'utf-8')], level=logging.DEBUG)


def main():
    init_logging()
    # try:
    Controller()

    # logging.error("TEST")
    # except Exception as e:
    #   logging.error(str(e))
    logging.shutdown()


if __name__ == '__main__':
    main()
