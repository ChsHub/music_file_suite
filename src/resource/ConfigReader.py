from configparser import ConfigParser
from enum import Enum
from logging import error

from os.path import abspath, exists


class ConfigReader(ConfigParser):
    def __init__(self, texts_path=''):
        super().__init__()
        if not texts_path:
            texts_path = 'resources/texts.cfg'

        if not exists(texts_path):
            # Quit if texts not found
            raise FileNotFoundError

        self.read(abspath(texts_path))

        class SelectionCodecs(Enum):
            EXTRACT = self['SelectionCodecs']['EXTRACT']
            MP3 = self['SelectionCodecs']['MP3']
            OPUS = self['SelectionCodecs']['OPUS']

        self.SelectionCodecs = SelectionCodecs

        class SelectionVideo(Enum):
            NO_VIDEO = self['SelectionVideo']['no_video']
            VIDEO = self['SelectionVideo']['video']

        self.SelectionVideo = SelectionVideo

        self.ffmpeg_path = abspath(self['Converter']['ffmpeg_path'])
        if not exists(self.ffmpeg_path):
            error('ffmpeg not found')
            raise FileNotFoundError
