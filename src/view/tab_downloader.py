from logging import info, exception, error

from wx import EXPAND, VERTICAL, TOP, ALL, LEFT
from wxwidgets import SimpleSizer, InputWidget, Table

from src.controller.controller_downloader import ControllerDownloader
from src.resource.meta_tags import DownloadTags
from src.view.standard_view.standard_selection import StandardSelection


class TabDownloader:
    def __init__(self, tab, texts, video_choices, border_size, config):

        self._controller = ControllerDownloader(self, config)

        download_input = InputWidget(tab, text_button=texts['text_download_input'], callback=self._download, reset=True)

        self.video_selection = StandardSelection(tab, callback=None, title=texts['text_video_option'],
                                                 choices=video_choices)
        self._download_list = Table(tab, headers=[str(x.value) for x in DownloadTags])

        with SimpleSizer(tab, VERTICAL) as sizer:
            sizer.Add(download_input, flag=ALL, border=border_size)
            sizer.Add(self.video_selection, flag=TOP | LEFT, border=border_size)
            sizer.Add(self._download_list, 1, flag=EXPAND | ALL, border=border_size)

        download_input.Layout()  # Remove wrong initial value

    # Notify model

    def _download(self, url: str):
        if not url:
            error('No valid url: %s' % url)
            return

        info('INFO: ' + url)
        self._controller.download(url, self.video_selection.get_selection())

    # Change view

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