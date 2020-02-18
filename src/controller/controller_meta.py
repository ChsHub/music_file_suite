from src.controller.generic_controller import GenericController
from src.model.songs.album import Album


class ControllerMeta(GenericController):
    def __init__(self, view, config):
        GenericController.__init__(self, view)
        self._album = Album(self)

    # Notify model

    def analyze_files(self, path, files):
        if self._album:
            self._submit(self._album.set_files, path, files)

    def set_data(self):
        if self._album:
            self._submit(self._album.set_data)

    def set_is_meta(self, is_meta):
        if self._album:
            self._submit(self._album.set_is_meta, is_meta)

    def set_is_album(self, is_album):
        if self._album:
            self._submit(self._album.set_is_album, is_album)

    def make_playlist(self):
        if self._album:
            self._submit(self._album.make_playlist)

    def edit_song(self, row, column, data):
        if self._album:
            self._submit(self._album.edit_song, row, column, data)
