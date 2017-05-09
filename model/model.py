from logging import error, info
from threading import BoundedSemaphore

from album import Album
from converter import Converter
from downloader import Downloader
from utility.os_interface import exists


class Model:
    _Controller = None
    _Album = None
    _Downloader = None
    _Converter = None
    _album_sem = None

    def __init__(self, Controller):
        self._Controller = Controller
        self._Downloader = Downloader()
        self._Converter = Converter()
        self._album_sem = BoundedSemaphore(value=1)

    def analyze_files(self, album_dir):
        if not exists(album_dir):
            return
        if self._Album:
            self._Album.set_inactive()

        with self._album_sem:
            self._Album = Album(album_dir, self._Controller.set_view)

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

    def download_file(self, url):
        self._Downloader.add_element(url)

    def convert_file(self):
        with self._album_sem:
            if self._Album:
                self._Converter.add_element(element=self._Album.album_path)  # add songs
            else:
                info("NO PATH OPENED")
