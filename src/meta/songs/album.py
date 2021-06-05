from logging import info
from os.path import isdir, split
from threading import BoundedSemaphore

from src.abstract.abstract_list_model import AbstractListModel
from src.meta.songs.song import Song
from src.resource.meta_tags import MetaTags
from src.resource.texts import SelectionAlbum, SelectionMeta


class Album(AbstractListModel):
    def __init__(self, controller):
        AbstractListModel.__init__(self, controller)
        self._album_sem = BoundedSemaphore(value=1)

        self.album_path = None
        # Meta
        self.use_meta = False  # Has to match initial selection in view
        self.is_album = False

        self._Songs = {}
        self._failed_Songs = None
        self.meta_data = None
        # Threading
        self._active = True

    def _read_album_path(self, album_path):
        album_path = split(album_path)[-1]
        # gather data from path
        if ' - ' in album_path:
            artist, album = album_path.split(' - ')
            self.meta_data[MetaTags.Artist] = artist
            self.meta_data[MetaTags.AlbumArtist] = artist  # Album path
            self.meta_data[MetaTags.Album] = album  # Album path

    def set_files(self, album_path, files):
        self._active = False  # join everything / wait

        with self._album_sem:
            self._active = True
            if not isdir(album_path):
                info('Not a valid path')
                return

            self.album_path = album_path
            self.meta_data = {}
            self._Songs = []

            self._read_album_path(self.album_path)

            for file in files:
                self._Songs.append(Song(album_path, file, self))

                if not self._active:  # interupt by another process
                    return

            info("ANALISE: DONE")
            for song in self._Songs:
                self.add_line([song[tag] for tag in MetaTags])

    def __getitem__(self, item) -> str:
        """
        Return meta data about the album
        :param item: Meta data tag
        """
        if item in self.meta_data:
            return self.meta_data[item]
        else:
            return ''

    def set_data(self):

        for i, song in enumerate(self._Songs):
            if song.set_data():
                self.set_color_ok(i)
            else:
                self._controller.set_color_warning(i)
        info('Set meta and rename complete')

    def set_is_album(self, is_album):
        with self._album_sem:

            is_album = SelectionAlbum(is_album)
            if is_album == SelectionAlbum.ALBUM:
                self.is_album = True
                for song in self._Songs:
                    song.set_album_strategy()
            elif is_album == SelectionAlbum.RANDOM:
                self.is_album = False
                for song in self._Songs:
                    song.set_common_strategy()
            else:
                raise ValueError
            self.update_view()

    def set_is_meta(self, use_meta):
        with self._album_sem:

            use_meta = SelectionMeta(use_meta)
            if use_meta == SelectionMeta.NO_META:
                self.use_meta = False
                for song in self._Songs:
                    song.set_ignore_meta()
            elif use_meta == SelectionMeta.META:
                self.use_meta = True
                for song in self._Songs:
                    song.set_use_meta()
            else:
                raise ValueError
            self.update_view()

    def edit_song(self, row, column, data):
        with self._album_sem:
            self._Songs[row].edit(column, data)
            self.update_song_view(row)

    # +++ View +++

    def update_view(self) -> None:
        """
        Update list view of all songs
        """
        for i, song in enumerate(self._Songs):
            self.update_song_view(i)

    def set_error_color(self, i):
        if self._Songs[i].get_error():
            self._controller.set_color_warning(i)
        else:
            self._controller.set_color_normal(i)

    def update_song_view(self, row):

        result = [self._Songs[row][tag] for tag in MetaTags]
        self.update_row(result, row)
        self.set_error_color(row)

    def make_playlist(self):
        raise NotImplementedError
        # TODO playlist
