# -*- coding: utf-8 -*-

from logging import info, error
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen._file import File
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TPE2
from utility.path_str import get_full_path


# mutagen-1.37
# TODO test if set is successful


class TagMP3:
    _tag = None
    file_path = None

    def __init__(self, path, file_name):

        self.file_path = get_full_path(path, file_name)

        if self.file_path is None:
            raise NameError

        try:
            self._tag = MP3(self.file_path)  # , ID3=EasyID3, encoding=3)
        except Exception as e:
            error("READ MP3 META " + self.file_path + " " + str(e))

        if self._tag is None:
            error("READ MP3 META : " + self.file_path + " is none")

    def save_tag(self):
        try:
            self._tag.save(v1=0, v2_version=3)
        except IOError as e:
            error("FAIL: Save Tag (file disabled wr rights)", "save_tag " + self.file_path, e)
        except NotImplementedError as e:
            error("Implement", self.file_path, e)
        except Warning as e:
            error("reset_tag corrupted file", self.file_path, e)

    # GETTER
    def get_attribute(self, attribute_str):

        if self._tag is not None:
            if attribute_str in self._tag:
                attribute = self._tag[attribute_str]
                if attribute:
                    return attribute[0]
        return None

    def get_tag_title(self):
        return self.get_attribute('TIT2')

    def get_tag_track_num(self):
        return self.get_attribute('TRCK')

    def get_artist(self):
        return self.get_attribute('TPE1')

    def get_album_artist(self):
        return self.get_attribute('TPE2')

    def get_album(self):
        return self.get_attribute('TALB')

    # SETTER
    def set_tag_title(self, title):
        if title:
            self._tag['TIT2'] = TIT2(encoding=3, text=title)

    def set_tag_track_num(self, track_num):
        if track_num:
            self._tag["TRCK"] = TRCK(encoding=3, text=track_num)

    def set_tag_artist(self, artist):
        if artist:
            self._tag['TPE1'] = TPE1(encoding=3, text=artist)

    def set_tag_album_artist(self, album_artist):
        if album_artist:
            self._tag["TPE2"] = TPE2(encoding=3, text=album_artist)

    def set_tag_album(self, album):
        if album:
            self._tag["TALB"] = TALB(encoding=3, text=album)

    def reset(self):
        if self._tag:
            self._tag.clear()
            return True
        else:
            error("COULD NOT RESET TAG " + self.file_path)
            return False
