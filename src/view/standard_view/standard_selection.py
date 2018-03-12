from wx import ComboBox, CB_DROPDOWN, CB_READONLY, EVT_TEXT, Panel, StaticText, BoxSizer, VERTICAL


class StandardSelection(Panel):
    def __init__(self, parent, callback, title, radio_enum):
        super().__init__(parent)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(StaticText(self, label=title))
        self.selection = ComboBox(self, style=CB_DROPDOWN | CB_READONLY,
                                  choices=[choice.value for choice in radio_enum])
        self.selection.SetValue(list(radio_enum)[0].value)
        if callback:
            self.selection.Bind(EVT_TEXT, lambda x: callback(self.selection.GetValue()))
        sizer.Add(self.selection)
        self.SetSizer(sizer)

    def get_selection(self):
        return self.selection.GetValue()
