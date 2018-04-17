# -*- coding: utf8 -*-
from enum import Enum
from configparser import ConfigParser
from utility.os_interface import exists

settings_path = 'resources/settings.cfg'
if not exists(settings_path):
    config = ConfigParser()
    config['SelectionAlbum'] = {'DETECTED': 'as detected',
                                'ALBUM': 'is Album',
                                'RANDOM': 'is random'}
    config['SelectionMeta'] = {'NO_META': 'Ignore/overwrite meta data',
                               'META': 'Use meta data'}
    config['SelectionCodecs'] = {'EXTRACT': 'Extract Audio only (Keep format)',
                                 'MP3': 'High quality mp3',
                                 'OPUS': 'Opus transparent'}
    config['Text'] = {'SelectionTabs': ['Download', 'Convert', 'Meta', 'Config', 'About'],

                      'text_preview_change': 'Apply Change',
                      'text_preview_playlist': 'Create Playlist',
                      'text_download_input': 'Download YouTube',
                      'text_convert_input': 'Convert',
                      'text_file_input': 'Open File',
                      'text_view_title': 'Music Suite',
                      'text_open_file_title': 'Open Files',
                      'text_open_file': 'Music or Video',

                      'text_selection_meta': 'Previous Meta Data',
                      'text_selection_album': 'Is Album',

                      'convert_directory': 'CONVERTED'}

    with open(settings_path, 'w') as configfile:
        config.write(configfile)


class SelectionAlbum(Enum):
    DETECTED = 'as detected'
    ALBUM = 'is Album'
    RANDOM = 'is random'


class SelectionMeta(Enum):
    NO_META = 'Ignore/overwrite meta data'
    META = 'Use meta data'


class SelectionCodecs(Enum):
    EXTRACT = 'Extract Audio only (Keep format)'
    MP3 = 'High quality mp3'
    OPUS = 'Opus transparent'


SelectionTabs = ['Download', 'Convert', 'Meta', 'Config', 'About']

text_preview_change = 'Apply Change'
text_preview_playlist = 'Create Playlist'
text_download_input = 'Download YouTube'
text_convert_input = 'Convert'
text_file_input = 'Open File'
text_view_title = 'Music Suite'
text_open_file_title = 'Open Files'
text_open_file = 'Music or Video'

text_selection_meta = 'Previous Meta Data'
text_selection_album = 'Is Album'

convert_directory = 'CONVERTED'
