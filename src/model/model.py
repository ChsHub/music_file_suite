from threading import BoundedSemaphore

from src.model.songs.album import Album


class Model:
    _Controller = None
    _Album = None
    _album_sem = None

    def __init__(self, controller):
        self._Controller = controller
        self._album_sem = BoundedSemaphore(value=1)

    # TODO refactor
    def analyze_files(self, path, files):
        if self._Album:
            self._Album.set_inactive()

        with self._album_sem:
            self._Album = Album(path, self._Controller.set_view)

    def set_data(self):
        self._Album.set_data()

    def set_is_album(self, is_album):
        with self._album_sem:
            if self._Album:
                self._Album.set_is_album(is_album)

    def set_is_meta(self, is_meta):
        with self._album_sem:
            if self._Album:
                self._Album.set_is_meta(is_meta)

    def make_playlist(self):
        pass  # TODO

    def set_download_progress(self, percent):
        self._Controller.set_download_progress(percent)
