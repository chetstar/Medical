import pandas as pd

df = pd.DataFrame({'a': range(10)})

with open('testfwf.txt', 'w') as f:
    f.write(df.to_string(index = False, header = False))

rows_to_skip = [0,1,2,6,9]

df = pd.read_fwf('testfwf.txt', colspecs = [(0,2)], names = ['a'])
print('The entire fixed width file in on dataframe: ')
print(df)

df = pd.read_fwf('testfwf.txt', colspecs = [(0,2)], names = ['a'], skiprows = rows_to_skip)
print('The fixed width file with rows 0,1,2,6,9 skipped: ')
print(df)

df_iter = pd.read_fwf('testfwf.txt', colspecs = [(0,2)], names = ['a'], iterator = True, 
                      chunksize = 2)
print('The entire fixed width file in chunks: ')
for df in df_iter:
    print(df)

df_iter = pd.read_fwf('testfwf.txt', colspecs = [(0,2)], names = ['a'], iterator = True, 
                      chunksize = 2, skiprows = rows_to_skip)
print('The fixed width file in chunks with rows 0,1,2,6,9 skipped: ')
for df in df_iter:
    print(df)

print('Notice how row 6 of the fixed width file has not been skipped even though it should')
print('have been.')

"""
cins = pd.read_fwf('testfwf.txt', colspecs = [(0,3),(3,6)], names = ['cin','elig'])

cinless_rows = set(cins[pd.isnull(cins['cin'])].index)
print('CINless rows: {}.'.format(cinless_rows))

cins = cins.sort(columns = ['cin','elig'], ascending = True, na_position = 'last')

duplicate_rows = set(cins[cins.duplicated(subset = 'cin')].index)
print('Duplicate rows: {}.'.format(duplicate_rows))

rows_to_skip = list(cinless_rows | duplicate_rows)
rows_to_skip.append(0)
print('Rows to skip: {}.'.format(rows_to_skip))

del cins

chunky = pd.read_fwf('testfwf.txt', skiprows = rows_to_skip, colspecs = [(0,3),(3,6)], 
                     names = ['cin','elig'], iterator = True, chunksize = 2 )

for df in chunky:
    print(df)

full = pd.read_fwf('testfwf.txt', colspecs = [(0,3),(3,6)], names = ['cin','elig'])

print(full)
"""
