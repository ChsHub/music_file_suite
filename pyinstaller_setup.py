# pyinstaller __main__.py --noconsole --onedir
# pyinstaller __main__.spec --noconsole
from re import search, M
from subprocess import Popen
from utility.os_interface import delete_file, exists, get_full_path, read_file_data, write_file_data, get_absolute_path, \
    depth_search_files

from src.resource.paths import icon_path
from src.resource.texts import text_view_title


def get_tuples():
    files = depth_search_files(path='./lib/ffmpeg', types="")
    files = [str(((get_full_path(directory, file)), directory)) for directory, file in files]
    files = ",".join(files)
    return files


# TODO RUN TESTS

# Search project version
# TODO def method with setup.py
def get_version():
    version_match = search(r"^__version__ = ['\"]([^'\"]*)['\"]", read_file_data('./__init__.py'), M)
    if version_match:
        return version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


# generate .spec file
spec_file = text_view_title + '.spec'
if not exists(spec_file):
    # generate dist --noconsole
    Popen('pyinstaller __main__.py  --noconfirm --onedir --name "' + text_view_title +
          '" --icon "' + icon_path + '"').communicate()

    spec_data = read_file_data(spec_file)
    spec_data = spec_data.replace("datas=[",
                                  "datas=[" + get_tuples() + ",('" + icon_path + "','./src/resource/icons')"
                                                                                 ",('./log_files','./log_files')")
    write_file_data(".", spec_file, spec_data)
# no else

# generate dist
Popen('pyinstaller "' + text_view_title + '.spec" --noconfirm').communicate()

# run application
command = '"' + get_absolute_path(get_full_path('./dist', text_view_title, text_view_title + '.exe')) + '"'
# print(command)
# Popen(command).communicate()

# TODO refactor, remove hard coded
