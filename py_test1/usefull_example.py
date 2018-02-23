def aaa():
    dic_list = {'timeout':'5' , 'b':2, 'c':3}
    print(dic_list)
    if 'timeout' in dic_list:
        print("True")
        aaa = int(dic_list['timeout'])
        print("aaa = %d" %aaa )

    contextcnt = 500
    new_cnt = int(contextcnt/2)
    print(new_cnt)

aaa()

##################
import re

title_line = "GTP IP Transport    | Attempted | Successful | Failed | Resendings | RTT (secs) | Rate (/sec)  |"

def get_title_po():
    name_list = []
    name_position = []
    for c in re.finditer(r'\|\s+(\S+)(\s+\(\S+\))*\s*', title_line):
        name_position.append((c.start(), c.end()))
        name_list.append(c.group(1))
    print(name_list)
    print(name_position)
    print(aaa)

get_title_po()

#################
import os,re

def get_gx_offline_cnt(self):
    f = open("C:\src_code\py\py_test1\gx_fail.txt","r")
    while True:
        line = f.readline()
        line = line.strip()
        if 'temporary-offline-sessions' in line:
            temporary = re.split(':', line)[1]
        if 'permanently-offline-sessions' in line:
            permanently = re.split(':', line)[1]
        if 'offline-sessions' in line:
            offline = re.split(':', line)[1]
            break
            return temporary, permanently, offline

#################
j = 0
count_loop = 0
for i in range(0, 20):
    if count_loop % 6 == 0:
        print(count_loop)
        j = j + 1
    print("j={},count_loop={}".format(j,count_loop))
    count_loop = count_loop + 1

output = '''
{'timeout': '5', 'b': 2, 'c': 3}
True
aaa = 5
250
['Attempted', 'Successful', 'Failed', 'Resendings', 'RTT', 'Rate']
[(20, 32), (32, 45), (45, 54), (54, 67), (67, 80), (80, 95)]
<function aaa at 0x007B3F60>
0
j=1,count_loop=0
j=1,count_loop=1
j=1,count_loop=2
j=1,count_loop=3
j=1,count_loop=4
j=1,count_loop=5
6
j=2,count_loop=6
j=2,count_loop=7
j=2,count_loop=8
j=2,count_loop=9
j=2,count_loop=10
j=2,count_loop=11
12
j=3,count_loop=12
j=3,count_loop=13
j=3,count_loop=14
j=3,count_loop=15
j=3,count_loop=16
j=3,count_loop=17
18
j=4,count_loop=18
j=4,count_loop=19
'''
