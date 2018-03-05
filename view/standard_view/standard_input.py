from logging import error

from wx import Panel, TextCtrl, Button, BoxSizer, EXPAND, HORIZONTAL, App, Frame, EVT_BUTTON

from resource.texts import text_file_input


class StandardInput(Panel):
    _text_input = None
    _callback = None

    def __init__(self, parent, callback, padding=30, width=300, button_text=text_file_input):
        super().__init__(parent, EXPAND)

        if not callback:
            error("callback is none")
            return

        self._callback = callback
        sizer = BoxSizer(HORIZONTAL)
        # create input and add to sizer
        self._text_input = TextCtrl(self, -1, size=(50, 22))
        sizer.Add(self._text_input, EXPAND)
        # create button, bind callback and add to sizer
        button = Button(self, -1, size=(100, 22), label=button_text)
        button.Bind(EVT_BUTTON, self.button_callback)
        sizer.Add(button)

        self.SetSizer(sizer)

    def button_callback(self, event):
        self._callback(self._text_input.GetValue())
        self._text_input.SetValue("")

    def get_input(self):  # TODO Alternative Implementation / Refactor Window
        return self._text_input.GetValue()


if __name__ == "__main__":
    app = App()
    frame = Frame(None, -1, 'win.py')

    StandardInput(frame, lambda x: x)

    frame.Show()
    app.MainLoop()
