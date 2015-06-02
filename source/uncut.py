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

#Load column_info.json into column_info.  This is a list of lists.                                 
with open('uncut_columns.json') as f:
    column_info = json.load(f)

#Bring in city_names_list from city_names.json
with open('city_names.json') as f:
    city_name_list = json.load(f)

#column_names and column_specifications are used by pandas.read_fwf to read in the Medi-Cal file. 
column_names, column_specifications = zip(*column_info)

#All columns should be brought in as strings.
converters = {name:str for name in column_names}

df = pd.read_fwf(config.medical_file,
                 colspecs = column_specifications,
                 header = None,
                 names = column_names, 
                 converters = converters )

#Code to delete the last row if its a summary row.
df = df.drop(df.index[-1])

#Drop all rows without a CIN.
df.dropna(subset = ['cin'], inplace = True)
print('cin-less rows dropped at: {}'.format(datetime.datetime.now()))

#Remove duplicate rows keeping the row with the best eligibilityStatus. 
df.sort(['cin','eligibilitystatus'], inplace = True)
df.drop_duplicates(subset = 'cin', inplace = True)
print('Duplicate rows removed at: {}'.format(datetime.datetime.now()))

#Wrap extractOne so that we can use it with apply and get back only a city name.
def extractOne_wrapper(city, city_name_list):
    """Returns the first item of the tuple retruned by fuzzywuzzy.process.extractOne"""
    return process.extractOne(city, city_name_list)[0]

#Fix mispelt city names.
df['city'] = df['city'].replace(city_map)
if (-df['city'].isin(city_name_list)).any(): #If ANY city is NOT in the city_name_list
    df['city'] = df['city'].apply(
        lambda x: process.extractOne(x, city_name_list)[0])
print('City name misspellings fixed at: {}'.format(datetime.datetime.now()))

#create calendar and bday columns.
df['calendar'] = pd.to_datetime(df['eligyear'] + df['eligmonth'], format = '%Y%m')
df['bday'] = pd.to_datetime(df['year'] + df['month'] + df['day'], format = '%Y%m%d')

#create hcplantext column and populate with hcpcode data.
df['hcplantext'] = df['hcpcode'].map(hcpcode_map)
#create language column and populate with the codes from lang.
df['language'] = df['lang'].map(language_map)
#create ethnicity column and populate with codes from race.
df['ethnicity'] = df['race'].map(ethnicity_map)
#create region and populate by matching citynames to the region they're in.
df['region'] = df['city'].map(region_map)

#If someone has an HCplanText but their HCPstatus is such that it is invalidated, change
#HCplanText to "z No Plan"
df.ix[df.hcpstatus.isin(["00","10","09","19","40","49","s0","s9"]),'hcplantext'] = "z No Plan"

#These are the columns that need to be saved into the .sav file.
columns_to_save = ['casename', 'respcounty', 'language', 'calendar', 'ssn', 'sex', 'ethnicity',
                   'street', 'state', 'zip', 'cin', 'bday', 'fname', 'lname', 'suffix',
                   'middleinitial', 'city', 'aidcode', 'ohc', 'socamount', 'eligibilitystatus',
                   'hcplantext', 'rescounty', 'govt', 'countycasecode', 'countyaidcode', 
                   'countycaseid', 'medicarestatus', 'hic', 'carriercode', 
                   'federalcontractnumber', 'planid', 'typeid', 'hcpstatus', 'hcpcode', 
                   'region', 'aidcodesp1', 'respcountysp1', 'eligibilitystatussp1', 
                   'aidcodesp2', 'respcountysp2', 'eligibilitystatussp2', 'aidcodesp3',
                   'respcountysp3', 'eligibilitystatussp3']

var_types = {column:20 for column in columns_to_save}

with SavWriter(config.uncut_file, columns_to_save, var_types, ioUtf8 = True) as writer:
    writer.writerows(df[columns_to_save].values)





