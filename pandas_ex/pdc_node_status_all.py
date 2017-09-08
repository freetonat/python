import pandas as pd
import csv
from pylab import *

txt_file = r"pdc_node_status_all.log"
csv_file = r"pdc_node_status_all.csv"

# use 'with' if the program isn't going to immediately terminate
# so you don't leave files open
# the 'b' is necessary on Windows
# it prevents \x1a, Ctrl-z, from ending the stream prematurely
# and also stops Python converting to / from different line terminators
# On other platforms, it has no effect
in_txt = csv.reader(open(txt_file, "rb"), delimiter = '|')
out_csv = csv.writer(open(csv_file, 'wb'))

out_csv.writerows(in_txt)

rdc = pd.read_csv(csv_file)

#print rdc['gc-0/5/1-averageCpuUsage'].mean()
#print('mean_rdc = %-5.1f%%' % rdc['gc-0/5/1-averageCpuUsage'].mean())
#print rdc.head(10)
#print rdc.index
#print rdc.columns
"""
aass = rdc.values
sumdata = []
for i in aass:
    sumdata.append(float(i[20]))
result = sum(sumdata)/len(sumdata)
print("result = %-5.1f%%" % result)
print("result = %-5.1f" % result)
"""
"""
rest =  rdc['gc-0/5/1-averageCpuUsage']
print rest.describe()
"""
"""
y =  (rdc.iloc[:,20])
plt.plot(y.index, y, 'ro')
show()
print y.mean()
"""
#print rest
print rdc.describe()

#print rdc.mean()





