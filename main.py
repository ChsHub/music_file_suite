# -*- coding: utf8 -*-
# python-2.7.12
__author__ = 'Christian'

import datetime
import logging

from model.model import Model
from view.view import View
import lib.utility.os_interface as os
import lib.utility.encoding as encoding

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

def get_log_name():
    #return os.get_cwd() + '/log_files/' + str(datetime.datetime.now()).replace(':', '_').replace('.', '_') + '.log'
    return encoding.f_decode('log_files/' + str(datetime.datetime.now()).replace(':', '_').replace('.', '_') + '.log')


def main():
    logging.basicConfig(filename=get_log_name(), level=logging.DEBUG)
    print(get_log_name())
    print(os.get_cwd())
    try:
        Controller()

        logging.warning("TEST")
    except Exception as e:
        logging.error(str(e))
    logging.shutdown()


if __name__ == '__main__':
    main()
