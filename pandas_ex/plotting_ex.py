from pylab import *

x = range(0, 100)
y = [v*v for v in x]
plt.plot(x, y, 'ro')
show()
