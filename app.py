
# -*- coding: utf8 -*-
# python-3.5
from src.controller.controller import Controller
from utility.logger import Logger
from logging import info

from utility.os_interface import get_cwd, exists
from src.resource.paths import icon_path


# pip install youtube-dl
# pip install mutagen


def main():

    logger = Logger(5)
    info(get_cwd())
    info(exists(icon_path))
    controller = Controller()
    controller._Main_view.MainLoop()
    logger.shutdown()

