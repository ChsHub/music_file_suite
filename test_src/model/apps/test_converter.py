from os.path import split

from hypothesis import given
from hypothesis.strategies import text, integers

from src.converter.converter import Converter
from src.resource.ConfigReader import ConfigReader
from os import getcwd, chdir

dir = getcwd()
for i in range(3):
    dir, _ = split(dir)
chdir(dir)

config = ConfigReader('.\\resources\\texts.cfg')
test_converter = Converter(None, config['Converter'], config.SelectionCodecs, config.ffmpeg_path)


def test___init__(self, controller):
    pass


@given(text(), text(), integers(min_value=0, max_value=100))
def test_add_job(path, file, file_count):
    test_converter.add_job(path, [file] * file_count)


def test_start_convert(self, selection):
    pass


def test__get_output_file_path(new_extension, file_path):
    pass


def test__get_audio_codec(self, file_path: str) -> str:
    pass


def test__get_file_extension(self, file_path: str, i: int) -> (str, str):
    pass


if __name__ == '__main__':
    test_add_job()
