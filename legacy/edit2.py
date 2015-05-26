import json

with open('columns_to_save.json') as f:
    cts = json.load(f)

for i,x in enumerate(cts):
    cts[i] = x.lower()

with open('columns_to_save.json', 'w') as f:
    json.dump(cts, f)

print(cts)
