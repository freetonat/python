

t = [30,20,10]

result = [j-i for i, j in zip(t[:-1], t[1:])]
print result


t = [30,20,10]
v = [t[i+1]-t[i] for i in range(len(t)-1)]
print v

t = [30,20,10]
v = [t[i]-t[i+1] for i in range(len(t)-1)]
print v