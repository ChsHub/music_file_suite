import logging
from Tkinter import *
from tkFileDialog import askdirectory

import lib.utility.encoding as encoding
import lib.utility.os_interface as os
import lib.utility.path_str as path_str
import resource.saved_input as saved_input


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
    _file_path_saved_input = os.get_absolute_path(u"/resource")
    _details = ["File Name",
                   "Album Name",
                   "Album Artist",
                   "Title",
                   "Track Num",
                   "Artist"]
    _options_title = ["Album"]
    _options = [["is Album", "is random"]]
    _options_values = [[True, False]]

    #_options = [["Album", "Sonst"],
     #           ["Meta", "Path"],
      #          ["Meta", "Path"],
       #         ["Meta", "File Name"],
        #        ["Meta", "File Name?", "Playlist"],
         #       ["Meta", "File Name", "Path"]]

    # gui data
    _apply_change_pos = (6, 0)
    _indices = [0]
    # gui elements
    _album_selection = None
    _preview_frame = None
    _frame2 = None
    _file_label = None

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
        frame1 = self._create_frame(self._root)
        frame1.pack(side=LEFT)
        self._create_file_input(frame1, file_path)
        self._create_selections(frame1)

        # get data from model
        file_path = encoding.f_encode(file_path)
        self._Controller.analyze_files(file_path, False)

        # second column
        self._frame2 = self._create_frame(self._root)
        self._frame2.pack()
        self._radio_callback() # create preview
        self._create_button("Apply Change", self._frame2, self._apply_change_callback, 0, 0, self._color).pack()
        # build gui
        self._root.mainloop()

    #### GUI FUNCTIONS ####

    def _create_file_input(self, master, album_dir):
        file_input_frame = self._create_frame(master)
        file_input_frame.pack()
        self._file_label = self._create_label(album_dir, file_input_frame, 0, 0, self._color)
        self._file_label.pack(side=LEFT)
        self._create_button("Open File", file_input_frame, self._open_file_callback, 0, 0, self._color).pack(side=LEFT)

    def _create_frame(self, master, padx=10, pady=10):
        result = Frame(master=master, padx=padx, pady=pady,
                       width=300, height=300)
        return result

    def _create_button(self, text, master, callback, padx, pady, color):
        return Button(master=master, width=20, height=2, bg=color, padx=padx,
                      pady=pady, text=text, command=callback)

    def _create_label(self, text, master, padx, pady, color):
        if not master:
            raise ValueError
        return Label(master=master, height=2, bg=color, padx=padx,
                     pady=pady, text=text, anchor=W)

    def _create_preview(self, data):

        if self._preview_frame:
            self._preview_frame.destroy()

        self._preview_frame = self._create_frame(self._frame2)
        self._preview_frame.pack(side=LEFT)

        for x in range(len(self._details)):

            frame = self._create_frame(self._preview_frame, 1, 10)
            frame.pack(side=LEFT)

            label = self._create_label(self._details[x], frame, 0, 0, self._color_preview)
            label.pack(expand=True, fill='both')

            for y in range(len(data)):
                self._create_label(data[y][x], frame, 0, 0, self._color_preview).pack(expand=True, fill='both')
                if y == 15:
                    break

    def _create_label_packed(self, master, text, padx, pady, color):
        if not master:
            raise ValueError

        b = self._create_label(text, master, padx, pady, color)
        b.pack(anchor=W)

    #### RADIO ####

    def _create_radio(self, master, index):
        if not master:
            raise ValueError

        self._indices[index] = IntVar()
        i = 0
        for mode in self._options[index]:
            b = Radiobutton(master, text=mode,
                            variable=self._indices[index], value=i, command=self._radio_callback)
            b.pack(anchor=W)
            i += 1

    #### SELECTION ####

    def _create_selection(self, title, master, index):
        selection_frame = self._create_frame(master)
        selection_frame.pack()
        self._create_label(title, selection_frame, 0, 0, self._color).pack()
        self._create_radio(selection_frame, index)

    def _create_selections(self, master):


        for y in range(len(self._options_title)):
            self._create_selection(self._options[y], master, y)

    #### CALLBACK FUNCTIONS ####

    def _radio_callback(self):

        data = self._Controller.get_data(self._options_values[0][self._indices[0].get()])
        self._create_preview(data)

    def _apply_change_callback(self):
        self._Controller.set_data(self._options_values[0][self._indices[0].get()])

    def _open_file_callback(self):
        album_dir = askdirectory()

        if album_dir == "":
            return
        album_dir = encoding.f_encode(album_dir)
        album_dir = path_str.get_clean_path(album_dir)

        logging.info("album_dir: " + album_dir)

        self._file_label.config(text=album_dir)
        self._save_input(album_dir)
        self._Controller.analyze_files(album_dir)

    #### WRITE FILE ####

    def _save_input(self, file_path):
        data = "# -*- coding: utf8 -*-\nfile_path = u'" + file_path + "'"

        os.write_file_data(path=self._file_path_saved_input,
                           file_name=u"saved_input.py", data=data)

    #### CONTROLLER ####

    def update_view(self, data):
        # UPDATE Preview
        raise NotImplementedError
