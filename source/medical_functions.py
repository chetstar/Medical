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
    var_types = { column: var_types[column] for column in columns_to_save}
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
    
    #Bring in text form of aid codes.
    ccstext = pd.read_csv(config.csstext_file,header=0)
    aidcodesshort= pd.read_csv(config.aidcodes_file,header=0)

    #Merge in text form of aid codes.
    df = pd.merge(df, ccstext, how='left',left_on='AidCode',right_on='AidCode')
    df = pd.merge(df, aidcodesshort, how='left',left_on='AidCode',right_on='aidcode')

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

def wide_to_long_by_month(df):
    """Reshape the dataframe from wider to longer by month"""

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
             'HCPstatus',
             'HCPcode',
             'OHC',
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

    #Change the column names we had to change earlier back to their original values.
    column_rename_dictionary = {'xEligibilityStatus':'EligibilityStatus', 
                                'xRespCounty':'RespCounty',
                                'xAidCode':'AidCode'}
    df.rename(columns=column_rename_dictionary, inplace = True)

    #Reset the index so it isn't multilevel.
    df.reset_index(inplace=True)
    df['id'] = df.index

    #varstocases isn't needed, drop it.
    df.drop(['calendar', 'varstocases'], axis=1, inplace=True)
    
    #Drop rows that are missing an eligYear or eligMonth.
    df = df.dropna(subset=['eligYear','eligMonth'])
    df[['eligYear','eligMonth']] = df[['eligYear','eligMonth']].astype(int)
    df['calendar'] = pd.to_datetime(df.eligYear*100 + df.eligMonth, format='%Y%m')

    return df

def wide_to_long_by_aidcode(df):

    #These are the three types of columns to go wide to long on.
    stubs = ['EligibilityStatus','RespCounty','AidCode']

    df = pd.wide_to_long(df,stubs, i = 'id', j = 'varstocases')

    #The wide to long produces a multi-level index that we don't need, flatten it.
    df.reset_index(inplace = True)

    #The wide to long creates a varstocases columns we don't need, drop it.
    df.drop(['varstocases'], axis = 1, inplace = True)

    return df

def create_medical_rank(row):
    """This function creates and populates a rank column depending on the eligibilityStatus, 
    RespCounty, full and ffp columns of the Medi-Cal data."""

    def is_eligible():
        if str(row['EligibilityStatus']) == 'nan':
            return False
        elif int(str(row['EligibilityStatus'])[0]) < 5:
            return True

    def is_local():
        if row['RespCounty'] == config.local_county_code:
            return True

    def is_covered():
        if row['Full'] == '1':
            return True

    def ffp_ge_than(percentage):
        if row['FFP'] >= percentage:
            return True

    if   is_eligible() and is_local() and is_covered() and ffp_ge_than(100): row['mcrank'] = 1
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(65 ): row['mcrank'] = 2
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(50 ): row['mcrank'] = 3

    elif is_eligible() and is_covered() and ffp_ge_than(100): row['mcrank'] = 4
    elif is_eligible() and is_covered() and ffp_ge_than(65 ): row['mcrank'] = 5
    elif is_eligible() and is_covered() and ffp_ge_than(50 ): row['mcrank'] = 6

    elif is_eligible() and is_local() and ffp_ge_than(100): row['mcrank'] = 7
    elif is_eligible() and is_local() and ffp_ge_than(65 ): row['mcrank'] = 8
    elif is_eligible() and is_local() and ffp_ge_than(50 ): row['mcrank'] = 9

    elif is_eligible() and ffp_ge_than(100): row['mcrank'] = 10
    elif is_eligible() and ffp_ge_than(65 ): row['mcrank'] = 11
    elif is_eligible() and ffp_ge_than(50 ): row['mcrank'] = 12

    elif is_eligible() and AidCode and ffp_ge_than(1): row['mcrank'] = 13

    return row

def create_mcelig(row):

    def is_eligible(column):
        if str(column) == 'nan':
            return False
        elif int(str(column)[0]) < 5:
            return True

    if (is_eligible(row['EligibilityStatus']) or is_eligible(row['EligibilityStatusSP1']) or 
        is_eligible(row['EligibilityStatusSP2']) or is_eligible(row['EligibilityStatusSP3'])):
        row['MCelig'] = 1

    return row

def drop_ineligible_months(df):
    """Select one instance of a given (CIN, calendar) and the highest MCelig."""
    df = df.dropna(subset=['MCelig'])
    df = df.sort(['CIN','calendar','MCelig']).groupby(['CIN','calendar'], as_index=False).last()
    #df["id"] = df.index
    return df
