from tkinter.font import Font
from logging import info
from tkinter import TOP, LEFT, BOTTOM, X, Y, NO
from tkinter.ttk import Treeview, Scrollbar
from meta_data import MetaData
from standard_button import StandardButton
from standard_frame import StandardFrame
from texts import text_preview_change, text_preview_playlist


class Preview(StandardFrame):
    _listbox = None
    preview_frame = None

    def __init__(self, master, data, apply_change_callback):
        super().__init__(master, borderwidth=1, side=TOP)
        self.preview_frame = StandardFrame(self, TOP, pady=0, fill=Y)

        self._listbox = MultiColumnListbox(self.preview_frame, [str(x.value) for x in MetaData], data)
        info("created List bod")
        # CONTROL FRAMES
        button_frame = StandardFrame(self, side=TOP, padx=0, pady=0, fill=X, expand=NO)
        left_button_frame = StandardFrame(button_frame, side=LEFT, padx=0, pady=0, fill=X)
        right_button_frame = StandardFrame(button_frame, side=LEFT, padx=0, pady=0, fill=X)
        # CONTROL
        StandardButton(text_preview_change, left_button_frame, callback=apply_change_callback).pack(side=BOTTOM)
        # TODO Playlist
        StandardButton(text_preview_playlist, right_button_frame, callback=None).pack(side=BOTTOM)

    def update_view(self, data):
        # self._listbox.destroy()
        # self._listbox._build_tree(text_preview_details, data)
        self._listbox.destroy()
        self._listbox = MultiColumnListbox(self.preview_frame, [str(x.value) for x in MetaData], data)


# https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
class MultiColumnListbox(Treeview):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, master, header, data_list):
        super().__init__(columns=header, show="headings")
        self._setup_widgets(master)
        self._build_tree(header, data_list)

    def _setup_widgets(self, master):

        # create a treeview with dual scrollbars
        vsb = Scrollbar(orient="vertical",
                        command=self.yview)
        hsb = Scrollbar(orient="horizontal",
                        command=self.xview)
        self.configure(yscrollcommand=vsb.set,
                       xscrollcommand=hsb.set)
        self.grid(column=0, row=0, sticky='nsew', in_=master)
        vsb.grid(column=1, row=0, sticky='ns', in_=master)
        hsb.grid(column=0, row=1, sticky='ew', in_=master)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

    def _build_tree(self, header, song_list):
        # for i, col in enumerate(header):
        for col in header:
            self.heading(col, text=col, command=lambda c=col: sort_by(self, c, 0))
            # adjust the column's width to the header string
            self.column(col, width=Font().measure(col.title()))

        if not song_list:
            return
        for item in song_list:
            self.insert('', 'end', values=item)

        for col in range(len(header)):
            # adjust column's width if necessary to fit each value
            col_width = 0
            for song in song_list:
                if song[col]:
                    width = Font().measure("i"*len(song[col]))
                    if col_width < width:
                        col_width = width
            self.column(header[col], width=col_width)


def sort_by(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sort_by(tree, col, int(not descending)))
