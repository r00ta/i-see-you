from threading import Lock

class CancellationToken:
    def __init__(self, value):
        self.value = value
        self.lock = Lock()

    def set(self, value):
        self.value = value

    def get(self):
        return self.value
