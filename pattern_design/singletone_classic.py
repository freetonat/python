class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class Child(Singleton):
    pass

singletone = Singleton()
print singletone
another_singletone = Singleton()
print singletone

singletone.only_one_var = "I'm only one var"
print singletone.only_one_var
print another_singletone.only_one_var
child = Child()
print child
print child.only_one_var