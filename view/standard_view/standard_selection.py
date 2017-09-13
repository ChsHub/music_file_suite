from tkinter import IntVar, W, LEFT, TOP

from view.standard_view.standard_frame import StandardFrame
from view.standard_view.standard_radiobutton import StandardRadiobutton


class StandardSelection(StandardFrame):
    radio = None

    def __init__(self, master, radio_enum, get_data):
        super().__init__(master, side=TOP, borderwidth=1, padx=10, pady=10)

        # StandardLabel(title, self, 0, 0, color).pack()
        self._get_data = get_data
        self.radio_values = list(radio_enum)
        self._index = IntVar()

        for i, text in enumerate([s.value for s in radio_enum]):
            b = StandardRadiobutton(self, text=text,
                                    variable=self._index, value=i,
                                    command=lambda: self._get_data(self.radio_values[self._index.get()]))
            b.pack(anchor=W, side=LEFT)
