import sys

from view.standard_view.standard_frame import StandardFrame
import toga

#class IORedirector:


class StdOutput(toga.Box):
    def __init__(self):
        super().__init__()

        self.label = toga.Label('Nandemo')
        self.add(self.label)

    def start_output(self):
        sys.stdout = self

    def stop_output(self):
        sys.stdout.close()  # ordinary file object
        sys.stdout = sys.__stdout__  # restore print commands to interactive prompt
        print("back to normal")  # this shows up in the interactive prompt

    def write(self, output):
        print("Hi")
        self.label = toga.Label(output)
        self.add(self.label)