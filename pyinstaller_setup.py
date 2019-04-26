# pip install youtube-dl
# pip install mutagen
# https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip
# C:\Python37\python.exe -m pip install youtube-dl --upgrade

# GENERATES build/dist/.EXE
from src.resource.texts import text_view_title

if __name__ == '__main__':
    from utility.setup_lib import setup_exe
    setup_exe(main_path='__main__.py', app_name=text_view_title, resource_paths=[('resources', '.cfg'), ('lib', '')])

