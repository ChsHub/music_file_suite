__author__ = 'Christian'
import datetime

import os_interface


class Log:
    fails_count = 0
    fails = ''

    def __init__(self):
        return

    def __new__(self):
        if logfile is None:
            return self
        return logfile

    def get_timestamp(self):
        return str(datetime.datetime.now()).replace(':', '_').replace('.', '_')

    def __print_log(self, fail_message):

        self.fails_count += 1
        self.fails += self.get_timestamp() + '  ' + fail_message + ' \n'

    def write_logfile(self, path):
        self.__write_logfile1(path, self.fails_count)

    def __write_logfile1(self, path, fails_count, file_count=0):

        file_name = 'FAILS ' + self.get_timestamp()

        if file_count != 0:
            o = str(fails_count) + ' of ' + str(file_count)
            file_name += ' ' + o + '.txt'
        else:
            file_name += '.txt'
        if fails_count > 0:
            os_interface.write_file_data(path, file_name, self.fails)

    def handle_error(self, e_kind, file_name, error=None):
        message = ''
        if error is not None:
            message = str(error)
        s_message = "FAIL [ "
        s_message +=  e_kind + " ]: "

        s_message += file_name
        s_message += " MESSAGE: "
        s_message +=   message
        self.__print_log( s_message)
        return 1

    def info_message(self, place, message):
        self.__print_log("INFO [ " + place + " ]: " + message)
        return 1


logfile = None
