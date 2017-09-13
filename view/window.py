from logging import info
from tkinter import Tk, BOTTOM

import toga
from resource.meta_tags import FileTypes
from resource.texts import SelectionTabs
from resource.texts import text_convert_input
from resource.texts import text_view_title, SelectionAlbum, SelectionMeta
from view.download_input import DownloadInput
from view.file_input import FileInput
from view.preview import Preview
from view.standard_view.colors import color_button
from view.standard_view.column import Column
from view.standard_view.notebook import Notebook
from view.standard_view.standard_button import StandardButton
from view.standard_view.standard_frame import StandardFrame
from view.standard_view.standard_radiobutton import StandardRadiobutton
from view.standard_view.standard_selection import StandardSelection
from view.std_output import StdOutput
# TODO more Feedback (Apply change, convert, download, ect.)
# TODO Strech Window

class Window(toga.App):
    # class
    _Controller = None
    # gui elements
    _album_selection = None
    _preview_songs = None
    _selection = None

    def __init__(self, controller, *args):
        super().__init__(*args)
        self._Controller = controller

    def startup(self):

        self._preview = {}
        self.main_window = toga.MainWindow(text_view_title)
        self.main_window.app = self
        self.main_window.content = toga.Box()

        self.outer_comlumn = Column(self.main_window.content, padding=0)
        StandardRadiobutton(self.outer_comlumn)

       # self.notebook = Notebook(self.outer_comlumn)
        self.main_window.show()
        return

        # column
        column = []
        for tab in SelectionTabs:
            column.append(Column(self.notebook))

        # Column 1
        self._preview[FileTypes.MP3] = Preview(column[0].get_parent(), None, self._Controller.set_data, self._Controller.make_playlist)
        StandardSelection(column[0].get_parent(), SelectionAlbum, self._Controller.set_is_album)
        StandardSelection(column[0].get_parent(), SelectionMeta, self._Controller.set_is_meta)
        StdOutput(column[0].get_parent())
        # Column 2
        Preview(column[1].get_parent(), None, self._Controller.set_data, self._Controller.make_playlist)
        DownloadInput(column[1].get_parent(), color_button, self._Controller.download)
        # Column 3
        self._preview[FileTypes.VIDEO] = Preview(column[2].get_parent(), None,
                                                 lambda: self._Controller.set_data(), self._Controller.make_playlist)
        button_frame = StandardFrame(master=column[2].get_parent(), side=BOTTOM, borderwidth=1)
        StandardButton(master=button_frame, text=text_convert_input, color=color_button,
                       callback=self._Controller.convert_all)

        for i, tab in enumerate(SelectionTabs):
            self.notebook.add_screen(column[i], tab)

        FileInput(self.outer_comlumn.get_parent(), color_button, self.analyze_files).pack(padx=10, pady=10)



    #### CONTROLLER ####
    def analyze_files(self, album_dir):
        self._Controller.analyze_files(album_dir)

    def set_preview_data(self, data, type):
        self._preview[type].update_view(data)
