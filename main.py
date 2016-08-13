# -*- coding: utf8 -*-
# python-2.7.12
__author__ = 'Christian'

import logging
from view.view import View
from model.model import Model
import datetime


class Controller:
    _Main_view = None
    _Main_model = None

    def __init__(self):
        self._Main_view = View(self)
        self._Main_view.init_gui()


    def analyze_files(self, file_path):
        self._Main_model = Model(self)
        self._Main_model.analyze_files(file_path)

    def update_view(self, album_names):
        self._Main_view.update_view(album_names)

    def write_data(self, is_album):
        self._Main_model.change_files(is_album)

def get_log_name():
    return str(datetime.datetime.now()).replace(':', '_').replace('.', '_')


def main():
    logging.basicConfig(filename='log_files/' + get_log_name() + '.log', level=logging.DEBUG)

    Controller()
    # TODO remove return
    return


if __name__ == '__main__':
    main()
