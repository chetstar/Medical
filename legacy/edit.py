"""get explode columns into shape."""
import json

with open('explode_columns.json') as f:
    cols = json.load(f)

reps = ['EligibilityStatus','RespCounty','AidCode']

changes = []

for name in cols:
    for rep in reps:
        if name[0].startswith(rep) and 'SP' not in name[0]:
            x = name[0].replace(rep,'')
            changes.append(rep + 'SP0' + x)
            name[0] = rep + 'SP0_' + x

print(cols)
        
new_cols = []
for x in cols:
    x[0] = x[0].lower()
    x[0] = x[0].replace('_','')
    new_cols.append(x)

print(new_cols)

with open('explode_columns.json','w') as f:
    json.dump(new_cols,f)
