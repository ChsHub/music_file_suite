import copy
from threading import Thread, BoundedSemaphore
import logging
import lib.utility.utilities as utilities
from Song_thread import SongThread


class Album(Thread):
    _album_dir = None
    _set_view = None
    # Threading
    _semaphore = None
    _sem_songs = None
    _active = True
    _threads = []
    _thread_count = 100
    # Meta
    _album = None
    _artist = None
    _album_artist = None
    _Songs = []
    _failed_Songs = None

    def __init__(self, album_dir, set_view):
        Thread.__init__(self)
        # gather data from path

        self._semaphore = BoundedSemaphore(value=1)
        self._sem_songs = BoundedSemaphore(value=1)
        if not album_dir:
            raise ValueError
        self._album_dir = album_dir
        self._set_view = set_view
        self.start()

    def run(self):

        artist, album = utilities.get_artist_and_album(self._album_dir)
        self._read_album_path(artist, album)

        files = utilities.get_mp3_files(self._album_dir)

        print("ANALYZE: START")
        for i in range(self._thread_count):
            new_t = SongThread(self._album_dir, self._is_active, i, self._thread_count, files, self.add_song)
            self._threads += [new_t]
        self.join_song_threads()

        logging.info("ANALIZE: DONE")
        if self._is_active():
            data = self.get_data()
            # TODO find none
            #data = sorted(data)
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
        print("COMPLETE")

    ## THREADING

    def set_inactive(self):

        self._semaphore.acquire()
        self._active = False
        self._semaphore.release()

    def set_active(self):

        self._semaphore.acquire()
        self._active = True
        self._semaphore.release()

    def _is_active(self):

        self._semaphore.acquire()
        result = copy.copy(self._active)
        self._semaphore.release()
        return result

    def join_song_threads(self):
        for s_thread in self._threads:
            s_thread.join()

    def add_song(self, song):
        self._sem_songs.acquire()
        self._Songs += [song]
        self._sem_songs.release()


        # self._failed_Songs = self._Songs[:]
        # map(lambda: not Song.get_error, self._Songs)
        # map(Song.get_error, self._Songs)

        # print("FAILED: " + str(len(self._failed_Songs)))
