from logging import info
from multiprocessing import cpu_count
from threading import Thread, BoundedSemaphore, Semaphore


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
class ThreadPoolExecutor:
    #    _Main_view = None
    _Main_model = None
    _Main_view = None
    _threads = []

    def __init__(self, max_workers=100):

        self._queue_sem = BoundedSemaphore(value=1)
        self._empty_sem = BoundedSemaphore(value=max_workers)  # producer
        self._fill_sem = Semaphore(value=0)  # consumer
        self._queue = []

        for i in range(cpu_count()):
            self._create_thread()

    def shutdown(self):

        for thread in self._threads:
            thread.set_active(False)
        for thread in self._threads:
            self.submit(thread.set_active, False)  # TODO remove
            # thread.join()
        info("TERMINATE THREADS")

    # called by view
    def submit(self, *element):
        self._empty_sem.acquire()

        with self._queue_sem:
            self._queue.append(element)  # store moodel procedure

        self._fill_sem.release()

    def _consume(self):
        self._fill_sem.acquire()

        with self._queue_sem:
            method, *element = self._queue.pop(0)  # get stored model procedure

        self._empty_sem.release()

        method(*element)

    def _create_thread(self):
        self._threads += [WorkThread(self._consume)]
