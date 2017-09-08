import re
import StringIO

wtindex=0
fw = open("C:\PyCharm\python\status_result.txt","w")
f = open("C:\PyCharm\python\status.txt","r")
while True:
    line = f.readline()
    mat = re.search("gc-0/6/1",line)
    if mat:
        wtindex = 4
    if wtindex > 0 :
        fw.write(line)
    wtindex -= 1
    #print(wtindex)



f.close()
fw.close()