
class TaskMapper():
    def __init__(self, args=()):
        self.args = args
        print(self.args)

    def get_object(self, name):
        cls_name = name.capitalize()+'Tasks'
        print(cls_name)
        try:
            cls = globals()[cls_name]
            print(cls)
        except KeyError:
            pass

class DallasTasks():
    def dallasprint(self):
        print('dallasprint')

class AAA():
    def aaa(self):
        print("aaa")


task = TaskMapper()
task.get_object('dallas')



