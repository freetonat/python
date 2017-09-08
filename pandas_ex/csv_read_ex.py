import pandas as pd
import numpy as np
import re
import sys

listhead = []

#rest = pd.read_table('csv_test.csv', sep = ',')
rest = pd.read_table('pdc_node_status_all.log', sep = '|')
#print rest.describe('gc-0/17/1-peakCpuUsage')
headlist = rest.head(0)
print headlist
print

for i in headlist:
    if re.search(r'\S*-average|gc-\S*-peak|gc-\S*-memory', i):
        listhead.append(i)

for i in listhead:
    sss = rest[i]
    print sss.describe()









#rest.to_csv(sys.stdout, sep='|')
#rest.to_csv('sepex.log', sep='|')
#rest.to_csv('aaa.log')