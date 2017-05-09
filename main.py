# -*- coding: utf8 -*-
# python-3.5
from controller import Controller
from utility.logger import Logger


def main():
    logger = Logger()
    controller = Controller()
    logger.shutdown()


if __name__ == '__main__':
    main()
