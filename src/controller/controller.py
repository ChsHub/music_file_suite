# python 3.2+
from concurrent.futures import ThreadPoolExecutor
from logging import error
from src.model.apps.downloader import Downloader
from src.model.apps.converter import Converter
from src.model.model import Model
from src.view.window import Window


class Controller:
    _Main_view = None
    _Main_model = None
    _Converter = None
    _Downloader = None

    def __init__(self):
        self.executor = ThreadPoolExecutor()

        self._Main_model = Model(self)
        self._Converter = Converter(self)
        self._Downloader = Downloader(self)
        self._Main_view = Window(self)

    def _submit(self, *args):
        #f, *args = args
        #f(*args)
        #return # TODO remove debug
        future = self.executor.submit(*args)
        # called after execution of this task
        future.add_done_callback(self.error_log)

    @staticmethod
    def error_log(future):
        # returns None if no exception occurred
        exception = future.exception()
        if exception:
            error(type(exception))
            error(exception)

    # +++View+++
    def analyze_files(self, path, files):
        if self._Main_model:
            self._submit(self._Main_model.analyze_files, path, files)

    def set_data(self):
        if self._Main_model:
            self._submit(self._Main_model.set_data)

    def set_is_meta(self, is_meta):
        if self._Main_model:
            self._submit(self._Main_model.set_is_meta, is_meta)

    def set_is_album(self, is_album):
        if self._Main_model:
            self._submit(self._Main_model.set_is_album, is_album)

    def download(self, url):
        if self._Downloader:
            self._submit(self._Downloader.consume_element, url)

    def add_convert(self, path, files):
        if self._Converter:
            self._submit(self._Converter.add_job, path, files)

    def make_playlist(self):
        if self._Main_model:
            self._submit(self._Main_model.make_playlist)

    def start_convert(self, selection):
        if self._Converter:
            self._submit(self._Converter.start_convert, selection)

    def edit_song(self, row, column, data):
        if self._Main_model:
            self._submit(self._Main_model.edit_song, row, column, data)

    # +++Model+++

    # called: Model -> Album -> Controller -> Window
    def set_view(self, data):
        if self._Main_view:
            self._Main_view.set_preview_data(data)

    def set_download_progress(self, percent):
        self._Main_view.set_download_progress(percent)

    def set_convert_progress(self, id, percent):
        self._Main_view.set_convert_progress(id, percent)

    def add_convert_line(self, line):
        self._Main_view.add_convert_line(line)

    def update_meta_line(self, row, data):
        if self._Main_view:
            self._Main_view.update_preview_row(row, data)

    def set_meta_color_normal(self, id):
        if self._Main_view:
            self._Main_view.set_meta_color_normal(id)

    def set_meta_color_warning(self, row):
        if self._Main_view:
            self._Main_view.set_meta_color_warning(row)

    def set_meta_color_ok(self, row):
        if self._Main_view:
            self._Main_view.set_meta_color_ok(row)