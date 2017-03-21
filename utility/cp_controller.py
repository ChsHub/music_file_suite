from logging import info
from multiprocessing import cpu_count
from threading import Thread, BoundedSemaphore, Semaphore
from model.model import Model
from window import Window

# python 3

# TODO concrete class inherits from cp controller
class WorkThread(Thread):
    _active = True

    def __init__(self, consume):
        Thread.__init__(self)

        self._consume = consume
        self._active = True
        self.start()

    def set_active(self, active):
        info("THREAD  " + str(self) + " INACTIVE")
        self._active = active

    # consume model calls
    def run(self):
        while self._active:
            info("THREAD  " + str(self) + " CONSUME")
            self._consume()
        print("END THREAD")


# uses consumer-producer-problem
# view stores model calls
class Controller:
    #    _Main_view = None
    _Main_model = None
    _Main_view = None
    _threads = []

    def __init__(self, queue_size=100):

        self._queue_sem = BoundedSemaphore(value=1)
        self._empty_sem = BoundedSemaphore(value=queue_size)  # producer
        self._fill_sem = Semaphore(value=0)  # consumer
        self._queue = []

        for i in range(cpu_count()):
            self.create_thread()

        self._Main_model = Model(self)
        self._Main_view = Window(self)
        self._Main_view.start()
        # self._Main_view = None

        for thread in self._threads:
            thread.set_active(False)
        for thread in self._threads:
            self.produce([thread.set_active, False])  # TODO remove
            # thread.join()
        info("TERMINATE THREADS")

    # called by view
    def produce(self, element):
        self._empty_sem.acquire()

        self._queue_sem.acquire()
        self._queue.append(element)  # store moodel procedure
        self._queue_sem.release()

        self._fill_sem.release()

    def _consume(self):
        self._fill_sem.acquire()

        self._queue_sem.acquire()
        element = self._queue.pop(0)  # get stored model procedure
        self._queue_sem.release()

        self._empty_sem.release()

        element.pop(0)(*element) # (*[x, y]) = (x, y)

    def create_thread(self):
        self._threads += [WorkThread(self._consume)]
