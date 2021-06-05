class AbstractConverter:
    def __init__(self, parent):
        self._parent = parent

    def set_time(self, row, column, new_data):
        self._parent.set_time(row, column, new_data)