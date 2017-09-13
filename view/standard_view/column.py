import toga
from colosseum import CSS
from view.standard_view.colors import color_background
from view.standard_view.standard_frame import StandardFrame


class Column(toga.Box):
    def __init__(self, master, padding=10):
        super().__init__(style=CSS(flex_direction='column', padding=padding))
        master.add(self)
