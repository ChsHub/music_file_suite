from standart_selection import StandardSelection
from standard_frame import StandardFrame
from tkinter import TOP
from texts import text_select_title, text_select_options
class StandartSelections:
    selection = None

    def __init__(self, master, color, get_data):

        self.selection = StandardSelection(StandardFrame(master, TOP, padx=0), text_select_title, text_select_options, [True, False], color, get_data)

    def get_is_album(self):
        return self.selection.get_is_album()