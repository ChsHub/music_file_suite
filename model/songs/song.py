# -*- coding: utf8 -*-
from logging import info, error
from file_data import File_data
from meta_tags import MetaTags
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
        self._file_type = file_name.split(".")[-1]
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
            error("INVALID NAME: SONG: " + self[MetaTags.FileName])
            return
        self._tag_data._set_new_tag(self)
        self._file_data.rename_file(self._Album.album_path, self[MetaTags.FileName], self._file_name)

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

    def set_no_ignore_meta(self):
        self._data_strategy.set_meta_no_ignore_strategy()

    # STRATEGIES

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
            self._getter[MetaTags.FileName] = self.get_title

        def get_title(self):
            title = self._getter[MetaTags.Title]()
            track_num = self._getter[MetaTags.TrackNum]()
            if not title:
                title = "NONE"
            if not track_num:
                track_num = "NONE"
            return track_num + u' ' + title

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
            self._getter[MetaTags.FileName] = self.get_title

        def get_title(self):
            artist = self._getter[MetaTags.Artist]()
            title = self._getter[MetaTags.Title]()
            if not artist:
                artist = "NONE"
            if not title:
                title = "NONE"
            return artist + ' - ' + title

        def set_meta_ignore_strategy(self):
            self._getter[MetaTags.Title] = lambda: self._song._file_data._title
            self._getter[MetaTags.Artist] = lambda: self._song._file_data._artist

        def set_meta_no_ignore_strategy(self):
            self._getter[MetaTags.Title] = lambda: self._song._tag_data.title
            self._getter[MetaTags.Artist] = lambda: self._song._tag_data._artist

        def __getitem__(self, item):
            return self._getter[item]()
