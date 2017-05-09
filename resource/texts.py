# -*- coding: utf8 -*-
from enum import Enum


class SelectionAlbum(Enum):
    DETECTED = "as detected"
    ALBUM = "is Album"
    RANDOM = "is random"


class SelectionMeta(Enum):
    META = "Use meta data"
    NO_META = "Ignore/overwrite meta data"


text_preview_change = "Apply Change"
text_preview_playlist = "Create Playlist"
text_download_input = "Download YT"
text_convert_input = "Convert"
text_file_input = "Open File"
text_view_title = 'mp3 organize'
