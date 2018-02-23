# StateMachine/mousetrap1/MouseTrapTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
import string
import sys

sys.path += ['../stateMachine', '../mouse']
from py_test1.FSM.Mouse_FSM.State import State
from py_test1.FSM.Mouse_FSM.StateMachine import StateMachine
from py_test1.FSM.Mouse_FSM.MouseAction import MouseAction
# A different subclass for each state:

class Waiting(State):
    print("Class waiting")
    def run(self):
        print("Waiting: Broadcasting cheese smell")

    def next(self, input):
        if input == MouseAction.appears:
            print("##############")
            print("class waiting input={}, MouseAction.appears={}".format(input,MouseAction.appears))
            print("##############")
            return MouseTrap.luring
        return MouseTrap.waiting

class Luring(State):
    def run(self):
        print("Luring: Presenting Cheese, door open")

    def next(self, input):
        if input == MouseAction.runsAway:
            return MouseTrap.waiting
        if input == MouseAction.enters:
            return MouseTrap.trapping
        return MouseTrap.luring

class Trapping(State):
    def run(self):
        print("Trapping: Closing door")

    def next(self, input):
        if input == MouseAction.escapes:
            return MouseTrap.waiting
        if input == MouseAction.trapped:
            return MouseTrap.holding
        return MouseTrap.trapping

class Holding(State):
    def run(self):
        print("Holding: Mouse caught")

    def next(self, input):
        if input == MouseAction.removed:
            return MouseTrap.waiting
        return MouseTrap.holding

class MouseTrap(StateMachine):
    def __init__(self):
        print("MouseTrap.init")
        # Initial state
        StateMachine.__init__(self, MouseTrap.waiting)

# Static variable initialization:
MouseTrap.waiting = Waiting()
print("MouseTrap.waiting={}".format(MouseTrap.waiting))
MouseTrap.luring = Luring()
MouseTrap.trapping = Trapping()
MouseTrap.holding = Holding()

moves = map(string.strip,
  open("./MouseMoves.txt").readlines())
print("moves={}".format(moves))
#MouseTrap().runAll(map(MouseAction, moves))
testaaa = MouseTrap()
listaaa = (map(MouseAction, moves))
print("listaaa={}".format(listaaa))
testaaa.runAll(listaaa)

output = '''
MouseAction self.action = mouse appears
MouseAction __str__ self.action = mouse appears
MouseAction=mouse appears
MouseAction self.action = mouse runs away
MouseAction self.action = mouse enters trap
MouseAction self.action = mouse escapes
MouseAction self.action = mouse trapped
MouseAction self.action = mouse removed
Class waiting
MouseTrap.waiting=<__main__.Waiting object at 0x010A0BB0>
'''
