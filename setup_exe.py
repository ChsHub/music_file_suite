# pip install youtube-dl
# pip install mutagen
# C:\Python38-32\python.exe -m pip install youtube-dl --upgrade

# GENERATES build/dist/.EXE
from src.resource.ConfigReader import ConfigReader
config = ConfigReader()

if __name__ == '__main__':
    from utility.setup_lib import setup_exe
    setup_exe(main_path='__main__.py', app_name=config['Window']['text_view_title'], resource_paths=[('resources', '.cfg'), ('lib', '')])
