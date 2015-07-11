import csv

with open('../source/aidcodes.csv', newline='') as fp:
    reader = csv.reader(fp)
    aidcodes = [row for row in reader][1:]

for i, row in enumerate(aidcodes):
    #Convert first column to integers or 0 if empty.
    if row[0]:
        row[0] = int(row[0])
    else:
        row[0] = 0

    #Columns 2,3 and 4: if they're 0 or Null, set to False, otherwise set to True.
    if row[2] and row[2] == '1':
        row[2] = True
    else:
        row[2] = False

    if row[3] and row[3] == '1':
        row[3] = True
    else:
        row[3] = False

    if row[4] and row[4] == '1':
        row[4] = True
    else:
        row[4] = False

    aidcodes[i] = row

with open('aidcodes.csv', 'w') as fp:
    writer = csv.writer(fp)
    writer.writerows(aidcodes)

"""
COPY aidcodes ( federal_financial_participation, aidcode, disabled, fully_covered, foster)
FROM '/Users/irisweiss/greg/Medical/db/db_aidcodes.csv'
WITH CSV HEADER;
"""
