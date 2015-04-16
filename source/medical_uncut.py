"""This script will load the Medi-Cal Tape file and create the medsCurrentUncut.sav file."""

#To determine how long it takes to run.
import datetime
start_time = datetime.datetime.now()
print('Starting at: {}'.format(start_time))

import pandas as pd
from fuzzywuzzy import process #For correcting misspelled city names.

#Load helper functions.
import medical_functions as mf 
#Load path to the Medi-Cal file and path to save medsCurrentUncut.sav, respectively.
from config import medical_file, meds_current_uncut_file
from medical_meta import translation_dictionary, city_names

#Create a pandas dataframe called medical_data from medical_file.
df = mf.load_medical_data(medical_file)

#Drop all rows without a CIN.
df.dropna(subset=['CIN'], inplace=True)

#Remove duplicate rows keeping the row with the best eligibilityStatus. 
df.sort(['CIN','EligibilityStatus'], inplace=True)
df.drop_duplicates(subset='CIN', inplace=True)

#Create calendar and bday columns.
df['calendar'] = pd.to_datetime(df['eligYear']*100 + df['eligMonth'], format='%Y%m')
df['bday'] = pd.to_datetime(df['year'] + df['month'] + df['day'], format='%Y%m%d')

#Create HCplanText column and populate with HCPcode data.
df['HCplanText'] = df['HCPcode']
#Create language column and populate with the codes from lang.
df['language'] = df['lang']
#Create ethnicity column and populate with codes from race.
df['ethnicity'] = df['race']
df['region']= df['city']

#Fix misspelt city names.
def fix_city_names(word, choices):
    #This function wraps fuzzywuzzy's extractOne, which returns a tuple, and grabs the first
    #item of that tuple.
    return process.extractOne(word,choices)[0]

df['city'] = df['city'].apply(fix_city_names, args = (city_names,))

#Replace the numeric codes in HCplanText, ethnicity, and language with their text equivalent.
df.replace(to_replace=translation_dictionary, inplace=True)

#If someone has an HCplanText but their HCPstatus is such that it is invalidated, change
#HCplanText to "z No Plan"
df.ix[df.HCPstatus.isin(["00","10","09","19","40","49","S0","S9"]),'HCplanText']="z No Plan"

#These are the columns that need to be saved into the .sav file.
columns_to_save = ['CaseName', 'RespCounty', 'language', 'calendar', 'ssn', 'sex', 'ethnicity',
                   'street', 'state', 'zip', 'CIN', 'bday', 'fname', 'lname', 'suffix',
                   'middleInitial', 'city', 'AidCode', 'OHC', 'SOCamount', 'EligibilityStatus',
                   'HCplanText', 'ResCounty', 'GOVT', 'CountyCaseCode', 'CountyAidCode', 
                   'CountyCaseID', 'MedicareStatus', 'HIC', 'CarrierCode', 
                   'FederalContractNumber', 'PlanID', 'TypeID', 'HCPstatus', 'HCPcode', 
                   'AidCodeSP1', 'RespCountySP1', 'EligibilityStatusSP1', 'AidCodeSP2', 
                   'RespCountySP2', 'EligibilityStatusSP2', 'AidCodeSP3', 'RespCountySP3', 
                   'EligibilityStatusSP3']
#Took out 'region' after 'HCPcode'

new_types = {'HCplanText':20, 'language':20, 'ethnicity':20, 'region':20, 'bday':0,
             'calendar':0}
new_formats = {'bday': 'DATE11', 'calendar':'MOYR6'}

#Create an SPSS .sav file with the columns named in columns_to_save.
mf.create_sav_file(meds_current_uncut_file, df, columns_to_save, new_types, new_formats)

finished_time = datetime.datetime.now()
print('Finished at: {}'.format(finished_time))

print('Total elapsed time: {}'.format(finished_time-start_time))
