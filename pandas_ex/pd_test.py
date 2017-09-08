from pandas import Series, DataFrame
import pandas as pd
import numpy as np

data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
frame2 = DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
                   index=['one', 'two', 'three', 'four', 'five'])
print frame2
DataFrame()
print

pop = {'Nevada': {2001: 10, 2002: 20},
       'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}

frame3 = DataFrame(pop)
print frame3
print


aaa = frame2.values
print aaa