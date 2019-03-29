# pip install youtube-dl
# pip install mutagen
# https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip
# pyinstaller __main__.py --noconsole --onedir
# pyinstaller __main__.spec --noconsole
# C:\Python37\python.exe -m pip install youtube-dl --upgrade

# GENERATES build/dist/.EXE
from os.path import join
from subprocess import Popen
from utility.os_interface import delete_file, exists, read_file_data, write_file_data, \
    get_absolute_path
from utility.setup_lib import get_tuples
from src.resource.paths import icon_path
from src.resource.texts import text_view_title


def generate_dist():
    # TODO RUN TESTS
    # Generate .spec file
    spec_file = text_view_title + '.spec'
    if not exists(spec_file): #
        Popen('pyinstaller __main__.py --noconfirm --onedir --noconsole --name "' + text_view_title +
              '" --icon "' + icon_path + '"').communicate()

        spec_data = read_file_data(spec_file)
        spec_data = spec_data.replace('datas=[',
                                      'datas=[' + get_tuples('./lib/', types='') + ','
                                      + get_tuples('resources', types=['.ico', '.cfg']))
        write_file_data(".", spec_file, spec_data)
    # no else

    # Generate dist
    # No confirm -> overwrite last dist
    Popen('pyinstaller "' + spec_file + '" --noconfirm').communicate()
    delete_file(spec_file)
    # Run application
    command = '"' + get_absolute_path(join('./dist', text_view_title, text_view_title + '.exe')) + '"'
    print(command)
    Popen(command).communicate()


if __name__ == '__main__':
    generate_dist()
