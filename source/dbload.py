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

def update_client_attributes(df):
    df = set_sex(df)
    df = format_date_of_birth(df)
    df = set_ethnicity(df)
    df = set_language(df)

    df_columns = ['cin', 'date_of_birth', 'meds_id', 'hic_number', 
                  'hic_suffix', 'ethnicity_code', 'gender', 'language_code']

    #Set np.nan to None because psycopg2 doesn't correctly convert np.nan.
    df.loc[:,df_columns] = df[df_columns].where(pd.notnull((df[df_columns])), None)

    sql = """INSERT INTO client_attributes 
    (cin, date_of_birth, meds_id, hic_number, hic_suffix, ethnicity, sex, primary_language) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    with conn.cursor() as cur:        
        cur.executemany(sql, df[df_columns].values)

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

    with psycopg2.connect(database="medical", user='irisweiss') as conn:
        for i, chunk in enumerate(chunked_data_iterator):
            update_client_attributes(chunk)

