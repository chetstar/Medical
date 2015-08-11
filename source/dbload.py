import json 
from datetime import datetime

import psycopg2
import pandas as pd

import common
import config

def set_sex(df):
    "If gender is M or F, set it to Male or Female, respectively.  Otherwise set to Unknown."""
    df.loc[( (df['gender'] != 'M') & (df['gender'] != 'F') ), 'gender'] = 'Unknown'
    df.loc[(df['gender']=='M'),'gender'] = 'Male'
    df.loc[(df['gender']=='F'),'gender'] = 'Female'
    return df

def format_date_of_birth(df):
    """Convert date_of_birth from a string to a datetime object."""
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    return df

def set_ethnicity(df):
    ethnicity_map = {'1':'White', '2':'Hispanic', '3':'Black', '4':'Asian or Pacific Islander',
                     '5':'Alaska Native or American Indian', '7':'Filipino', '8':'Unknown',
                     '9':'Unknown', 'A':'Ameriasian', 'C':'Chinese', 'H':'Cambodian', 
                     'J':'Japanese', 'K':'Korean', 'N':'Asian Indian', 'P':'Hawaiian',
                     'R':'Guamanian', 'L':'Laotian', 'V':'Vietnamese', 'Z':'Other', 
                     None:'Unknown'}
    df.loc[:,'ethnicity_code'] = df['ethnicity_code'].map(ethnicity_map)
    return df

def set_language(df):
    language_map = {'B': 'Chinese', 'P': 'Portugese', 'A': 'Other Sign', 'D': 'Cambodian', 
                    '2': 'Cantonese', 'N': 'Russian', None: 'Unknown', '1': 'Spanish', 
                    '3': 'Japanese', 'G': 'Mien', '4': 'Korean', '5': 'Tagalog', 
                    'C': 'Other Chinese', 'V': 'Vietnamese', '0': 'American Sign', 
                    '7': 'English', 'S': 'Samoan', 'J': 'Hebrew', 'U': 'Farsi', 
                    'R': 'Arabic', 'Q': 'Italian', 'M': 'Polish', 'F': 'Llacano', 
                    '9': 'Unknown', '8': 'Unknown', 'I': 'Lao', 'H': 'Hmong', '6': 'Other', 
                    'T': 'Thai', 'K': 'French', 'E': 'Armenian'}
    df.loc[:,'language_code'] = df['language_code'].map(language_map)
    return df

def create_staging_tables():
    sql = """CREATE TEMP TABLE "staging_attributes" (
       -- (Tested, works)
       -- cin = client index number
       -- hic = health insurance claim
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "date_of_birth" DATE,
       "meds_id" TEXT,
       "hic_number" TEXT, 
       "hic_suffix" TEXT,
       "ethnicity" TEXT, --Make table to constrain to. Store English term, not code.
       "sex" SEX_ENUM, 
       "primary_language" TEXT, --Make table to constrain to. Store English term, not code.
       CONSTRAINT staging_attributes_CK_cin_length CHECK (char_length(cin) <= 9),
       CONSTRAINT staging_attributes_CK_meds_id_length CHECK (char_length(meds_id) <= 9),
       CONSTRAINT staging_attributes_CK_hic_number_length CHECK (char_length(hic_number) <= 9),
       CONSTRAINT staging_attributes_CK_hic_suffix_length CHECK (char_length(hic_suffix) <= 2),
       CONSTRAINT staging_attributes_CK_date CHECK 
       		  (date_of_birth > to_date('1895-01-01','YYYY-MM-DD')),
       CONSTRAINT staging_attributes_UQ_cin UNIQUE (cin)
);

CREATE TEMP TABLE "staging_names" (
       -- (Tested, works)
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source" TEXT,
       "source_date" DATE,
       "first_name" TEXT,
       "middle_name" TEXT,
       "last_name" TEXT,
       "middle_initial" TEXT,
       "full_name" TEXT,
       "suffix" TEXT,
       CONSTRAINT staging_names_FK_cin FOREIGN KEY (cin)
       		  REFERENCES staging_attributes (cin) ON DELETE RESTRICT
);

CREATE TEMP TABLE "staging_addresses" (
       -- (Tested, works)
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "street" TEXT,
       "unit" TEXT,
       "city" TEXT,
       "state" TEXT, --Constrain to list?
       "zip" TEXT, --How to deal with zip+4?
       "raw" TEXT, --Unparsed address.
       "source" TEXT,
       CONSTRAINT staging_addresses_FK_cin FOREIGN KEY (cin)
       		  REFERENCES staging_attributes (cin) ON DELETE RESTRICT       
);
"""
    cur.execute(sql)
    
def convert_nans_to_nones(df, df_columns):
    """Set np.nan to None because psycopg2 doesn't correctly convert np.nan."""
    df.loc[:,df_columns] = df[df_columns].where(pd.notnull((df[df_columns])), None)
    return df

def populate_staging_attributes(df):
    df = set_sex(df)
    df = format_date_of_birth(df)
    df = set_ethnicity(df)
    df = set_language(df)

    df_columns = ['cin', 'date_of_birth', 'meds_id', 'hic_number', 
                  'hic_suffix', 'ethnicity_code', 'gender', 'language_code']

    df = convert_nans_to_nones(df, df_columns)
    
    sql = """INSERT INTO staging_attributes 
             (cin, date_of_birth, meds_id, hic_number, hic_suffix, ethnicity, sex, primary_language) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cur.executemany(sql, df[df_columns].values)

def populate_staging_names(df):
    df_columns = ['cin', 'first_name', 'middle_initial', 'last_name', 'name_suffix', 'source_date', 'source']

    df = convert_nans_to_nones(df, df_columns)

    sql = """INSERT INTO staging_names
             (cin, first_name, middle_initial, last_name, suffix, source_date, source)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    cur.executemany(sql, df[df_columns].values)
        
def create_source_date_column(df):
    source_date = datetime(int(df['eligibility_year_0'][df.index[0]]),
                           int(df['eligibility_month_0'][df.index[0]]), 1)
    df['source_date'] = source_date
    return df

def create_source_column(df):
    df['source'] = 'Medi-Cal'
    return df

def populate_staging_addresses(df):

    df_columns = ['cin', 'address_line_1', 'address_line_2', 'address_state',
                  'address_city', 'address_zip_code', 'source_date', 'source']

    df = convert_nans_to_nones(df, df_columns)
    
    sql = """INSERT INTO staging_addresses
             (cin, street, unit, state, city, zip, source_date, source)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    cur.executemany(sql, df[df_columns].values)

def populate_new_cins_table():
    """Create and populate new_cins table.  This table contains all cins that
    are in staging_attributes that aren't in client_attributes."""
    
    create = """
             --Create table for CINs that aren't in the database.
             CREATE TEMP TABLE new_cins (
             "id" SERIAL PRIMARY KEY,
             "cin" TEXT NOT NULL UNIQUE
             );"""
    
    populate = """
             --Populate new_cins table. (Tested, works)
             INSERT INTO new_cins (cin)
             SELECT S.cin
             FROM client_attributes C
                 RIGHT OUTER JOIN staging_attributes S
                 ON C.cin = S.cin
             WHERE C.id IS NULL
             ;"""

    cur.execute(create)
    cur.execute(populate)
        
def update_existing_client_attributes():
    pass

def update_client_names():
    """For existing clients if the name fields have changed add a new entry.
    For new clients add a new entry."""
    pass

def insert_new_client_names():
    sql = """
          --Insert names for new clients
          INSERT INTO client_names
              (cin, source_date, first_name, middle_initial, last_name)
          SELECT S.cin, source_date AS creation_date, first_name, middle_initial, last_name
          FROM new_cins N
              INNER JOIN staging_names S
              ON N.cin = S.cin;"""

    cur.execute(sql)

def insert_new_client_addresses():
    sql = """
          --Insert address for new clients.
          INSERT INTO client_addresses
              (cin, source_date, street, unit, city, state, zip, raw)
          SELECT S.cin, source_date, street, unit, city, state, zip, raw
          FROM new_cins N
              INNER JOIN staging_addresses S
              ON N.cin = S.cin;"""
    
    cur.execute(sql)
        
def insert_new_client_attributes():
    sql = """--Insert attributes for new clients
          INSERT INTO client_attributes
              (cin, date_of_birth, meds_id, hic_number, 
               hic_suffix, ethnicity, sex, primary_language)
          SELECT S.cin, S.date_of_birth, S.meds_id, S.hic_number, S.hic_suffix, 
              S.ethnicity, S.sex, S.primary_language
          FROM new_cins N
              INNER JOIN staging_attributes S
              ON N.cin = S.cin;"""

    cur.execute(sql)

def insert_client_eligibility_base(df, chunk_number):
    #cin,medical_date,resident_county,soc_amount,medicare_status,carrier_code,
    #federal_contract_number,plan_id,plan_type,surs_code,special_obligation,healthy_families_date
    df_columns = ['cin', 'source_date', 'resident_county', 'share_of_cost_amount',
                  'medicare_status', 'carrier_code', 'federal_contract_number', 'plan_id',
                  'plan_type', 'surs_code', 'special_obligation', 'healthy_families_date',
                  'eligibility_date']

    df = convert_nans_to_nones(df, df_columns)

    sql = """
          INSERT INTO client_eligibility_base
              (cin, source_date, resident_county, soc_amount, medicare_status, carrier_code, 
               federal_contract_number, plan_id, plan_type, surs_code, special_obligation,
               healthy_families_date, eligibility_date)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    
    try:
        cur.executemany(sql, df[df_columns].values)
    except psycopg2.IntegrityError as e:
        if e.pgcode == '23505':
            print('Some eligibility_base rows in chunk {} have already been inserted'.format(chunk_number))
            conn.commit()
        else:
            raise e
    finally:
        conn.commit()
        
def insert_client_eligibility_status(dw):
    eligibility_status_columns = ['cin', 'source_date', 'eligibility_date', 'cardinal', 'aidcode',
                  'eligibility_status', 'responsible_county']

    dw = convert_nans_to_nones(dw, eligibility_status_columns)

    sql = """
          INSERT INTO client_eligibility_status
              (cin, source_date, eligibility_date, cardinal, aidcode, eligibility_status,
               responsible_county)
          VALUES (%s, %s, %s, %s, %s, %s, %s); """
    
    try:
        cur.executemany(sql, dw[eligibility_status_columns].values)
    except psycopg2.IntegrityError as e:
        if e.pgcode == '23505':
            print('Some eligibility_status rows in chunk {} have already been inserted'.format(chunk_number))
            conn.commit()
        else:
            raise e
    finally:
        conn.commit()
       
def create_eligibility_date_column(df):
    df['eligibility_date'] = pd.to_datetime(df['eligibility_year'] + df['eligibility_month'] + '01')
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

def insert_client_hcp_status(dw):
    df_columns = ['cin', 'source_date', 'eligibility_date', 'health_care_plan_status',
                  'health_care_plan_code', 'cardinal']

    dw = convert_nans_to_nones(dw, df_columns)
    
    sql = """
          INSERT INTO client_hcp_status
          (cin, source_date, eligibility_date, hcp_status, hcp_code, cardinal)
          VAlUES (%s, %s, %s, %s, %s, %s); """

    try:
        cur.executemany(sql, dw[df_columns].values)
    except psycopg2.IntegrityError as e:
        if e.pgcode == '23505':
            print('Some hcp_status rows in chunk {} have already been inserted'.format(chunk_number))
        else:
            raise e
    finally:
        conn.commit()            

def wide_to_long_by_month(df, stubs):
    df = pd.wide_to_long(df, stubs, 'cin', 'j')
    df = df.reset_index()
    return df

def get_aidcode_info():
    """Get data from info_aidcodes table and put it into df_aidcodes"""
    
    sql = """
          SELECT aidcode, federal_financial_participation, fully_covered, disabled, foster
          FROM aidcodes """

    cur.execute(sql)
    records = cur.fetchall()
    df_aidcodes = pd.DataFrame(data = records,
                               columns = ['aidcode', 'ffp', 'full', 'disabled', 'foster'])
    return df_aidcodes

def make_eligibility_bitmask(dw):
    elig = dw['eligibility_status'].dropna().str[0].astype(int).le(5).reindex(
        index = dw.index, fill_value = False) 
    return elig

def make_local_bitmask(dw):
    return dw['responsible_county'].dropna().eq('01').reindex(index = dw.index, fill_value = False)

def make_covered_bitmask(dw):
    return dw['full'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def make_disabled_bitmask(dw):
    return dw['disabled'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def make_foster_bitmask(dw):
    return dw['foster'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def merge_aidcode_info(dw, df_aidcodes):
    """Merge in aidcode based info: foster, disabled, full, ffp."""
    dw = dw.merge(df_aidcodes, how = 'left')
    return dw

def mcrank(dw, elig, local, covered):
    """Create Medi-Cal ranks."""
    #Done in this order so worse ranks don't overwrite better ones.
    dw['mcrank'] = ((dw['aidcode'].notnull()) & (dw['ffp'] >= 1)).map({True:13})
    dw.loc[elig,'mcrank'] = dw['ffp'][elig].map({100:10, 65:11, 50:12})
    dw.loc[(elig & local), 'mcrank'] = dw['ffp'][elig & local].map({100:7, 65:8, 50:9})
    dw.loc[(elig & covered), 'mcrank'] = dw['ffp'][elig & covered].map({100:4, 65:5, 50:6})
    dw.loc[(elig & local & covered), 'mcrank'] = dw['ffp'][elig & local & covered].\
                                                 map({100:1, 65:2, 50:3})
    dw['mcrank'] = dw['mcrank'].fillna(14)
    return dw

def make_primary_codes(dw, elig):
    """Set primary_aid_code equal to aidcode and eligibility_county_code equal to respcounty."""
    dw.loc[elig, 'primary_aidcode'] = dw['aidcode'][elig]
    dw.loc[elig, 'eligibility_county_code'] = dw['responsible_county'][elig]
    return dw

def make_disabled_column(dw, elig, disabled):
    dw['disabled'] = (elig & disabled)
    dw.loc[:,'disabled'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['disabled'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'disabled_r']
    return dw

def make_foster_column(dw, elig, foster):
    dw['foster'] = (elig & foster)
    dw.loc[:,'foster'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['foster'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'foster_r']
    return dw

def make_retromc_column(dw):
    """If the last character of the primary_Aid_Code is 2,3, or 5 set RetroMC to 1."""
    dw['retromc'] = dw['primary_aidcode'].dropna().str[-1].isin(['2','3','5'])
    dw.loc[:,'retromc'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['retromc'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'retromc_r']
    return dw

def make_ssi_column(dw, ssicodes):
    """If any aidcode in row is in ssicodes set ssi to '1'."""
    dw['ssi'] = dw['aidcode'].isin(ssicodes)
    dw.loc[:,'ssi'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['ssi'], 
                              on=['cin','eligibility_date'], rsuffix='_r').loc[:,'ssi_r']
    return dw

def make_ccsaidcode_column(dw, ccscodes):
    """If any aidcode in row is in ccscodes set ccsaidcode to '1'."""
    dw['ccsaidcode'] = dw['aidcode'].isin(ccscodes)
    dw.loc[:,'ccsaidcode'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['ccsaidcode'], 
                                     on=['cin','eligibility_date'], rsuffix='_r').loc[:,'ccsaidcode_r']
    return dw

def make_ihssaidcode_column(dw, ihsscodes):
    """If any aidcode in row is in ihsscodes set ihssaidcode to '1'."""
    dw['ihssaidcode'] = dw['aidcode'].isin(ihsscodes)
    dw.loc[:,'ihssaidcode'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['ihssaidcode'], 
                                      on=['cin','eligibility_date'], rsuffix='_r').loc[:,'ihssaidcode_r']
    return dw

def make_socmc_column(dw):
    """If the last character of any eligibility status in row is 1, set socmc to '1'."""
    dw['socmc'] = dw['eligibility_status'].dropna().str[-1].astype(int).eq(1)
    dw.loc[:,'socmc'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['socmc'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'socmc_r']
    return dw

def insert_client_derived_status(df):
    sql = """INSERT INTO client_derived_status
          (cin, source_date, eligibility_date, rank, primary_aidcode, disabled,
           foster, retro, ssi, ccs, ihss, soc)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    client_derived_columns = ['cin', 'source_date', 'eligibility_date', 'mcrank',
                              'primary_aidcode', 'disabled', 'foster', 'retromc',
                              'ssi', 'ccsaidcode', 'ihssaidcode', 'socmc']

    df = convert_nans_to_nones(df, client_derived_columns)
    cur.executemany(sql, df[client_derived_columns].values)

def keep_best_mcrank(dw):
    """Groupby cin and calendar and keep only the row with the best mcrank for each group."""
    dw = dw.sort('mcrank', ascending = True).groupby(['cin', 'eligibility_date']).first()
    dw['cin'] = dw.index.get_level_values('cin')
    dw['eligibility_date'] = dw.index.get_level_values('eligibility_date')
    return dw

def no_nulls(dw):
    no_null_cols = ['disabled', 'foster', 'retromc', 'ssi', 'ccsaidcode', 'ihssaidcode', 'socmc']
    dw.loc[:,no_null_cols] = dw[no_null_cols].fillna(False)
    return dw

def process_chunk(df, chunk_number, chunksize, dupemask):
    df = common.drop_duplicate_rows(df, chunk_number, chunksize, dupemask)
    df = create_source_date_column(df)
    df = create_source_column(df)
    create_staging_tables()
    populate_staging_attributes(df)
    populate_staging_names(df)
    populate_staging_addresses(df)
    populate_new_cins_table()
    conn.commit()
    #update_existing_client_attributes()
    insert_new_client_attributes()
    #update_client_names()
    insert_new_client_names()
    #update_client_addresses()
    insert_new_client_addresses()
    conn.commit()
    
    df = wide_to_long_by_month(df, month_stubs)
    df = create_eligibility_date_column(df)
    insert_client_eligibility_base(df, chunk_number)
    conn.commit()

    dw = wide_to_long(df, hcp_stubs)
    insert_client_hcp_status(dw)
    conn.commit()
    del dw
    
    dw = wide_to_long(df, aidcode_stubs)
    insert_client_eligibility_status(dw)
    conn.commit()

    df_aidcodes = get_aidcode_info()
    dw = merge_aidcode_info(dw, df_aidcodes)

    elig = make_eligibility_bitmask(dw)
    local = make_local_bitmask(dw)
    covered = make_covered_bitmask(dw)
    disabled = make_disabled_bitmask(dw)
    foster = make_foster_bitmask(dw)

    dw = mcrank(dw, elig, local, covered)    
    
    dw = make_primary_codes(dw, elig)
    dw = make_disabled_column(dw, elig, disabled)
    dw = make_foster_column(dw, elig, foster)
    dw = make_retromc_column(dw)
    dw = make_ssi_column(dw, ssicodes)
    dw = make_ccsaidcode_column(dw, ccscodes)
    dw = make_ihssaidcode_column(dw, ihsscodes)
    dw = make_socmc_column(dw)

    dw = keep_best_mcrank(dw)
    dw = no_nulls(dw)

    insert_client_derived_status(dw)

    
if __name__ == "__main__":
    #Aidcodes that indicate specific statuses.
    ssicodes = ['10','20','60']
    ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
    ihsscodes = ['2L','2M','2N']

    aidcode_stubs = ['aidcode', 'eligibility_status', 'responsible_county']
    
    hcp_stubs = ['health_care_plan_status', 'health_care_plan_code']
    
    month_stubs = ["eligibility_year", "eligibility_month", "aidcode_sp0",
                   "responsible_county_sp0", "resident_county", "eligibility_status_sp0",
                   "share_of_cost_amount", "medicare_status", "carrier_code", 
                   "federal_contract_number", "plan_id", "plan_type",
                   "health_care_plan_status_s0", "health_care_plan_code_s0",
                   "other_health_coverage", "surs_code", "aidcode_sp1", 
                   "responsible_county_sp1", "eligibility_status_sp1", "aidcode_sp2",
                   "responsible_county_sp2", "eligibility_status_sp2", "special_obligation",
                   "healthy_families_date", "aidcode_sp3", "responsible_county_sp3",
                   "eligibility_status_sp3", "health_care_plan_status_s1",
                   "health_care_plan_code_s1", "health_care_plan_status_s2", 
                   "health_care_plan_code_s2"]
    
    medical_file = config.medical_file

    #Create bitmask used to remove duplicate rows and rows without a CIN.
    dupemask = common.make_duplicates_bitmask(medical_file)

    #column_names and column_specifications are used by pandas.read_fwf to read Medi-Cal file.
    with open(config.db_load_info) as f:
        column_names, column_specifications, _ = zip(*json.load(f))

    #Create an iterator to read chunks of the fixed width Medi-Cal file.
    chunksize = config.chunk_size
    chunked_data_iterator = pd.read_fwf(medical_file,
                                        colspecs = column_specifications, 
                                        names = column_names, 
                                        converters = {name:str for name in column_names}, 
                                        iterator = True,
                                        chunksize = chunksize)

    for chunk_number, chunk in enumerate(chunked_data_iterator):
        with psycopg2.connect(database="medical", user='greg') as conn:
            with conn.cursor() as cur:
                process_chunk(chunk, chunk_number, chunksize, dupemask)

