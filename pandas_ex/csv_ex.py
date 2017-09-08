import pandas as pd
import numpy as np
import openpyxl
import matplotlib.pyplot as pl

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print('<<< df >>>')
print(df)

df.to_csv('csv_test.csv')
xl_df = pd.read_csv('csv_test.csv')
xl_df.to_excel('csv_test.xlsx', sheet_name='sheet1')

xl_rd = pd.read_excel('csv_test.xlsx', 'sheet1', index_col=None, na_values=['NA'])
print(xl_rd)