import threading

class DallasTasks():
    def start(self):
        try:
            print("testmethod start****")
        except:
            pass

class WorkWrapper():
    def __init__(self, work, name):
        self._work = work
        self._name = name
        self.thread = threading.Thread(target=self.go, name=name)
        print("***** WorkWrapper *****")
        print(self._work)
        print(self._name)

    def start(self):
        print("WorkWrapper start")
        return self.thread.start()

    def go(self):
        try:
            self._work()
            print("work.go")
        except:
            pass

cls = DallasTasks()
fun = getattr(cls, 'start')

workers = WorkWrapper(fun, 'install-dallas')
workers.start()
