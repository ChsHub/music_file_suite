from tkFileDialog import askdirectory
from Tkinter import Label
from Tkinter import TkVersion
from Tkinter import LEFT
from Tkinter import *
import logging
import lib.utility.os_interface as os
import resource.saved_input as saved_input
import lib.utility.path_str as path_str
import lib.utility.encoding as encoding


class View:
    _root = None
    _Controller = None
    _color = u'#C6E89C'
    _select_color = u'#64DBC0'
    _title = u'mp3 organise'
    _file_path_saved_input = os.get_absolute_path(u"/resource")

    _apply_change_pos = (4,0)
    _album_selection = None

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

        # first row
        self._create_label_in_grid(file_path, 0, 0)
        self._create_button_in_grid("Open File", 1, 0, self._open_file_callback)
        # third row
        self._create_button_in_grid("Apply Change",
                                    self._apply_change_pos[0],
                                    self._apply_change_pos[1], self._apply_change_callback)

        file_path = encoding.f_encode(file_path)
        self._Controller.analyze_files(file_path)

        self._root.mainloop()

    #### GUI FUNCTIONS ####

    def _create_button(self, text, callback):
        return Button(self._root, width=20, height=2, bg=self._color, padx=10,
                      pady=10, text=text, command=callback)

    def _create_button_in_grid(self, text, x, y, callback):
        self._create_button(text, callback).grid(column=x, row=y)

    def _create_frame_in_grid(self, text, x, y):
        result = Frame(master=self._root, padx=10, pady=10,
                       width=300, height=300)
        result.grid(row=y, column=x)

        self._create_label(text, result, self._select_color).pack()

        return result

    def _create_label_in_grid(self, text, x, y):
        return self._create_label(text, self._root, self._color).grid(row=y, column=x)

    def _create_label(self, text, master, color):
        if not master:
            raise ValueError

        return Label(master=master, width=50, height=2, bg=color, padx=10,
                     pady=10, text=text)

    def _create_radio(self, master, modes):
        if not master:
            raise ValueError

        v = StringVar()
        v.set("L")  # initialize

        i = 0
        for mode in modes:
            b = Radiobutton(master, text=mode,
                            variable=v, value=i)
            b.pack(anchor=W)
            i += 1

    #### SELECTION ####

    def _create_selection(self, names, title, x,y):
        selection_grid = self._create_frame_in_grid(title, x,y)
        self._create_radio(selection_grid, names)

    #### CALLBACK FUNCTIONS ####

    def _apply_change_callback(self):
        raise NotImplementedError

    def _open_file_callback(self):
        album_dir = askdirectory()
        print album_dir
        if album_dir == "":
            return
        album_dir = path_str.get_clean_path(album_dir)

        logging.info(u"album_dir: " + album_dir)

        self._create_label_in_grid(album_dir, 0, 0)
        self._save_input(album_dir)
        self._Controller.analyze_files(album_dir)

    #### WRITE FILE ####

    def _save_input(self, file_path):
        data = u"# -*- coding: utf8 -*-\nfile_path = u'" + file_path + u"'"

        os.write_file_data(path=self._file_path_saved_input,
                           file_name=u"saved_input.py", data=data)

    #### CONTROLLER ####

    def update_view(self, album_names):

        self._create_selection(album_names, "Select Album Name", 0, 1)
        self._create_selection(album_names, "Select Album Artist", 0, 2)
        self._create_selection(album_names, "Select Title", 0, 3)
        self._create_selection(album_names, "Select Track Num", 0, 4)
        self._create_selection(album_names, "Select Artist", 0, 5)

