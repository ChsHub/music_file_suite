from tkFileDialog import askopenfilename
from Tkinter import Label
from Tkinter import TkVersion
from Tkinter import LEFT
from Tkinter import *


class View:
    _root = None
    _Model = None
    _file_label = None
    _color = '#C6E89C'

    def __init__(self, Model):
        self._Model = Model

        # self._gui.button("File Open", self.callback)


        # self._gui.button("Klick me too!", self.button_callback)

        # self._gui.listbox(["one", "two", "three"], self.listboxcallback)
        # self._gui.listbox(["A", "B", "C"], self.listboxcallback)
        # self._gui.scale("Scale me!", self.scalecallback)

        root = Tk()
        root.rowconfigure(1, weight=1)
        root.columnconfigure(1, weight=1)

        self._file_label = self._create_label("NONE", 0, 0)
        self._create_button("Open File", 1, 0, self._open_file_callback)
        self._create_button("Apply Change", 1, 1, None)

        self._root = root
        root.mainloop()

    def _create_button(self, text, x, y, callback):
        Button(self._root, width=20, height=2, bg=self._color, padx=10,
               pady=10, text=text, command=callback).grid(column=x, row=y)

    def _create_label(self, text, x, y):
        return Label(self._root, width=50, height=2, bg=self._color, padx=10,
                     pady=10, text=text).grid(row=x, column=y)

    def _open_file_callback(self):
        name = askopenfilename()
        print name
        self._file_label = self._create_label(name, 0, 0)

        #    def listboxcallback(self, text):
        #       self._gui.status("listbox select: '{0}'".format(text))

        #  def scalecallback(self, text):
        #     self._gui.status("scale value: '{0}'".format(text))
