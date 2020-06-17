from queue import Queue

class MainThreadQueue:
    queue = Queue()
    instance = None

    # This is a singleton, since there is only 1 main thread
    def __new__(cls, *args, **kwargs) -> None:
        if not cls.instance:
            cls.instance = super(MainThreadQueue, cls).__new__(cls, *args, **kwargs)

        return cls.instance

    def register(self, callback):
        self.queue.put(callback)
    
    def execute(self):
        callback = self.queue.get()
        callback()
