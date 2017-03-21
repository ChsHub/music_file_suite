from threading import BoundedSemaphore
from album import Album
from converter import Converter
from downloader import Downloader
from os_interface import exists


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

        self._album_sem.acquire()
        self._Album = Album(album_dir, self._set_view)
        self._album_sem.release()

    def set_data(self):
        self._Album.set_data()

    def _set_view(self, data):
        self._Controller.set_view(data)

    def update_view(self, is_album):

        data = None
        self._album_sem.acquire()
        if self._Album:
            self._Album.set_is_album(is_album)
            data = self._Album.get_data()
        self._album_sem.release()

        if data:
            self._Controller.set_view(data)

    def download_file(self, url):
        self._Downloader.add_element(url)

    def convert_file(self, url):
        self._Converter.add_element(url)
