# -*- coding: utf8 -*-
from logging import info, error
from os.path import splitext

from src.model.songs.meta_data.file_data import File_data
from src.model.songs.meta_data.tag_data import Tag_data
from src.resource.meta_tags import MetaTags


class Song:
    file_name = None
    _tag_data = None
    _file_data = None
    _ignore_meta = True
    _data_strategy = None
    _Album = None
    _error = False

    def __init__(self, album_path, file_name, album):

        self.file_name, self._file_type = splitext(file_name)
        self._error = False
        self._Album = album

        # READ
        self._tag_data = Tag_data(album_path, file_name)  # Meta
        self._file_data = File_data(self.file_name)
        # self.read_playlist(nr_in_playlist)  # Playlist
        self.set_detected_strategy()

    # GETTER #

    def __getitem__(self, item):
        result = self._data_strategy[item]
        info(result)
        return result

    def get_error(self):
        return self._error

    # SETTER #

    def __setitem__(self, key, value):
        if key == MetaTags.FileName:
            self._file_data = File_data(value)

    def set_data(self):
        if self._error:
            error("INVALID NAME: SONG: " + self[MetaTags.FileName])
            return False
        else:
            if not self._tag_data.set_new_tag(self):
                error('Apply Tag Error')
                raise ValueError
            # no else
            self._file_data.rename_file(album_path=self._Album.album_path,
                                        file_name=self.file_name + self._file_type,
                                        new_name=self[MetaTags.FileName] + self._file_type)
            return True

    def edit(self, column, data):
        tag = list(MetaTags)[column]
        self[tag] = data

    # +++Strategy setter+++

    def set_detected_strategy(self):
        if self._file_data.get_is_album():
            self.set_album_strategy()
        else:
            self.set_common_strategy()

    def set_album_strategy(self):
        self._data_strategy = self.AlbumStrategy(self)

    def set_common_strategy(self):
        self._data_strategy = self.CommonStrategy(self)

    def set_ignore_meta(self):
        self._data_strategy.set_meta_ignore_strategy()

    def set_use_meta(self):
        self._data_strategy.set_meta_use_strategy()

    # STRATEGIES
    # TODO make getter normally usable without calling
    class AlbumStrategy:
        _getter = None

        def __init__(self, song):
            self._getter = {}
            self._song = song
            self._getter[MetaTags.Album] = lambda: song._Album[MetaTags.Album]
            self._getter[MetaTags.AlbumArtist] = lambda: song._Album[MetaTags.AlbumArtist]
            self._getter[MetaTags.Artist] = lambda: song._Album[MetaTags.Artist]

            self.set_meta_ignore_strategy()
            # track_nr = utilities.track_nr_int_to_str(track_num)
            self._getter[MetaTags.FileName] = self.get_file_name

        def get_file_name(self):
            title = self._getter[MetaTags.Title]()
            track_num = self._getter[MetaTags.TrackNum]()
            if title and track_num:
                self._song._error = False  # TODO refactor error management
                return track_num + ' ' + title
            else:
                self._song._error = True
                return self._song.file_name

        def set_meta_ignore_strategy(self):
            self._getter[MetaTags.Title] = lambda: self._song._file_data._title
            self._getter[MetaTags.TrackNum] = lambda: self._song._file_data._track_num

        def set_meta_no_ignore_strategy(self):
            self._getter[MetaTags.Title] = lambda: self._song._tag_data.title
            self._getter[MetaTags.TrackNum] = lambda: self._song._tag_data._track_num

        def __getitem__(self, item):
            return self._getter[item]()

    class CommonStrategy:
        _getter = None

        def __init__(self, song):
            self._getter = {}
            self._song = song

            self._getter[MetaTags.TrackNum] = lambda: ""
            self._getter[MetaTags.Album] = lambda: ""
            self._getter[MetaTags.AlbumArtist] = lambda: ""

            self.set_meta_ignore_strategy()
            self._getter[MetaTags.FileName] = self.get_file_name

        def get_file_name(self):
            artist = self._getter[MetaTags.Artist]()
            title = self._getter[MetaTags.Title]()

            if artist and title:
                self._song._error = False
                return artist + ' - ' + title
            else:
                self._song._error = True
                return self._song.file_name

        def set_meta_ignore_strategy(self):
            self._getter[MetaTags.Title] = lambda: self._song._file_data._title
            self._getter[MetaTags.Artist] = lambda: self._song._file_data._artist

        def set_meta_use_strategy(self):
            self._getter[MetaTags.Title] = lambda: self._song._tag_data.title
            self._getter[MetaTags.Artist] = lambda: self._song._tag_data._artist

        def __getitem__(self, item):
            return self._getter[item]()
