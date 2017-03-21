# -*- coding: utf8 -*-
# python-3.5
from controller import Main_Controller
from utility.logger import Logger


def main():
    logger = Logger()
    controller = Main_Controller()
    logger.shutdown()


if __name__ == '__main__':
    main()
