from utilities import get_files, get_artist_and_album
from logging import info
from meta_data import MetaData
from song import Song
from texts import Selection

class Album:
    album_path = None
    # Meta
    _Songs = []
    _failed_Songs = None
    # Threading
    active = True
    meta_data = None

    def __init__(self, album_path, set_view):

        if not album_path:
            raise ValueError

        self.meta_data = {}
        self.album_path = album_path

        # gather data from path
        artist, album = get_artist_and_album(self.album_path)
        self.meta_data[MetaData.Artist] = artist
        self.meta_data[MetaData.AlbumArtist]  = artist  # Album path
        self.meta_data[MetaData.Album]  = album  # Album path

        info("ANALYZE: START")
        for file in get_files(self.album_path, [".mp3", ".mp4", ".webm", ".flv"]):
            self.add_song(album_path, file)
            if not self.active: # interupt by another process
                return

        info("ANALIZE: DONE")
        set_view(self.get_data())

    # DATA #

    def __getitem__(self, item):
        return self.meta_data[item]

    def get_data(self):
        return [[song[x] for x in MetaData] for song in self._Songs]

    def set_data(self):
        for song in self._Songs:
            song.set_data(self, self.album_path)
        info("COMPLETE")

    def add_song(self, album_path, file):
        new_song = Song(album_path, file, self)
        if not new_song.get_error():
            self._Songs += [new_song]

    # Threading
    def set_inactive(self):
        self.active = False

    def set_is_album(self, is_album):

        if is_album == Selection.ALBUM:
            for song in self._Songs:
                song.set_album_strategy()
        elif is_album == Selection.RANDOM:
            for song in self._Songs:
                song.set_common_strategy()
        elif is_album == Selection.DETECTED:
            for song in self._Songs:
                song.set_detected_strategy()
