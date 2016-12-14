import tkinter.font as tkFont
from tkinter import TOP, LEFT
from tkinter.ttk import Treeview, Scrollbar

from standard_button import StandardButton
from standard_frame import StandardFrame
from texts import text_preview_details, text_preview_change, text_preview_playlist


class Preview(StandardFrame):
    def __init__(self, master, data, apply_change_callback):
        super().__init__(master, side=TOP)

        preview_border_frame = StandardFrame(self, TOP, borderwidth=1)
        preview_frame = StandardFrame(preview_border_frame, TOP, pady=0)

        if not data:
            return

        self.listbox = MultiColumnListbox(preview_frame, text_preview_details, data)

        # CONTROL FRAMES
        button_frame = StandardFrame(preview_border_frame, side=TOP, padx=0, pady=0)
        left_button_frame = StandardFrame(button_frame, side=LEFT, padx=0, pady=0)
        right_button_frame = StandardFrame(button_frame, side=LEFT, padx=0, pady=0)
        # CONTROL
        StandardButton(text_preview_change, left_button_frame, apply_change_callback, 0, 0).pack(side=TOP)
        StandardButton(text_preview_playlist, right_button_frame, None, 0, 0).pack(side=TOP)

    def scroll_callback(self, scroll, step):
        print(scroll)

    def update_view(self, data):
        self.listbox._build_tree(text_preview_details, data)


# https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
class MultiColumnListbox(Treeview):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, master, car_header, car_list):
        super().__init__(columns=car_header, show="headings")
        self._setup_widgets(master)
        self._build_tree(car_header, car_list)

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
        for col in header:
            self.heading(col, text=col.title(),
                         command=lambda c=col: sortby(self, c, 0))
            # adjust the column's width to the header string
            self.column(col, width=tkFont.Font().measure(col.title()))

        for item in song_list:
            self.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.column(header[ix], width=None) < col_w:
                    self.column(header[ix], width=col_w)


def sortby(tree, col, descending):
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
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))
