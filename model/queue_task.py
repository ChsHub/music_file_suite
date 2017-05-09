from collections import deque
from threading import BoundedSemaphore


class QueueTask:
    __queue = []
    __queue_sem = None

    def __init__(self):
        self.__queue = deque([])
        self.__queue_sem = BoundedSemaphore(value=1)

    def add_element(self, element):
        with self.__queue_sem:
            not_empty = len(self.__queue) == 0
            self.__queue.appendleft(element)

        while not_empty:
            self.consume_element(self.__queue[0])

            with self.__queue_sem:
                self.__queue.popleft()
                not_empty = len(self.__queue) != 0

    def consume_element(self, element):
        raise NotImplementedError
