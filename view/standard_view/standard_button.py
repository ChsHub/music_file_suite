from wx import Button, EVT_BUTTON

from view.standard_view.colors import color_button


class StandardButton(Button):
    def __init__(self, parent, text, callback, color=color_button, style=None):
        super().__init__(parent, label=text)
        self.Bind(EVT_BUTTON, callback)
