# python-3.5


if __name__ == '__main__':
    from utility.logger import Logger
    from logging import info, error

    with Logger(20):
        try:
            from src.controller.controller import Controller
            from utility.os_interface import get_cwd, exists
            from src.resource.paths import icon_path

            info(get_cwd())
            info(exists(icon_path))
            controller = Controller()
            controller._Main_view.MainLoop()

        except Exception as exception:
            error(exception)

    # TODO youtube link history
    # TODO Resume in next session
    # TODO click on links in download list,  open directories from link
    # TODO Languages
