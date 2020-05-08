import logging
from os.path import join
from shutil import move
from re import sub, findall


class File_data:
    _track_num = ''
    _artist = ''
    _title = ''
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

        self._clean_title()

    def _clean_title(self):
        for old, new in [('*', ''), ('/', ' '), ('"', ''), (':', ''), ('#', ''), ('[', '('), ('_', ' '), (']', ')'),
                         ('(', ' ('), ('Feat', 'ft.'), ('ft', 'ft.'), ('vs', 'ft.'), ('Vs.', 'ft.'), ('  ', ' '),
                         ('..', '.'), ('..', '.')]:
            self._title = self._title.replace(old, new)

    # Artist - Song
    def _read_song_title(self, file_name):
        #        if not self._artist:
        title = file_name.split(" - ")
        if len(title) == 2:
            self._artist = title[0]
            self._title = title[1]
            return True
        else:
            return False

    # 00 Song.mp3
    def _read_song_title_album(self, file_name):
        match = findall(r"(\d+)\s(.+)", file_name)
        if len(match) == 1:
            self._track_num = match[0][0]
            self._title = match[0][1][:-4]
            return True
        else:
            return False

    def rename_file(self, album_path, file_name, new_name):
        new_name = sub(r'([?\\/:*"><|])', '', new_name).strip()  # Remove invalid characters under windows
        move(join(album_path, file_name), join(album_path, new_name))
