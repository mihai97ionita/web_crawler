import concurrent


class FutureCollector:

    def __init__(self):
        self.futures = []

    def collect(self, new_futures):
        try:
            iter(new_futures)
            self.futures.extend(new_futures)
        except TypeError as te:
            self.futures.append(new_futures)

    def wait_all(self):
        concurrent.futures.wait(self.futures)
