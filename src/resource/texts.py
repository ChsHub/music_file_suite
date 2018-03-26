# -*- coding: utf8 -*-
from enum import Enum


class SelectionAlbum(Enum):
    DETECTED = "as detected"
    ALBUM = "is Album"
    RANDOM = "is random"


class SelectionMeta(Enum):
    NO_META = "Ignore/overwrite meta data"
    META = "Use meta data"



class SelectionCodecs(Enum):
    EXTRACT = "Extract Audio only (Keep format)"
    MP3 = "High quality mp3"
    OPUS = "Opus transparent"


SelectionTabs = ["Download", "Convert", "Meta", "Config"]

text_preview_change = "Apply Change"
text_preview_playlist = "Create Playlist"
text_download_input = "Download YouTube"
text_convert_input = "Convert"
text_file_input = "Open File"
text_view_title = 'Music Suite'
text_open_file_title = "Open Files"
text_open_file = "Music or Video"

text_selction_meta = "Previous Meta Data"
text_selction_album = "Is Album"

convert_directory = "CONVERTED"
