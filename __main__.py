# TODO catch wx exceptions http://www.blog.pythonlibrary.org/2014/03/14/wxpython-catching-exceptions-from-anywhere/
from logger_default import Logger

if __name__ == '__main__':
    from logging import exception

    with Logger(debug=True):
        try:
            from src.abstract.view.window import Window

            _main_view = Window()
            _main_view.MainLoop()

        except Exception as e:
            exception(e)

    # TODO click on links in download list,  open directories from link
