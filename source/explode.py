import json

import pandas as pd

import config

#Load column_info.json into column_info.  This is a list of lists.                                 
with open('explode_columns.json') as f:
    column_info = json.load(f)

#Split column_info into its four component lists.
#column_names and column_specifications are used by pandas.read_fwf to read in the Medi-Cal file. 
column_names, column_specifications, types_list, formats_list = zip(*column_info)

#All columns should be brought in as strings.
converters = {name:str for name in column_names}

chunked_data_iterator = pd.read_fwf(config.medical_file, 
                                    colspecs = column_specifications, 
                                    names = column_names, 
                                    converters = converters, 
                                    iterator = True,
                                    chunksize = 10000)

stubs = ['eligYear', 'eligMonth', 'xAidCode', 'xRespCounty', 'xEligibilityStatus',
         'SOCamount', 'MedicareStatus', 'HCPstatus', 'HCPcode', 'HCplanText', 'OHC',
         'AidCodeSP1', 'RespCountySP1', 'EligibilityStatusSP1', 'AidCodeSP2', 'RespCountySP2',
         'EligibilityStatusSP2', 'AidCodeSP3', 'RespCountySP3', 'EligibilityStatusSP3']

def is_eligible(column, value = 5):
    try:
        if int(column)[0] < value:
            return True
        else:
            return False
    except ValueError:
        return False

def create_dates(row):
    """Create MedsMonth, calendar, and bday columns. MedsMonth is the month and year the Medi-Cal
    eligibility file was created and calendar is the month that specific row of eligibility
    data is for. bday is the clients birthday."""

    row['calendar'] = pd.to_datetime(row['eligYear'] + row['eligMonth'], format = '%Y%m')
    row['MedsMonth'] = pd.to_datetime(meds_month, format = '%Y%m')
    row['bday'] = pd.to_datetime(row['bday'], format = '%d%m%Y')

def create_disabled(row):
    #Create and set a disabled column to 1 if eligible.
    if ( (is_eligible(row['EligibilityStatus'], value = 9) and row['Disabled'] == 1) or
         (is_eligible(row['EligibilityStatusSP1'], value = 9) and row['Disabledsp1'] == 1) or
         (is_eligible(row['EligibilityStatusSP2'], value = 9) and row['Disabledsp2'] == 1) or
         (is_eligible(row['EligibilityStatusSP3'], value = 9) and row['Disabledsp3'] == 1) ):
        row['DisabledX'] = 1
    else:
        row ['DisabledX'] = np.nan

def create_foster(row):
    #Create and set a foster column to 1 if eligible.
    if ( (is_eligible(row['EligibilityStatus']) and row['Foster'] == 1) or
         (is_eligible(row['EligibilityStatusSP1']) and row['Fostersp1'] == 1) or
         (is_eligible(row['EligibilityStatusSP2']) and row['Fostersp2'] == 1) or
         (is_eligible(row['EligibilityStatusSP3']) and row['Fostersp3'] == 1) ):
        row['FosterX'] = 1
    else:
        row['FosterX'] = np.nan

def create_explode(row):
    create_dates(row)
    create_foster(row)
    create_disabled(row)
    create_retromc(row)
    create_socmc(row)
    create_mcrank(row)
    return row

def match_aidcodes(df):
    """Merge in text form of aid codes."""
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCode', right_on = 'aidcode')
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCodeSP1', right_on = 'aidcode',
                  suffixes = ('','sp1'))
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCodeSP2', right_on = 'aidcode',
                  suffixes = ('','sp2'))
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'AidCodeSP3', right_on = 'aidcode',
                  suffixes = ('','sp3'))
    return df

eligibilities = ['eligibilityStatus', 'eligibilityStatusSP1', 
                 'eligibilityStatusSP3', 'eligibilityStatusSP3']
aidcodes = ['AidCode', 'AidCodeSP1', 'AidCodeSP2', 'AidCodeSP3']
ssicodes = ['10','20','60']
ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
ihsscodes = ['2L','2M','2N']
fosters = ['Foster', 'Fostersp1', 'Fostersp2', 'Fostersp3']
disableds = ['Disabled', 'Disabledsp1', 'Disabledsp2', 'Disabledsp3']

with SavWriter(config.nodupe_file, columns_to_save, variable_types, formats = variable_formats, 
               ioUtf8 = True) as writer:
    for df in chunked_data_iterator:

        #Wide to long by month.
        df = pd.wide_to_long(df, stubs, i, j)

        #Drop all rows for months with no eligibility.
        df = df[(df[eligibilities].apply(
            lambda x: x.dropna().str[0].astype(int))).lt(5,axis=0).any(axis=1)]

        #Join in aidcode tables.
        df = match_aidcodes(df)

        #Create ssi column. Populate with '1' if any aidcode in that row is in ssicodes.
        df['ssi'] = df[aidcodes].isin(ssicodes).any(axis = 1).map({True:'1'})

        df['CCSaidCode'] = df[aidcodes].isin(ccscodes).any(axis = 1).map({True:'1'})

        df['IHSSaidCode'] = df[aidcodes].isin(ihsscodes).any(axis = 1).map({True:'1'})

        df['SOCmc'] = (df[eligibilities].apply(lambda x: x.dropna().str[-1].astype(int))).\
                      eq(1,axis=0).any(axis = 1).map({True:'1'})




        df['fosterx'] = df[(((df[eligibilities].apply( lambda x: x.dropna().str[0].astype(int))).\
                             lt(5,axis=0)) & (df[disableds] == 1)).any(axis = 1).map({True:'1'})]
        
        df.apply(create_explode, axis = 1)

