from tkinter import LEFT, IntVar, Frame, BOTH, RIDGE, Radiobutton, TOP


# http://flylib.com/books/en/2.9.1.239/1/

class Notebook(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master, borderwidth=2, relief=RIDGE)
        self.active_frame = None
        self.choice = IntVar(0)
        self.buttons_frame = Frame(master, borderwidth=2, relief=RIDGE)
        self.buttons_frame.pack(side=TOP, fill=BOTH)
        self.pack(fill=BOTH, side=TOP)

    # unpacked frame with master=Notebook, title, callback when frame is swapped
    # pack children of frame before add_screen(...)
    def add_screen(self, frame, title, callback=None):
        Radiobutton(self.buttons_frame, text=title, indicatoron=0, variable=None,
                    value=len(self.buttons_frame.children), command=lambda: self.display(frame, callback)
                    ).pack(fill=BOTH, side=LEFT)
        if not self.active_frame:  # if no frame is active yet
            frame.pack(fill=BOTH, expand=1)
            self.active_frame = frame

    def display(self, frame, callback):
        self.active_frame.forget()
        frame.pack(fill=BOTH, expand=1)
        self.active_frame = frame

        if callback:
            callback()
