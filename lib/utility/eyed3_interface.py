__author__ = 'Christian'

from lib import *
import eyed3
import encoding
import logging
import path_str


class Tag:
    tag = None
    file_path = None

    def __init__(self, path, file_name):
        self.tag = self.__get_tag(path, file_name)
        self.file_path = path_str.get_full_path(path, file_name)
        if self.file_path is None:
            raise NameError

    def __new__(self):
        return self

    # TODO
    def __get_audiofile(self, path, file_name):
        full_path_uni = encoding.f_decode(path_str.get_full_path(path, file_name))
        try:
            audiofile = eyed3.load(full_path_uni)
        except Warning as e:
            logging.error("__get_audiofile corrupted file", self.file_path, e)
            return None
        except ValueError as e:
            logging.error("__get_audiofile", self.file_path, e)
            return None

        if audiofile is None:
            logging.error("get_audiofile", "audiofile is none: " + file_name)
            return None
        return audiofile

    def __get_tag(self, path, file_name):
        audiofile = self.__get_audiofile(path, file_name)
        tag = audiofile.tag

        if tag is None:
            logging.error("get_tag", "tag is none: " + file_name)
            return None
        return tag

    def __reset_tag_data(self):
        self.tag.title = None
        self.tag.track_num = None
        self.tag.artist = None
        self.tag.album_artist = None
        self.tag.album = None
        self.save_tag()

    def reset_tag(self):
        # get working tag
        #self.tag = self.__get_tag(u"/media/christian/Daten/Making/Python/music_file_suite", u"Benny Benassi - Cinema (Skrillex Remix).mp3")
        self.tag = self.__get_tag(u"D:\Making\Python\music_file_suite", u"Benny Benassi - Cinema (Skrillex Remix).mp3")

        self.__reset_tag_data()

        self.tag.file_info = eyed3.id3.FileInfo(encoding.f_decode(self.file_path))
        self.save_tag()


    def save_tag(self):
        try:
            self.tag.save()
        except IOError as e:
            logging.error("FAIL: Save Tag (file disabled wr rights)", "save_tag " + self.file_path, e)
        except NotImplementedError as e:
            logging.error("Implement", self.file_path, e)
        except Warning as e:
            logging.error("reset_tag corrupted file", self.file_path, e)

    # GETTER
    def get_tag_title(self):
        if self.tag is not None:
            return encoding.f_encode(self.tag.title)
        return None

    def get_tag_track_num(self):
        if self.tag is not None:
            return self.tag.track_num[0]

    def get_artist(self):

        if self.tag is not None:
            return encoding.f_encode(self.tag.artist)
        return None

    def get_album_artist(self):

        if self.tag is not None:
            return encoding.f_encode(self.tag.album_artist)
        return None

    def get_album(self):

        if self.tag is not None:
            return encoding.f_encode(self.tag.album)
        return None

    # SETTER
    def set_tag_title(self, title):

        self.tag.title = encoding.f_decode(title)
        self.save_tag()

    def set_tag_track_num(self, track_num):

        self.tag.track_num = (track_num, None)
        self.save_tag()

    def set_tag_artist(self, artist):

        self.tag.artist = encoding.f_decode(artist)
        self.save_tag()

    def set_tag_album_artist(self, album_artist):

        self.tag.album_artist = encoding.f_decode(album_artist)
        self.save_tag()

    def set_tag_album(self, album):

        self.tag.album = encoding.f_decode(album)
        self.save_tag()
