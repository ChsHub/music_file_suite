from tkinter import IntVar, Radiobutton, W, LEFT


class StandardRadio:
    _index = None
    _get_data = None
    radio_values = None

    def __init__(self, master, radio_titles, radio_values, get_data):

        if not master:
            raise ValueError

        self._get_data = get_data
        self.radio_values = radio_values
        self._index = IntVar()

        for i in range(len(radio_titles)):
            b = Radiobutton(master, text=radio_titles[i],
                            variable=self._index, value=i, command=self._radio_callback, indicatoron=0)
            b.pack(anchor=W, side=LEFT)

    #### CALLBACK ####

    def _radio_callback(self):
        result = self.radio_values[self._index.get()]
        self._get_data(result)
