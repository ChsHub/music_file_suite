from logging import info
from os_interface import exists
import lib.utility.utilities as utilities
from song import Song

class Album:
    _album_dir = None
    _set_view = None
    # Meta
    _album = None
    _artist = None
    _album_artist = None
    _Songs = []
    _failed_Songs = None
    # Threading
    active = True

    def __init__(self, album_dir, set_view):

        # gather data from path

        if not album_dir:
            raise ValueError

        self._album_dir = album_dir
        self._set_view = set_view

        artist, album = utilities.get_artist_and_album(self._album_dir)
        self._read_album_path(artist, album)

        files = utilities.get_mp3_files(self._album_dir)

        info("ANALYZE: START")
        for file in files:
            self.add_song(album_dir, file)
            if not self.active:
                return

        info("ANALIZE: DONE")

        data = self.get_data()
        # TODO find none
        # data = sorted(data)
        self._set_view(data)


    ## DATA ##

    def _read_album_path(self, artist, album):
        self._artist = artist
        self._album_artist = artist  # Album path
        self._album = album  # Album path


    def get_data(self):
        return [song.get_data(self._artist, self._album_artist, self._album) for song in self._Songs]


    def set_data(self):
        for song in self._Songs:
            song.set_data(self._album_dir, self._artist, self._album_artist, self._album)
        info("COMPLETE")


    def add_song(self, album_path, file):
        new_song = Song(album_path, file)
        if not new_song.get_error():
            self._Songs += [new_song]


        # self._failed_Songs = self._Songs[:]
        # map(lambda: not Song.get_error, self._Songs)
        # map(Song.get_error, self._Songs)

        # info("FAILED: " + str(len(self._failed_Songs)))

    # Threading
    def set_inactive(self):
        self.active = False