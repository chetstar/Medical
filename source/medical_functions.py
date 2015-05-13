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
    df['calendar'] = pd.to_datetime(df['eligYear'].astype(int)*100 + df['eligMonth'].astype(int),
                                    format='%Y%m')
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
def rename_columns(df):

    for column_name in df.columns:
        if '_' in column_name:
            df.rename(columns = {column_name:column_name.replace('_','')}, inplace = True)
    for column_name in df.columns:
        if ( any(stub in column_name for stub in ['EligibilityStatus', 'RespCounty', 'AidCode'])
             and 'SP' not in column_name):
            df.rename(columns = {column_name:('x' + column_name)}, inplace = True)

    return df
            
def drop_unneeded_columns(df):

    stubs = ['SOCamount', 'CIN', 'bday', 'HCplanText', 'MedicareStatus', 'HCPstatus', 'HCPcode', 
             'OHC', 'eligYear', 'eligMonth', 'EligibilityStatus', 'RespCounty', 'AidCode']

    columns_to_keep = []

    for stub_name in stubs:
        for column_name in df.columns:
            if stub_name in column_name:
                columns_to_keep.append(column_name)

    df = df[columns_to_keep]

    return df

def wide_to_long(row):

    def remove_month_suffix(name_list, suffix):
        """Remove the month indicator (1-15) appended to the base column name"""
        for index, name in enumerate(name_list):
            name_list[index] = name[:-(len(str(suffix)))]
        return name_list

    #These are the stubs, or start of, column names that need to be kept.
    stubs = ['eligYear', 'eligMonth', 'xAidCode', 'xRespCounty', 'xEligibilityStatus',
             'SOCamount', 'MedicareStatus', 'HCPstatus', 'HCPcode', 'HCplanText', 'OHC',
             'AidCodeSP1', 'RespCountySP1', 'EligibilityStatusSP1', 'AidCodeSP2', 'RespCountySP2',
             'EligibilityStatusSP2', 'AidCodeSP3', 'RespCountySP3', 'EligibilityStatusSP3']

    #These are the columns that will be kept as is.
    ids = ['CIN','bday']

    #Initialize an empty dataframe.
    new_df = pd.DataFrame()

    #Populate the new stub with data from the original dataframe.
    #print('row[stubs+ids] is :', row[stubs+ids])
    new_df = new_df.append(row[stubs+ids])
    #print('new_df after first append:\n', new_df)
    row.drop(stubs, inplace = True )

    #For each month numbered 15 through 1, for each stub name in stubs, if that stubs name
    #matches the start of a column name in df.columns and the end of that column name is
    #the number of the month, append that column name to the list month_columns.
    for x in reversed(range(1,16)):
        month_columns = []
        for stub in stubs:
            for name in row.index:
                name_minus_stub = name.replace(stub,'')
                if ((stub in name) and (name_minus_stub.endswith(str(x)))):
                    month_columns.append(name)
        
        print('Month columns is:', month_columns)
        #Make a copy of month_columns as month_plus_ids and add 'CIN' and 'bday' to it.
        month_plus_ids = month_columns[:]
        month_plus_ids.extend(ids)

        #Create a temp data frame with a copy of the wanted rows from the original dataframe.
        temp_df = pd.DataFrame(row[month_plus_ids]).T
        
        row.drop(month_columns, inplace = True)
        #print(type(new_df))

        #Create a dictionary that maps the current months column names to the column names
        #needed to append to the new_df.
        main_to_month_mapping = {column_name:new_column_name for column_name, new_column_name in
                                 zip(month_columns,remove_month_suffix(month_columns[:],x))}
        print('main_to_month_mapping is: ', main_to_month_mapping)

        #Rename the columns of the temp_df useing the main_to_month_mapping.
        temp_df.rename(columns=main_to_month_mapping,inplace = True)
        
        #import pdb; pdb.set_trace()
        print('new_df_index: ', new_df.index)
        print('temp_df_index: ', temp_df.index)
        #Add the rows of temp_df to the new_df.
        import pdb; pdb.set_trace()
        new_df = new_df.append(temp_df, ignore_index = True)

    #Remove 'x' from column names where it is no longer needed.
    new_df.rename(columns={'xAidCode':'AidCode', 'xRespCounty':'RespCounty', 
                           'xEligibilityStatus':'EligibilityStatus'}, inplace = True)

    return new_df

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

def create_medical_rank(row):
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

def aid_code_matching(df):

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

def set_status(row):
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

    #Create calendar column.
    #df.dropna(subset=['eligYear','eligMonth'], inplace = True)
    row[['eligYear','eligMonth']] = row[['eligYear','eligMonth']].astype(int)
    row['calendar'] = pd.to_datetime(row.eligYear*100 + row.eligMonth, format='%Y%m')

    #Create a MedsMonth column that is the same as calendar.
    row['MedsMonth'] = row['calendar']

    return row

    #Bring in aidcode data from the aidcodesshort.csv.
    aidcodesshort = pd.read_csv(config.aidcodes_file,header=0)

def create_calendar_column(row):
    #Create calendar and bday columns.
    row['calendar'] = pd.to_datetime(row['eligYear'].astype(int)*100 + 
                                     row['eligMonth'].astype(int), format='%Y%m')
    row['bday'] = pd.to_datetime(row['year'] + row['month'] + row['day'], format='%Y%m%d')

    return row

def create_meds_explode(df):

    df = drop_unneeded_columns(df)
    df = rename_columns(df)

    var_types = variable_types
    var_formats = variable_formats

    #A number of columns are saved under different names than they were imported as.
    rename_dictionary = {'AidCodeSP1':'aidCodeSP1', 'AidCodeSP2':'aidCodeSP2',
                         'AidCodeSP3':'aidCodeSP3', 'Full':'full', 'Fullsp1':'fullsp1',
                         'Fullsp2':'fullsp2', 'Fullsp3':'fullsp3', 'HCplanText':'HCPlanText',
                         'eligYear':'eligibility_year', 'eligMonth': 'eligibility_month'}

    #These are the stubs, or start of, column names that need to be kept.
    stubs = ['eligYear', 'eligMonth', 'xAidCode', 'xRespCounty', 'xEligibilityStatus',
             'SOCamount', 'MedicareStatus', 'HCPstatus', 'HCPcode', 'HCplanText', 'OHC',
             'AidCodeSP1', 'RespCountySP1', 'EligibilityStatusSP1', 'AidCodeSP2', 'RespCountySP2',
             'EligibilityStatusSP2', 'AidCodeSP3', 'RespCountySP3', 'EligibilityStatusSP3']

    #Load list of columns to save for medsExplodeNoDupeAidCodes.sav
    with open('columns_to_save.json') as f:
        columns_to_save = json.load(f)

    #These are types and formats of columns not originally in the Medi-Cal file.
    new_types = {'primary_Aid_Code':2, 'ELIGIBILITY_COUNTY_code':2, 'FFP':0, 'FFPsp1':0,
                 'FFPsp2':0, 'FFPsp3':0, 'full':0, 'fullsp1':0, 'fullsp2':0, 'fullsp3':0,
                 'SSI':0, 'Foster':0, 'Disabled':0, 'HCPlanText':20, 'language':25, 
                 'ethnicity':20, 'region':18, 'bday':0, 'calendar':0, 'aidCodeSP1':0, 
                 'aidCodeSP2':0, 'aidCodeSP3':0, 'eligibility_year':0,
                 'eligibility_month':0, 'mcRank':0, 'RetroMC':0, 'SOCmc':0, 'CCSaidCode':2,
                 'IHSSaidCode':2, 'MedsMonth':0}

    new_formats = {'bday': 'DATE11', 'calendar':'MOYR6', 'MedsMonth':'MOYR6'}

    var_types.update(new_types)
    var_formats.update(new_formats)

    #Remove key value pairs where the key is not in columns_to_save. This must be
    #done because SavWriter will choke if there is an item in types/formats dictionaries
    #that is not in the list of columns to save.
    var_types = { column: var_types[column] for column in columns_to_save if
                  var_types.get(column) != None}
    var_formats = { column: var_formats[column] for column in columns_to_save if 
                    var_formats.get(column) != None}

    with SavWriter(config.nodupe_file, columns_to_save, var_types, formats = var_formats, 
                   ioUtf8 = True) as writer:

        def all_meds_explode(wide_row):
            df_narrow = wide_to_long(wide_row)
            print('df_narrow types is: ', type(df_narrow))
            print('df_narrow.columns is:\n', df_narrow.columns)
            df_narrow = df_narrow.apply(create_mcelig, axis = 1)
            import pdb; pdb.set_trace()
            df_narrow = df_narrow.apply(create_calendar_column, axis = 1)
            df_narrow = drop_ineligible_months(df_narrow)
            df_narrow = aid_code_matching(df_narrow)
            df_narrow = df_narrow.apply(set_status, axis = 1)
            df_narrow = df_narrow.apply(create_medical_rank, axis = 1)

            df_narrow.rename(columns = rename_dictionary, inplace = True)
            
            for row in map(list, df_narrow[columns_to_save].values):
                writer.writerow(row)

        df.apply(all_meds_explode, axis = 1)
