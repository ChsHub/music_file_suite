# -*- coding: utf8 -*-
# python-2.7.12
__author__ = 'Christian'
import exceptions

import utility.log as log
from view.view import View

def main():
    log.logfile = log.Log()

    try:

        Main_view = View()

        # TODO remove return
        return

    except exceptions as e:
        log.logfile.handle_error("UNKNOWN", "UNKNOWN", e)

    log.logfile.write_logfile(u".")


if __name__ == '__main__':
    main()