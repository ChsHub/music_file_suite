from wx import App, Frame, Notebook, Panel, EXPAND, BoxSizer, VERTICAL, EVT_CLOSE, \
    HORIZONTAL
from wx.lib.agw.hyperlink import HyperLinkCtrl
from wxwidgets.input_widget import InputWidget
from wxwidgets.preview import Table, Preview

from src.resource.meta_tags import MetaTags, SimpleTags, FileTypes
from src.resource.texts import SelectionTabs, text_download_input, text_selction_meta, text_selction_album, \
    SelectionCodecs, text_open_file_title
from src.resource.texts import text_preview_change, text_preview_playlist
from src.resource.texts import text_view_title, SelectionAlbum, SelectionMeta
from src.view.file_input import FileInput
from src.view.standard_view.standard_selection import StandardSelection


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

        selections = Panel(tab)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(FileInput(tab, text=text_open_file_title, callback=self.analyze_files,
                            file_type=FileTypes.MUSIC.value.replace(".", "*.").replace(",", ";")))
        sizer.Add(selections)
        self._preview = Preview(tab, MetaTags, [self.set_meta, text_preview_change],
                                [self._Controller.make_playlist, text_preview_playlist])
        sizer.Add(self._preview, 1, EXPAND)

        sel_sizer = BoxSizer(HORIZONTAL)
        sel_sizer.Add(StandardSelection(parent=selections, radio_enum=SelectionAlbum,
                                        callback=self._Controller.set_is_album, title=text_selction_album))
        sel_sizer.Add(StandardSelection(parent=selections, radio_enum=SelectionMeta,
                                        callback=self._Controller.set_is_meta, title=text_selction_meta))
        selections.SetSizer(sel_sizer)

        tab.SetSizer(sizer)

    # TODO link ids for multiple downloads
    def init_tab_download(self, tab):
        download_input = InputWidget(tab, text=text_download_input, callback=self._download, reset=True)
        self._download_list = Table(tab, headers=["File", "Progress"])

        sizer = BoxSizer(VERTICAL)
        sizer.Add(download_input)
        sizer.Add(self._download_list, 1, EXPAND)
        tab.SetSizer(sizer)
        download_input.Layout()  # Remove wrong initial value

    # TODO remove all hard coded
    def init_tab_convert(self, tab):
        convert_input = FileInput(tab, text=text_open_file_title, callback=self.add_convert,
                                  file_type=FileTypes.VIDEO.value.replace(".", "*.").replace(",", ";"))
        self._convert_list = Preview(tab, SimpleTags, [self.start_convert, "Start"])
        self.codec_selection = StandardSelection(tab, callback=None, title="Codec", radio_enum=SelectionCodecs)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(convert_input)
        sizer.Add(self.codec_selection)
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

    def add_convert(self, path, files):
        self._Controller.add_convert(path, files)

    # ++++ CONTROLLER ++++
    def set_meta(self, event):
        self._Controller.set_data()

    def analyze_files(self, path, files):
        self._Controller.analyze_files(path, files)

    def set_preview_data(self, data, type):
        self._preview.clear()
        self._preview.add_lines(data)

    def set_meta_color(self, event):
        self._preview.set_row_color(0, "#00FFFF")

    def update_preview(self, data):
        pass

    def _download(self, url):
        self._download_list.add_line([url, "0%"])
        self._Controller.download(url)

    def set_download_progress(self, percent):
        self._download_list.update_last_cell(data=percent, column=1)

    def set_convert_progress(self, id, percent):
        self._convert_list.update_cell(percent, 1, row=id)

    def add_convert_line(self, line):
        self._convert_list.add_line(line)
