import logging
import re
import utility.os_interface as os_interface
from utility.path_str import change_file_name
from utility.utilities import get_file_type


class File_data:
    _track_num = None
    _artist = None
    _title = None
    # decisions
    is_album = None
    _error = False

    def __init__(self, file_name):

        if self._read_song_title(file_name):  # Artist - Song.mp3
            self.is_album = False
        elif self._read_song_title_album(file_name):  # 00 Song.mp3
            self.is_album = True
        else:
            logging.error("FAIL: " + file_name)
            self._error = True
            return

        self.clean_title()

    def clean_title(self):
        # TODO Regex
        self._title = self._title.replace(":", "").replace("*", "").replace("/", " ").replace('"', "").replace(
            '#', "")
        self._title = self._title.replace("[", "(").replace("]", ")").replace("é", "e")
        self._title = change_file_name(self._title)

    # Artist - Song
    def _read_song_title(self, file_name):
        #        if not self._artist:
        title = file_name.split(" - ")
        if len(title) is 2:
            self._artist = title[0]
            self._title = title[1][:-4]
            return True

        return False

    # 00 Song.mp3
    def _read_song_title_album(self, file_name):
        match = re.findall(r"(\d+)\s(.+)", file_name)
        if len(match) == 1:
            self._track_num = match[0][0]
            self._title = match[0][1][:-4]
            return True
        return False

    def get_is_album(self):
        return self.is_album

    def rename_file(self, album_path, new_name, file_name):

        os_interface.rename_file(album_path, file_name, new_name + get_file_type(file_name))  # TODO non mp3

        self._file_name = new_name
        return 0
