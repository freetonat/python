a = [ '1 2 3', '4 5 6', '7 8 9']
b = [ [int(y) for y in x.split()] for x in a]
b[0] # [1,2,3]
sum(b[0])
c = [sum(x) for x in b]
sum(c)