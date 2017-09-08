import pandas as pd
import numpy as np
import matplotlib.pyplot as pl

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print('<<< df >>>')
print(df)

df2 = pd.DataFrame({ 'A' : 1.,'B' : pd.Timestamp('20130102'),'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                     'D' : np.array([3] * 4,dtype='int32'),'E' : pd.Categorical(["test","train","test","train"]),'F' : 'foo' })
print('<<< df2 >>>')
print(df2)
print("<<< df2.dtypes >>>")
print(df2.dtypes)

print('<<< df.head >>>')
print(df.head(2))
print('<<< df.tail >>>')
print(df.tail(1))
print('<<< df.index >>>')
print(df.index)
print('<<< df.columns >>>')
print(df.columns)
print('<<< df.values >>>')
print(df.values)
print('<<< df.describe >>>')
print(df.describe())
print('<<< df.T >>>')
print(df.T)
print('<<< df.sort_index(axis=1, ascending=False) >>>')
print(df.sort_index(axis=1, ascending=False))
print("<<< df.sort_values(by='B') >>>")
print(df.sort_values(by='B'))
print("<<< df['A'] >>>")
print(df['A'])
print("<<< df[0:3] >>>")
print(df[0:3])
print("<<< df['20130102':'20130104'] >>>")
print(df['20130102':'20130104'])
print("<<< df.loc[dates[0]] >>>")
print(df.loc[dates[0]])
print("<<< df.loc[:,['A','B']] >>>")
print(df.loc[:,['A','B']])
print("<<< df.loc['20130102':'20130104',['A','B']] >>>")
print(df.loc['20130102':'20130104',['A','B']])
print("df.loc[dates[0],'A']")
print(df.loc[dates[0],'A'])
print("<<< df.at[dates[0],'A'] >>>")
print(df.at[dates[0],'A'])