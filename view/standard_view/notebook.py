from tkinter import IntVar, Frame, BOTH, SOLID, BOTTOM, W, X, S, N, E, Grid

from view.standard_view.standard_radiobutton import StandardRadiobutton


# http://flylib.com/books/en/2.9.1.239/1/

class Notebook(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master, relief=SOLID)
        self.active_frame = None
        self.choice = IntVar(0)
        self.buttons_frame = Frame(master, relief=SOLID)
        self.pack(fill=BOTH, side=BOTTOM)
        self.buttons_frame.pack(fill=X, side=BOTTOM, padx=10, pady=10)

    # unpacked frame with master=Notebook, title, callback when frame is swapped
    # pack children of frame before add_screen(...)
    def add_screen(self, frame, title, callback=None):  # TODO Remove choice
        b = StandardRadiobutton(self.buttons_frame, text=title, variable=self.choice,
                                value=len(self.buttons_frame.children), command=lambda: self.display(frame, callback))
        b.grid(row=0, column=len(self.buttons_frame.children), sticky=N + S + E + W)
        Grid.columnconfigure(self.buttons_frame, index=len(self.buttons_frame.children), weight=1)
        Grid.rowconfigure(self.buttons_frame, index=0, weight=1)

        if not self.active_frame:  # if no frame is active yet
            frame.pack(fill=BOTH, expand=True, anchor=W)
            self.active_frame = frame

    def display(self, frame, callback):
        self.active_frame.forget()
        frame.pack(fill=BOTH, expand=True)
        self.active_frame = frame

        if callback:
            callback()
