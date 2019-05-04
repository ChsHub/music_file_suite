# -*- coding: utf8 -*-
from enum import Enum
from configparser import ConfigParser
from os.path import abspath

from utility.os_interface import exists

texts_path = abspath('resources/texts.cfg')
config = ConfigParser()

# Write default settings, if missing
if not exists(texts_path):
    config['SelectionAlbum'] = {'DETECTED': 'as detected',
                                'ALBUM': 'is Album',
                                'RANDOM': 'is random'}
    config['SelectionMeta'] = {'NO_META': 'Ignore/overwrite meta data',
                               'META': 'Use meta data'}
    config['SelectionCodecs'] = {'EXTRACT': 'Extract Audio only (Keep format)',
                                 'MP3': 'High quality mp3',
                                 'OPUS': 'Opus transparent'}
    config['Text'] = {'SelectionTabs': ",".join(['Download', 'Convert', 'Meta', 'Config', 'About']),

                      'text_preview_change': 'Apply Change',
                      'text_preview_playlist': 'Create Playlist',
                      'text_download_input': 'Download YouTube',
                      'text_convert_input': 'Convert',
                      'text_file_input': 'Open File',
                      'text_view_title': 'Music Suite',
                      'text_set_download': 'Set Download Directory',
                      'text_open_file_title': 'Open Files',
                      'text_open_file': 'Music or Video',

                      'text_selection_meta': 'Previous Meta Data',
                      'text_selection_album': 'Is Album',

                      'convert_directory': 'CONVERTED'}

    with open(texts_path, 'w') as configfile:
        config.write(configfile)

# Read settings
config.read(texts_path)

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


SelectionTabs = config['Text']['SelectionTabs'].split(',')

text_preview_change = config['Text']['text_preview_change']
text_preview_playlist = config['Text']['text_preview_playlist']
text_download_input = config['Text']['text_download_input']
text_convert_input = config['Text']['text_convert_input']
text_file_input = config['Text']['text_file_input']
text_view_title = config['Text']['text_view_title']
text_set_download = config['Text']['text_set_download']
text_open_file_title = config['Text']['text_open_file_title']
text_open_file = config['Text']['text_open_file']

text_selection_meta = config['Text']['text_selection_meta']
text_selection_album = config['Text']['text_selection_album']

convert_directory = config['Text']['convert_directory']
