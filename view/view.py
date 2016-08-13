from tkFileDialog import askopenfilename
from Tkinter import Label
from Tkinter import TkVersion
from Tkinter import LEFT
from Tkinter import *
import logging
import lib.utility.os_interface as os
import resource.saved_input as saved_input


class View:
    _root = None
    _Model = None
    _file_label = None
    _color = '#C6E89C'

    def __init__(self, Model):
        self._Model = Model

        root = Tk()
        root.rowconfigure(1, weight=1)
        root.columnconfigure(1, weight=1)

        # TODO fail
        try:
            file_path = saved_input.file_path
        except AttributeError as e:
            file_path = None

        self._file_label = self._create_label(file_path, 0, 0)
        self._create_button("Open File", 1, 0, self._open_file_callback)
        self._create_button("Apply Change", 1, 1, None)

        self._root = root
        self._Model.analyze_files(file_path)

        root.mainloop()

    #### GUI FUNCTIONS ####

    def _create_button(self, text, x, y, callback):
        Button(self._root, width=20, height=2, bg=self._color, padx=10,
               pady=10, text=text, command=callback).grid(column=x, row=y)

    def _create_label(self, text, x, y):
        return Label(self._root, width=50, height=2, bg=self._color, padx=10,
                     pady=10, text=text).grid(row=x, column=y)

    #### CALLBACK FUNCTIONS ####

    def _open_file_callback(self):
        file_path = askopenfilename()

        logging.info(u"file_path: " + file_path)

        self._file_label = self._create_label(file_path, 0, 0)
        self._save_input(file_path)
        self._Model.analyze_files(file_path)

    #### WRITE FILE ####

    def _save_input(self, file_path):
        data = u"# -*- coding: utf8 -*-\nfile_path = u'" + file_path + u"'"

        os.write_file_data(path=os.get_absolute_path(u"/resource"),
                           file_name=u"saved_input.py", data=data)

        #    def listboxcallback(self, text):
        #       self._gui.status("listbox select: '{0}'".format(text))

        #  def scalecallback(self, text):
        #     self._gui.status("scale value: '{0}'".format(text))
