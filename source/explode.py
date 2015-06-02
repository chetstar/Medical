import json
from datetime import datetime

import pandas as pd
from savReaderWriter import SavWriter

import config

start_time = datetime.now()

#Load column_info.json into column_info.  This is a list of lists.                                 
with open('explode_columns.json') as f:
    column_info = json.load(f)

#column_names and column_specifications are used by pandas.read_fwf to read in the Medi-Cal file. 
column_names, column_specifications = zip(*column_info)

#All columns should be brought in as strings.
converters = {name:str for name in column_names}

cins = pd.read_fwf(config.medical_file, colspecs = [(209,218)], colnames = ['cin'])
rows_to_skip = pd.isnull(cins).any(axis=1).nonzero()[0]
del cins

#Create an iterator to read 10000 line chunks of the fixed width Medi-Cal file.
chunked_data_iterator = pd.read_fwf(config.medical_file,
                                    skiprows = rows_to_skip,
                                    colspecs = column_specifications, 
                                    names = column_names, 
                                    converters = converters, 
                                    iterator = True,
                                    chunksize = 10000)

#List of base names, or stubs, to use when doing wide to long by month.
stubs = ['eligyear', 'eligmonth', 'aidcodesp0', 'respcountysp0', 'eligibilitystatussp0',
         'socamount', 'medicarestatus', 'hcpstatus', 'hcpcode', 'hcplantext', 'ohc',
         'aidcodesp1', 'respcountysp1', 'eligibilitystatussp1', 'aidcodesp2', 'respcountysp2',
         'eligibilitystatussp2', 'aidcodesp3', 'respcountysp3', 'eligibilitystatussp3']

#Bring in file that matches aidcodes with other attributes: foster, disabled, full, ffp.
with open(config.aidcodes_file) as f:
    aidcodesshort = pd.read_csv(f, header = 0)

#Aidcodes that match to their respective categories.
ssicodes = ['10','20','60']
ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
ihsscodes = ['2L','2M','2N']

eligibilities = ['eligibilitystatussp0', 'eligibilitystatussp1', 
                 'eligibilitystatussp3', 'eligibilitystatussp3']
aidcodes = ['aidcodesp0', 'aidcodesp1', 'aidcodesp2', 'aidcodesp3']

#with open('columns_to_save.json') as f:
#    columns_to_save = json.load(f)
#columns_to_save = [x.lower() for x in columns_to_save]#fix the file so this goes away.
columns_to_save = ['aidcodesp0', 'respcountysp0', 'eligibilitystatussp0']

variable_types = {x:20 for x in columns_to_save}

with SavWriter(config.nodupe_file, columns_to_save, variable_types, 
               ioUtf8 = True) as writer:

    for i,df in enumerate(chunked_data_iterator):
        chunkstart = datetime.now()

        #medsmonth is the most recent month with eligibility data in the file..
        medsmonth = df['eligmonth'][0] + df['eligyear'][0]
        df['medsmonth'] = pd.to_datetime(medsmonth, format = '%m%Y')
        df['bday'] = pd.to_datetime(df['month']+df['day']+df['year'], format = '%m%d%Y')
        df = df.drop(['month','day','year'], axis = 1)

        #Wide to long by month.
        wide_start = datetime.now()
        print('There are {} rows prior to wide_to_long by month'.format(len(df)))
        df = pd.wide_to_long(df, stubs, 'cin', 'j')
        df = df.reset_index()
        print('Wide to long finished in: ', str(datetime.now()-wide_start))
        print('There are {} rows after wide_to_long by month'.format(len(df)))
        print('df.columns after wide to long: ', df.columns)
        print('df.index after wide to long(and after reset index): ', df.index)

        #Drop all rows for months with no eligibility.
        elig_drop_start = datetime.now()
        df = df[(df[eligibilities].apply(
            lambda x: x.dropna().str[0].astype(int))).lt(5,axis = 0).any(axis = 1).reindex(
                index = df.index, fill_value = False)]
        print('Ineligible rows dropped in: ', str(datetime.now()-elig_drop_start))

        #Create calendar column.
        df['calendar'] = pd.to_datetime(df['eligmonth']+df['eligyear'], format='%m%Y')
                
        mcrank_start = datetime.now()

        #Wide to long by aidcode
        aidcode_stubs = ['aidcode','respcounty','eligibilitystatus']
        cols_to_keep= [col for col in df.columns for stub in aidcode_stubs if col.startswith(stub)]
        cols_to_keep.extend(['cin', 'calendar'])
        dw = df[cols_to_keep].copy()
        dw['id'] = dw.index
        print('There are {} rows prior to wide_to_long by aidcode'.format(len(dw)))
        dw = pd.wide_to_long(dw, aidcode_stubs, 'cin', 'j')
        dw = dw.reset_index()
        print('There are {} rows after to wide_to_long by aidcode'.format(len(dw)))

        #Match in additional info on aidcode.
        dw = pd.merge(dw, aidcodesshort, how = 'left', on = 'aidcode', suffixes = ('', 'r'))

        #Create bitmasks for eligibilitystatus, respcounty, full, disabled and foster statuses.
        elig = dw['eligibilitystatus'].dropna().str[0].astype(int).le(5).reindex(
            index = dw.index, fill_value = False)
        local = dw['respcounty'].dropna().eq('01').reindex(index = dw.index, fill_value = False)
        covered = dw['full'].dropna().eq(1).reindex(index = dw.index, fill_value = False)
        disabled = dw['disabledx'].dropna().eq(1).reindex(index = dw.index, fill_value = False)
        foster = dw['fosterx'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

        #Create Medi-Cal ranks.
        dw['mcrank'] = ((dw['aidcode'].notnull()) & (dw['ffp'] >= 1)).map({True:13})
        dw['mcrank'] = dw['ffp'][elig].map({100:10, 65:11, 50:12})
        dw['mcrank'] = dw['ffp'][elig & local].map({100:7, 65:8, 50:9})
        dw['mcrank'] = dw['ffp'][elig & covered].map({100:4, 65:5, 50:6})
        dw['mcrank'] = dw['ffp'][elig & local & covered].map({100:1, 65:2, 50:3})

        #Groupby cin and calendar and keep only the row with the best mcrank for each group.
        dw = dw.sort('mcrank', ascending = True).groupby(['cin', 'calendar']).first()

        #Set primary_aid_code equal to aidcode and eligibility_county_code equal to respcounty.
        dw['primary_aid_code'] = dw['aidcode']
        dw['eligibility_county_code'] = dw['respcounty']
        
        #Create disabled and foster columns
        dw['disabled'] = (elig & disabled).map({True:1})
        dw['foster'] = (elig & foster).map({True:1})

        #Merge the columns we want to keep from the wide_by_aidcode dataframe (dw) back into df.
        dw = dw.set_index('id')
        cols_to_merge = ['primary_aid_code', 'eligibility_county_code', 'mcrank', 'disabled',
                         'foster']
        df = pd.merge(df, dw[cols_to_merge], how = 'left', left_index = True, right_index = True) 
        print('mcrank finished in: ', str(datetime.now()-mcrank_start))

        #If the last character of the primary_Aid_Code is 2,3, or 5 set RetroMC to 1. 
        df['retromc'] = df['primary_aid_code'].dropna().str[-1].isin(['2','3','5']).map({True:1})
        #Create ssi column. Populate with '1' if any aidcode in that row is in ssicodes.
        df['ssi'] = df[aidcodes].isin(ssicodes).any(axis = 1).map({True:'1'})
        df['ccsaidcode'] = df[aidcodes].isin(ccscodes).any(axis = 1).map({True:'1'})
        df['ihssaidcode'] = df[aidcodes].isin(ihsscodes).any(axis = 1).map({True:'1'})
        df['socmc'] = (df[eligibilities].apply(lambda x: x.dropna().str[-1].astype(int))).\
                      eq(1,axis=0).any(axis = 1).map({True:'1'})

        #Write our columns out as an SPSS .sav file.
        write_file_start = datetime.now()
        print('There are {} rows in the dataframe prior to writing'.format(len(df)))
        #df.apply(lambda x: writer.writerow(x[columns_to_save].values), axis = 1)
        writer.writerows(df[columns_to_save].values)
        print('Write_file finished in: ', str(datetime.now()-write_file_start))

        print('Chunk ', i, ' finished in: ', str(datetime.now() - chunkstart))

print('Program finished in: ', str(datetime.now() - start_time))

