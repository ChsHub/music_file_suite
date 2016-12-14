import logging
from threading import Thread

from song import Song


class SongThread(Thread):
    _album_path = None
    _files = None
    _id = None
    _padding = None
    _add_song = None

    def __init__(self, album_path, is_active, id, padding, files, add_song):
        Thread.__init__(self)
        self._is_active = is_active
        self._album_path = album_path
        self._files = files
        self._id = id
        self._padding = padding

        self._add_song = add_song
        self.start()

    def run(self):

        for i in range(self._id, len(self._files), self._padding):
            new_s = Song(self._album_path, self._files[i])
            if not new_s.get_error():
                self._add_song(new_s)

            if not self._is_active():
                logging.info("TERMINATE SONG THREAD")
                return
