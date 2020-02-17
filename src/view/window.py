from logging import info

from timerpy import Timer
from wx import App, Frame, Notebook, Panel, EXPAND, EVT_CLOSE, \
    BITMAP_TYPE_ANY, Bitmap, Icon

from src import __version__
from src.resource.ConfigReader import ConfigReader
from src.view.tab_about import TabAbout
from src.view.tab_config import TabConfig
from src.view.tab_converter import TabConverter
from src.view.tab_downloader import TabDownloader
from src.view.tab_meta import TabMeta
# TODO file types open



class Window(App):
    # TODO BUG set wrong song on META RENAME
    def __init__(self):
        super().__init__()
        config = ConfigReader()
        border_size = 10
        texts = config['Window']
        codec_choices = config.SelectionCodecs
        video_choices = config.SelectionVideo

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

            self._tab_downloader = TabDownloader(tabs[0], texts, video_choices, border_size, config)

            self._converter_tab = TabConverter(tabs[1], texts, codec_choices, border_size, config)
            self._tab_meta = TabMeta(tabs[2], texts, border_size, config)
            TabConfig(tabs[3], texts, border_size)
            TabAbout(tabs[4], border_size)

            for i, label in enumerate(tab_labels):
                self.notebook.AddPage(tabs[i], label)
            window.Show()

    # TODO link ids for multiple downloads
    # TODO COLORS when done
