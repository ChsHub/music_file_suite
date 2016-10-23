# -*- coding: utf8 -*-
__author__ = 'Christian'
import logging
import re

import lib.utility.tag_interface as eyed3_interface
import lib.utility.os_interface as os_interface
from lib.utility import encoding
from lib.utility import utilities


class Song:
    # meta data
    _album = None
    _album_artist = None
    _title = None
    _title_file_name = None
    _track_num = None
    _track_num_file_name = None
    _artist = None
    # file property
    _file_name = None
    _audio_tag = None
    _error = None
    # desicions
    _is_album = None

    def _clean_title(self):
        # TODO Regex
        self._title = self._title.replace(":", "").replace("*", "").replace("/", " ").replace('"', "").replace('#', "")
        self._title = self._title.replace("[", "(").replace("]", ")").replace(encoding.f_encode(u"é"), "e")

    def __init__(self, album_path, file_name):  # , ign_meta, name_album, is_album, read_path):

        self._album = {}
        self._album_artist = {}
        self._title = {}
        self._title_file_name = None
        self._track_num = {}
        self._track_num_file_name = None
        self._artist = {}
        self._error = False
        self._audio_tag = eyed3_interface.Tag(album_path, file_name)
        self._file_name = file_name

        # READ
        self.read_tag_data()  # Meta
        # self.read_playlist(nr_in_playlist)  # Playlist
        # TODO remove is_file_name normal -> just read file name
        if not self._read_song_title():  # Artist - Song.mp3
            if not self._read_song_title_album():  # 00 Song.mp3
                print "ERROR Handling needed"
                logging.error("FAIL: " + self._file_name)
                self._error = True

        print("END")
        # ERROR CHECK

    # TODO remove
    def __new__(self):
        return self

    def get_file_normal_name(self, title, artist):
        if not artist or not title:
            logging.error("artist is missing: get_file_normal_name")
            return None

        return artist + ' - ' + title

    def get_file_album_name(self, title, track_num):

        track_nr = utilities.track_nr_int_to_str(track_num)
        return track_nr + ' ' + str(title)

    def read_tag_data(self):

        album = self._audio_tag.get_album()
        if album:
            self._album["Meta"] = [album]

        album_artist = self._audio_tag.get_album_artist()
        if album_artist:
            self._album_artist["Meta"] = [album_artist]

        title = self._audio_tag.get_tag_title()
        if title:
            self._title["Meta"] = [title]

        track_num = self._audio_tag.get_tag_track_num()
        if track_num:
            self._track_num["Meta"] = [track_num]

        artist = self._audio_tag.get_artist()
        if artist:
            self._artist["Meta"] = [artist]

    # 00 Song.mp3
    def _read_song_title_album(self):

        match = re.findall(r"(\d+)\s(\w+)", self._file_name)
        if len(match) == 3 and match[0] == None:
            self._track_num_file_name = match[1]
            self._title_file_name = match[2][:-4]
            return True
        return False

    def _read_song_title(self):
        #        if not self._artist:
        title = self._file_name.split(" - ")
        if len(title) is 2:
            self._artist["File Name"] = title[0]
            self._title_file_name = title[1][:-4]
            return True

        return False

    def read_playlist(self, nr_in_playlist):

        if nr_in_playlist:
            self._track_num["Playlist"] = [nr_in_playlist]

    #### GETTER ####

    def get_album_names(self):
        return self._album

    #### Apply changes ####

    def _rename_file(self, album_path, new_name):

        os_interface.rename_file(album_path, self._file_name, new_name + '.mp3')

        self._file_name = new_name
        return 0

    def _set_new_tag(self, data):

        #self._audio_tag.reset_tag() TODO REmove
        self._audio_tag.set_tag_title(data[3])
        self._audio_tag.set_tag_artist(data[5])

    def _set_new_tag_album(self, data):

        self._set_new_tag(data)

        self._audio_tag.set_tag_track_num(data[4])
        self._audio_tag.set_tag_album_artist(data[2])
        self._audio_tag.set_tag_album(data[1])

    def set_data_album(self, album_path, artist, album_artist, album):

        if self._error:
            logging.error("FAIL: " + self._file_name)
            return
        data = self.get_data_album(artist, album_artist, album)
        self._set_new_tag_album(data)
        self._rename_file(album_path, data[0])

    def set_data(self, album_path):

        if self._error:
            logging.error("FAIL: " + self._file_name)
            return
        # self._clean_title()
        data = self.get_data()
        self._set_new_tag(data)
        self._rename_file(album_path, data[0])

    #### GETTER ####

    def get_data_album(self, artist, album_artist, album):

        ignore_meta = True

        if ignore_meta:
            track_num = self._track_num_file_name
            title = self._title_file_name

            if "File Name" in self._artist:
                artist = self._artist["File Name"]
                # no else
        else:
            raise NotImplementedError

        return [self.get_file_album_name(title, track_num),
                album,
                album_artist,
                title,
                track_num,
                artist]

    def get_data(self):
        ignore_meta = True

        if ignore_meta:
            track_num = None

            title = self._title_file_name

            if "File Name" in self._artist:
                artist = self._artist["File Name"]
            else:
                return [self._file_name, "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"]

            album = None
            album_artist = None

        else:
            raise NotImplementedError

        return [self.get_file_normal_name(title, artist),
                album,
                album_artist,
                title,
                track_num,
                artist]
