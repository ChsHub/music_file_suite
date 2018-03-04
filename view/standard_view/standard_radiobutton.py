#import toga.optioncontainer as Radiobutton
from colosseum import CSS
from view.standard_view.colors import color_button


class StandardRadiobutton(Radiobutton):
    def __init__(self, master, text, variable, value, command, color=color_button, padx=0, pady=0):
        super().__init__(style=CSS(padding=padx))
                         #width=20,
                         #height=2,
                         #bg=color,
                         #padx=padx,
                         #pady=pady,
                         #text=text,
                         #c#ommand=command,
                         #variable=variable,
                         #value=value,
                         #indicatoron=0)
        master.add(self)