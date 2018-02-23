class Test:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "<Test a:%s b:%s>" % (self.a, self.b)

    def __str__(self):
        return "From str method of Test: a is %s, b is %s" % (self.a, self.b)

    def __hash__(self):
        return hash(100)

t = Test(123, 456)
print(t)
print(repr(t))
print(str(t))
print(hash(t))
print
output = '''
From str method of Test: a is 123, b is 456
<Test a:123 b:456>
From str method of Test: a is 123, b is 456
100
'''
