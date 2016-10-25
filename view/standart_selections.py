from standart_selection import StandartSelection


class StandartSelections:
    selection = None

    def __init__(self, master, color, get_data):
        self.selection = StandartSelection(master, "Album", ["is Album", "is random"], [True, False], color, get_data)

    def get_is_album(self):
        return self.selection.get_is_album()