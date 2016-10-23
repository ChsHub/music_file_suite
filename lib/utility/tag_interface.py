__author__ = 'Christian'

import logging
import encoding
import path_str
# mutagen-1.34.1
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


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
        full_path_uni = encoding.f_decode(full_path_uni)

        audiofile = None
        try:
            audiofile = EasyID3(full_path_uni)

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

    def reset_tag(self):

        self._tag.delete()
        self._tag = MP3(encoding.f_decode(self.file_path), ID3=EasyID3)

    def save_tag(self):
        try:
            self._tag.save()
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
                    # if attribute_str == "tracknumber":
                    #   print "here"
                    return encoding.f_encode(attribute[0])
        return None

    def get_tag_title(self):
        return self.get_attribute("title")

    def get_tag_track_num(self):
        return self.get_attribute("tracknumber")

    def get_artist(self):
        return self.get_attribute("artist")

    def get_album_artist(self):
        return self.get_attribute("albumartist")

    def get_album(self):
        return self.get_attribute("album")

    # SETTER
    def set_tag_title(self, title):

        self._tag["title"] = encoding.f_decode(title)
        self.save_tag()

    def set_tag_track_num(self, track_num):

        if track_num:
            self._tag["tracknumber"] = encoding.f_decode(track_num)
            self.save_tag()

    def set_tag_artist(self, artist):

        self._tag["artist"] = encoding.f_decode(artist)
        self.save_tag()

    def set_tag_album_artist(self, album_artist):

        self._tag["albumartist"] = encoding.f_decode(album_artist)
        self.save_tag()

    def set_tag_album(self, album):

        self._tag["album"] = encoding.f_decode(album)
        self.save_tag()
