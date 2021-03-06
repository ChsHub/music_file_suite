from configparser import ConfigParser
from genericpath import exists

settings_path = 'resources/settings.cfg'
config = ConfigParser()


def set_download_directory(path):
    config['Paths'] = {'download': path.strip()}

    with open(settings_path, 'w') as configfile:
        config.write(configfile)


# Write default settings, if missing
if not exists(settings_path):
    set_download_directory('C:\\Downloads')

config.read(settings_path)
download_path = config['Paths']['download']
