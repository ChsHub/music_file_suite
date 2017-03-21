from logging import info
from tkinter import Tk

from colors import color_button
from column import Column
from convert_input import ConvertInput
from download_input import DownloadInput
from file_input import FileInput
from notebook import Notebook
from preview import Preview
from standard_selection import StandardSelection
from std_output import StdOutput
from texts import text_view_title, Selection


# TODO more Feedback (Apply change, convert, download, ect.)
# TODO Strech Window

class Window:
    # class
    _root = None
    _Controller = None
    # gui elements
    _album_selection = None
    _preview = None
    _selection = None

    def __init__(self, controller):
        self._Controller = controller
        self._root = Tk()
        self._root.title(text_view_title)
        # self._root = StandardFrame(self._root, side=LEFT, fill=BOTH)
        self.outer_comlumn = Column(self._root, pady=0, padx=0)
        self.outer_comlumn.pack()

        self.notebook = Notebook(self.outer_comlumn.get_parent())

        # column
        column2 = Column(self.notebook)
        column3 = Column(self.notebook)
        column1 = Column(self.notebook)
        # Column 1
        self._preview = Preview(column1.get_parent(), None, self._apply_change_callback)
        StandardSelection(column1.get_parent(), Selection, controller.update_view)
        StdOutput(column1.get_parent())
        # Column 2
        self._preview = Preview(column2.get_parent(), None, self._apply_change_callback)
        DownloadInput(column2.get_parent(), color_button, self._Controller.download)
        # Column 3
        self._preview = Preview(column3.get_parent(), None, self._apply_change_callback)
        ConvertInput(column3.get_parent(), color_button, self._Controller.convert_all)

        self.notebook.add_screen(column1, "Meta")
        self.notebook.add_screen(column2, "Download")
        self.notebook.add_screen(column3, "Convert")
        FileInput(self.outer_comlumn.get_parent(), color_button, self.analyze_files).pack(padx=10, pady=10)

    def start(self):
        self._root.mainloop()
        info("WINDOW CLOSED")

    #### GUI FUNCTIONS ####

    def _create_preview(self, data):
        info("CREATE preview")
        self._preview.update_view(data)

    #### CALLBACK ####

    def _apply_change_callback(self):
        self._Controller.set_data()

    #### CONTROLLER ####
    def analyze_files(self, album_dir):
        self._Controller.analyze_files(album_dir)

    def set_preview_data(self, data):
        self._create_preview(data)
