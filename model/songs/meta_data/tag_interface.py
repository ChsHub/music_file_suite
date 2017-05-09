# -*- coding: utf-8 -*-

from logging import info, error
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen._file import File
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TPE2
from utility.path_str import get_full_path


# TODO test if set is successful


class Tag:
    _tag = None
    file_path = None

    def __init__(self, path, file_name):

        self.file_path = get_full_path(path, file_name)
        self._tag = self.__get_tag(self.file_path)

        if self.file_path is None:
            raise NameError

    def __get_tag(self, full_path_uni):

        try:
            # audio_file = File(full_path_uni)
            audio_file = MP3(full_path_uni)  # , ID3=EasyID3, encoding=3 )#,, ID3=EasyID3, encoding=3

        except Exception as e:
            error("get audio_file " + full_path_uni)
            return None

        if audio_file is None:
            error("get_audiofile audio_file is none: " + full_path_uni)
            return None

        return audio_file

    def save_tag(self):
        try:
            self._tag.save(v1=0, v2_version=3)  #
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

        self._tag['TIT2'] = TIT2(encoding=3, text=title)
        # self._tag['title'] = title
        self.save_tag()

    def set_tag_track_num(self, track_num):

        if track_num:
            self._tag["TRCK"] = TRCK(encoding=3, text=track_num)
            # self._tag["track_num"] = track_num
            self.save_tag()

    def set_tag_artist(self, artist):

        self._tag['TPE1'] = TPE1(encoding=3, text=artist)
        # self._tag["artist"] = artist
        self.save_tag()

    def set_tag_album_artist(self, album_artist):

        self._tag["TPE2"] = TPE2(encoding=3, text=album_artist)
        # self._tag["albumartist"] = album_artist
        self.save_tag()

    def set_tag_album(self, album):

        self._tag["TALB"] = TALB(encoding=3, text=album)
        # self._tag["album"] = album
        self.save_tag()

    def reset(self):
        if self._tag:
            self._tag.clear()
            return True
        else:
            error("COULD NOT RESET TAG " + self.file_path)
            return False
