from wx import App, Frame, Notebook, Panel, StaticText, Button, EXPAND, BoxSizer, VERTICAL, HORIZONTAL, GridSizer
from view.preview import Table

from resource.meta_tags import FileTypes
from resource.texts import SelectionTabs, text_convert_input, text_download_input, text_preview_change
from resource.texts import text_view_title, SelectionAlbum, SelectionMeta
from view.file_input import FileInput
from view.preview import Preview
from view.standard_view.colors import color_button
from view.standard_view.column import Column
# from view.standard_view.standard_button import StandardButton
# from view.standard_view.standard_frame import StandardFrame
from view.standard_view.standard_input import StandardInput
# from view.standard_view.standard_radiobutton import StandardRadiobutton
# from view.standard_view.standard_selection import StandardSelection
from view.std_output import StdOutput
from resource.texts import text_preview_change, text_preview_playlist


# TODO more Feedback (Apply change, convert, download, ect.)
# TODO Strech Window


class Window(App):
    # class
    _Controller = None
    # gui elements
    _album_selection = None
    _preview_songs = None
    _selection = None

    def __init__(self, controller):
        super().__init__()
        self._Controller = controller

        frame = Frame(None, title='Music Suite')  # Create a Window TODO title

        self.notebook = Notebook(frame, EXPAND)  # Tabs
        # tabs
        tabs = []

        for label in SelectionTabs:
            tabs.append(Panel(self.notebook, EXPAND))

        self.init_tab_meta(tabs[0])
        self.init_tab_download(tabs[1])
        self.init_tab_convert(tabs[2])

        for i, label in enumerate(SelectionTabs):
            self.notebook.AddPage(tabs[i], label)

        frame.Show()
        return
        # Column 1
        StandardSelection(tabs[0].get_parent(), SelectionAlbum, self._Controller.set_is_album)
        StandardSelection(tabs[0].get_parent(), SelectionMeta, self._Controller.set_is_meta)
        StdOutput(tabs[0].get_parent())
        # Column 2
        # Column 3

        # button_frame = StandardFrame(master=tabs[2].get_parent(), side=BOTTOM, borderwidth=1)
        # StandardButton(master=button_frame, text=text_convert_input, color=color_button,
        #               callback=self._Controller.convert_all)

        FileInput(self.outer_comlumn.get_parent(), color_button, self.analyze_files).pack(padx=10, pady=10)

    def init_tab_meta(self, tab):
        sizer = BoxSizer(VERTICAL)
        sizer.Add(StandardInput(tab), 1, EXPAND)
        sizer.Add(Preview(tab, [self._Controller.set_data, text_preview_change],
                          [self._Controller.make_playlist, text_preview_playlist]), 1, EXPAND)
        tab.SetSizer(sizer)

    def init_tab_download(self, tab):
        download_input = StandardInput(tab, button_text=text_download_input, callback=self._download)
        self._download_list = Table(tab, headers=["File", "Progress"])

        sizer = BoxSizer(VERTICAL)
        sizer.Add(download_input, 1, EXPAND)
        sizer.Add(self._download_list, 1, EXPAND)
        tab.SetSizer(sizer)

    def init_tab_convert(self, tab):
        # Column 3 CONVERT
        convert_input = StandardInput(tab)
        # tabs[2].add(convert_input)
        # tabs[2].add(Preview([lambda x: self._Controller.convert_all(convert_input.get_input()),
        #                     text_convert_input]))

    #### CONTROLLER ####
    def analyze_files(self, album_dir):
        self._Controller.analyze_files(album_dir)

    def set_preview_data(self, data, type):
        self._preview[type].update_view(data)

    def _download(self, url):

        self._download_list.add_line([url, "0%"])
        self._Controller.download(url)

    def set_download_progress(self, percent):
        self._download_list.update_cell(data=percent, column=1)