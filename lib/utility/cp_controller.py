from logging import info
from multiprocessing import cpu_count
from threading import Thread, BoundedSemaphore, Semaphore
from model.model import Model
from window import Window


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


# python 3
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

        element[0](element[1])

    def create_thread(self):
        self._threads += [WorkThread(self._consume)]

        ## MODEL

    def analyze_files(self, file_path):
        self.produce([self._Main_model.analyze_files, file_path])

    def set_data(self):
        if self._Main_model:
            return self._Main_model.set_data()

    def update_view(self, album_names):
        if self._Main_view:
            self._Main_view.update_view(album_names)

    # called: Model -> Album -> Controller -> Window
    def set_view(self, data):
        if self._Main_view:
            self._Main_view.set_preview_data(data)

    def download(self, url):
        self.produce([self._Main_model.download_file, url])

    def convert_all(self, path):
        self.produce([self._Main_model.convert_file, path])
