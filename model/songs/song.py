# -*- coding: utf8 -*-
__author__ = 'Christian'
import logging

from file_data import File_data
from tag_data import Tag_data


class Song:
    _file_name = None

    _tag_data = None
    _file_data = None
    _ignore_meta = True

    def __init__(self, album_path, file_name):

        self._file_name = file_name
        self._error = False

        # READ
        self._tag_data = Tag_data(album_path, self._file_name)  # Meta
        self._file_data = File_data(self._file_name)
        # self.read_playlist(nr_in_playlist)  # Playlist

    #### GETTER ####


    def get_data(self, artist, album_artist, album):
        # Album
        if self._file_data.get_is_album():

            if self._ignore_meta:
                title = self._file_data._title
                track_num = self._file_data._track_num
            else:
                title = self._tag_data.title
                track_num = self._tag_data._track_num

            file_name = self.get_file_album_name(title, track_num)
        # No Album
        else:
            track_num = ""
            album = ""
            album_artist = ""

            if self._ignore_meta:
                title = self._file_data._title
                artist = self._file_data._artist
            else:
                title = self._tag_data.title
                artist = self._tag_data._artist

            file_name = self.get_file_normal_name(title, artist)

        return [file_name, album, album_artist, title, track_num, artist]

    def get_error(self):
        return self._error

    def get_file_normal_name(self, title, artist):
        if not artist or not title:
            logging.error("artist is missing: get_file_normal_name")
            return None

        return artist + ' - ' + title

    def get_file_album_name(self, title, track_num):
        # track_nr = utilities.track_nr_int_to_str(track_num)
        return track_num + u' ' + title

    # SET DATA

    def set_data(self, album_path, artist, album_artist, album):

        data = self.get_data(artist, album_artist, album)
        if self._error:
            return
        self._tag_data._set_new_tag(data)
        self._file_data._rename_file(album_path, data[0], self._file_name)
