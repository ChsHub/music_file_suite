from logging import info

from meta_tags import FileTypes
from meta_tags import MetaTags
from utility.os_interface import get_dir_list
from song import Song
from texts import SelectionAlbum, SelectionMeta
from utility.utilities import get_artist_and_album


class Album:
    album_path = None
    # Meta
    _Songs = {}
    _failed_Songs = None
    # Threading
    active = True
    meta_data = None

    def __init__(self, album_path, set_view):

        if not album_path:
            raise ValueError

        self.meta_data = {}
        self._Songs = set()
        self.album_path = album_path
        self._set_view = set_view

        # gather data from path
        artist, album = get_artist_and_album(self.album_path)
        self.meta_data[MetaTags.Artist] = artist
        self.meta_data[MetaTags.AlbumArtist] = artist  # Album path
        self.meta_data[MetaTags.Album] = album  # Album path
        info("ANALYZE: START")

        for file in get_dir_list(self.album_path):
            self._Songs.add(Song(album_path, file, self))

            if not self.active:  # interupt by another process
                return

        info("ANALISE: DONE")
        self.set_all_view()

    def __getitem__(self, item):
        return self.meta_data[item]

    def set_all_view(self):
        self._set_view([[song[tag] for tag in MetaTags] for song in self._Songs], FileTypes.MP3)

    def set_data(self):

        for song in self._Songs:
            song.set_data()

        self._set_view([[song[tag] for tag in MetaTags] for song in self._Songs], FileTypes.MP3)
        info("COMPLETE")

    def set_is_album(self, is_album):

        if is_album == SelectionAlbum.ALBUM:
            for song in self._Songs:
                song.set_album_strategy()
        elif is_album == SelectionAlbum.RANDOM:
            for song in self._Songs:
                song.set_common_strategy()
        elif is_album == SelectionAlbum.DETECTED:
            for song in self._Songs:
                song.set_detected_strategy()

        self.set_all_view()

    def set_is_meta(self, is_meta):

        if is_meta == SelectionMeta.NO_META:
            for song in self._Songs:
                song.set_ignore_meta()
        elif is_meta == SelectionMeta.META:
            for song in self._Songs:
                song.set_no_ignore_meta()

        self.set_all_view()

    # Threading
    def set_inactive(self):
        self.active = False
