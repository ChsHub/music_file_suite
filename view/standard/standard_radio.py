from tkinter import IntVar, Radiobutton, W, LEFT


class StandardRadio:
    _index = None
    get_data = None
    radio_values = None

    def __init__(self, master, radio_titles, radio_values, get_data):

        if not master:
            raise ValueError

        self.get_data = get_data
        self.radio_values = radio_values
        self._index = IntVar()

        for i in range(len(radio_titles)):
            b = Radiobutton(master, text=radio_titles[i],
                            variable=self._index, value=i, command=self._radio_callback, indicatoron=0)
            b.pack(anchor=W, side=LEFT)

    #### CALLBACK ####

    def _radio_callback(self):
        self.get_data(self.get_is_album())

    def get_is_album(self):
        return self.radio_values[self._index.get()]
