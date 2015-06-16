import json
import datetime

from savReaderWriter import SavWriter #For saving SPSS .sav files.
import pandas as pd
from fuzzywuzzy import process #For spell checking city names.

import config

#These dictionaries are used to translate numeric codes into their English equivalents.
#Health care plan codes and names.
hcpcode_map = {'300':'Alliance', '340':'Blue Cross', '051':'Center for Elders',
                       '056':'ONLOK Seniors', '000':'z No Plan', None:'z No Plan'}

#Language codes and their respective languages.
language_map = {'B': 'Chinese', 'P': 'Portugese', 'A': 'Other Sign', 'D': 'Cambodian', 
                '2': 'Cantonese', 'N': 'Russian', None: 'Missing', '1': 'Spanish', 
                '3': 'Japanese', 'G': 'Mien', '4': 'Korean', '5': 'Tagalog', 
                'C': 'Other Chinese', 'V': 'Vietnamese', '0': 'American Sign', 
                '7': 'English', 'S': 'Samoan', 'J': 'Hebrew', 'U': 'Farsi', 
                'R': 'Arabic', 'Q': 'Italian', 'M': 'Polish', 'F': 'Llacano', 
                '9': 'Missing', '8': 'Missing', 'I': 'Lao', 'H': 'Hmong', '6': 'Other', 
                'T': 'Thai', 'K': 'French', 'E': 'Armenian'}

#Ethnicity codes and their respective catagories.
ethnicity_map = {'A': 'Asian/PI', 'C': 'Asian/PI', '0': 'Unknown', 'H': 'Asian/PI', 
                 'K': 'Asian/PI', 'J': 'Asian/PI', 'M': 'Asian/PI', 'N': 'Asian/PI', 
                 'P': 'Asian/PI', 'R': 'Asian/PI', '4': 'Asian/PI', '7': 'Asian/PI', 
                 'V': 'Asian/PI', '9': 'Unknown', '8': 'Unknown', 'T': 'Asian/PI',
                 '1': 'Caucasian', '2': 'Latino', '3': 'African American',
                 '5': 'Native American', 'Z': 'Other', None: 'Unknown'}

#Dictionary to set blank, NaN and Transient city values.
city_map = {'TRANSIENT':'HOMELESS', '':'UNKNOWN', None:'UNKNOWN'}

#Match city names to their respective regions.
region_map = {'ALAMEDA' :'1. North', 'ALBANY' :'1. North', 'BERKELEY' :'1. North',
              'OAKLAND' :'1. North', 'EMERYVILLE' :'1. North', 'PIEDMONT' :'1. North',
              'HAYWARD' :'2. Central', 'SAN LEANDRO' :'2. Central', 
              'SAN LORENZO' :'2. Central', 'CASTRO VALLEY' :'2. Central',
              'PLEASANTON' :'4. East', 'LIVERMORE' :'4. East', 'SUNOL' :'4. East',     
              'DUBLIN' :'4. East', 'UNION CITY' :'3. South', 'FREMONT' :'3. South', 
              'NEWARK' :'3. South', 'UNKNOWN' :'6. Unknown', None: '6. Unknown'}

#Bring in city_names_list from city_names.json
with open(config.city_names) as f:
    city_name_list = json.load(f)

def drop_summary_row(df):
    #Code to delete the last row if its a summary row.
    df.drop(df.index[-1], inplace = True)
    return df

def drop_cinless_rows(df):
    #Drop all rows without a CIN.
    df.dropna(subset = ['cin'], inplace = True)
    print('cin-less rows dropped at: {}'.format(datetime.datetime.now()))
    return df

def drop_duplicate_rows(df):
    #Remove duplicate rows keeping the row with the best eligibilityStatus. 
    df.sort(['cin','eligibilitystatus'], inplace = True)
    df.drop_duplicates(subset = 'cin', inplace = True)
    print('Duplicate rows removed at: {}'.format(datetime.datetime.now()))
    return df

def fix_city_names(df):
    #Fix mispelt city names.
    df['city'] = df['city'].replace(city_map)
    if (-df['city'].isin(city_name_list)).any(): #If ANY city is NOT in the city_name_list
        df['city'] = df['city'].apply(
            lambda x: process.extractOne(x, city_name_list)[0])
    print('City name misspellings fixed at: {}'.format(datetime.datetime.now()))
    return df

def make_calendar_column(df):
    df['calendar'] = writer.spssDateTime((df['eligyear'] + df['eligmonth']), '%Y%m')
    return df

def make_bday_column(df):
    df['bday'] = pd.to_datetime(df['year'] + df['month'] + df['day'], '%Y%m%d')
    return df

def make_hcplantext_column(df):
    #create hcplantext column and populate with hcpcode data.
    df['hcplantext'] = df['hcpcode'].map(hcpcode_map)
    return df

def make_language_column(df):
    #create language column and populate with the codes from lang.
    df['language'] = df['lang'].map(language_map)
    return df

def make_ethnicity_column(df):
    #create ethnicity column and populate with codes from race.
    df['ethnicity'] = df['race'].map(ethnicity_map)
    return df

def make_region_column(df):
    #create region and populate by matching citynames to the region they're in.
    df['region'] = df['city'].map(region_map)
    return df

def fix_hcpstatus(df):
    #If someone has an HCplanText but their HCPstatus is such that it is invalidated, change
    #HCplanText to "z No Plan"
    df.ix[df.hcpstatus.isin(["00","10","09","19","40","49","S0","S9"]),'hcplantext'] = "z No Plan"
    df['hcplantext'].fillna('z No Plan')
    df = fix_hcpstatus(df)
    return df

def format_string_columns(df, save_info):
    """  SavWriter will translate NaNs in string columns to output the string 'NaN'. Since that
    isn't the desired output, replace each NaN in a string column with an empty string."""
    string_cols = [x for x in save_info['types'] if save_info['types'][x] > 0]
    df[string_cols] = df[string_cols].fillna('')
    return df

if __name__ == '__main__':

    #column_names and column_specifications are used by pandas.read_fwf to read Medi-Cal file.
    with open(config.uncut_load_info) as f:
        column_names, column_specifications = zip(*json.load(f))

    #All columns should be brought in as strings.
    converters = {name:str for name in column_names}

    df = pd.read_fwf(config.medical_file,
                     colspecs = column_specifications,
                     header = None,
                     names = column_names, 
                     converters = converters )


    with open('uncut_columns_save_info.json') as fp:
        save_info = json.load(fp)

    formats = {'ssn':'N9.0', 'zip':'N5.0', 'planid':'F3.0', 'govt':'F1.0', 'bday':'SDATE10',
               'calendar':'MOYR6'} 

    with SavWriter(config.uncut_file, save_info['column_names'], save_info['types'], 
                   measureLevels = save_info['measure_levels'],
                   alignments = save_info['alignment'],
                   columnWidths = save_info['column_width'], ioUtf8 = True) as writer:

        #Proccess Medi-Cal data.
        df = drop_summary_row(df) 
        df = drop_cinless_rows(df) 
        df = drop_duplicate_rows(df) 
        df = fix_city_names(df) 
        df = make_hcplantext_column(df) 
        df = make_language_column(df)
        df = make_ethnicity_column(df)
        df = make_region_column(df)
        df = format_string_columns(df, save_info)
        df = make_calendar_column(df) 
        df = make_bday_column(df) 
        writer.writerows(df[save_info['column_names']].values)

        



