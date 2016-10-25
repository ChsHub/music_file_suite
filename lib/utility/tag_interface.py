# -*- coding: utf-8 -*-
__author__ = 'Christian'

import logging

import path_str
from mutagen._file import File
from mutagen.id3 import TRCK, TIT2, TPE1, TALB, TPE2


# TODO test if set is successful


class Tag:
    _tag = None
    file_path = None

    def __init__(self, path, file_name):
        # print(EasyID3.valid_keys.keys())
        self._tag = self.__get_tag(path, file_name)
        self.file_path = path_str.get_full_path(path, file_name)

        if self.file_path is None:
            raise NameError

    def __get_audiofile(self, path, file_name):

        full_path_uni = path_str.get_full_path(path, file_name)

        audiofile = None
        try:
            audiofile = File(full_path_uni)
            # audiofile = MP3(full_path_uni, ID3=EasyID3, encoding=3)

        except Exception as e:
            logging.error("error get audiofile")

        if audiofile is None:
            logging.error("get_audiofile audiofile is none: " + file_name)
            return None

        return audiofile

    def __get_tag(self, path, file_name):
        audiofile = self.__get_audiofile(path, file_name)
        tag = audiofile

        if tag is None:
            logging.error("get_tag tag is none: " + file_name)
            return None
        return tag

    def save_tag(self):
        try:
            self._tag.save(v1=0, v2_version=3)
        except IOError as e:
            logging.error("FAIL: Save Tag (file disabled wr rights)", "save_tag " + self.file_path, e)
        except NotImplementedError as e:
            logging.error("Implement", self.file_path, e)
        except Warning as e:
            logging.error("reset_tag corrupted file", self.file_path, e)

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
        self.save_tag()

    def set_tag_track_num(self, track_num):

        if track_num:
            self._tag["TRCK"] = TRCK(encoding=3, text=track_num)
            self.save_tag()

    def set_tag_artist(self, artist):

        self._tag['TPE1'] = TPE1(encoding=3, text=artist)
        self.save_tag()

    def set_tag_album_artist(self, album_artist):

        self._tag["TPE2"] = TPE2(encoding=3, text=album_artist)
        self.save_tag()

    def set_tag_album(self, album):

        self._tag["TALB"] = TALB(encoding=3, text=album)
        self.save_tag()
