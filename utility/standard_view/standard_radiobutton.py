from tkinter import Radiobutton

from colors import color_button


class StandardRadiobutton(Radiobutton):
    def __init__(self, master, text, variable, value, command, color=color_button, padx=0, pady=0):
        super().__init__(master=master,
                         width=20,
                         height=2,
                         bg=color,
                         padx=padx,
                         pady=pady,
                         text=text,
                         command=command,
                         variable=variable,
                         value=value,
                         indicatoron=0)
