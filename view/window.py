from wx import App, Frame, Notebook, Panel, EXPAND, BoxSizer, VERTICAL, EVT_CLOSE, \
    HORIZONTAL, GridSizer, StaticText
from wx.lib.agw.hyperlink import HyperLinkCtrl

from view.preview import Table

from resource.texts import SelectionTabs, text_convert_input, text_download_input, text_preview_change, \
    text_selction_meta, text_selction_album, SelectionCodecs
from resource.texts import text_view_title, SelectionAlbum, SelectionMeta
from view.file_input import FileInput
from view.preview import Preview
from view.standard_view.standard_input import StandardInput
from view.standard_view.standard_selection import StandardSelection
from resource.texts import text_preview_change, text_preview_playlist
from view.standard_view.standard_button import StandardButton


# TODO more Feedback (Apply change, convert, ect.)


class Window(App):
    # class
    _Controller = None
    # gui elements
    _album_selection = None
    _preview_songs = None
    _selection = None
    _frame = None
    _convert_list = None

    def __init__(self, controller):
        super().__init__()
        self._Controller = controller

        frame = Frame(None, title=text_view_title, size=(600, 300))  # Create a Window
        self._frame = frame
        frame.Bind(EVT_CLOSE, lambda x: frame.Destroy())  # Close Window

        self.notebook = Notebook(frame, EXPAND)  # Tabs
        # tabs
        tabs = []

        for label in SelectionTabs:
            tabs.append(Panel(self.notebook, EXPAND))

        self.init_tab_download(tabs[0])
        self.init_tab_convert(tabs[1])
        self.init_tab_meta(tabs[2])
        self._init_tab_config(tabs[3])

        for i, label in enumerate(SelectionTabs):
            self.notebook.AddPage(tabs[i], label)

        frame.Layout()  # Update Layout to fix black square
        frame.Show()
        return

    def init_tab_meta(self, tab):

        sizer = BoxSizer(VERTICAL)
        sizer.Add(StandardInput(tab, self.analyze_files), 1, EXPAND)
        sizer.Add(Preview(tab, [self._Controller.set_data, text_preview_change],
                          [self._Controller.make_playlist, text_preview_playlist]), 1, EXPAND)

        selections = Panel(tab)
        sizer.Add(selections)
        sel_sizer = BoxSizer(HORIZONTAL)
        sel_sizer.Add(
            StandardSelection(parent=selections, radio_enum=SelectionAlbum, callback=self._Controller.set_is_album,
                              title=text_selction_album))
        sel_sizer.Add(
            StandardSelection(parent=selections, radio_enum=SelectionMeta, callback=self._Controller.set_is_meta,
                              title=text_selction_meta))
        selections.SetSizer(sel_sizer)
        tab.SetSizer(sizer)

    def init_tab_download(self, tab):
        download_input = StandardInput(tab, button_text=text_download_input, callback=self._download)
        self._download_list = Table(tab, headers=["File", "Progress"])

        sizer = BoxSizer(VERTICAL)
        sizer.Add(download_input, 1, EXPAND)
        sizer.Add(self._download_list, 1, EXPAND)
        tab.SetSizer(sizer)

    def init_tab_convert(self, tab):
        convert_input = FileInput(tab, self._Controller.add_convert)
        self._convert_list = Table(tab, headers=["File", "Progress"])
        sizer = BoxSizer(VERTICAL)
        sizer.Add(convert_input, 1, EXPAND)
        self.codec_selection = StandardSelection(tab, callback=None, title="Codec", radio_enum=SelectionCodecs)
        sizer.Add(self.codec_selection)
        sizer.Add(StandardButton(tab, text="Start",
                                 callback=self.start_convert))

        sizer.Add(self._convert_list, 1, EXPAND)
        tab.SetSizer(sizer)

    def _init_tab_config(self, tab):
        sizer = BoxSizer(VERTICAL)
        text = HyperLinkCtrl(tab, label="https://www.youtube.com/")
        sizer.Add(text, 1, EXPAND)
        tab.SetSizer(sizer)
        # text.GotoURL(URL="") TODO BUTTONS FOR LIBS

    def start_convert(self, event):
        self._Controller.start_convert(self.codec_selection.get_selection())

    #### CONTROLLER ####
    def analyze_files(self, path, files):
        self._Controller.analyze_files(path, files)

    def set_preview_data(self, data, type):
        raise NotImplementedError
        self._preview[type].update_view(data)

    def _download(self, url):
        self._download_list.add_line([url, "0%"])
        self._Controller.download(url)

    def set_download_progress(self, percent):
        self._download_list.update_cell(data=percent, column=1)

    def set_convert_progress(self, id, percent):
        self._convert_list.update_cell(percent, 1, row=id)

    def add_convert_line(self, line):
        self._convert_list.add_line(line)
