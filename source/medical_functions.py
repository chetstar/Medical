import datetime
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

    #Code to delete the last row if its a summary row.
    df = df.drop(df.index[-1])
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
    print('CIN-less rows dropped at: {}'.format(datetime.datetime.now()))

    #Remove duplicate rows keeping the row with the best eligibilityStatus. 
    df.sort(['CIN','EligibilityStatus'], inplace=True)
    df.drop_duplicates(subset='CIN', inplace=True)
    print('Duplicate rows removed at: {}'.format(datetime.datetime.now()))

    #Wrap extractOne so that we can use it with apply and get back only a city name.
    def extractOne_wrapper(city, city_name_list):
        """Returns the first item of the tuple retruned by fuzzywuzzy.process.extractOne"""
        return process.extractOne(city, city_name_list)[0]

    #Bring in city_names_list from city_names.json
    with open('city_names.json') as f:
        city_name_list = json.load(f)

    #Fix mispelt city names. city_names 
    df['city'] = df['city'].apply(extractOne_wrapper, args = (city_name_list,))
    print('City name misspellings fixed at: {}'.format(datetime.datetime.now()))

    return df

def add_supplementary_columns(df):
    """Add calendar, bday, HCplanText, language, ethnicity and region columns"""

    #Create calendar and bday columns.
    df['calendar'] = pd.to_datetime(df['eligYear'].astype(int)*100 + df['eligMonth'].astype(int), format='%Y%m')
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
    #ccstext = pd.read_csv(config.csstext_file,header=0)
    aidcodesshort = pd.read_csv(config.aidcodes_file,header=0)

    #Merge in text form of aid codes.
    #df = pd.merge(df, ccstext, how='left',left_on='AidCode',right_on='AidCode')
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCode', right_on = 'aidcode')
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCodeSP1', right_on = 'aidcode',
                  suffixes = ('','sp1'))
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCodeSP2', right_on = 'aidcode',
                  suffixes = ('','sp2'))
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCodeSP3', right_on = 'aidcode',
                  suffixes = ('','sp3'))
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
    ##Investigate missing data and ways to fill it in.
    df = df.dropna(subset=['eligYear','eligMonth'])
    df[['eligYear','eligMonth']] = df[['eligYear','eligMonth']].astype(int)
    df['calendar'] = pd.to_datetime(df.eligYear*100 + df.eligMonth, format='%Y%m')

    return df

def wide_rank(row):
    """This function returns a numerical rank depending on the eligibilityStatus, 
    RespCounty, Full and FFP columns of the Medi-Cal data.

    This function expects the Medi-Cal data to have NOT undergone wide_to_long_by_aidcode."""

    def is_eligible():
        if str(row[0]) == 'nan':
            return False
        elif int(str(row[0])[0]) < 5:
            return True

    def is_local():
        if (row[1] == config.local_county_code):
            return True

    def is_covered():
        if row[2] == '1':
            return True

    def ffp_ge_than(percentage):
        if row[3] >= percentage:
            return True

    if   is_eligible() and is_local() and is_covered() and ffp_ge_than(100): return 1
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(65 ): return 2
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(50 ): return 3

    elif is_eligible() and is_covered() and ffp_ge_than(100): return 4
    elif is_eligible() and is_covered() and ffp_ge_than(65 ): return 5
    elif is_eligible() and is_covered() and ffp_ge_than(50 ): return 6

    elif is_eligible() and is_local() and ffp_ge_than(100): return 7
    elif is_eligible() and is_local() and ffp_ge_than(65 ): return 8
    elif is_eligible() and is_local() and ffp_ge_than(50 ): return 9

    elif is_eligible() and ffp_ge_than(100): return 10
    elif is_eligible() and ffp_ge_than(65 ): return 11
    elif is_eligible() and ffp_ge_than(50 ): return 12

    elif is_eligible() and AidCode and ffp_ge_than(1): return 13
    
    else: return 99

def create_medical_rank_from_wide_data(row):
    """Create mcrank, Primary_Aid_Code, and ELIGIBILITY_COUNTY_code columns from Medi-Cal data
    that has not undergone wide_to_long_by_aidcode."""

    ranking_data=[[row['EligibilityStatus'],row['RespCounty'],
                   row['Full'],row['FFP'],row['AidCode']],
                  [row['EligibilityStatusSP1'],row['RespCountySP1'],
                   row['Fullsp1'],row['FFPsp1'],row['AidCodeSP1']],
                  [row['EligibilityStatusSP2'],row['RespCountySP2'],
                   row['Fullsp2'],row['FFPsp2'],row['AidCodeSP2']],
                  [row['EligibilityStatusSP3'],row['RespCountySP3'],
                   row['Fullsp3'],row['FFPsp3'],row['AidCodeSP3']]]

    mcrank = 99
    Primary_Aid_Code = np.nan
    ELIGIBILITY_COUNTY_code = np.nan

    for sub_list in ranking_data:
        current_rank = wide_rank(sub_list)
        if current_rank < mcrank:
            mcrank = current_rank
            Primary_Aid_Code = sub_list[4]
            ELIGIBILITY_COUNTY_code = sub_list[1]
    
    row['mcRank'] = mcrank
    row['primary_Aid_Code'] = Primary_Aid_Code
    row['ELIGIBILITY_COUNTY_code'] = ELIGIBILITY_COUNTY_code
        
    return row

def is_eligible(column, value = 5):
    if str(column) == 'nan':
        return False
    elif int(str(column)[0]) < value:
        return True

def create_mcelig(row):
    """Determine eligibility for the month by looking at all four EligibilityStatus columns.
    Create an MCelig column with that data in it."""

    if (is_eligible(row['EligibilityStatus']) or is_eligible(row['EligibilityStatusSP1']) or 
        is_eligible(row['EligibilityStatusSP2']) or is_eligible(row['EligibilityStatusSP3'])):
        row['MCelig'] = 1
    else:
        row['MCelig'] = np.nan

    return row

def drop_ineligible_months(df):
    """Select one instance of a given (CIN, calendar) and the highest MCelig."""
    df = df.dropna(subset=['MCelig'])
    df = df.sort(['CIN','calendar','MCelig']).groupby(['CIN','calendar'], as_index=False).last()
    #df["id"] = df.index
    return df

def set_status(row):
    """Create SSI column and set to 1 if any AidCode is 10,20, or 60 and MCelig is true"""
    
    #Condense aidcode columns into a list.
    aidcodes = [row['AidCode'], row['AidCodeSP1'], row['AidCodeSP2'], row['AidCodeSP3']]
        
    #If any aidcode is 10,20, or 60 SSI is set to 1.
    if any(code in aidcodes for code in ['10','20','60']):
        row['SSI'] = 1
    else:
        row['SSI'] = np.nan

    #If aidcode is one of: ['9K','9M','9N','9R','9U','9V','9W'] ccsaidcode is set to that aidcode.
    ccsaidcode = next((code in ['9K','9M','9N','9R','9U','9V','9W'] for code in aidcodes if code),
                      None)
    if ccsaidcode:
        row['CCSaidCode'] = ccsaidcode
    else:
        row['CCSaidCode'] = np.nan

    #If aidcode is on of: ['2L','2M','2N'] ihssaidcode column is set to that aidcode.
    ihssaidcode = next((code in aidcodes for code in ['2L','2M','2N'] if code), None)
    if ihssaidcode:
        row['IHSSaidCode'] = ihssaidcode
    else:
        row['IHSSaidCode'] = np.nan

    #Create and set a foster column to 1 if eligible.
    if ( (is_eligible(row['EligibilityStatus']) and row['Foster'] == 1) or
         (is_eligible(row['EligibilityStatusSP1']) and row['Fostersp1'] == 1) or
         (is_eligible(row['EligibilityStatusSP2']) and row['Fostersp2'] == 1) or
         (is_eligible(row['EligibilityStatusSP3']) and row['Fostersp3'] == 1) ):
        row['FosterX'] = 1
    else:
        row['FosterX'] = np.nan

    #Create and set a disabled column to 1 if eligible.
    if ( (is_eligible(row['EligibilityStatus'], value = 9) and row['Disabled'] == 1) or
         (is_eligible(row['EligibilityStatusSP1'], value = 9) and row['Disabledsp1'] == 1) or
         (is_eligible(row['EligibilityStatusSP2'], value = 9) and row['Disabledsp2'] == 1) or
         (is_eligible(row['EligibilityStatusSP3'], value = 9) and row['Disabledsp3'] == 1) ):
        row['DisabledX'] = 1
    else:
        row ['DisabledX'] = np.nan
    
    #If the last character of the primary_Aid_Code is 2,3, or 5 set RetroMC to 1. 
    try:
        if str(row['primary_Aid_Code'])[2] in ['2','3','5']:
            row['RetroMC'] = 1
    except Exception:
            row['RetroMC'] = np.nan

    #Set SOCmc to 1 if the first character of any EligibilityStatus is 5.
    def soc_mc(column):
        try:
            if int(str(column)[0]) == 5:
                return True
        except Exception:
            pass
    if ( soc_mc(row['EligibilityStatus']) or soc_mc(row['EligibilityStatusSP1']) or
         soc_mc(row['EligibilityStatusSP2']) or soc_mc(row['EligibilityStatusSP3']) ):
        row['SOCmc'] = 1
    else:
        row['SOCmc'] = np.nan

    return row
    
def create_statuses(df):
    """Create columns for SSI, Foster, Disabled, CCSaidCode, IHSSaidCode"""

    df = df.apply(set_status, axis = 1)

    df[['Disabled','Foster']] = df[['DisabledX','FosterX']]
    
    return df

def create_meds_explode(df):
    #Load list of columns to save for medsExplodeNoDupeAidCodes.sav
    with open('columns_to_save.json') as f:
        columns_to_save = json.load(f)

    rename_dictionary = {'AidCodeSP1':'aidCodeSP1', 'AidCodeSP2':'aidCodeSP2',
                         'AidCodeSP3':'aidCodeSP3', 'Full':'full', 'Fullsp1':'fullsp1',
                         'Fullsp2':'fullsp2', 'Fullsp3':'fullsp3', 'HCplanText':'HCPlanText',
                         'eligYear':'eligibility_year', 'eligMonth': 'eligibility_month'}

    df.rename(columns = rename_dictionary, inplace = True)

    df['MedsMonth'] = df['calendar']

    #These are types and formats of columns not originally in the Medi-Cal file.
    new_types = {'primary_Aid_Code':2, 'ELIGIBILITY_COUNTY_code':2, 'FFP':0, 'FFPsp1':0,
                 'FFPsp2':0, 'FFPsp3':0, 'full':0, 'fullsp1':0, 'fullsp2':0, 'fullsp3':0,
                 'SSI':0, 'Foster':0, 'Disabled':0, 'HCPlanText':20, 'language':25, 
                 'ethnicity':20, 'region':18, 'bday':0, 'calendar':0, 'aidCodeSP1':0, 
                 'aidCodeSP2':0, 'aidCodeSP3':0, 'eligibility_year':0,
                 'eligibility_month':0, 'mcRank':0, 'RetroMC':0, 'SOCmc':0, 'CCSaidCode':2,
                 'IHSSaidCode':2, 'MedsMonth':0}

    new_formats = {'bday': 'DATE11', 'calendar':'MOYR6', 'MedsMonth':'MOYR6'}

    create_sav_file(config.nodupe_file, df, columns_to_save, new_types, new_formats)
