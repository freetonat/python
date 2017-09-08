import pandas as pd
from pylab import *

ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000',periods=1000))
ts = ts.cumsum()
ts.plot()
show()