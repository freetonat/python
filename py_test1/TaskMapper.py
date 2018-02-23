import sys, os

class NodeTasks():
    def __init__(self, args):
        self.args = args
        print('self.args = {}'.format(self.args))

    def install(self):
        print('NodeTasks.install')

class TaskMapper():
    def __init__(self):
        pass

    def get_obj(self, nodetasks):
        cls_name = nodetasks
        cls = globals()[cls_name]
        print('cls = {}'.format(cls))
        obj = cls('Hi')
        print('obj = {}'.format(obj))
        return obj

    def get_task(self):
        action = 'install'
        return getattr(self.get_obj('NodeTasks'), action)

taskmapper =  TaskMapper()
task = taskmapper.get_task()
print('task = {}'.format(task))
task()output = '''
cls = <class '__main__.NodeTasks'>
self.args = Hi
obj = <__main__.NodeTasks object at 0x00606330>
task = <bound method NodeTasks.install of <__main__.NodeTasks object at 0x00606330>>
NodeTasks.install
'''
