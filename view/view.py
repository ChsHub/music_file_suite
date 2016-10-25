from tkinter import Tk, LEFT, W

import resource.saved_input as saved_input
from download_input import DownloadInput
from file_input import FileInput
from standard_button import StandardButton
from standard_frame import StandardFrame
from standard_label import StandardLabel
from standart_selections import StandartSelections


# TODO Feedback for apply change

class View:
    # class
    _root = None
    _Controller = None
    # color
    _color = u'#C6E89C'
    _color_select = u'#64DBC0'
    _color_preview = u'#FFFFFF'
    # gui text
    _title = u'mp3 organise'

    _details = ["File Name",
                "Album Name",
                "Album Artist",
                "Title",
                "Track Num",
                "Artist"]

    # gui data
    _apply_change_pos = (6, 0)

    # gui elements
    _album_selection = None
    _preview_frame = None
    _frame2 = None
    _selection = None

    def __init__(self, Controller):
        self._Controller = Controller

    def init_gui(self):
        self._root = Tk()
        self._root.title = self._title
        self._root.rowconfigure(1, weight=1)
        self._root.columnconfigure(1, weight=1)

        # TODO fail
        try:
            file_path = saved_input.file_path
        except AttributeError as e:
            file_path = None

        # first column
        frame1 = StandardFrame(self._root)
        frame1.pack(side=LEFT)
        FileInput(frame1, file_path, self._color, self.analyze_files)
        self._selection = StandartSelections(frame1, self._color, self.get_data)
        DownloadInput(frame1, self._color)

        # get data from model
        self._Controller.analyze_files(file_path, False)

        # second column
        self._frame2 = StandardFrame(self._root)
        self._frame2.pack()
        self.get_data(True)  # create preview TODO initializing???
        StandardButton("Apply Change", self._frame2, self._apply_change_callback, 0, 0, self._color).pack()
        # build gui
        self._root.mainloop()

    #### GUI FUNCTIONS ####


    def _create_preview(self, data):

        if self._preview_frame:
            self._preview_frame.destroy()

        self._preview_frame = StandardFrame(self._frame2)
        self._preview_frame.pack(side=LEFT)

        for x in range(len(self._details)):

            frame = StandardFrame(self._preview_frame, 1, 10)
            frame.pack(side=LEFT)

            label = StandardLabel(self._details[x], frame, 0, 0, self._color_preview)
            label.pack(expand=True, fill='both')

            for y in range(len(data)):
                StandardLabel(data[y][x], frame, 0, 0, self._color_preview).pack(expand=True, fill='both')
                if y == 15:
                    break

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
