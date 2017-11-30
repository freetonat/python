class Borg(object):
    _shared_state = {}
    def __new__(cls, *args, **kwargs):
        obj = super(Borg, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

class Child(Borg):
    pass

borg = Borg()
print borg
anotherborg = Borg()
print anotherborg
child = Child()
print child
borg.only_one_var = "I'm the only one var"
print anotherborg.only_one_var
print child.only_one_var