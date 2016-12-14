import datetime
import logging
import sys

import utility.os_interface as os

_max_count_logfiles = 10


class Logger:
    def __init__(self):
        # Delete old log files
        logging_path = os.get_cwd() + '/log_files'
        dir_list = os.get_dir_list(logging_path)

        while len(dir_list) > _max_count_logfiles:
            os.delete_file(logging_path, dir_list.pop(0))

        # WRITE Log
        logging.basicConfig(handlers=[logging.FileHandler(self._get_log_name(), 'w', 'utf-8')], level=logging.DEBUG)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
       # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logging.getLogger().addHandler(ch)

    def _get_log_name(self):
        return 'log_files/' + str(datetime.datetime.now()).replace(':', '_').replace('.', '_') + '.log'

    def shutdown(self):
        logging.shutdown()
