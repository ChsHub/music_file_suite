from logging import info

from wx import Panel, EXPAND, VERTICAL, HORIZONTAL, TOP, ALL, RIGHT, LEFT
from wxwidgets import SimpleSizer, FileInput, Preview

from src.controller.controller_meta import ControllerMeta
from src.resource.meta_tags import MetaTags
from src.resource.texts import SelectionAlbum, SelectionMeta
from src.view.abstract_list_view import AbstractListView
from src.view.standard_view.standard_selection import StandardSelection


class TabMeta(AbstractListView):
    def __init__(self, tab, texts, border_size, config):
        AbstractListView.__init__(self, None)
        self._controller = ControllerMeta(self, config)

        selections = Panel(tab)

        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(FileInput(tab, text_button=texts['text_open_file_title'], callback=self.analyze_files,
                                text_title=texts['text_open_file_title'], text_open_file=texts['text_open_file']),
                      flag=TOP | LEFT | RIGHT, border=border_size)

            sizer.Add(selections, flag=EXPAND | TOP | LEFT | RIGHT, border=border_size)

            self._data_list = Preview(tab, MetaTags, border=border_size,
                                      buttons=[[self.set_meta, texts['text_preview_change']],
                                               [self._controller.make_playlist, texts['text_preview_playlist']]],
                                      edit_callback=self._edit_song)
            sizer.Add(self._data_list, 1, flag=EXPAND | ALL, border=border_size)

            with SimpleSizer(selections, HORIZONTAL) as sel_sizer:
                sel_sizer.Add(StandardSelection(parent=selections, choices=SelectionAlbum,
                                                callback=self._controller.set_is_album,
                                                title=texts['text_selection_album']),
                              flag=RIGHT | TOP, border=border_size)
                sel_sizer.Add(StandardSelection(parent=selections, choices=SelectionMeta,
                                                callback=self._controller.set_is_meta,
                                                title=texts['text_selection_meta']),
                              flag=TOP, border=border_size)

    # Notify model

    def _edit_song(self, row, column, data):
        info("EDIT SONG: " + str(row) + " " + str(column) + " " + str(data))
        self._controller.edit_song(row, column, data)

    def set_meta(self, event):
        self._controller.set_data()

    def analyze_files(self, path, files):
        self._data_list.clear()  # Clear previous lines
        self._controller.analyze_files(path, files)
