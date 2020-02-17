# TODO catch wx exceptions http://www.blog.pythonlibrary.org/2014/03/14/wxpython-catching-exceptions-from-anywhere/


if __name__ == '__main__':
    from logging import exception

    try:
        from src.view.window import Window

        _main_view = Window()
        _main_view.MainLoop()
    except Exception as e:
        exception(e)

    # TODO click on links in download list,  open directories from link
