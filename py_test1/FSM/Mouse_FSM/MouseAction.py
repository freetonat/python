# StateMachine/mouse/MouseAction.py

class MouseAction:
    def __init__(self, action):
        self.action = action
        print("MouseAction self.action = {}".format(self.action))

    def __str__(self):
        print("MouseAction __str__ self.action = {}".format(self.action))
        return self.action

    def __cmp__(self, other):
        print("########## cmp self.action={}, other.action={}".format(self.action, other.action))
        return cmp(self.action, other.action)
    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        print("########### hash")
        return hash(self.action)

# Static fields; an enumeration of instances:
MouseAction.appears = MouseAction("mouse appears")
print("MouseAction={}".format(MouseAction.appears))
MouseAction.runsAway = MouseAction("mouse runs away")
MouseAction.enters = MouseAction("mouse enters trap")
MouseAction.escapes = MouseAction("mouse escapes")
MouseAction.trapped = MouseAction("mouse trapped")
MouseAction.removed = MouseAction("mouse removed")
output = '''
MouseAction self.action = mouse appears
MouseAction __str__ self.action = mouse appears
MouseAction=mouse appears
MouseAction self.action = mouse runs away
MouseAction self.action = mouse enters trap
MouseAction self.action = mouse escapes
MouseAction self.action = mouse trapped
MouseAction self.action = mouse removed
'''
