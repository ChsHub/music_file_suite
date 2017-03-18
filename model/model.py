from album import Album
from os_interface import exists
from threading import BoundedSemaphore
from downloader import Downloader
from converter import Converter


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
        self._Album = Album(album_dir, self.set_view)
        self._album_sem.release()


    def set_data(self):
        self._Album.set_data()

    def set_view(self, data):
        self._Controller.set_view(data)

    def download_file(self, url):
        self._Downloader.add_element(url)
        
    def convert_file(self, url):
        self._Converter.add_element(url)