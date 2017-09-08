class myTasks():
    print('I am myTasks class')

argss = ( '<.robustness testMethod = test_Robustness >' )

class TaskMapper():
    def __init__(self, args=()):
        self.args = args
        print(self.args)


    def get_object(self, name):
        cls_name = name
        try:
            cls = globals()[cls_name]
            print(cls)



taskmapper = TaskMapper(argss)
taskmapper.get_object(myTasks)