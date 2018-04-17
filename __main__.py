from logging import info

from utility.os_interface import get_cwd, exists

from app import main
from src.resource.paths import icon_path

if __name__ == '__main__':
    print(get_cwd())
    print(exists(icon_path))
    main().MainLoop()
