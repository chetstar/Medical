import json
from datetime import datetime

import pandas as pd
from savReaderWriter import SavWriter

import config

#Aidcodes that match to their respective categories.
ssicodes = ['10','20','60']
ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
ihsscodes = ['2L','2M','2N']

aidcodes = ['aidcodesp0', 'aidcodesp1', 'aidcodesp2', 'aidcodesp3']
eligibilities = ['eligibilitystatussp0', 'eligibilitystatussp1', 
                 'eligibilitystatussp3', 'eligibilitystatussp3']

def make_duplicates_bitmask(df):
    #Bring in CINs and eligibility status for the entire file to identify duplicate rows.
    cinless = df['cin'].isnull()
    df = df.sort(columns = ['cin','elig'], ascending = True, na_position = 'last')
    dupemask = df.duplicated(subset = ['cin'])
    dropmask = ~(cinless | dupemask) 
    return dropmask

def drop_duplicate_rows(df, chunknum, chunksize, dupemask):
    #Drop duplicate rows and rows without CINs.
    df.index = range(chunknum*chunksize, chunknum*chunksize + len(df.index))
    df = df[dupemask[df.index]]
    return df

def make_medsmonth_column(df):
    #Medsmonth is the most recent month with eligibility data in the file.
    medsmonth = df['eligmonth'][df.index[0]] + df['eligyear'][df.index[0]]
    df['medsmonth'] = medsmonth
    return df

def datetime_to_integer(ts):
    return writer.spssDateTime(ts,'%m%Y')

def format_date_columns(df):
    df['medsmonth'] = df['medsmonth'].map(datetime_to_integer)
    df['calendar'] = df['calendar'].map(datetime_to_integer)
    return df

def wide_to_long_by_month(df, stubs):
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

def make_calendar_column(df):
    df['calendar'] = df['eligmonth']+df['eligyear']
    return df
   
def wide_to_long_by_aidcode(df):
    aidcode_stubs = ['aidcode','respcounty','eligibilitystatus','full','fosterx','disabledx','ffp']
    cols_to_keep= [col for col in df.columns for stub in aidcode_stubs if col.startswith(stub)]
    cols_to_keep.extend(['cin', 'calendar'])
    dw = df[cols_to_keep].copy()
    dw['id'] = dw.index
    print('There are {} rows prior to wide_to_long by aidcode'.format(len(dw)))
    dw = pd.wide_to_long(dw, aidcode_stubs, 'cin', 'j')
    dw = dw.reset_index()
    print('There are {} rows after to wide_to_long by aidcode'.format(len(dw)))
    return dw

def make_eligibility_bitmask(dw):
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
    dw.loc[elig,'mcrank'] = dw['ffp'][elig].map({100:10, 65:11, 50:12})
    dw.loc[(elig & local), 'mcrank'] = dw['ffp'][elig & local].map({100:7, 65:8, 50:9})
    dw.loc[(elig & covered), 'mcrank'] = dw['ffp'][elig & covered].map({100:4, 65:5, 50:6})
    dw.loc[(elig & local & covered), 'mcrank'] = dw['ffp'][elig & local & covered].\
                                                 map({100:1, 65:2, 50:3})
    print('mcrank finished in: ', str(datetime.now()-mcrank_start))
    return dw

def keep_best_mcrank(dw):
    #Groupby cin and calendar and keep only the row with the best mcrank for each group.
    dw = dw.sort('mcrank', ascending = True).groupby(['cin', 'calendar']).first()
    return dw

def make_primary_codes(dw):
    #Set primary_aid_code equal to aidcode and eligibility_county_code equal to respcounty.
    dw['primary_aid_code'] = dw['aidcode']
    dw['eligibility_county_code'] = dw['respcounty']
    return dw

def make_disabled_column(dw, elig, disabled):
    dw['disabled'] = (elig & disabled).map({True:1})
    return dw

def make_foster_column(dw, elig, foster):
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

def merge_aidcode_info(df, aidcode_info):
    #Merge in aidcode based info.
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp0', 
                  right_on = 'xaidcode', suffixes = ('','sp0'))
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp1', 
                  right_on = 'xaidcode', suffixes = ('','sp1'))
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp2', 
                  right_on = 'xaidcode', suffixes = ('','sp2'))
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp3', 
                  right_on = 'xaidcode', suffixes = ('','sp3'))
    df = df.rename(columns = {'full':'fullsp0', 'disabledx':'disabledxsp0', 'fosterx':'fosterxsp0',
                              'ffp':'ffpsp0'})
    return df

def fix_hcplantext(df):
    #If someone has an HCplanText but their HCPstatus is such that it is invalidated, change
    #HCplanText to "z No Plan"
    df.ix[df.hcpstatus.isin(["00","10","09","19","40","49","S0","S9"]),'hcplantext'] = "z No Plan"
    df['hcplantext'] = df['hcplantext'].fillna('z No Plan')
    return df

def make_hcplantext_column(df):
    #create hcplantext column and populate with hcpcode data.
    hcpcode_map = {'300':'Alliance', '340':'Blue Cross', '051':'Center for Elders',
                   '056':'ONLOK Seniors', '000':'z No Plan', None:'z No Plan'}
    df['hcplantext'] = df['hcpcode'].map(hcpcode_map)
    df = fix_hcplantext(df)
    return df

def format_string_columns(df, save_info):
    """  SavWriter will translate NaNs in string columns to output the string 'NaN'. Since that
    isn't the desired output, replace each NaN in a string column with an empty string."""
    string_cols = [x for x in save_info['types'] if save_info['types'][x] > 0]
    df[string_cols] = df[string_cols].fillna('')
    return df

def rename_columns_for_saving(df):
    df = df.rename(columns = {'eligibilitystatussp0':'eligibilitystatus', 'fullsp0':'full',
                              'respcountysp0':'respcounty', 'eligmonth':'eligibility_month', 
                              'eligyear':'eligibility_year', 'aidcodesp0':'aidcode',
                              'ffpsp0':'ffp',})
    return df

if __name__ == '__main__':

    start_time = datetime.now()

    df = pd.read_fwf(config.medical_file,colspecs = [(209,218),(255,258)],names = ['cin','elig'])
    dupemask = make_duplicates_bitmask(df)

    #column_names and column_specifications are used to read in the Medi-Cal file. 
    with open(config.explode_load_info) as f:
        column_names, column_specifications = zip(*json.load(f))

    #All columns should be brought in as strings.
    converters = {name:str for name in column_names}
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
        aidcode_info = pd.read_csv(f, header = 0)

    with open(config.explode_save_info) as f:
        save_info = json.load(f)

    formats = {'calendar':'MOYR6', 'medsmonth':'MOYR6', 'ffp':'F3.0', 'ffpsp1':'F3.0', 
               'ffpsp2':'F3.0', 'ssi':'F1.0', 'eligibility_year':'F4.0', 'eligibility_month':'F2.0',
               'ffpsp3':'F3.0', 'full':'F1.0', 'fullsp1':'F1.0', 'fullsp2':'F1.0', 'fullsp3':'F1.0',
               'mcrank':'F2.0', 'disabled':'F1.0', 'foster':'F1.0', 'retroMC':'F1.0', 'socmc':'F1.0'}

    with SavWriter(config.explode_file, save_info['column_names'], save_info['types'], 
                   measureLevels = save_info['measure_levels'],
                   alignments = save_info['alignments'],
                   columnWidths = save_info['column_widths'],
                   formats = formats) as writer:

        for i, df in enumerate(chunked_data_iterator):
            chunkstart = datetime.now()

            df = drop_duplicate_rows(df, i, chunksize, dupemask)
            df = make_medsmonth_column(df)
            df = wide_to_long_by_month(df, stubs)
            df = drop_ineligible_rows(df)
            df = make_calendar_column(df)
            df = merge_aidcode_info(df, aidcode_info)

            dw = wide_to_long_by_aidcode(df)

            elig = make_eligibility_bitmask(dw)
            local = make_local_bitmask(dw)
            covered = make_covered_bitmask(dw)
            disabled = make_disabled_bitmask(dw)
            foster = make_foster_bitmask(dw)

            dw = mcrank(dw, elig, local, covered)
            dw = keep_best_mcrank(dw)
            dw = make_primary_codes(dw)
            dw = make_disabled_column(dw, elig, disabled)
            dw = make_foster_column(dw, elig, foster)

            df = long_to_wide_by_aidcode(df, dw)

            df = make_retromc_column(df)
            df = make_ssi_column(df)
            df = make_ccsaidcode_column(df)
            df = make_ihssaidcode_column(df)
            df = make_socmc_column(df)
            df = make_hcplantext_column(df)
            df = rename_columns_for_saving(df)
            df = format_string_columns(df, save_info)
            df = format_date_columns(df)

            #Write our columns out as an SPSS .sav file.
            write_file_start = datetime.now()
            print('There are {} rows in the dataframe prior to writing'.format(len(df)))
            writer.writerows(df[save_info['column_names']].values)
            print('Write_file finished in: ', str(datetime.now()-write_file_start))
            print('Chunk ', i, ' finished in: ', str(datetime.now() - chunkstart))

    print('Program finished in: ', str(datetime.now() - start_time))

