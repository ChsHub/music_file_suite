
# -*- coding: utf8 -*-
# python-3.5
from src.controller.controller import Controller
from utility.logger import Logger


# pip install youtube-dl
# pip install mutagen


def main():
    logger = Logger(5)
    controller = Controller()
    #logger.shutdown()
    return controller.Main_view
