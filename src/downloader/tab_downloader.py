from logging import info, error

from wx import EXPAND, VERTICAL, TOP, ALL, LEFT
from wxwidgets import SimpleSizer, InputWidget, Table

from src.downloader.controller_downloader import ControllerDownloader
from src.resource.meta_tags import DownloadTags
from src.abstract.abstract_list_view import AbstractListView
from src.abstract.view.standard_view.standard_selection import StandardSelection


class TabDownloader(AbstractListView):
    def __init__(self, tab, texts, video_choices, border_size, config):
        AbstractListView.__init__(self, 2)
        self._controller = ControllerDownloader(self, config)

        download_input = InputWidget(tab, text_button=texts['text_download_input'], callback=self._download, reset=True)

        self.video_selection = StandardSelection(tab, callback=None, title=texts['text_video_option'],
                                                 choices=video_choices)
        self._data_list = Table(tab, headers=[str(x.value) for x in DownloadTags])

        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(download_input, flag=ALL, border=border_size)
            sizer.Add(self.video_selection, flag=TOP | LEFT, border=border_size)
            sizer.Add(self._data_list, 1, flag=EXPAND | ALL, border=border_size)

        download_input.Layout()  # Remove wrong initial value

    # Notify model

    def _download(self, url: str):
        if not url:
            error('No valid url: %s' % url)
            return

        info('INFO: ' + url)
        self._controller.download(url, self.video_selection.get_selection())
