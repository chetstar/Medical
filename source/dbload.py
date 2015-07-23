import json 

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
       "date" DATE,
       "first_name" TEXT,
       "middle_name" TEXT,
       "last_name" TEXT,
       "middle_initial" TEXT,
       "full_name" TEXT,
       CONSTRAINT staging_names_FK_cin FOREIGN KEY (cin)
       		  REFERENCES staging_attributes (cin) ON DELETE RESTRICT
);

CREATE TEMP TABLE "staging_addresses" (
       -- (Tested, works)
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "date" DATE NOT NULL,
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
    
def populate_staging_attributes(df):
    df = set_sex(df)
    df = format_date_of_birth(df)
    df = set_ethnicity(df)
    df = set_language(df)

    df_columns = ['cin', 'date_of_birth', 'meds_id', 'hic_number', 
                  'hic_suffix', 'ethnicity_code', 'gender', 'language_code']

    df = convert_nans_to_nones(df, df_columns)
    #source, creation_date
    sql = """INSERT INTO staging_attributes 
             (cin, date_of_birth, meds_id, hic_number, hic_suffix, ethnicity, sex, primary_language) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    with conn.cursor() as cur:        
        cur.executemany(sql, df[df_columns].values)

def populate_staging_names(df):
    df_columns = ['cin', 'first_name', 'middle_initial', 'last_name', 'name_suffix']
    #souce, creation_date
    df = convert_nans_to_nones(df, df_columns)

    sql = """INSERT INTO staging_names
             (cin, first_name, middle_initial, last_name, suffix)
             VALUES (%s, %s, %s, %s, %s, %s)"""

    with conn.cursor() as cur:
        cur.executemany(sql, df[df_columns].values)

def populate_staging_addresses(df):
    #df_columns = ['cin', 'street', 'unit', 'state', 'city', 'zip']

    sql = """INSERT INTO staging_addresses
             (cin, street, unit, state, city, zip, raw)
             VALUES (%s, %s, %s, %s, %s, %s)"""

    with conn.cursor() as cur:
        cur.executemany(sql, df[df_columns].values)

def populate_new_cins_table():
    """Create and populate new_cins table.  This table contains all cins that
    are in staging_attributes that aren't in client_attributes."""
    
    sql = """--Create table for CINs that aren't in the database.
             CREATE TEMP TABLE new_cins (
             "id" SERIAL PRIMARY KEY,
             "cin" TEXT NOT NULL UNIQUE
             );

             --Populate new_cins table. (Tested, works)
             INSERT INTO new_cins (cin)
             SELECT S.cin
             FROM client_attributes C
                 RIGHT OUTER JOIN staging_attributes S
                 ON C.cin = S.cin
             WHERE C.id IS NULL
             ;"""
    with conn.cursor() as cur:
        cur.execute(sql)

def process_chunk(chunk):
    create_staging_tables()
    populate_staging_attributes()
    populate_staging_names()
    populate_staging_addresses()
    create_new_cins_table()
    update_client_attributes()
    update_client_names()
    update_client_addresses()
    update_client_eligibility_base()
    update_client_eligibility_status()
    update_client_hcp_status()

if __name__ == "__main__":

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

    
    for i, chunk in enumerate(chunked_data_iterator):
        with psycopg2.connect(database="medical", user='irisweiss') as conn:
            update_client_attributes(chunk)

