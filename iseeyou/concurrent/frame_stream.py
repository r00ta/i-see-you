import time
from threading import Lock

class FrameStreamListener:
    def __init__(self):
        self.stream = []
        self.lock = Lock()

    def publish(self, captured_frame):
        with self.lock:
            self.stream.append(captured_frame)

    def pop(self, index = -1):
        with self.lock:
            return self.stream.pop(index)


