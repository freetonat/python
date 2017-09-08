import re
sleeptime=('1y2w15d2h10m1s88')

for sleep_unit in [x for x in re.split(r'(\d+[ywdhms]?)', sleeptime)
                   if x]:
    print(sleep_unit)