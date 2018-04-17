# -*- coding: utf8 -*-
# python-3.5
from logging import info

from utility.os_interface import get_cwd, exists

from src.controller import Controller
from utility.logger import Logger

# pip install youtube-dl
# pip install mutagen

def main():
    logger = Logger(5)

    controller = Controller()
    logger.shutdown()

if __name__ == '__main__':
    # https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip
    main()
    # TODO youtube link history
    # TODO Resume in next session
    # TODO Settings
    # TODO Languages
    # TODO upgrade youtube-dl, mutagen
    # TODO click on links in download list
    # TODO open directories from link
