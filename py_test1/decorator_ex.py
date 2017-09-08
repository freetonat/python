import time

def checkTime(func):
    def newFunc(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print end - start
    return newFunc

@checkTime
def aFunc(maxValue):
    for i in range(1,maxValue+1):
        print i

@checkTime
def bFunc():
    print "This is Function-B"

@checkTime
def cFunc(start, end):
    for i in range(start, end+1):
        print i

class Elapse:
    def __init__(self, f):
        print "initiate Elapse"
        self.func = f
        print(self.func)

    def __call__(self, *args, **kwargs):
        start = time.time()
        self.func(*args, **kwargs)
        end = time.time()
        print "%s : %s - %s = %f" % (self.func.__name__, time.localtime(end).tm_sec, time.localtime(start).tm_sec, end-start)

@Elapse
def eFunc(minValue, maxValue):
    for i in range(minValue, maxValue+1):
        print i
    time.sleep(1)

eFunc(1,19)

def fFunc(maxValue):
    for i in range(0,maxValue):
        print i
    time.sleep(1)

fFunc = Elapse(fFunc)
fFunc(10)
