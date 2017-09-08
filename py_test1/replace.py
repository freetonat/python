with open("./tcdb.db", "rt") as fin:
    with open("out.txt", "wt") as fout:
        for line in fin:
            fout.write(line.replace('testcase', 'Orange'))
            print line