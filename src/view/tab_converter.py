from wx import VERTICAL, ALL, TOP, LEFT, EXPAND
from wxwidgets import FileInput, Preview, SimpleSizer

from src.controller.controller_converter import ControllerConverter
from src.resource.meta_tags import SimpleTags
from src.view.standard_view.standard_selection import StandardSelection


class TabConverter:
    def __init__(self, tab, texts, SelectionCodecs, border_size, config):
        self._controller = ControllerConverter(self, config)

        convert_input = FileInput(tab, text_button=texts['text_open_file_title'], callback=self._add_convert,
                                  text_title=texts['text_open_file_title'], text_open_file=texts['text_open_file'])

        self.codec_selection = StandardSelection(tab, callback=None, title=texts['text_codec_selection'],
                                                 choices=SelectionCodecs)
        self._convert_list = Preview(tab, SimpleTags, border=border_size,
                                     buttons=[(self._start_convert, texts['text_start_convert']),
                                              (self._reset_convert, texts['text_reset_convert'])])

        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(convert_input, flag=ALL, border=border_size)
            sizer.Add(self.codec_selection, flag=TOP | LEFT, border=border_size)
            sizer.Add(self._convert_list, 1, flag=EXPAND | ALL, border=border_size)

    # Notify model

    def _add_convert(self, path, files):
        self._controller.add_convert(path, files)

    def _start_convert(self, event):
        self._controller.start_convert(self.codec_selection.get_selection())

    def _reset_convert(self, event):
        self._controller.reset_convert()
        self._convert_list.clear()

    # Change view

    def set_convert_progress(self, id, percent):
        self._convert_list.update_cell(percent, 1, row=id)

    def add_convert_line(self, line):
        self._convert_list.add_line(line)
