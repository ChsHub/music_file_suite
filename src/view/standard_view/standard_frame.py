import toga
from src.view.standard_view.colors import color_background
from colosseum import CSS


class StandardFrame(toga.Box):
    def __init__(self, style=CSS(padding=0, margin=0)):
        super().__init__(style=style)
