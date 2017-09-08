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

get_title_po()