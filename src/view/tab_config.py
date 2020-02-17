from wx import VERTICAL, ALL
from wxwidgets import DirectoryInput, SimpleSizer

from src.resource.settings import *


class TabConfig:
    def __init__(self, tab, texts, border_size):
        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(
                DirectoryInput(parent=tab, text_button=texts['text_set_download'], callback=set_download_directory,
                               text_title=texts['text_set_download'], initial=download_path),
                flag=ALL, border=border_size)
