import sys
from tkinter import TOP, YES, X

from standard_view.standard_frame import StandardFrame
from standard_view.standard_label import StandardLabel


class StdOutput(StandardFrame):
    def __init__(self, master):
        super().__init__(master, TOP, borderwidth=1)

        self.label = StandardLabel('', self).pack(expand=YES, fill=X)

    def start_output(self):
        self.temp = sys.stdout  # store original stdout object for later
        sys.stdout = self.create_label

    def stop_output(self):
        sys.stdout.close()  # ordinary file object
        sys.stdout = self.temp  # restore print commands to interactive prompt
        print("back to normal")  # this shows up in the interactive prompt

    def create_label(self, output):
        self.label = StandardLabel('', self).pack(expand=YES, fill=X)
