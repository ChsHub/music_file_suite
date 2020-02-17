from concurrent.futures.thread import ThreadPoolExecutor
from logging import exception


class GenericController:

    def __init__(self):
        self._executor = ThreadPoolExecutor()

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
