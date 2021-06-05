# -*- coding: utf8 -*-
from logging import error
from os.path import splitext

from src.meta.songs.meta_data.file_data import File_data
from src.meta.songs.meta_data.tag_data import Tag_data
from src.resource.meta_tags import MetaTags


class AbstractStrategy:
    def __init__(self, song, use_meta):
        self._getter = {}
        self._song = song
        self._getter[MetaTags.FileName] = self.get_file_name

        if use_meta:
            self.set_meta_use_strategy()
        else:
            self.set_meta_ignore_strategy()

    def get_file_name(self):
        raise NotImplementedError

    def set_meta_ignore_strategy(self):
        raise NotImplementedError

    def set_meta_use_strategy(self):
        raise NotImplementedError

    def __getitem__(self, item):
        return self._getter[item]()

    def __contains__(self, item):
        return item in self._getter


class Song:
    def __init__(self, album_path, file_name, album):

        self.file_name, self._file_type = splitext(file_name)
        self._error = False
        self._Album = album

        # READ
        self._tag_data = Tag_data(album_path, file_name)  # Meta
        self._file_data = File_data(self.file_name)
        # self.read_playlist(nr_in_playlist)  # Playlist
        if self._Album.is_album:
            self._data_strategy = self.AlbumStrategy(self, self._Album.use_meta)
        else:
            self._data_strategy = self.CommonStrategy(self, self._Album.use_meta)

    # GETTER #

    def __getitem__(self, item):
        """
        Return meta data about the song
        :param item: Meta data tag
        """
        return self._data_strategy[item]

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

    def set_album_strategy(self):
        self._data_strategy = self.AlbumStrategy(self, self._Album.use_meta)

    def set_common_strategy(self):
        self._data_strategy = self.CommonStrategy(self, self._Album.use_meta)

    def set_ignore_meta(self):
        self._data_strategy.set_meta_ignore_strategy()

    def set_use_meta(self):
        self._data_strategy.set_meta_use_strategy()

    # STRATEGIES
    # TODO make getter normally usable without calling

    class AlbumStrategy(AbstractStrategy):
        def __init__(self, song, use_meta):
            AbstractStrategy.__init__(self, song, use_meta)
            self._getter[MetaTags.Album] = lambda: song._Album[MetaTags.Album]
            self._getter[MetaTags.AlbumArtist] = lambda: song._Album[MetaTags.AlbumArtist]
            self._getter[MetaTags.Artist] = lambda: song._Album[MetaTags.Artist]

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

        def set_meta_use_strategy(self):
            self._getter[MetaTags.Title] = lambda: self._song._tag_data.title
            self._getter[MetaTags.TrackNum] = lambda: self._song._tag_data._track_num

    class CommonStrategy(AbstractStrategy):
        def __init__(self, song, use_meta):
            AbstractStrategy.__init__(self, song, use_meta)

            self._getter[MetaTags.TrackNum] = lambda: ""
            self._getter[MetaTags.Album] = lambda: ""
            self._getter[MetaTags.AlbumArtist] = lambda: ""

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
