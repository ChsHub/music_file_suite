from hypothesis import given, example
from hypothesis.strategies import text
from model.model import Model
from tempfile import TemporaryDirectory
from unittest import case

class TestModel:
    @given(None)
    def test_init__(self):
        self.model = Model(None)


    def get_valid_path(self):
        dir = TemporaryDirectory
        return dir


    @given(text())
    @example("")
    def test_analyze_files(self, strategy):
        model = Model(None)
        model.analyze_files(strategy)
        assert not model._Album


    @example(get_valid_path(None))
    def test_analyze_files_valid(self, strategy):
        model = Model(None)
        model.analyze_files(strategy)
        assert model._Album


    def test_set_data(self):
        pass


    def test_set_is_album(self):
        pass


    def test_set_is_meta(self):
        pass


    def test_download_file(self):
        pass


    def test_convert_file(self):
        pass