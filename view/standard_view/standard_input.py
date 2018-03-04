from wx import Panel, TextCtrl, Button, BoxSizer, EXPAND, HORIZONTAL, App, Frame, EVT_BUTTON
from wx.grid import Grid
from resource.texts import text_file_input


class StandardInput(Panel):
    _text_input = None
    _callback = None

    def __init__(self, parent, padding=30, width=300, button_text=text_file_input, callback=None):
        super().__init__(parent, EXPAND)

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

        # self.add(toga.Button(button_text, on_press=self.button_callback,  style=CSS())) # TODO open file dialoge
        # self.add(toga.Button(text, on_press=self.button_callback, style=CSS())) # adding width on Button changes row

    def button_callback(self, event):
        self._callback(self._text_input.GetValue())
        self._text_input.value = ""

    def get_input(self):
        return self._text_input.value

if __name__ == "__main__":
    app = App()
    frame = Frame(None, -1, 'win.py')

    StandardInput(frame)

    frame.Show()
    app.MainLoop()
