import lib.utility.utilities as utilities
from song import Song


class Album:
    _album_dir = None
    # Meta
    _album = None
    _artist = None
    _album_artist = None
    _Songs = None
    _failed_Songs = None

    def __init__(self, album_dir):

        # gather data from path
        if not album_dir:
            raise ValueError

        self._album_dir = album_dir

        artist, album = utilities.get_artist_and_album(album_dir)
        self._read_album_path(artist, album)

        files = utilities.get_mp3_files(album_dir)

        print("ANALYZE FILES")
        self._Songs = []
        self._failed_Songs = []

        for file in files:
            new_song = Song(album_dir, file)
            if new_song.get_error():
                self._failed_Songs += [new_song]
            else:
                self._Songs += [new_song]

        print("FAILED: "+str(len(self._failed_Songs)))

    def _read_album_path(self, artist, album):

        self._artist = artist
        self._album_artist = artist  # Album path
        self._album = album  # Album path


    def get_data(self):

        return [song.get_data(self._artist, self._album_artist, self._album) for song in self._Songs]

    def set_data(self, is_album):
        if is_album:
            [song.set_data_album(self._album_dir, self._artist, self._album_artist, self._album) for song in self._Songs]
        else:
            [song.set_data(self._album_dir) for song in self._Songs]

        print("COMPLETE")

    def change_files(self, is_album):
        for song in self._Songs:
            song.write_date(is_album)
        print("CHANGE FILES")
        print("RETURN FEEDBACK")