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

    with conn.cursor() as cur:
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

    with conn.cursor() as cur:        
        cur.executemany(sql, df[df_columns].values)

def populate_staging_names(df):
    df_columns = ['cin', 'first_name', 'middle_initial', 'last_name', 'name_suffix', 'source_date', 'source']

    df = convert_nans_to_nones(df, df_columns)

    sql = """INSERT INTO staging_names
             (cin, first_name, middle_initial, last_name, suffix, source_date, source)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    with conn.cursor() as cur:
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

    with conn.cursor() as cur:
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

    with conn.cursor() as cur:
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
              (cin, creation_date, first_name, middle_initial, last_name)
          SELECT S.cin, source_date AS creation_date, first_name, middle_initial, last_name
          FROM new_cins N
              INNER JOIN staging_names S
              ON N.cin = S.cin
          ;"""

    with conn.cursor() as cur:
        cur.execute(sql)

def insert_new_client_addresses():
    sql = """
          --Insert address for new clients.
          INSERT INTO client_addresses
              (cin, creation_date, street, unit, city, state, zip, raw)
          SELECT S.cin, source_date, street, unit, city, state, zip, raw
          FROM new_cins N
              INNER JOIN staging_addresses S
              ON N.cin = S.cin
          ;"""
    
    with conn.cursor() as cur:
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
              ON N.cin = S.cin
          ;"""
    
    with conn.cursor() as cur:
        cur.execute(sql)

def insert_client_eligibility_base(df):
    #cin,medical_date,resident_county,soc_amount,medicare_status,carrier_code,
    #federal_contract_number,plan_id,plan_type,surs_code,special_obligation,healthy_families_date
    df_columns = ['cin', 'source_date', 'resident_county', 'share_of_cost_amount', 'medicare_status',
                  'carrier_code', 'federal_contract_number', 'plan_id', 'plan_type', 'surs_code',
                  'special_obligation', 'healthy_families_date']

    df = convert_nans_to_nones(df, df_columns)

    sql = """
          INSERT INTO client_eligibility_base
              (cin, medical_date, resident_county, soc_amount, medicare_status, carrier_code, 
               federal_contract_number, plan_id, plan_type, surs_code, special_obligation,
               healthy_families_date)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    with conn.cursor() as cur:
        cur.executemany(sql, df[df_columns].values)

def create_eligibility_date_column(df):
    df['eligibility_date'] = pd.to_datetime(df['eligibility_year'] + df['eligibility_month'] + '01')
    return df
        
def process_chunk(df, chunk_number, chunksize, dupemask):
    df = common.drop_duplicate_rows(df, chunk_number, chunksize, dupemask)
    df = create_source_date_column(df)
    df = create_source_column(df)
    create_staging_tables()
    populate_staging_attributes(df)
    populate_staging_names(df)
    populate_staging_addresses(df)
    populate_new_cins_table()
    #update_existing_client_attributes()
    insert_new_client_attributes()
    #update_client_names()
    insert_new_client_names()
    #update_client_addresses()
    insert_new_client_addresses()
    df = common.wide_to_long_by_month(df, stubs)
    create_eligibility_date_column(df)
    df = insert_client_eligibility_base(df)
    #dw = common.wide_to_long_by_aidcode(df)
    #insert_client_eligibility_status()
    #dw = wide_to_long_by_hcp(df)
    #insert_client_hcp_status()

if __name__ == "__main__":

    stubs = ["eligibility_year", "eligibility_month", "aidcode_sp0",
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
            process_chunk(chunk, chunk_number, chunksize, dupemask)

