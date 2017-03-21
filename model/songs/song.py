# -*- coding: utf8 -*-
from logging import info, error
from file_data import File_data
from meta_data import MetaData
from tag_data import Tag_data


class Song:
    _file_name = None
    _file_type = None
    _tag_data = None
    _file_data = None
    _ignore_meta = True
    _data_strategy = None
    _Album = None

    def __init__(self, album_path, file_name, album):

        self._file_name = file_name
        self._file_type = file_name[-4:]
        self._error = False
        self._Album = album

        # READ
        self._tag_data = Tag_data(album_path, self._file_name)  # Meta
        self._file_data = File_data(self._file_name)
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

    def set_data(self):

        if self._error:
            error("INVALID NAME: SONG: "+self[MetaData.FileName])
            return
        self._tag_data._set_new_tag(self)
        self._file_data.rename_file(self._Album.album_path, self[MetaData.FileName], self._file_name)

    def set_detected_strategy(self):
        if self._file_data.get_is_album():
            self.set_album_strategy()
        else:
            self.set_common_strategy()

    def set_album_strategy(self):
        self._data_strategy = self.AlbumStrategy(self)

    def set_common_strategy(self):
        self._data_strategy = self.CommonStrategy(self)

    def set_ignore_meta(self, ignore):
        if ignore:
            self._data_strategy.set_meta_ignore_strategy()
        else:
            self._data_strategy.set_meta_no_ignore_strategy()

    # STRATEGIES

    class AlbumStrategy:
        _getter = None

        def __init__(self, song):
            self._getter = {}
            self._song = song
            self._getter[MetaData.Album] = lambda: song._Album[MetaData.Album]
            self._getter[MetaData.AlbumArtist] = lambda: song._Album[MetaData.AlbumArtist]
            self._getter[MetaData.Artist] = lambda: song._Album[MetaData.Artist]

            self.set_meta_ignore_strategy()
            # track_nr = utilities.track_nr_int_to_str(track_num)
            self._getter[MetaData.FileName] = self.get_title

        def get_title(self):
            title = self._getter[MetaData.Title]()
            track_num = self._getter[MetaData.TrackNum]()
            if not title:
                title = "NONE"
            if not track_num:
                track_num = "NONE"
            return track_num + u' ' + title

        def set_meta_ignore_strategy(self):
            self._getter[MetaData.Title] = lambda: self._song._file_data._title
            self._getter[MetaData.TrackNum] = lambda: self._song._file_data._track_num

        def set_meta_no_ignore_strategy(self):
            self._getter[MetaData.Title] = lambda: self._song._tag_data.title
            self._getter[MetaData.TrackNum] = lambda: self._song._tag_data._track_num

        def __getitem__(self, item):
            return self._getter[item]()

    class CommonStrategy:
        _getter = None

        def __init__(self, song):
            self._getter = {}
            self._song = song

            self._getter[MetaData.TrackNum] = lambda: ""
            self._getter[MetaData.Album] = lambda: ""
            self._getter[MetaData.AlbumArtist] = lambda: ""

            self.set_meta_ignore_strategy()
            self._getter[MetaData.FileName] = self.get_title

        def get_title(self):
            artist = self._getter[MetaData.Artist]()
            title = self._getter[MetaData.Title]()
            if not artist:
                artist = "NONE"
            if not title:
                title = "NONE"
            return artist + ' - ' + title

        def set_meta_ignore_strategy(self):
            self._getter[MetaData.Title] = lambda: self._song._file_data._title
            self._getter[MetaData.Artist] = lambda: self._song._file_data._artist

        def set_meta_no_ignore_strategy(self):
            self._getter[MetaData.Title] = lambda: self._song._tag_data.title
            self._getter[MetaData.Artist] = lambda: self._song._tag_data._artist

        def __getitem__(self, item):
            return self._getter[item]()
