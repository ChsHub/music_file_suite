from tkinter import TOP, GROOVE
from standard_frame import StandardFrame
from standard_label import StandardLabel
from standard_radio import StandardRadio


class StandardSelection(StandardFrame):
    radio = None

    def __init__(self, master, title, radio_titles, radio_values, color, get_data):
        super().__init__(master, side=TOP, borderwidth=1, padx=10, pady=10)

        StandardLabel(title, self, 0, 0, color).pack()
        self.radio = StandardRadio(self, radio_titles, radio_values, get_data)

    def get_is_album(self):
        return self.radio.get_is_album()
