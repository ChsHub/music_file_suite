from tkinter import Tk, LEFT, W, TOP, BOTTOM, Frame, Button, X, BOTH, YES, RIGHT

import resource.saved_input as saved_input
from download_input import DownloadInput
from file_input import FileInput
from standard_frame import StandardFrame
from colors import color_button
from standart_selections import StandartSelections
from preview import Preview
from texts import text_view_title
from std_output import StdOutput
# TODO Feedback for apply change

class View:
    # class
    _root = None
    _Controller = None

    # gui elements
    _album_selection = None
    _preview = None
    _frame2 = None
    _selection = None

    def __init__(self, Controller):
        self._Controller = Controller

    def init_gui(self):
        self._root = Tk()
        self._root.title = text_view_title
        self._root = StandardFrame(self._root, side=LEFT)
        # TODO fail
        try:
            file_path = saved_input.file_path
        except AttributeError as e:
            file_path = None

        # first column
        frame1 = StandardFrame(self._root, side=LEFT)

        FileInput(frame1, file_path, color_button, self.analyze_files)
        self._selection = StandartSelections(frame1, color_button, self.get_data)
        DownloadInput(frame1, color_button, self._Controller.download)
        StdOutput(frame1)

        # get data from model
        self._Controller.analyze_files(file_path, False)

        # second column
        self._frame2 = StandardFrame(self._root, side=LEFT)

        self.get_data(True)  # create preview TODO initializing???

        # build gui
        self._root.mainloop()


    #### GUI FUNCTIONS ####

    def _create_preview(self, data):

        if self._preview:
            self._preview.destroy()

        self._preview = Preview(self._frame2, data, self._apply_change_callback)

    #### CALLBACK ####

    def _apply_change_callback(self):
        is_album = self._selection.get_is_album()
        self._Controller.set_data(is_album)

    #### CONTROLLER ####

    def update_view(self, data):
        # UPDATE Preview
        raise NotImplementedError

    def analyze_files(self, album_dir):
        is_album = self._selection.get_is_album()
        self._Controller.analyze_files(album_dir, is_album)

    def get_data(self, is_album):
        data = self._Controller.get_data(is_album)
        self._create_preview(data)
