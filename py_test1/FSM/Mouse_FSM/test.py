class Singleton(type):
    def __init__(self, name, bases, dict):
        print "init"
        super(Singleton, self).__init__(name, bases, dict)
        self.instance = None

    def __call__(self, *args, **kw):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kw)

        return self.instance

class MyClass(object):
    __metaclass__ = Singleton

print MyClass()
print MyClass()