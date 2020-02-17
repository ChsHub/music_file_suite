from logging import info
from os.path import isdir, split
from threading import BoundedSemaphore

from src.model.songs.song import Song
from src.resource.meta_tags import MetaTags
from src.resource.texts import SelectionAlbum, SelectionMeta


class Album:
    def __init__(self, controller):
        self.album_path = None
        # Meta
        self._Songs = {}
        self._failed_Songs = None
        # Threading
        self._active = True
        self.meta_data = None

        self._Controller = controller
        self._album_sem = BoundedSemaphore(value=1)

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

            # gather data from path
            if ' - ' in self.album_path:
                artist, album = split(self.album_path)[-1].split(' - ')
                self.meta_data[MetaTags.Artist] = artist
                self.meta_data[MetaTags.AlbumArtist] = artist  # Album path
                self.meta_data[MetaTags.Album] = album  # Album path

            for file in files:
                self._Songs.append(Song(album_path, file, self))

                if not self._active:  # interupt by another process
                    return

            info("ANALISE: DONE")
            self.set_all_view()

    def __getitem__(self, item):
        return self.meta_data[item]

    def set_all_view(self):
        result = [[song[tag] for tag in MetaTags] for song in self._Songs]
        self._Controller.set_view(result)

        for i in range(len(self._Songs)):
            self.set_error_color(i)

    def set_error_color(self, i):
        if self._Songs[i].get_error():
            self._Controller.set_meta_color_warning(i)
        else:
            self._Controller.set_meta_color_normal(i)

    def set_data(self):

        for i, song in enumerate(self._Songs):
            if song.set_data():
                self._Controller.set_meta_color_ok(i)
            else:
                self._Controller.set_meta_color_warning(i)
        info('Set meta and rename complete')

    def set_is_album(self, is_album):
        with self._album_sem:

            is_album = SelectionAlbum(is_album)
            if is_album == SelectionAlbum.ALBUM:
                for song in self._Songs:
                    song.set_album_strategy()
            elif is_album == SelectionAlbum.RANDOM:
                for song in self._Songs:
                    song.set_common_strategy()
            else:
                raise ValueError
            self.set_all_view()

    def set_is_meta(self, use_meta):
        with self._album_sem:

            use_meta = SelectionMeta(use_meta)
            if use_meta == SelectionMeta.NO_META:
                for song in self._Songs:
                    song.set_ignore_meta()
            elif use_meta == SelectionMeta.META:
                for song in self._Songs:
                    song.set_use_meta()
            else:
                raise ValueError
            self.set_all_view()

    def edit_song(self, row, column, data):
        with self._album_sem:
            self._Songs[row].edit(column, data)
            self.update_song_view(row)

    def update_song_view(self, row):

        result = [self._Songs[row][tag] for tag in MetaTags]
        self._Controller.update_meta_line(row, result)
        self.set_error_color(row)

    def create_playlist(self):
        raise NotImplementedError
        # TODO playlist
