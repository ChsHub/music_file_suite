import datetime
import sys
from logging import  basicConfig, StreamHandler, FileHandler, DEBUG, Formatter, getLogger, shutdown

from os_interface import get_dir_list, delete_file
from os_interface import make_directory


class Logger:
    def __init__(self):
        _max_count_logfiles = 10
        # Delete old log files
        logging_path = './log_files'
        make_directory(logging_path)

        dir_list = get_dir_list(logging_path)
        filter(lambda x: ".log" in x, dir_list)

        for file in dir_list[:-_max_count_logfiles]:

            delete_file(logging_path, file)

        # WRITE Log
        basicConfig(handlers=[FileHandler(self._get_log_name(), 'w', 'utf-8')], level=DEBUG)

        ch = StreamHandler(sys.stdout)
        ch.setLevel(DEBUG)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = Formatter('%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        getLogger().addHandler(ch)

    def _get_log_name(self):
        return 'log_files/' + str(datetime.datetime.now()).replace(':', '_').replace('.', '_') + '.log'

    def shutdown(self):
        shutdown()
