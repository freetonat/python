import pandas as pd
import numpy as np
from pylab import *
import matplotlib.pyplot as pl

df = pd.DataFrame(np.random.randn(1000, 4),index=pd.date_range('1/1/2000', periods=1000),columns=['A', 'B', 'C', 'D'])
df = df.cumsum()
df.rolling(window=60).sum().plot(subplots=True)
show()