# pip install youtube-dl
# pip install mutagen
# https://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip
# pyinstaller __main__.py --noconsole --onedir
# pyinstaller __main__.spec --noconsole
# C:\Python36-32\python.exe -m pip install youtube-dl --upgrade

# GENERATES build/dist/.EXE
from re import search, M
from subprocess import Popen
from utility.os_interface import delete_file, exists, get_full_path, read_file_data, write_file_data, \
    get_absolute_path, depth_search_files, make_directory

from src.resource.paths import icon_path
from src.resource.texts import text_view_title


def get_tuples(path, types):
    files = depth_search_files(path=path, types=types)
    files = [str(((get_full_path(directory, file)), directory)) for directory, file in files]
    files = ",".join(files)
    return files


# Search project version
def get_version():
    version_match = search(r"^__version__ = ['\"]([^'\"]*)['\"]", read_file_data('./__init__.py'), M)
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError('Unable to find version string.')


def generate_dist():
    # TODO RUN TESTS
    # generate .spec file
    spec_file = text_view_title + '.spec'
    if not exists(spec_file): #
        Popen('pyinstaller __main__.py --noconfirm --onedir --noconsole --name "' + text_view_title +
              '" --icon "' + icon_path + '"').communicate()

        spec_data = read_file_data(spec_file)
        lib_data = get_tuples('./lib/', types='') + ',' + \
                   get_tuples('resources', types=['.ico', '.cfg'])
        print(lib_data)
        spec_data = spec_data.replace('datas=[',
                                      'datas=[' + lib_data)
        write_file_data(".", spec_file, spec_data)
    # no else

    # generate dist
    # no confirm -> overwrite last dist
    Popen('pyinstaller "' + spec_file + '" --noconfirm').communicate()
    delete_file(spec_file)
    # run application
    command = '"' + get_absolute_path(get_full_path('./dist', text_view_title, text_view_title + '.exe')) + '"'
    print(command)
    Popen(command).communicate()

    # TODO refactor, remove hard coded


if __name__ == '__main__':
    generate_dist()