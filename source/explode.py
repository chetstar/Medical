import json
from datetime import datetime
import multiprocessing as mp
import sys

import pandas as pd
from savReaderWriter import SavWriter
import numpy as np

import common
import config

def make_duplicates_bitmask(df):
    """Use CIN and eligibility status for entire file to make bitmask
    of duplicate and cinless rows."""
    cinless = df['cin'].isnull()
    df = df.sort(columns = ['cin','elig'], ascending = True, na_position = 'last')
    dupemask = df.duplicated(subset = ['cin'])
    dropmask = ~(cinless | dupemask) 
    return dropmask

def drop_duplicate_rows(df, chunknum, chunksize, dupemask):
    """Drop duplicate rows and rows without CINs."""
    df.index = range(chunknum*chunksize, chunknum*chunksize + len(df.index))
    df = df[dupemask[df.index]]
    return df

def make_medsmonth_column(df):
    """Medsmonth is the most recent month with eligibility data in the file."""
    month_time = datetime(int(df['eligyear'][df.index[0]]), int(df['eligmonth'][df.index[0]]), 1)
    zero_time = datetime(1582,10,14) #0 in SPSS time system.
    medsmonth = int((month_time - zero_time).total_seconds())
    df.loc[:,'medsmonth'] = medsmonth
    return df

def wide_to_long_by_month(df, stubs):
    df = pd.wide_to_long(df, stubs, 'cin', 'j')
    df = df.reset_index()
    return df

def spss_date(row):
    """Create an SPSS format date, which is the number of seconds since October 14, 1582."""
    zero_time = datetime(1582,10,14) #0 in SPSS time system.
    time_to_convert = datetime(int(row['eligyear']),int(row['eligmonth']),1)
    return int((time_to_convert - zero_time).total_seconds())

def make_calendar_column(df):
    """Create a calendar column in SPSS date format using 'eligyear' and 'eligmonth'"""
    df['calendar'] = df.apply(spss_date, axis = 1)
    return df
   
def wide_to_long_by_aidcode(df):
    aidcode_stubs = ['aidcode', 'respcounty', 'eligibilitystatus', 'full',
                     'fosterx', 'disabledx', 'ffp']
    cols_to_keep= [col for col in df.columns for stub in aidcode_stubs if col.startswith(stub)]
    cols_to_keep.extend(['cin', 'calendar'])
    dw = df[cols_to_keep].copy()
    dw['id'] = dw.index
    dw = pd.wide_to_long(dw, aidcode_stubs, 'cin', 'j')
    dw = dw.reset_index()
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
    """Create Medi-Cal ranks."""
    #Done in this order so worse ranks don't overwrite better ones.
    dw['mcrank'] = ((dw['aidcode'].notnull()) & (dw['ffp'] >= 1)).map({True:13})
    dw.loc[elig,'mcrank'] = dw['ffp'][elig].map({100:10, 65:11, 50:12})
    dw.loc[(elig & local), 'mcrank'] = dw['ffp'][elig & local].map({100:7, 65:8, 50:9})
    dw.loc[(elig & covered), 'mcrank'] = dw['ffp'][elig & covered].map({100:4, 65:5, 50:6})
    dw.loc[(elig & local & covered), 'mcrank'] = dw['ffp'][elig & local & covered].\
                                                 map({100:1, 65:2, 50:3})
    return dw

def keep_best_mcrank(dw):
    """Groupby cin and calendar and keep only the row with the best mcrank for each group."""
    dw = dw.sort('mcrank', ascending = True).groupby(['cin', 'calendar']).first()
    return dw

def make_primary_codes(dw):
    """Set primary_aid_code equal to aidcode and eligibility_county_code equal to respcounty."""
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
    """Merge the columns we want to keep from the long_by_aidcode dataframe (dw) back into df."""
    dw = dw.set_index('id')
    cols_to_merge = ['primary_aid_code', 'eligibility_county_code', 'mcrank', 'disabled', 
                     'foster', 'ccsaidcode', 'ihssaidcode', 'ssi', 'retromc', 'socmc']
    df = pd.merge(df, dw[cols_to_merge], how = 'left', left_index = True, right_index = True) 
    return df

def make_retromc_column(dw):
    """If the last character of the primary_Aid_Code is 2,3, or 5 set RetroMC to 1."""
    dw['retromc'] = dw['primary_aid_code'].dropna().str[-1].isin(['2','3','5']).map({True:1})    
    return dw

def make_ssi_column(dw, ssicodes):
    """If any aidcode in row is in ssicodes set ssi to '1'."""
    dw['ssi'] = dw['aidcode'].isin(ssicodes).map({True:'1'})
    return dw

def make_ccsaidcode_column(dw, ccscodes):
    """If any aidcode in row is in ccscodes set ccsaidcode to '1'."""
    dw['ccsaidcode'] = dw['aidcode'].isin(ccscodes).map({True:'1'}).reindex(
        index = dw.index, fill_value = None)
    return dw

def make_ihssaidcode_column(dw, ihsscodes):
    """If any aidcode in row is in ihsscodes set ihssaidcode to '1'."""
    dw['ihssaidcode'] = dw['aidcode'].isin(ihsscodes).map({True:'1'})
    return dw

def make_socmc_column(dw):
    """If the last character of any eligibility status in row is 1, set socmc to '1'."""
    dw['socmc'] = dw['eligibilitystatus'].dropna().str[-1].astype(int).eq(1).map({True:'1'})
    return dw

def merge_aidcode_info(df, aidcode_info):
    """Merge in aidcode based info: foster, disabled, full, ffp."""
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp0', 
                  right_on = 'xaidcode', suffixes = ('','sp0'))
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp1', 
                  right_on = 'xaidcode', suffixes = ('','sp1'))
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp2', 
                  right_on = 'xaidcode', suffixes = ('','sp2'))
    df = pd.merge(df, aidcode_info, how = 'left', left_on = 'aidcodesp3', 
                  right_on = 'xaidcode', suffixes = ('','sp3'))
    df = df.rename(columns = {'full':'fullsp0', 'disabledx':'disabledxsp0', 
                              'fosterx':'fosterxsp0','ffp':'ffpsp0'})
    return df

def rename_columns_for_saving(df):
    df = df.rename(columns = {'eligibilitystatussp0':'eligibilitystatus', 'fullsp0':'full',
                              'respcountysp0':'respcounty', 'eligmonth':'eligibility_month', 
                              'eligyear':'eligibility_year', 'aidcodesp0':'aidcode',
                              'ffpsp0':'ffp',})
    return df

def process_chunk(chunk):

    chunkstart = datetime.now()

    chunk_number, df = chunk

    df = drop_duplicate_rows(df, chunk_number, chunksize, dupemask)
    df = make_medsmonth_column(df)
    df = wide_to_long_by_month(df, stubs)
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
    dw = make_retromc_column(dw)
    dw = make_ssi_column(dw, ssicodes)
    dw = make_ccsaidcode_column(dw, ccscodes)
    dw = make_ihssaidcode_column(dw, ihsscodes)
    dw = make_socmc_column(dw)
    
    df = long_to_wide_by_aidcode(df, dw)

    df = common.make_hcplantext_column(df)
    df = rename_columns_for_saving(df)
    #df = common.format_string_columns(df, save_info)

    values = df[save_info['column_names']].values
    values = [[item if item is not np.nan else None for item in row] for row in values]
    print('Chunk {} finished in: {}'.format(chunk_number, str(datetime.now() - chunkstart)))
    return chunk_number, values

if __name__ == '__main__':

    start_time = datetime.now()

    medical_file = common.set_medical_file_location(sys.argv)

    #Create bitmask used to remove duplicate rows and rows without a CIN.
    df = pd.read_fwf(medical_file, colspecs = [(209,218),(255,258)], names = ['cin','elig'])
    dupemask = make_duplicates_bitmask(df)

    #Aidcodes that indicate specific statuses.
    ssicodes = ['10','20','60']
    ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
    ihsscodes = ['2L','2M','2N']

    #column_names and column_specifications are used to read in the Medi-Cal file. 
    with open(config.explode_load_info) as f:
        column_names, column_specifications = zip(*json.load(f))

    #Create an iterator to read chunks of the fixed width Medi-Cal file.
    chunksize = config.chunk_size
    chunked_data_iterator = pd.read_fwf(medical_file,
                                        colspecs = column_specifications, 
                                        names = column_names, 
                                        converters = {name:str for name in column_names}, 
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

    with SavWriter(config.explode_file, 
                   save_info['column_names'], 
                   save_info['types'], 
                   measureLevels = save_info['measure_levels'],
                   alignments = save_info['alignments'],
                   columnWidths = save_info['column_widths'],
                   formats = save_info['formats']) as writer:

        pool = mp.Pool(mp.cpu_count()-1)
        for i, df in pool.imap_unordered(process_chunk, enumerate(chunked_data_iterator), 1):
            print('Writing chunk {}.'.format(i))
            writer.writerows(df)
        pool.close()
        pool.join()

    print('Program finished in: ', str(datetime.now() - start_time))

