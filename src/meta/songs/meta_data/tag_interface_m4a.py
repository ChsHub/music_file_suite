# -*- coding: utf-8 -*-

from logging import info, error, exception
from os.path import join

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen._file import File
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TPE2
from tag_interface import Tag


# mutagen-1.37
# TODO test if set is successful


class Tag(Tag):
    _tag = None
    file_path = None

    def __init__(self, path, file_name):

        self.file_path = join(path, file_name)

        if self.file_path is None:
            raise NameError

        try:
            self._tag = File(self.file_path)
        except Exception as e:
            exception("get audio_file " + self.file_path)

        if self._tag is None:
            exception("get_audiofile audio_file is none: " + self.file_path)

        print(type(self._tag))

    def save_tag(self):
        try:
            self._tag.save()
        except IOError as e:
            error("FAIL: Save Tag (file disabled wr rights)", "save_tag " + self.file_path, e)
        except NotImplementedError as e:
            error("Implement", self.file_path, e)
        except Warning as e:
            error("reset_tag corrupted file", self.file_path, e)
        except Exception as e:
            error(str(e))

    # GETTER
    def get_attribute(self, attribute_str):

        if self._tag is not None:
            if attribute_str in self._tag:
                attribute = self._tag[attribute_str]
                if attribute:
                    return attribute[0]
        return None

    def get_tag_title(self):
        return self.get_attribute('title')

    def get_tag_track_num(self):
        return self.get_attribute('track_num')

    def get_artist(self):
        return self.get_attribute('artist')

    def get_album_artist(self):
        return self.get_attribute('albumartist')

    def get_album(self):
        return self.get_attribute('album')

    # SETTER
    def set_tag_title(self, title):
        self._tag['\xa9nam'] = title

    def set_tag_track_num(self, track_num):
        if track_num:
            self._tag["trkn"] = track_num

    def set_tag_artist(self, artist):
        self._tag['\xa9ART'] = artist

    def set_tag_album_artist(self, album_artist):
        self._tag["aART"] = album_artist

    def set_tag_album(self, album):
        self._tag["\xa9alb"] = album

    def reset(self):
        if self._tag:
            self._tag.clear()
            return True
        else:
            error("COULD NOT RESET TAG " + self.file_path)
            return False
