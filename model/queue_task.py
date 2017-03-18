from threading import BoundedSemaphore


class QueueTask:
    __queue = []
    __queue_sem = None

    def __init__(self):
        self.__queue = []
        self.__queue_sem = BoundedSemaphore(value=1)

    def add_element(self, element):

        self.__queue_sem.acquire()
        not_empty = self.__queue == []
        self.__queue.append(element)
        self.__queue_sem.release()


        while not_empty:
            self.consume_element(self.__queue[0])

            self.__queue_sem.acquire()
            self.__queue.pop(0)
            not_empty = self.__queue != []
            self.__queue_sem.release()


    def consume_element(self, element):
        raise NotImplementedError
