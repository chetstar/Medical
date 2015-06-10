import json
from datetime import datetime

import pandas as pd
from savReaderWriter import SavWriter

import config

start_time = datetime.now()

#column_names and column_specifications are used by pandas.read_fwf to read in the Medi-Cal file. 
with open(config.explode_load_info) as f:
    column_names, column_specifications = zip(*json.load(f))

#All columns should be brought in as strings.
converters = {name:str for name in column_names}

#Bring in CINs and eligibility status for the entire file to identify duplicate rows.
cins = pd.read_fwf(config.medical_file, colspecs = [(209,218),(255,258)], names = ['cin','elig'])
cins = cins.sort(columns = ['cin','elig'], ascending = True, na_position = 'last')
dupemask = ~cins.duplicated(subset = ['cin'])

#Create an iterator to read 10000 line chunks of the fixed width Medi-Cal file.
chunksize = 10000
chunked_data_iterator = pd.read_fwf(config.medical_file,
                                    colspecs = column_specifications, 
                                    names = column_names, 
                                    converters = converters, 
                                    iterator = True,
                                    chunksize = chunksize)

#List of base names, or stubs, to use when doing wide to long by month.
stubs = ['eligyear', 'eligmonth', 'aidcodesp0', 'respcountysp0', 'eligibilitystatussp0',
         'socamount', 'medicarestatus', 'hcpstatus', 'hcpcode', 'hcplantext', 'ohc',
         'aidcodesp1', 'respcountysp1', 'eligibilitystatussp1', 'aidcodesp2', 'respcountysp2',
         'eligibilitystatussp2', 'aidcodesp3', 'respcountysp3', 'eligibilitystatussp3']

#Bring in file that matches aidcodes with other attributes: foster, disabled, full, ffp.
with open(config.aidcodes_file) as f:
    aidcodesshort = pd.read_csv(f, header = 0)

codes = aidcodesshort.copy()
codes = codes.rename(columns = {'aidcode': 'aidcodem'})
codes = codes.drop(['fosterx','disabledx'], axis = 1)

#Aidcodes that match to their respective categories.
ssicodes = ['10','20','60']
ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
ihsscodes = ['2L','2M','2N']

eligibilities = ['eligibilitystatussp0', 'eligibilitystatussp1', 
                 'eligibilitystatussp3', 'eligibilitystatussp3']
aidcodes = ['aidcodesp0', 'aidcodesp1', 'aidcodesp2', 'aidcodesp3']

#Create SavWriter settings.
with open(config.explode_save_info) as f:
    save_info = json.load(f)


colnames, coltypes = zip(*save_info)
variable_types = {colname:coltype for (colname,coltype) in save_info}
colnames = list(colnames)

#Create list columns that are composed of strings.
string_cols = [x for x in variable_types if variable_types[x] ]
#Set alignments for string columns to left and for numerical columns to right.
alignments = {x:'left' if x in string_cols else 'right' for x in colnames}
#Set column_width to None for numerical columns and to length + 1 for string columns.
column_widths = {x: None if x not in string_cols else variable_types[x]+1 for x in colnames}
#Set measure level to nominal for string columns and to scale for numerical columns.
measure_levels = {x:'nominal' if x in string_cols else 'scale' for x in colnames}

def drop_duplicate_rows(df, chunksize, dupemask):
    #Drop duplicate rows and rows without CINs.
    df.index = range(i*chunksize, i*chunksize + len(df.index))
    df = df[dupemask]
    df = df.dropna(subset= ['cin'])
    return df

def make_medsmonth(df):
    #Medsmonth is the most recent month with eligibility data in the file.
    medsmonth = df['eligmonth'][df.index[0]] + df['eligyear'][df.index[0]]
    df['medsmonth'] = pd.to_datetime(medsmonth, format = '%m%Y')
    return df

def make_bday(df):
    df['bday'] = pd.to_datetime(df['month']+df['day']+df['year'], format = '%m%d%Y')
    df = df.drop(['month','day','year'], axis = 1)
    return df

def wide_to_long_by_month(df, stubs):
    #Wide to long by month.
    wide_start = datetime.now()
    print('There are {} rows prior to wide_to_long by month'.format(len(df)))
    df = pd.wide_to_long(df, stubs, 'cin', 'j')
    df = df.reset_index()
    print('Wide to long finished in: ', str(datetime.now()-wide_start))
    print('There are {} rows after wide_to_long by month'.format(len(df)))
    return df

def drop_ineligible_rows(df):
    #Drop all rows for months with no eligibility.
    elig_drop_start = datetime.now()
    df = df[(df[eligibilities].apply(
        lambda x: x.dropna().str[0].astype(int))).lt(5,axis = 0).any(axis = 1).reindex(
            index = df.index, fill_value = False)]
    print('Ineligible rows dropped in: ', str(datetime.now()-elig_drop_start))
    return df

def make_calendar(df):
    df['calendar'] = pd.to_datetime(df['eligmonth']+df['eligyear'], format='%m%Y')
    
def wide_to_long_by_aidcode(df):
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
        return dw

def narrow_aidcode_match(dw, aidcodesshort):
    return pd.merge(dw, aidcodesshort, how = 'left', on = 'aidcode', suffixes = ('', 'r'))

def make_eligibilit_bitmask(dw):
    elig = dw['eligibilitystatus'].dropna().str[0].astype(int).le(5).reindex(
        index = dw.index, fill_value = False)
    return elig

def make_local_bitmask(dw):
    return dw['respcounty'].dropna().eq('01').reindex(index = dw.index, fill_value = False)

def make_covered_bitmask(dw):
    return dw['full'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def make_disabled_bitmask(dw):
    return dw['disabledx'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def make_foster_bitmask(dw):
    return dw['fosterx'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def mcrank(dw, elig, local, covered):
    mcrank_start = datetime.now()
    #Create Medi-Cal ranks. Done in this order so worse ranks don't overwrite better ones.
    dw['mcrank'] = ((dw['aidcode'].notnull()) & (dw['ffp'] >= 1)).map({True:13})
    dw['mcrank'] = dw['ffp'][elig].map({100:10, 65:11, 50:12})
    dw['mcrank'] = dw['ffp'][elig & local].map({100:7, 65:8, 50:9})
    dw['mcrank'] = dw['ffp'][elig & covered].map({100:4, 65:5, 50:6})
    dw['mcrank'] = dw['ffp'][elig & local & covered].map({100:1, 65:2, 50:3})
    #Groupby cin and calendar and keep only the row with the best mcrank for each group.
    dw = dw.sort('mcrank', ascending = True).groupby(['cin', 'calendar']).first()
    print('mcrank finished in: ', str(datetime.now()-mcrank_start))
    return dw

def make_primary_codes(dw):
    #Set primary_aid_code equal to aidcode and eligibility_county_code equal to respcounty.
    dw['primary_aid_code'] = dw['aidcode']
    dw['eligibility_county_code'] = dw['respcounty']
    return dw

def make_foster_column(dw):
    dw['disabled'] = (elig & disabled).map({True:1})
    return dw

def make_foster_column(dw):
    dw['foster'] = (elig & foster).map({True:1})
    return dw

def long_to_wide_by_aidcode(df, dw):
    #Merge the columns we want to keep from the long_by_aidcode dataframe (dw) back into df.
    dw = dw.set_index('id')
    cols_to_merge = ['primary_aid_code', 'eligibility_county_code', 'mcrank', 'disabled', 'foster']
    df = pd.merge(df, dw[cols_to_merge], how = 'left', left_index = True, right_index = True) 
    return df

def make_retromc_column(df):
    #If the last character of the primary_Aid_Code is 2,3, or 5 set RetroMC to 1. 
    df['retromc'] = df['primary_aid_code'].dropna().str[-1].isin(['2','3','5']).map({True:1})    
    return df

def make_ssi_column(df):
    #If any aidcode in row is in ssicodes set ssi to '1'
    df['ssi'] = df[aidcodes].isin(ssicodes).any(axis = 1).map({True:'1'})
    return df

def make_ccsaidcode_column(df):
    #If any aidcode in row is in ccscodes set ccsaidcode to '1'.
    df['ccsaidcode'] = df[aidcodes].isin(ccscodes).any(axis = 1).map({True:'1'})
    return df

def make_ihssaidcode_column(df):
    #If any aidcode in row is in ihsscodes set ihssaidcode to '1'.
    df['ihssaidcode'] = df[aidcodes].isin(ihsscodes).any(axis = 1).map({True:'1'})
    return df

def make_socmc_column(df):
    #If the last character of any eligibility status in row is 1, set socmc to '1'.
    df['socmc'] = (df[eligibilities].apply(lambda x: x.dropna().str[-1].astype(int))).\
                  eq(1,axis=0).any(axis = 1).map({True:'1'})
    return df

def merge_aidcode_info(df, codes):
    #Merge in aidcode based info.
    df = pd.merge(df, codes, how = 'left', left_on = 'aidcodesp0', 
                  right_on = 'aidcodem', suffixes = ('','sp0'))
    df = pd.merge(df, codes, how = 'left', left_on = 'aidcodesp1', 
                  right_on = 'aidcodem', suffixes = ('','sp1'))
    df = pd.merge(df, codes, how = 'left', left_on = 'aidcodesp2', 
                  right_on = 'aidcodem', suffixes = ('','sp2'))
    df = pd.merge(df, codes, how = 'left', left_on = 'aidcodesp3', 
                  right_on = 'aidcodem', suffixes = ('','sp3'))
    return df

if __name__ == '__main__':

    with SavWriter(config.explode_file, colnames, variable_types) as writer:

        for i,df in enumerate(chunked_data_iterator):
            chunkstart = datetime.now()

            dw = wide_to_long_by_aidcode(df)
            dw = narrow_aidcode_match(dw, aidcodesshort)

            elig = make_eligibility_bitmask(dw)
            local = make_local_bitmask(dw)
            covered = make_covered_bitmask(dw)
            disabled = make_disabled_bitmask(dw)
            foster = make_foster_bitmask(dw)


            #A few columns need to be renamed for output.
            df = df.rename(columns = {'eligibilitystatussp0':'eligibilitystatus', 
                                  'respcountysp0':'respcounty', 'eligmonth':'eligibility_month', 
                                  'eligyear':'eligibility_year', 'aidcodesp0':'aidcode'})

            #SavWriter will translate NaNs in string columns to output the string 'NaN'. Since that 
            #isn't the desired output, replace each NaN in a string column with an empty string.
            df[string_cols] = df[string_cols].fillna('')

            #Write our columns out as an SPSS .sav file.
            write_file_start = datetime.now()
            print('There are {} rows in the dataframe prior to writing'.format(len(df)))
            writer.writerows(df[colnames].values)
            print('Write_file finished in: ', str(datetime.now()-write_file_start))

            print('Chunk ', i, ' finished in: ', str(datetime.now() - chunkstart))


        print('Program finished in: ', str(datetime.now() - start_time))

