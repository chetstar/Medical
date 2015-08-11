with open('db_aidcodes.csv') as fp:
    codes = fp.readlines()

codes = [x[:-1] for x in codes]

for i, row in enumerate(codes):
    row = row.split(',')
    row[0], row[1] = row[1], row[0]
    codes[i] = ','.join(row)

with open('newcodes.csv', 'w') as fp:
    for row in codes:
        fp.write("%s\n" % row)


    
        
