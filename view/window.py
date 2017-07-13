from logging import info
from tkinter import Tk, BOTTOM

from standard_view.colors import color_button
from standard_view.column import Column
from standard_view.notebook import Notebook
from standard_view.standard_button import StandardButton
from standard_view.standard_frame import StandardFrame
from standard_view.standard_selection import StandardSelection

from download_input import DownloadInput
from file_input import FileInput
from meta_tags import FileTypes
from preview import Preview
from std_output import StdOutput
from texts import text_convert_input
from texts import text_view_title, SelectionAlbum, SelectionMeta
from texts import SelectionTabs

# TODO more Feedback (Apply change, convert, download, ect.)
# TODO Strech Window

class Window:
    # class
    _root = None
    _Controller = None
    # gui elements
    _album_selection = None
    _preview_songs = None
    _selection = None

    def __init__(self, controller):
        self._Controller = controller
        self._preview = {}
        self._root = Tk()
        self._root.title(text_view_title)
        self.outer_comlumn = Column(self._root, pady=0, padx=0)
        self.outer_comlumn.pack()
        self.notebook = Notebook(self.outer_comlumn.get_parent())

        # column
        column = []
        for tab in SelectionTabs:
            column.append(Column(self.notebook))

        # Column 1
        self._preview[FileTypes.MP3] = Preview(column[0].get_parent(), None, self._Controller.set_data, self._Controller.make_playlist)
        StandardSelection(column[0].get_parent(), SelectionAlbum, controller.set_is_album)
        StandardSelection(column[0].get_parent(), SelectionMeta, controller.set_is_meta)
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

    def start(self):
        self._root.mainloop()
        info("WINDOW CLOSED")

    #### CONTROLLER ####
    def analyze_files(self, album_dir):
        self._Controller.analyze_files(album_dir)

    def set_preview_data(self, data, type):
        self._preview[type].update_view(data)
