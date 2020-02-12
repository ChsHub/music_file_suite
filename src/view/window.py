from logging import info, exception, error

from timerpy import Timer
from wx import App, Frame, Notebook, Panel, EXPAND, VERTICAL, EVT_CLOSE, \
    HORIZONTAL, TOP, ALL, RIGHT, LEFT, BITMAP_TYPE_ANY, Bitmap, Icon
from wx.lib.agw.hyperlink import HyperLinkCtrl
from wxwidgets import DirectoryInput, SimpleSizer, FileInput, InputWidget, Table, Preview

from src import __version__
from src.resource.meta_tags import MetaTags, SimpleTags, FileTypes, DownloadTags
from src.resource.settings import *
from src.resource.texts import SelectionAlbum, SelectionMeta
from src.view.standard_view.colors import color_red, color_green, color_white
from src.view.standard_view.standard_selection import StandardSelection


# TODO file types open

class Window(App):
    # class
    _Controller = None
    # gui elements
    _album_selection = None
    _preview_songs = None
    _selection = None
    _frame = None
    _convert_list = None
    codec_selection = None
    _download_list = None
    _border_size = 10

    # TODO RESET CONVERT LIST
    # TODO BUG set wrong song on META RENAME
    def __init__(self, controller, texts, codec_choices, video_choices):
        super().__init__()
        self._Controller = controller

        with Timer("WINDOW BUILT", info):
            # Create a Window
            window = Frame(None, title=texts['text_view_title'] + ' ' + __version__, size=(1300, 800))
            self._frame = window
            window.Bind(EVT_CLOSE, lambda x: window.Destroy())  # Close Window event

            # Set Icon
            icon_path = texts['icon_path']
            loc = Icon()
            loc.CopyFromBitmap(Bitmap(icon_path, BITMAP_TYPE_ANY))
            window.SetIcon(loc)

            # Create tabs
            self.notebook = Notebook(window, EXPAND)
            tabs = []
            tab_labels = texts['SelectionTabs'].split(',')

            for label in tab_labels:
                tabs.append(Panel(self.notebook, EXPAND))

            self._init_tab_download(tabs[0], texts, video_choices)
            self._init_tab_convert(tabs[1], texts, codec_choices)
            self._init_tab_meta(tabs[2], texts)
            self._init_tab_config(tabs[3], texts)
            self._init_tab_about(tabs[4])

            for i, label in enumerate(tab_labels):
                self.notebook.AddPage(tabs[i], label)

            window.Show()

    def _init_tab_meta(self, tab, texts):

        selections = Panel(tab)

        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(FileInput(tab, text_button=texts['text_open_file_title'], callback=self.analyze_files,
                                text_title=texts['text_open_file_title'], text_open_file=texts['text_open_file']),
                      flag=TOP | LEFT | RIGHT, border=self._border_size)

            sizer.Add(selections, flag=EXPAND | TOP | LEFT | RIGHT, border=self._border_size)

            self._preview = Preview(tab, MetaTags, border=self._border_size,
                                    buttons=[[self.set_meta, texts['text_preview_change']],
                                             [self._Controller.make_playlist, texts['text_preview_playlist']]],
                                    edit_callback=self._edit_song)
            sizer.Add(self._preview, 1, flag=EXPAND | ALL, border=self._border_size)

            with SimpleSizer(selections, HORIZONTAL) as sel_sizer:
                sel_sizer.Add(StandardSelection(parent=selections, choices=SelectionAlbum,
                                                callback=self._Controller.set_is_album,
                                                title=texts['text_selection_album']),
                              flag=RIGHT | TOP, border=self._border_size)
                sel_sizer.Add(StandardSelection(parent=selections, choices=SelectionMeta,
                                                callback=self._Controller.set_is_meta,
                                                title=texts['text_selection_meta']),
                              flag=TOP, border=self._border_size)

    # TODO link ids for multiple downloads
    # TODO COLORS when done
    def _init_tab_download(self, tab, texts, video_choices):

        download_input = InputWidget(tab, text_button=texts['text_download_input'], callback=self._download, reset=True)

        self.video_selection = StandardSelection(tab, callback=None, title=texts['text_video_option'],
                                                 choices=video_choices)
        self._download_list = Table(tab, headers=[str(x.value) for x in DownloadTags])

        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(download_input, flag=ALL, border=self._border_size)
            sizer.Add(self.video_selection, flag=TOP | LEFT, border=self._border_size)
            sizer.Add(self._download_list, 1, flag=EXPAND | ALL, border=self._border_size)

        download_input.Layout()  # Remove wrong initial value

    def _init_tab_convert(self, tab, texts, SelectionCodecs):

        convert_input = FileInput(tab, text_button=texts['text_open_file_title'], callback=self._add_convert,
                                  text_title=texts['text_open_file_title'], text_open_file=texts['text_open_file'])

        self.codec_selection = StandardSelection(tab, callback=None, title=texts['text_codec_selection'],
                                                 choices=SelectionCodecs)
        self._convert_list = Preview(tab, SimpleTags, border=self._border_size,
                                     buttons=[[self._start_convert, texts['text_start_convert']]])

        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(convert_input, flag=ALL, border=self._border_size)
            sizer.Add(self.codec_selection, flag=TOP | LEFT, border=self._border_size)
            sizer.Add(self._convert_list, 1, flag=EXPAND | ALL, border=self._border_size)

    def _init_tab_config(self, tab, texts):
        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(
                DirectoryInput(parent=tab, text_button=texts['text_set_download'], callback=set_download_directory,
                               text_title=texts['text_set_download'], initial=download_path),
                flag=ALL, border=self._border_size)

    def _init_tab_about(self, tab):
        with SimpleSizer(tab, VERTICAL) as sizer:
            text = HyperLinkCtrl(tab, label="https://www.youtube.com/", URL="https://www.youtube.com/")
            sizer.Add(text, flag=TOP, border=self._border_size)

            text = HyperLinkCtrl(tab, label="This software uses libraries from the FFmpeg project under the LGPLv2.1",
                                 URL="https://www.ffmpeg.org/")
            sizer.Add(text, flag=TOP, border=self._border_size)

    def _start_convert(self, event):
        self._Controller.start_convert(self.codec_selection.get_selection())

    def _add_convert(self, path, files):
        self._Controller.add_convert(path, files)

    def _edit_song(self, row, column, data):
        info("EDIT SONG: " + str(row) + " " + str(column) + " " + str(data))
        self._Controller.edit_song(row, column, data)

    # ++++ CONTROLLER ++++
    def set_meta(self, event):
        self._Controller.set_data()

    def analyze_files(self, path, files):
        self._Controller.analyze_files(path, files)

    def set_preview_data(self, data):
        self._preview.clear()
        self._preview.add_lines(data)

    def set_meta_color_normal(self, row):
        self._preview.set_row_color(row, color_white)

    def set_meta_color_warning(self, row):
        self._preview.set_row_color(row, color_red)

    def set_meta_color_ok(self, row):
        self._preview.set_row_color(row, color_green)

    def update_preview_row(self, row, data):
        info("UPDATE PREVIEW ROW: " + str(row) + " " + str(data))
        self._preview.update_row(data, row)

    # +++ Downloader +++

    def _download(self, url: str):
        if not url:
            error('No valid url: %s' % url)
            return

        info('INFO: ' + url)
        self._Controller.download(url, self.video_selection.get_selection())

    def set_download_progress(self, id, percent):
        self._download_list.update_cell(data=percent, column=2, row=id)

    def set_download_title(self, id, title, url):
        # TODO find bug (Invalid item index)
        try:
            self._download_list.update_cell(data=url, column=0, row=id)
            self._download_list.update_cell(data=title, column=1, row=id)
        except Exception as e:
            error('SET DOWNLOAD TITLE:%s%s%s' % (id, title, url))
            exception(e)

    def set_download_size(self, id, size):
        self._download_list.update_cell(data=size, column=3, row=id)

    # +++ CONVERTER +++

    def set_convert_progress(self, id, percent):
        self._convert_list.update_cell(percent, 1, row=id)

    def add_convert_line(self, line):
        self._convert_list.add_line(line)
