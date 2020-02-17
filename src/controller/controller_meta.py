from src.controller.generic_controller import GenericController
from src.model.songs.album import Album


class ControllerMeta(GenericController):
    def __init__(self, view, config):
        GenericController.__init__(self)
        self._view = view
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
            self._submit(self._album.make_playlist) # TODO make playlist

    def edit_song(self, row, column, data):
        if self._album:
            self._submit(self._album.edit_song, row, column, data)

    # Notify view

    def set_view(self, data):
        if self._view:
            self._view.set_preview_data(data)
            
    def set_meta_color_normal(self, id):
        if self._view:
            self._view.set_meta_color_normal(id)

    def set_meta_color_warning(self, row):
        if self._view:
            self._view.set_meta_color_warning(row)

    def set_meta_color_ok(self, row):
        if self._view:
            self._view.set_meta_color_ok(row)