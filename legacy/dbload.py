import json
import re
from copy import copy

with open('db_chunk') as fp:
    chunk = json.load(fp)

full = []
full.extend(chunk)

for x in range(1,16):
    for row in chunk:
        name = row[0]
        position = copy(row[1])
        desc = row[2]

        temp = []
        temp.append(re.sub('\_0$', ('_' + str(x)), name))
        
        print(position)
        position[0] = position[0] + (x * 93)
        position[1] = position[1] + (x * 93)
        print(position)

        temp.append(position)
        temp.append(desc)

        full.append(temp)

print(full)

with open('db_endchunk','w') as fp:
    json.dump(full, fp)
