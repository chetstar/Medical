import json

import pandas as pd
from savReaderWriter import SavWriter

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

stubs = ['eligyear', 'eligmonth', 'aidcodesp0', 'respcountysp0', 'eligibilitystatussp0',
         'socamount', 'medicarestatus', 'hcpstatus', 'hcpcode', 'hcplantext', 'ohc',
         'aidcodesp1', 'respcountysp1', 'eligibilitystatussp1', 'aidcodesp2', 'respcountysp2',
         'eligibilitystatussp2', 'aidcodesp3', 'respcountysp3', 'eligibilitystatussp3']

def is_eligible(column, value = 5):
    if str(column) == 'nan':
        return False
    elif int(str(column)[0]) < value:
        return True

def create_disabled(row):
    #Create and set a disabled column to 1 if eligible.
    if ( (is_eligible(row['eligibilitystatussp0'], value = 9) and row['disabledsp0'] == 1) or
         (is_eligible(row['eligibilitystatussp1'], value = 9) and row['disabledsp1'] == 1) or
         (is_eligible(row['eligibilitystatussp2'], value = 9) and row['disabledsp2'] == 1) or
         (is_eligible(row['eligibilitystatussp3'], value = 9) and row['disabledsp3'] == 1) ):
        row['disabled'] = '1'
    else:
        row ['disabled'] = None

def create_foster(row):
    #Create and set a foster column to 1 if eligible.
    if ( (is_eligible(row['eligibilitystatussp0']) and row['fostersp0'] == 1) or
         (is_eligible(row['eligibilitystatussp1']) and row['fostersp1'] == 1) or
         (is_eligible(row['eligibilitystatussp2']) and row['fostersp2'] == 1) or
         (is_eligible(row['eligibilitystatussp3']) and row['fostersp3'] == 1) ):
        row['foster'] = '1'
    else:
        row['foster'] = None

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
            
    if is_eligible():
        if is_local():
            if is_covered():
                if ffp_ge_than(100): 
                    return 1
                elif ffp_ge_than(65 ): 
                    return 2
                elif ffp_ge_than(50 ): 
                    return 3
            else:
                if ffp_ge_than(100): 
                    return 7
                elif ffp_ge_than(65 ): 
                    return 8
                elif ffp_ge_than(50 ): 
                    return 9
        else:
            if is_covered(): 
                if ffp_ge_than(100): 
                    return 4
                elif ffp_ge_than(65 ): 
                    return 5
                elif ffp_ge_than(50 ): 
                    return 6
            else:
                if ffp_ge_than(100): 
                    return 10
                if ffp_ge_than(65 ): 
                    return 11
                if ffp_ge_than(50 ): 
                    return 12

    #elif row[4] and ffp_ge_than(1): 
        #return 13

    else:
        return 99

def create_mcrank(row):
    """Create mcrank, primary_aid_code, and eligibility_county_code columns from medi-cal data
    that has not undergone wide_to_long_by_aidcode."""

    ranking_data=[[row['eligibilitystatussp0'],row['respcountysp0'],
                   row['fullsp0'],row['ffpsp0'],row['aidcodesp0']],
                  [row['eligibilitystatussp1'],row['respcountysp1'],
                   row['fullsp1'],row['ffpsp1'],row['aidcodesp1']],
                  [row['eligibilitystatussp2'],row['respcountysp2'],
                   row['fullsp2'],row['ffpsp2'],row['aidcodesp2']],
                  [row['eligibilitystatussp3'],row['respcountysp3'],
                   row['fullsp3'],row['ffpsp3'],row['aidcodesp3']]]

    mcrank = 99
    primary_aid_code = None
    eligibility_county_code = None

    for sub_list in ranking_data:
        current_rank = wide_rank(sub_list)
        if current_rank < mcrank:
            mcrank = current_rank
            primary_aid_code = sub_list[4]
            eligibility_county_code = sub_list[1]
    
    row['mcrank'] = mcrank
    row['primary_aid_code'] = primary_aid_code
    row['eligibility_county_code'] = eligibility_county_code
        
    return row

def match_aidcodes(df):
    """Merge in text form of aid codes."""
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'aidcodesp0', right_on = 'aidcode',
                  suffixes = ('','sp0'))
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'aidcodesp1', right_on = 'aidcode',
                  suffixes = ('','sp1'))
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'aidcodesp2', right_on = 'aidcode',
                  suffixes = ('','sp2'))
    df = pd.merge(df, aidcodesshort, how = 'left', left_on = 'aidcodesp3', right_on = 'aidcode',
                  suffixes = ('','sp3'))
    df = df.rename(columns = {'ffp':'ffpsp0','full':'fullsp0',
                              'disabled':'disabledsp0','foster':'fostersp0'})
    return df

with open(config.aidcodes_file) as f:
    aidcodesshort = pd.read_csv(f, header = 0)

eligibilities = ['eligibilitystatussp0', 'eligibilitystatussp1', 
                 'eligibilitystatussp3', 'eligibilitystatussp3']
aidcodes = ['aidcodesp0', 'aidcodesp1', 'aidcodesp2', 'aidcodesp3']
ssicodes = ['10','20','60']
ccscodes = ['9K','9M','9N','9R','9U','9V','9W']
ihsscodes = ['2L','2M','2N']
fosters = ['fostersp0', 'fostersp1', 'fostersp2', 'fostersp3']
disableds = ['disabledsp0', 'disabledsp1', 'disabledsp2', 'disabledsp3']

#with open('columns_to_save.json') as f:
#    columns_to_save = json.load(f)
#columns_to_save = [x.lower() for x in columns_to_save]#fix the file so this goes away.
columns_to_save = ['aidcodesp0', 'respcountysp0', 'eligibilitystatussp0']

variable_types = {x:20 for x in columns_to_save}

print(variable_types)

with SavWriter(config.nodupe_file, columns_to_save, variable_types, 
               ioUtf8 = True) as writer:

    def create_explode(row):
        create_foster(row)
        create_disabled(row)
        #create_mcrank(row)
        #create_retromc(row)
        writer.writerow(list(row[columns_to_save].values))
        return row

    for df in chunked_data_iterator:

        #medsmonth is the most recent month with eligibility data in the file..
        medsmonth = df['eligmonth'][0] + df['eligyear'][0]
        df['medsmonth'] = pd.to_datetime(medsmonth, format = '%m%Y')
        df['bday'] = pd.to_datetime(df['month']+df['day']+df['year'], format = '%m%d%Y')
        df = df.drop(['month','day','year'], axis = 1)

        #Wide to long by month.
        df = pd.wide_to_long(df, stubs, 'cin', 'j')
        df = df.reset_index()

        #Drop all rows for months with no eligibility.
        df = df[(df[eligibilities].apply(
            lambda x: x.dropna().str[0].astype(int))).lt(5,axis = 0).any(axis = 1).reindex(
                index = df.index, fill_value = False)]

        #Create calendar column.
        df['calendar'] = pd.to_datetime(df['eligmonth']+df['eligyear'], format='%m%Y')

        #Join in aidcode tables.
        df = match_aidcodes(df)

        #Create ssi column. Populate with '1' if any aidcode in that row is in ssicodes.
        df['ssi'] = df[aidcodes].isin(ssicodes).any(axis = 1).map({True:'1'})

        df['ccsaidcode'] = df[aidcodes].isin(ccscodes).any(axis = 1).map({True:'1'})

        df['ihssaidcode'] = df[aidcodes].isin(ihsscodes).any(axis = 1).map({True:'1'})

        df['socmc'] = (df[eligibilities].apply(lambda x: x.dropna().str[-1].astype(int))).\
                      eq(1,axis=0).any(axis = 1).map({True:'1'})

        df = df.apply(create_explode, axis = 1)

