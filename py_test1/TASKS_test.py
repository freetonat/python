TASKS = [
    ('configure node',),

    ('install node',),
    ('install dallas',),

    ('reload outline', 'install dallas'),
    ('reload node', 'install node', 'configure node'),

    ('reload dallas', 'install dallas'),
    ('reload snmp', 'install dallas'),
    ('reload lns', 'install dallas'),
    ('reload mcd', 'install dallas'),
    ('reload cgf', 'install dallas'),
    ('reload diameter', 'install dallas'),
    ('reload dhcp', 'install dallas'),
    ('reload radius', 'install dallas'),
    ('reload dns', 'install dallas'),

    ('configure outline', 'reload outline',),
    ('configure snmp', 'reload snmp'),
    ('configure diameter', 'reload diameter'),
    ('configure dallas', 'reload dallas'),
    ('configure lns', 'reload lns'),
    ('configure mcd', 'reload mcd'),
    ('configure cgf', 'reload cgf'),
    ('configure dhcp', 'reload dhcp'),
    ('configure radius', 'reload radius'),
    ('configure dns', 'reload dns'),

    ('start outline', 'configure outline', 'configure snmp',
     'configure lns', 'configure mcd', 'configure cgf', 'configure diameter',
     'configure radius', 'configure dns'),
    ('start mcd', 'start outline'),
    ('start diameter', 'start mcd'),
    ('start cgf', 'start diameter'),
    ('start lns', 'start cgf'),
    ('start dns', 'start lns'),
    ('start dhcp', 'start lns', 'start dns'),
    ('start radius', 'start dhcp'),
    ('start snmp', 'start radius'),
    ('start node', 'reload node', 'start radius'),
    ('start ixia', 'start node'),
    ('start dallas', 'configure dallas', 'start node'),
    ('start testmethod', 'start outline', 'start mcd', 'start dns',
     'start diameter', 'start cgf', 'start lns', 'start dhcp', 'start radius',
     'start node', 'start ixia', 'start dallas'),

    ('stop ixia', 'start testmethod'),
    ('stop dallas', 'stop ixia'),
    ('stop lns', 'start testmethod'),
    ('stop snmp', 'start testmethod'),
    ('stop diameter', 'start testmethod'),
    ('stop cgf', 'start testmethod'),
    ('stop dhcp', 'start testmethod'),
    ('stop radius', 'start testmethod'),
    ('stop dns', 'start testmethod'),
    ('stop mcd', 'start testmethod', 'stop snmp', 'stop diameter', 'stop cgf', 'stop dhcp', 'stop radius', 'stop dns'),
    ('stop outline', 'start testmethod', 'stop snmp', 'stop diameter', 'stop cgf', 'stop dhcp', 'stop radius', 'stop dns'),
    ('stop node', 'stop dallas'),

    ('getlog node',),
    ('getlog dallas',),
    ('getlog outline',),

    ('clearlog node', 'getlog node'),
    ('clearlog dallas', 'getlog dallas'),
    ('clearlog outline', 'getlog outline'),
]

ALIASES = {
    'go': ["install", "reload", "configure", "start", "stop"],
    'go_css': ["configure", "start", "stop"]}


class Task(object):

    def __init__(self, name, *depends):
        #print('## class Task name = %s, depends = %s' %(name, depends))
        self.name = name
        self.deps = set(depends)

    def add_deps(self, *deps):
        self.deps = set(list(self.deps) + list(deps))

    def mark_done(self, name):
        #print('mark_done.name = {}'.format(name))
        try:
            self.deps.remove(name)
        except KeyError:
            pass

    def __str__(self):
        return self.name

class TaskPool(object):

    def __init__(self):
        self.tasks = []

    def add(self, name, *depends):
        self.tasks.append(Task(name, *depends))

    def contains(self, pattern):
        for name in [t.name for t in self.tasks]:
            if name.count(pattern):
                return True

    def is_empty(self):
        """Return True if the pool empty."""
        return len(self.tasks) == 0

    def mark_done(self, done):
        #print('done = {}'.format(done))
        """Mark task as done, removing it from pool."""
        if type(done) == str:
            tasks = [t for t in self.tasks if t.name.count(done)]
            #print('tasks_1 = {}'.format(tasks))
        else:
            tasks = [done]
        for done in tasks:
            #print('done1 = {}'.format(done))
            if done not in self.tasks:
                raise ValueError("Unknown task: %r" % done)
            self.tasks.remove(done)
            #print('self.taks.remove = {}'.format(self.tasks))
            for task in self.tasks:
                if done.name not in task.deps:
                    continue
                task.mark_done(done.name)
                task.add_deps(*done.deps)

    def get_final_task_list(self):
        tasks = []
        for act, attr in [t.name.split(" ") for t in self.tasks]:
            tasks.append(" ".join([act, attr]))
        return tasks

    def format_tasks(self):
        actions = []
        tmap = {}
        for act, attr in [t.name.split(" ") for t in self.tasks]:
            if attr != 'pre':
                if tmap.get(act):
                    tmap[act].append(attr)
                else:
                    tmap[act] = [attr]
            actions.append(act)
        info = []
        num = 0
        seen = set()
        for act in actions:
            if act in seen:
                continue
            else:
                seen.add(act)
            num += 1
            attrs = ", ".join(tmap[act])
            info.append("action %s %-9s - %s" % (num, act, attrs))
        return info

class TaskPoolGraph(TaskPool):

    def _get_name_to_deps(self):
        return dict((n.name, set(n.deps)) for n in self.tasks)

    def _get_task_batches(self):
        name_to_instance = dict((n.name, n) for n in self.tasks)
        name_to_deps = self._get_name_to_deps()
        batches = []
        while name_to_deps:
            ready = {n for n, dep in name_to_deps.iteritems() if not dep}
            if not ready:
                msg = "Circular dependencies found\n"
                msg += self.format_dependencies(name_to_deps)
                raise ValueError(msg)
            for name in ready:
                del name_to_deps[name]
            for deps in name_to_deps.itervalues():
                deps.difference_update(ready)
            batches.append({name_to_instance[name] for name in ready})
        return batches

    def get_tasks(self):
        try:
            return list(self._get_task_batches()[0])
        except IndexError:
            return []

class TaskPoolHandler(object):
    def __init__(self, taskpool, tasks=None):
        if not tasks:
            tasks = TASKS[:]
        self.taskpool = taskpool
        self.tasks = tasks
        self.next_action = None
        self.attributes = None

    def is_valid_action(self, action):
        return action in [t[0].split(" ")[0] for t in self.tasks]

    @staticmethod
    def is_valid_task(action, attr):
        if attr in ['all', 'not']:
            return True
        task = "%s %s" % (action, attr)
        return task in [t[0] for t in TASKS]

    def add_tasks(self, action, attrs):
        print(action, attrs)
        for attr in attrs:
            name = "%s %s" % (action, attr)
            ts = [t for t in self.tasks if name == t[0]]
            if not ts:
                raise ValueError("Invalid task: %s" % name)
            for t in ts:
                self.tasks.remove(t)

    def get_all(self, action):
        attrs = []
        for t in self.tasks:
            act, attr = t[0].split(" ")
            if action == act:
                attrs.append(attr)
        return remove_duplicates(attrs)

    def finalize(self):
        for t in self.tasks:
            self.taskpool.mark_done(t[0])
        self.tasks = None
        return self.taskpool

class CLITaskParser(object):
    def __init__(self, tph, aliases=None):
        if aliases is None:
            aliases = ALIASES
        self.tph = tph
        self.aliases = aliases
        self.in_invert = False

    def lookup_alias(self, args):
        for alias, result in self.aliases.iteritems():
            if alias in args:
                if len(args) > 1:
                    raise E.SetupError("Alias can only be used by itself: %s" % alias)
                return result
        return args

    def add_action(self, action, attrs, invert_attrs):
        if attrs == 'all' or attrs == []:
            attrs = self.tph.get_all(action)
        if invert_attrs:
            if invert_attrs == 'all':
                return
            attrs = filter(lambda x: x not in invert_attrs, attrs)
        try:
            self.tph.add_tasks(action, attrs)
        except ValueError:
            raise E.SetupError("Invalid action: %s %s" % (action, " ".join(attrs)))

    def parse(self, args):
        self.in_invert = False
        args = self.lookup_alias(args)
        action = None
        invert = False
        attrs = []
        invert_attrs = []
        for arg in [a.lower() for a in args]:
            if arg == "not" or arg == "except":
                if invert:
                    raise E.SetupError("Can only give 'not' once per action")
                invert = True
            elif arg == "all":
                if invert:
                    invert_attrs = 'all'
                else:
                    attrs = 'all'
            elif self.tph.is_valid_action(arg):
                if action is not None:
                    self.add_action(action, attrs, invert_attrs)
                action = arg
                print('action = {}'.format(action))
                attrs = []
                invert_attrs = []
                invert = False
            elif self.tph.is_valid_task(action, arg):
                if invert:
                    invert_attrs.append(arg)
                else:
                    attrs.append(arg)
            else:
                raise E.SetupError("Invalid action or attribute: %s" % arg)
        self.add_action(action, attrs, invert_attrs)

def remove_duplicates(seq, idfun=None):
    """Remove duplicates from list."""
    if idfun is None:
        # pylint: disable=E0102
        def idfun(x):
            return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result

def get_task_pool(warp=True):
    if warp:
        tm = TaskPoolGraph()
    for t in TASKS:
        tm.add(*t)
    return tm

#rest = ['configure', 'install', 'reload', 'start', 'not', 'testmethod']
rest = ["install", "reload", "configure", "start", "stop"]

tp = get_task_pool()
taskpool_handler = TaskPoolHandler(tp)
cli_parser = CLITaskParser(taskpool_handler)
cli_parser.parse(rest)
taskpool_handler.finalize()
command_list = tp.get_final_task_list()
for line in tp.format_tasks():
    print line
rest = tp.contains('install')
print rest
for task in tp.get_tasks():
    print task