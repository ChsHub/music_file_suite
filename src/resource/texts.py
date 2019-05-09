# -*- coding: utf8 -*-
from enum import Enum

from src.resource.ConfigReader import ConfigReader

config = ConfigReader()


class SelectionAlbum(Enum):
    RANDOM = config['SelectionAlbum']['RANDOM']
    ALBUM = config['SelectionAlbum']['ALBUM']


class SelectionMeta(Enum):
    NO_META = config['SelectionMeta']['NO_META']
    META = config['SelectionMeta']['META']


class SelectionCodecs(Enum):
    EXTRACT = config['SelectionCodecs']['EXTRACT']
    MP3 = config['SelectionCodecs']['MP3']
    OPUS = config['SelectionCodecs']['OPUS']
