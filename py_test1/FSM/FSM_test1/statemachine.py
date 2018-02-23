class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.endStates = []
        self.startState = None

    def add_state(self, name, handler, end_state=0):
        self.handlers[name] = handler
        #print("self.handlers={}".format(self.handlers))
        if end_state:
            self.endStates.append(name)
        #print("self.endStates={}".format(self.endStates))

    def set_start(self, name):
        self.startState = name
        #print("self.startState={}".format(self.startState))

    def run(self, content):
        if self.startState in self.handlers:
            handler = self.handlers[self.startState]
            print("handler={}".format(handler))
        else:
            raise "InitializationError", ".set_start() has to be called before .run()"
        if not self.endStates:
            raise  "InitializationError", "at least one state must be an end_state"

        oldState = self.startState
        while 1:
            (newState, content) = handler(content, oldState)
            print("newState={},content={}".format(newState,content))
            if newState in self.endStates:
                print "reached ", newState, "which is an end state"
                break
            else:
                handler = self.handlers[newState]
            oldState = newState