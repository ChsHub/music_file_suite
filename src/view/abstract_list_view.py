from src.abstract_list_function import AbstractListFunction
from src.view.standard_view.colors import color_green


class AbstractListView(AbstractListFunction):
    def __init__(self, progress_column):
        AbstractListFunction.__init__(self)
        self._data_list = None
        self.progress_column = progress_column

    @property
    def _observer(self):
        return self._data_list

    # Change view

    def set_progress(self, id, percent):
        self._data_list.update_cell(percent, column=self.progress_column, row=id)

    def set_color_ok(self, row):
        self._data_list.set_row_color(row, color_green)
