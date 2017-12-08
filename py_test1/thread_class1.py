import test1
import time


class BBB():
    def bbb(self):
        t = test1.AAA('http://google.com')
        t.start()
        for i in range(1, 5):
            print("bbb")
            time.sleep(2)


bbb = BBB()
bbb.bbb()


print("### End ###")