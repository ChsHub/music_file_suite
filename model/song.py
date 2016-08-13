# -*- coding: utf8 -*-
__author__ = 'Christian'
import logging
import lib.utility.os_interface as os_interface
from lib.utility import encoding

import lib.utility.eyed3_interface as eyed3_interface
from lib.utility import utilities
import re


class Song:
    # meta data
    _album = []
    _album_artist = []
    _title = []
    _track_num = []
    _artist = []
    # file property
    _file_name = None
    _album_path = None
    _audio_tag = None
    _error = None

    def _clean_title(self):
        # TODO Regex
        self._title = self._title.replace(":", "").replace("*", "").replace("/", " ").replace('"', "").replace('#', "")
        self._title = self._title.replace("[", "(").replace("]", ")").replace(encoding.f_encode(u"é"), "e")

    # overwrite old tags for one song
    def __init__(self, file_name,
                 album_path, nr_in_playlist, artist, album):  # , ign_meta, name_album, is_album, read_path):

        self._album = []
        self._album_artist = []
        self._title = []
        self._track_num = []
        self._artist = []
        self._error = False

        self._file_name = file_name
        self._album_path = album_path
        self._audio_tag = eyed3_interface.Tag(album_path, file_name)

        # READ
        self.read_tag_data()  # Meta
        self.read_playlist(nr_in_playlist)  # Playlist
        # TODO remove is_file_name normal -> just read file name

        if utilities.is_file_name_normal(file_name):
            self._read_song_title()  # Artist - Song.mp3
        elif not self._read_song_title_album():  # 00 Song.mp3

            print "ERROR Handling needed"
            logging.error("FAIL: " + self._file_name)
            self._error = True
        # TODO take in
        self.read_album_path(artist, album)

        # ERROR CHECK
        if len(self._album) != 2:
            raise IndexError

        if len(self._album_artist) != 2:
            raise IndexError

        if len(self._title) != 1:
            print self._title
            raise IndexError

        if len(self._track_num) != 2:
            raise IndexError

        if len(self._artist) != 2:
            print self._artist
            raise IndexError
        print "DONE: " + self._file_name

    def _select_data(self, indices):
        self._album = self._album[indices[0]]
        self._album_artist = self._album_artist[indices[1]]
        self._title = self._title[indices[2]]
        self._track_num = self._track_num[indices[3]]
        self._artist = self._artist[indices[4]]

    def write_date(self, is_album, indices):

        if self._error:
            # TODO move to error repo
            return
        # WRITE
        self._select_data(indices)

        self._clean_title()
        self._rename_file(is_album)
        self._audio_tag = eyed3_interface.Tag(self._album_path, self._file_name)

        self._set_new_tag(is_album)  # delete old tags

    # TODO remove
    def __new__(self):
        return self

    def _set_new_tag(self, is_album):

        self._audio_tag.reset_tag()

        self._audio_tag.set_tag_title(self._title)

        self._audio_tag.set_tag_artist(self._artist)

        if is_album:
            self._audio_tag.set_tag_track_num(self._track_num)
            self._audio_tag.set_tag_album_artist(self._album_artist)
            self._audio_tag.set_tag_album(self._album)

    def get_file_normal_name(self):
        if self._artist is None:
            logging.error("artist is missing", "get_file_normal_name: " + self._file_name)
            return None
        return self._artist + ' - '

    def get_file_album_name(self):

        if self._track_num is None:
            logging.error("track num missing", self._file_name)
            return
        track_nr = utilities.track_nr_int_to_str(self._track_num)
        return track_nr + ' '

    def _rename_file(self, name_album):

        new_name = ''
        if name_album:
            new_name = self.get_file_album_name()
        else:
            new_name = self.get_file_normal_name()

        self.set_file_name(new_name)

    def set_file_name(self, new_name):

        if new_name is None:
            logging.error("set_file_name", "New name is none")
            return 0
        new_name = new_name + self._title + '.mp3'

        os_interface.rename_file(self._album_path, self._file_name, new_name)

        self._file_name = new_name
        return 0

    def read_tag_data(self):

        self._title += [self._audio_tag.get_tag_title()]
        self._track_num += [self._audio_tag.get_tag_track_num()]
        self._artist += [self._audio_tag.get_artist()]  # self.audio_tag.get_album_artist()
        self._album_artist += [self._audio_tag.get_album_artist()]
        self._album += [self._audio_tag.get_album()]

    # 00 Song.mp3
    def _read_song_title_album(self):

        match = re.findall(r"(\d+)\s(\w+)", self._file_name)
        if len(match) == 3 and match[0] == None:
            self._track_num += [match[1]]
            self._title += [match[2][:-4]]
            return True
        return False

    # Artist - Song.mp3
    def _get_song_artist_and_title(self, file_name):

        title = file_name.split(" - ")
        if len(title) is 2:
            self._artist += [title[0]]
            self._title += [title[1][:-4]]

    def _read_song_title(self):
        if not self._artist:
            self._get_song_artist_and_title(self._file_name)

    def read_album_path(self, artist, album):

        self._artist += [artist]  # 1. File Name 2. Album path
        self._album_artist += [artist]  # Album path
        self._album += [album]  # Album path

    def read_playlist(self, nr_in_playlist):
        self._track_num += [nr_in_playlist]

    #### GETTER ####

    def get_album_names(self):
        return self._album
