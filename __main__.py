

if __name__ == '__main__':
    from utility.logger import Logger
    from logging import info, exception

    with Logger(20):
        try:
            from src.controller.controller import Controller
            from utility.os_interface import get_cwd, exists
            from src.resource.paths import icon_path

            info(get_cwd())
            info(exists(icon_path))
            controller = Controller()

        except Exception as e:
            exception(e)

    # TODO click on links in download list,  open directories from link
