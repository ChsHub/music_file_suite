from wx import ComboBox, CB_DROPDOWN, CB_READONLY, EVT_TEXT, Panel, StaticText, BoxSizer, VERTICAL
from enum import EnumMeta


class StandardSelection(Panel):
    def __init__(self, parent, callback, title, choices):
        super().__init__(parent)

        sizer = BoxSizer(VERTICAL)
        sizer.Add(StaticText(self, label=title))

        # TODO remove the ENUMS
        if type(choices) == EnumMeta:
            self.selection = ComboBox(self, style=CB_DROPDOWN | CB_READONLY,
                                      choices=[choice.value for choice in choices])
            self.selection.SetValue(list(choices)[0].value)
        else:
            self.selection = ComboBox(self, style=CB_DROPDOWN | CB_READONLY,
                                      choices=choices)

            self.selection.SetValue(choices[0])

        if callback:
            self.selection.Bind(EVT_TEXT, lambda x: callback(self.selection.GetValue()))
        sizer.Add(self.selection)
        self.SetSizer(sizer)

    def get_selection(self):
        return self.selection.GetValue()
