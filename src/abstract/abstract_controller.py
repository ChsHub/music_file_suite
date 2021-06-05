from concurrent.futures.thread import ThreadPoolExecutor
from logging import exception

from src.abstract.abstract_list_function import AbstractListFunction


class AbstractController(AbstractListFunction):

    def __init__(self, view):
        AbstractListFunction.__init__(self)
        self._executor = ThreadPoolExecutor()
        self._view = view

    def _submit(self, *args):
        future = self._executor.submit(*args)
        # called after execution of this task
        future.add_done_callback(self.error_log)

    @staticmethod
    def error_log(future):
        # returns None if no exception occurred
        result = future.exception()
        if result:
            exception(result)

    @property
    def _observer(self):
        return self._view
