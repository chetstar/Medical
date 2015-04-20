import json

import numpy as np
import pandas as pd
from fuzzywuzzy import process

import config
from medical_meta import (translation_dictionary, 
                          column_names, 
                          column_specifications, 
                          variable_types,
                          variable_formats,
                          converters)
from savReaderWriter import SavWriter

def load_medical_data(file_location):
    df = pd.read_fwf(file_location,
                     colspecs = column_specifications,
                     header = None,
                     names = column_names, 
                     keep_date_col = True,
                     converters = converters)
    return df

def create_sav_file(file_name, dataframe, columns_to_save, new_types, new_formats):

    var_types = variable_types
    var_formats = variable_formats

    #Update dictionaries to merge in meta-data for new columns.
    var_types.update(new_types)
    var_formats.update(new_formats)
    
    #Remove key value pairs where the key is not in columns_to_save. This must be
    #done because SavWriter will choke if there is an item in types/formats dictionaries
    #that is not in the list of columns to save.
    var_types = { column: var_types[column] for column in columns_to_save if 
                       var_types.get(column) != None}
    var_formats = { column: var_formats[column] for column in columns_to_save if 
                         var_formats.get(column) != None}

    with SavWriter(file_name, columns_to_save, var_types, formats = var_formats, 
                   ioUtf8 = True) as writer:

        #Convert from python datetime objects to spssDateTime.
        dataframe['calendar'] = dataframe['calendar'].apply(writer.spssDateTime,args=('%Y-%m-%d',))
        dataframe['bday'] = dataframe['bday'].apply(writer.spssDateTime, args = ('%Y-%m-%d',))

        for row in map(list, dataframe[columns_to_save].values):
            writer.writerow(row)

    print('File {} created.'.format(file_name))

def clean_medical_data(df):
    """Fix mispelt cities, drop duplicate rows and drop rows with no CIN"""

    #Drop all rows without a CIN.
    df.dropna(subset=['CIN'], inplace=True)

    #Remove duplicate rows keeping the row with the best eligibilityStatus. 
    df.sort(['CIN','EligibilityStatus'], inplace=True)
    df.drop_duplicates(subset='CIN', inplace=True)

    #Wrap extractOne so that we can use it with apply and get back only a city name.
    def extractOne_wrapper(city, city_name_list):
        """Returns the first item of the tuple retruned by fuzzywuzzy.process.extractOne"""
        return process.extractOne(city, city_name_list)[0]

    #Bring in city_names_list from city_names.json
    with open('city_names.json') as f:
        city_name_list = json.load(f)

    #Fix mispelt city names. city_names 
    df['city'] = df['city'].apply(extractOne_wrapper, args = (city_name_list,))

    return df

def add_supplementary_columns(df):
    """Add calendar, bday, HCplanText, language, ethnicity and region columns"""

    #Create calendar and bday columns.
    df['calendar'] = pd.to_datetime(df['eligYear']*100 + df['eligMonth'], format='%Y%m')
    df['bday'] = pd.to_datetime(df['year'] + df['month'] + df['day'], format='%Y%m%d')

    #Create HCplanText column and populate with HCPcode data.
    df['HCplanText'] = df['HCPcode']
    #Create language column and populate with the codes from lang.
    df['language'] = df['lang']
    #Create ethnicity column and populate with codes from race.
    df['ethnicity'] = df['race']
    #Create region column and populate with city names.
    df['region']= df['city']

    #Replace the numeric codes in HCplanText, ethnicity, and language with their text equivalent.
    #Also replace the cities in the region with the region that city is in.
    df.replace(to_replace=translation_dictionary, inplace=True)

    #If someone has an HCplanText but their HCPstatus is such that it is invalidated, change
    #HCplanText to "z No Plan"
    df.ix[df.HCPstatus.isin(["00","10","09","19","40","49","S0","S9"]),'HCplanText']="z No Plan"

    return df

def create_meds_current_uncut(df):
    """Create the SPSS .sav file medsCurrentUncut.sav."""

    #These are the columns that need to be saved into the .sav file.
    columns_to_save = ['CaseName', 'RespCounty', 'language', 'calendar', 'ssn', 'sex', 'ethnicity',
                       'street', 'state', 'zip', 'CIN', 'bday', 'fname', 'lname', 'suffix',
                       'middleInitial', 'city', 'AidCode', 'OHC', 'SOCamount', 'EligibilityStatus',
                       'HCplanText', 'ResCounty', 'GOVT', 'CountyCaseCode', 'CountyAidCode', 
                       'CountyCaseID', 'MedicareStatus', 'HIC', 'CarrierCode', 
                       'FederalContractNumber', 'PlanID', 'TypeID', 'HCPstatus', 'HCPcode', 
                       'region', 'AidCodeSP1', 'RespCountySP1', 'EligibilityStatusSP1', 
                       'AidCodeSP2', 'RespCountySP2', 'EligibilityStatusSP2', 'AidCodeSP3',
                       'RespCountySP3', 'EligibilityStatusSP3']

    #These are types and formats of the new columns created in add_supplementary_columns)
    new_types = {'HCplanText':20, 'language':25, 'ethnicity':20, 'region':18, 'bday':0,
                 'calendar':0}
    new_formats = {'bday': 'DATE11', 'calendar':'MOYR6'}

    #Create an SPSS .sav file with the columns named in columns_to_save.
    create_sav_file(config.meds_current_uncut_file, df, columns_to_save, new_types, new_formats)

def is_eligible():
    if s['EligibilityStatus'][0] < 5:
        return True

def is_local():
    if s['RespCounty'] == config.local_county_code:
        return True

def is_covered():
    if s['Full'] == 1:
        return True

def ffp_ge_than(percentage):
    if s['Ffp'] >= percentage:
        return True

def create_medical_rank(s):
    """This function creates and populates a rank column depending on the eligibilityStatus, 
    RespCounty, full and ffp columns of the Medi-Cal data."""
    if   is_eligible() and is_local() and is_covered() and ffp_ge_than(100): s['rank'] = 1
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(65 ): s['rank'] = 2
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(50 ): s['rank'] = 3

    elif is_eligible() and is_covered() and ffp_ge_than(100): s['rank'] = 4
    elif is_eligible() and is_covered() and ffp_ge_than(65 ): s['rank'] = 5
    elif is_eligible() and is_covered() and ffp_ge_than(50 ): s['rank'] = 6

    elif is_eligible() and is_local() and ffp_ge_than(100): s['rank'] = 7
    elif is_eligible() and is_local() and ffp_ge_than(65 ): s['rank'] = 8
    elif is_eligible() and is_local() and ffp_ge_than(50 ): s['rank'] = 9

    elif is_eligible() and ffp_ge_than(100): s['rank'] = 10
    elif is_eligible() and ffp_ge_than(65 ): s['rank'] = 11
    elif is_eligible() and ffp_ge_than(50 ): s['rank'] = 12

    elif is_eligible() and AidCode and ffp_ge_than(1): s['rank'] = 13

    return s

def wide_to_long_by_month(df):

    #Drop all the 'v' columns.
    cols = [c for c in df.columns if c[0].lower() == 'v']
    df.drop(cols,axis=1,inplace=True)

    #Prepend x to AidCode, RespCount, and EligibilityStatus columns that do not have 'SP' in them.
    #Also remove all underscores in column names.
    #This step can not be skipped, wide_to_long will fail if it is.
    column_rename_dictionary = {}
    for c in df.columns:
        if ('AidCode' in c or 'RespCounty' in c or 'EligibilityStatus' in c) and 'SP' not in c:
            column_rename_dictionary.update({c:"x"+c})
        if '_' in c:
            b =unicode( str(c).translate(None,'_'))
            column_rename_dictionary.update({c:b})

    df.rename(columns=column_rename_dictionary, inplace=True)



    #print(column_rename_dictionary)

    df['id']=df.index
    stubs = ['eligYear', 
             'eligMonth',
             'xAidCode',
             'xRespCounty', 
             'ResCounty',
             'xEligibilityStatus',
             'SOCamount',
             'MedicareStatus', 
             'CarrierCode',
             'FederalContractNumber', 
             'PlanID',
             'TypeID',
             #'v16',
             'HCPstatus',
             'HCPcode',
             'OHC',
             #'v70',
             'AidCodeSP1', 
             'RespCountySP1',
             'EligibilityStatusSP1',
             'AidCodeSP2', 
             'RespCountySP2',
             'EligibilityStatusSP2', 
             'SOCpctSP',
             'HFEligDaySP',
             'AidCodeSP3', 
             'RespCountySP3',
             'EligibilityStatusSP3']

    df=pd.wide_to_long(df, stubs, i = 'id', j = 'varstocases')
    return df
