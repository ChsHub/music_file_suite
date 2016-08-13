# -*- coding: utf8 -*-
# python-2.7.12
__author__ = 'Christian'

import logging
from view.view import View
from model.model import Model
import datetime


def get_log_name():
    return str(datetime.datetime.now()).replace(':', '_').replace('.', '_')


def main():
    logging.basicConfig(filename='log_files/' + get_log_name() + '.log', level=logging.DEBUG)
    Main_model = Model()
    Main_view = View(Main_model)

    # TODO remove return
    return


if __name__ == '__main__':
    main()
