import re, os

with open("./tcdb.db", "rt") as fin:
    with open("out.txt", "wt") as fout:
        for line in fin:
            if 'TC' in line:
                line = re.sub(r'TC=TC17734\S+', 'TC=17734.9', line)
            fout.write(line.replace('testcase', 'Orange'))
            print line