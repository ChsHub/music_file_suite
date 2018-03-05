from wx import Panel, BoxSizer, HORIZONTAL, Button, StaticText, VERTICAL, EXPAND, ListCtrl, LC_REPORT, BORDER_SUNKEN
from wx.grid import Grid

from resource.meta_tags import MetaTags
from standard_view.colors import color_blue
from resource.texts import text_preview_change, text_preview_playlist
from view.standard_view.standard_button import StandardButton
from view.standard_view.standard_frame import StandardFrame
from view.standard_view.column import Column


class Table(ListCtrl):
    row_index = 0

    def __init__(self, parent, headers):
        super().__init__(parent, size=(-1, 100), style=LC_REPORT | BORDER_SUNKEN)
        # sizer = Grid(self)#cols=len(headers))

        for i, text in enumerate(headers):
            # self.
            self.InsertColumn(i, text)
            # sizer.Add(header)
        # self.SetSizer(sizer)
        # self.SetBackgroundColour(color_blue)

    def add_line(self, data_list):

        self.InsertItem(self.row_index, data_list.pop(0))
        for i, item in enumerate(data_list):
            self.SetItem(self.row_index, i + 1, item)

        self.row_index += 1

    def update_cell(self, data, column, row=row_index):
        self.SetItem(row, column, data)


class Preview(Panel):
    _listbox = None

    def __init__(self, parent, *buttons):
        super().__init__(parent)

        self._listbox = Table(self, headers=[str(x.value) for x in MetaTags])  # , size=(600, 200))

        # CONTROL FRAMES
        button_frame = Panel(self)
        for callback, text in buttons:
            StandardButton(button_frame, text=text, callback=callback)
        # ALIGN
        sizer = BoxSizer(VERTICAL)
        sizer.Add(self._listbox, 1, EXPAND)
        sizer.Add(button_frame, 1)
        self.SetSizer(sizer)

    def update_view(self, data):
        for line in data:
            self._listbox.add_line(data)
        # self._listbox.destroy()
        # self._listbox = toga.Table(self.preview_frame, [str(x.value) for x in MetaTags], data)
