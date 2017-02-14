import logging
from tkinter import Tk, LEFT, BOTH
from colors import color_button
from column import Column
from convert_input import ConvertInput
from download_input import DownloadInput
from file_input import FileInput
from preview import Preview
from standard_frame import StandardFrame
from std_output import StdOutput
from texts import text_view_title


# TODO Feedback for apply change

class Window:
    # class
    _root = None
    _Controller = None

    # gui elements
    _album_selection = None
    _preview = None

    _selection = None

    def __init__(self, Controller):
        self._Controller = Controller

    def init_gui(self):
        self._root = Tk()
        self._root.title(text_view_title)
        self._root = StandardFrame(self._root, side=LEFT, fill=BOTH)

        # column
        column1 = Column(self._root)
        column2 = Column(self._root)

        self._preview = Preview(column2, None, self._apply_change_callback)
        # COLUMN 1
        FileInput(column2.get_parent(), color_button, self.analyze_files)
        # self._selection = StandardSelections(frame1, color_button, self.get_data)
        DownloadInput(column1.get_parent(), color_button, self._Controller.download)
        ConvertInput(column1.get_parent(), color_button, self._Controller.convert_all)
        StdOutput(column1.get_parent())

        # build gui
        self._root.mainloop()

    #### GUI FUNCTIONS ####

    def _create_preview(self, data):
        logging.info("CREATE preview")
        self._preview.update_view(data)

    #### CALLBACK ####

    def _apply_change_callback(self):
        # is_album = self._selection.get_is_album() TODO remove
        self._Controller.set_data()

    #### CONTROLLER ####
    def analyze_files(self, album_dir):
        # is_album = self._selection.get_is_album()
        self._Controller.analyze_files(album_dir)
        # self.get_preview_data() TODO remove

    def set_preview_data(self, data):
        self._create_preview(data)

        # def get_preview_data(self):
        #    data = self._Controller.get_preview_data()
        #   self._create_preview(data)
