class AbstractListFunction:
    _observer = None

    # Notify

    def set_progress(self, row: int, percent: str):
        self._observer.set_progress(row, percent)

    def set_color_ok(self, row: int):
        self._observer.set_color_ok(row)

    def set_color_normal(self, row: int):
        self._observer.set_color_normal(row)

    def set_color_warning(self, row: int):
        self._observer.set_color_warning(row)

    def add_line(self, line: list):
        self._observer.add_line(line)

    def update_row(self, data: list, row: int):
        self._observer.update_row(data, row)

    def update_cell(self, data: list, column: int, row: int):
        self._observer.update_cell(data, column, row)
