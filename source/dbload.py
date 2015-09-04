import argparse
import json 
from datetime import datetime
import multiprocessing as mp

import psycopg2
import pandas as pd
import numpy as np
from psycopg2.extensions import register_adapter, adapt

from medi_cal_analysis import medi_cal_analysis
import config

def set_sex(df):
    """If gender is M or F, set it to Male or Female, respectively.  
    Otherwise set to Unknown."""
    df.loc[( (df['gender'] != 'M') & (df['gender'] != 'F') ), 'gender'] = 'Unknown'
    df.loc[(df['gender']=='M'),'gender'] = 'Male'
    df.loc[(df['gender']=='F'),'gender'] = 'Female'
    return df

def format_date_of_birth(df):
    """Convert date_of_birth from a string to a datetime object."""
    df.loc[:,['date_of_birth']] = pd.to_datetime(df['date_of_birth'])
    return df

def set_ethnicity(df):
    ethnicity_map = {'1':'White', '2':'Hispanic', '3':'Black',
                     '4':'Asian or Pacific Islander',
                     '5':'Alaska Native or American Indian', '7':'Filipino',
                     '8':'Unknown', '9':'Unknown', 'A':'Ameriasian',
                     'C':'Chinese', 'H':'Cambodian', 'J':'Japanese',
                     'K':'Korean', 'N':'Asian Indian', 'P':'Hawaiian',
                     'R':'Guamanian', 'L':'Laotian', 'V':'Vietnamese',
                     'Z':'Other', None:'Unknown'}
    df.loc[:,'ethnicity_code'] = df['ethnicity_code'].map(ethnicity_map)
    return df

def set_language(df):
    language_map = {'B': 'Chinese', 'P': 'Portugese', 'A': 'Other Sign',
                    'D': 'Cambodian', '2': 'Cantonese', 'N': 'Russian',
                    None: 'Unknown', '1': 'Spanish', '3': 'Japanese',
                    'G': 'Mien', '4': 'Korean', '5': 'Tagalog', 
                    'C': 'Other Chinese', 'V': 'Vietnamese',
                    '0': 'American Sign', '7': 'English', 'S': 'Samoan',
                    'J': 'Hebrew', 'U': 'Farsi', 'R': 'Arabic', 'Q': 'Italian',
                    'M': 'Polish', 'F': 'Llacano', '9': 'Unknown',
                    '8': 'Unknown', 'I': 'Lao', 'H': 'Hmong', '6': 'Other', 
                    'T': 'Thai', 'K': 'French', 'E': 'Armenian'}
    df.loc[:,'language_code'] = df['language_code'].map(language_map)
    return df

def insert_medi_cal_attributes(df):
    df = set_sex(df)
    df = format_date_of_birth(df)
    df = set_ethnicity(df)
    df = set_language(df)

    df_columns = ['cin', 'source_date', 'date_of_birth', 'meds_id',
                  'hic_number', 'hic_suffix', 'ethnicity_code',
                  'gender', 'language_code']

    sql = """
    INSERT INTO medi_cal_attributes
        (cin, source_date, date_of_birth, meds_id, 
         health_insurance_claim_number, health_insurance_claim_suffix, 
         ethnicity, sex, primary_language)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cur.executemany(sql, df[df_columns].values)

def insert_medi_cal_names(df):
    #df = clean_city_names()
    name_columns = ['cin', 'first_name', 'middle_initial', 'last_name',
                    'name_suffix', 'source_date']

    sql = """
    INSERT INTO medi_cal_names
        (cin, first_name, middle_initial, last_name, suffix, source_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cur.executemany(sql, df[name_columns].values)
        
def insert_medi_cal_addresses(df):
    df.loc[:,'street_address'] = (df['address_line_1'].fillna('').str.strip()
                                  + ' ' +
                                  df['address_line_2'].fillna('').str.strip())

    df_columns = ['cin', 'street_address', 'address_state',
                  'address_city', 'address_zip_code', 'source_date']

    sql = """
    INSERT INTO medi_cal_addresses
        (cin, street_address, state, city, zip, source_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.executemany(sql, df[df_columns].values)
    
def insert_medi_cal_eligibility_base(df, chunk_number):
    df_columns = ['cin', 'source_date', 'resident_county',
                  'share_of_cost_amount', 'medicare_status', 'carrier_code',
                  'federal_contract_number', 'plan_id', 'plan_type',
                  'surs_code', 'special_obligation', 'healthy_families_date',
                  'eligibility_date', 'other_health_coverage']

    sql = """
    INSERT INTO medi_cal_eligibility_base
        (cin, source_date, resident_county, soc_amount, medicare_status, 
         carrier_code, federal_contract_number, plan_id, plan_type, surs_code, 
         special_obligation, healthy_families_date, eligibility_date, 
         other_health_coverage)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(sql, df[df_columns].values)
    except psycopg2.IntegrityError as e:
        if e.pgcode == '23505':
            print('Some eligibility_base rows in chunk {} have already been inserted'
                  .format(chunk_number))
            conn.commit()
        else:
            raise e
    finally:
        conn.commit()
        
def insert_medi_cal_eligibility_status(dw, chunk_number):
    eligibility_status_columns = ['cin', 'source_date', 'eligibility_date',
                                  'cardinal', 'aidcode', 'eligibility_status',
                                  'responsible_county']

    sql = """
    INSERT INTO medi_cal_eligibility_status
        (cin, source_date, eligibility_date, cardinal, 
         aidcode, eligibility_status, responsible_county)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(sql, dw[eligibility_status_columns].values)
    except psycopg2.IntegrityError as e:
        if e.pgcode == '23505':
            print('Some eligibility_status rows in chunk {} have already been inserted'
                  .format(chunk_number))
            conn.commit()
        else:
            raise e
    finally:
        conn.commit()

def insert_medi_cal_hcp_status(dw, chunk_number):
    df_columns = ['cin', 'source_date', 'eligibility_date',
                  'health_care_plan_status', 'health_care_plan_code',
                  'cardinal']

    sql = """
    INSERT INTO medi_cal_hcp_status
        (cin, source_date, eligibility_date, hcp_status_code, 
         hcp_code, cardinal)
    VAlUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cur.executemany(sql, dw[df_columns].values)
    except psycopg2.IntegrityError as e:
        if e.pgcode == '23505':
            print('Some hcp_status rows in chunk {} have already been inserted'
                  .format(chunk_number))
        else:
            raise e
    finally:
        conn.commit()            

def insert_medi_cal_derived_status(df, chunk_number):
    sql = """
    INSERT INTO medi_cal_derived_status
        (cin, source_date, eligibility_date, rank, primary_aidcode, disabled,
         foster, retro, ssi, ccs, ihss, soc, primary_county_code)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    medi_cal_derived_columns = ['cin', 'source_date', 'eligibility_date',
                                'mcrank', 'primary_aidcode', 'disabled',
                                'foster', 'retromc', 'ssi', 'ccsaidcode',
                                'ihssaidcode', 'socmc',
                                'eligibility_county_code']

    try:
        cur.executemany(sql, df[medi_cal_derived_columns].values)
    except psycopg2.IntegrityError as e:
        if e.pgcode == '23505':
            print('Some derived_status rows in chunk {} have already been inserted'
                  .format(chunk_number))
            conn.commit()
        else:
            raise e
    finally:
        conn.commit()

def create_source_date_column(df):
    source_date = datetime(int(df['eligibility_year_0'][df.index[0]]),
                           int(df['eligibility_month_0'][df.index[0]]), 1)
    df.loc[:,'source_date'] = source_date
    return df
       
def create_eligibility_date_column(df):
    df.loc[:,'eligibility_date'] = pd.to_datetime(df['eligibility_year'] +
                                            df['eligibility_month'] + '01')
    return df

def wide_to_long(df, stubs):
    #Only operate on necesarry columns to keep memory usage down.
    cols_to_keep= [col for col in df.columns for stub in stubs if col.startswith(stub)]
    cols_to_keep.extend(['cin', 'source_date', 'eligibility_date'])
    dw = df[cols_to_keep].copy()
    dw['id'] = dw.index
    dw = pd.wide_to_long(dw, stubs, 'cin', 'j')
    dw['cardinal'] = dw.index.get_level_values('j').str[-1]
    dw = dw.reset_index()
    return dw

def wide_to_long_by_month(df, stubs):
    df = pd.wide_to_long(df, stubs, 'cin', 'j')
    df = df.reset_index()
    return df

def get_aidcode_info():
    """Get data from info_aidcodes table and put it into df_aidcodes"""
    
    sql = """
    SELECT aidcode, federal_financial_participation, fully_covered, 
           disabled, foster
    FROM rules_aidcodes
    """
    
    cur.execute(sql)
    records = cur.fetchall()
    df_aidcodes = pd.DataFrame(data = records,
                               columns = ['aidcode', 'ffp', 'full',
                                          'disabled', 'foster'])
    return df_aidcodes

def insert_duplicate_rows(df):
    sql = """
    INSERT INTO medi_cal_duplicates (row_text)
    VALUES (%s)
    """
    
    if not df.empty:
        duplicate_rows = [[x] for x in
                          df.to_string(header = False, index = False).split('\n')]
        cur.executemany(sql, duplicate_rows)

def process_chunk(params):
    
    chunk_number, df, chunksize, dupemask = params
    df, df_dupe_rows = drop_duplicate_rows(df, chunk_number,
                                           chunksize, dupemask)
    insert_duplicate_rows(df_dupe_rows)
    df = create_source_date_column(df)

    insert_medi_cal_attributes(df)
    insert_medi_cal_names(df)
    insert_medi_cal_addresses(df)
    
    df = wide_to_long_by_month(df, month_stubs)
    df = create_eligibility_date_column(df)

    insert_medi_cal_eligibility_base(df, chunk_number)
    
    df_hcp = wide_to_long(df, hcp_stubs)
    insert_medi_cal_hcp_status(df_hcp, chunk_number)
    del df_hcp
    
    dw = wide_to_long(df, aidcode_stubs)
    insert_medi_cal_eligibility_status(dw, chunk_number)

    df_aidcodes = get_aidcode_info()
    dw = medi_cal_analysis(dw, df_aidcodes, ssicodes, ccscodes, ihsscodes)
    insert_medi_cal_derived_status(dw, chunk_number)
    conn.commit()
    
def nan_to_null(f,
                _NULL=psycopg2.extensions.AsIs('NULL'),
                _NaN=np.NaN,
                _Float=psycopg2.extensions.Float):
    if f is not _NaN:
        return _Float(f)
    return _NULL

def process_arguments():
    parser = argparse.ArgumentParser(description='Process Medi-Cal File.')
    parser.add_argument('infile', 
                        nargs = '?',
                        default = config.medical_file,
                        help = 'Location of Medi-Cal file to process.')
    parser.add_argument('-o', '--outfile',
                        default = config.explode_file,
                        help = 'File name and path of output file.')
    parser.add_argument('-m', '--multi-process',
                        action = 'store_true',
                        help = 'Run in multi-process mode. Default is single process.')
    return parser.parse_args()

def multi_process_run(params):
    pool = mp.Pool(mp.cpu_count()//2)
    for i, df in pool.imap_unordered(process_chunk, params):
        print('Processing chunk {}.'.format(i))
    pool.close()
    pool.join()

def single_process_run(params):
    for chunk in params:
        process_chunk(chunk)

def drop_duplicate_rows(df, chunknum, chunksize, dupemask):
    """Drop duplicate rows and rows without CINs."""
    df.index = range(chunknum*chunksize, chunknum*chunksize + len(df.index))
    df_dupe_rows = df[-dupemask[df.index]]
    df = df[dupemask[df.index]]
    return df, df_dupe_rows

def make_duplicates_bitmask(medical_file):
    """Use CIN and eligibility status for entire file to make bitmask
    of duplicate and cinless rows."""
    df = pd.read_fwf(medical_file, colspecs = [(209,218),(255,258)],
                     names = ['cin','elig'])
    cinless = df['cin'].isnull()
    df = df.sort(columns = ['cin','elig'], ascending = True,
                 na_position = 'last')
    dupemask = df.duplicated(subset = ['cin'])
    dropmask = ~(cinless | dupemask) 
    return dropmask

if __name__ == "__main__":
    #Aidcodes that indicate specific statuses.
    ssicodes = ['10','20','60']
    ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
    ihsscodes = ['2L','2M','2N']

    #Parse command line arguments.
    args = process_arguments()
        
    aidcode_stubs = ['aidcode', 'eligibility_status', 'responsible_county']
    
    hcp_stubs = ['health_care_plan_status', 'health_care_plan_code']
    
    month_stubs = ['eligibility_year', 'eligibility_month', 'aidcode_sp0',
                   'responsible_county_sp0', 'resident_county',
                   'eligibility_status_sp0', 'share_of_cost_amount',
                   'medicare_status', 'carrier_code',
                   'federal_contract_number', 'plan_id', 'plan_type',
                   'health_care_plan_status_s0', 'health_care_plan_code_s0',
                   'other_health_coverage', 'surs_code', 'aidcode_sp1',
                   'responsible_county_sp1', 'eligibility_status_sp1',
                   'aidcode_sp2', 'responsible_county_sp2',
                   'eligibility_status_sp2', 'special_obligation',
                   'healthy_families_date', 'aidcode_sp3',
                   'responsible_county_sp3', 'eligibility_status_sp3',
                   'health_care_plan_status_s1', 'health_care_plan_code_s1',
                   'health_care_plan_status_s2', 'health_care_plan_code_s2']
    
    medical_file = config.medical_file
    database_name = config.database_name
    database_user = config.database_user
    
    #Create bitmask used to remove duplicate rows and rows without a CIN.
    dupemask = make_duplicates_bitmask(medical_file)

    #column_names and column_specifications are used by pandas.read_fwf to
    #read Medi-Cal file.
    with open(config.db_load_info) as f:
        column_names, column_specifications, _ = zip(*json.load(f))

    #Create an iterator to read chunks of the fixed width Medi-Cal file.
    chunksize = config.chunk_size
    chunked_data_iterator = pd.read_fwf(medical_file,
                                        colspecs = column_specifications, 
                                        names = column_names, 
                                        converters = {name:str for name in
                                                      column_names},
                                        iterator = True,
                                        chunksize = chunksize)

    with psycopg2.connect(database = database_name,
                          user = database_user) as conn:
        register_adapter(float, nan_to_null)
        with conn.cursor() as cur:
            params = ((x[0], x[1], chunksize, dupemask) for x in
                      enumerate(chunked_data_iterator))
            if args.multi_process:
                multi_process_run(params)
            else:
                single_process_run(params)
