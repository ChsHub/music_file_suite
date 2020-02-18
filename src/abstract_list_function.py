class AbstractListFunction:
    _observer = None
    # Notify

    def set_progress(self, id: int, percent: str):
        self._observer.set_progress(id, percent)

    def set_color_ok(self, row: int):
        self._observer.set_color_ok(row)

    def add_line(self, line: list):
        self._observer.add_line(line)

    def update_row(self, data, row):
        self._observer.update_row(data, row)

    def update_cell(self, data, column, row):
        self._observer.update_cell(data, column, row)