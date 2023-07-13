import queue
from threading import Thread


class CustomThread(Thread):
    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None
    ):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


class ThreadStarter:
    def __init__(self, threads):
        self.threads = threads
        self.results = []

    def start(self):
        result_queue = queue.Queue()

        # Start the threads
        for thread in self.threads:
            thread.start()

        # Wait for the threads to finish
        for thread in self.threads:
            result_queue.put(thread.join())

        # Get the returned values
        while not result_queue.empty():
            result = result_queue.get()
            self.results.append(result)
