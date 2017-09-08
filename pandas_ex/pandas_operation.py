import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

dates = pd.date_range('20170101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print('<<< df >>>')
print(df)
#print(df.mean(1))
s = pd.Series([1,3,5,np.nan,6,8], index=dates).shift(2)
print s
print df.sub(s, axis = 'index')
print
print df.apply(np.cumsum)
