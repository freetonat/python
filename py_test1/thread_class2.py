import time
import threading

class AAA(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        for i in range(1, 100):
            print(self.url)
            time.sleep(4)
