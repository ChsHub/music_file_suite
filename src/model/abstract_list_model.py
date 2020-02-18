from src.abstract_list_function import AbstractListFunction


class AbstractListModel(AbstractListFunction):
    def __init__(self, controller):
        AbstractListFunction.__init__(self)
        self._controller = controller

    @property
    def _observer(self):
        return self._controller
