import datetime
import logging

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

    def _get_log_name(self):
        return 'log_files/' + str(datetime.datetime.now()).replace(':', '_').replace('.', '_') + '.log'

    def shutdown(self):
        logging.shutdown()
