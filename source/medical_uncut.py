"""This script will load the Medi-Cal Tape file and create the medsCurrentUncut.sav file."""

import pandas
import medical_functions as mf
import config as config
from medical_meta import translation_dictionary

#Path to the Medi-Cal Tape file.
medical_file = config.medical_file
#Path and file name we want to save medsCurrentUncut.sav to.
meds_current_uncut_file = config.meds_current_uncut_file

#Create a pandas dataframe called medical_data from medical_file.
df = mf.load_medical_data(medical_file)

#Drop all rows without a CIN.
df.dropna(subset=['CIN'], inplace=True)

#Rename three columns. These are the names expected in the .sav file.
df.rename(columns={'xAidCode':'AidCode','xRespCounty':'RespCounty', 
                   'xEligibilityStatus':'EligibilityStatus'}, inplace=True)

#Remove duplicate rows keeping the row with the best eligibilityStatus. 
df.sort(['CIN','EligibilityStatus'], inplace=True)
df.drop_duplicates(subset='CIN', inplace=True)

#Create HCplanText column and populate with HCPcode data.
df['HCplanText']=df['HCPcode']
#Create language column and populate with the codes from lang.
df['language']=df['lang']
#Uppercase the city column.
df['city']=df['city'].str.upper()
#Replace the numeric codes in HCplanText and language with their text equivalent.
#Also replace some misspelled city names with the correct spelling.
df.replace(to_replace=translation_dictionary, inplace=True)

#These are the columns that need to be saved into the .sav file.
columns_to_save = ['CaseName', 'respCounty', 'language', 'calendar', 'ssn', 'sex', 'ethnicity',
                   'street', 'state', 'zip', 'CIN', 'bday', 'fname', 'lname', 'suffix',
                   'middleInitial', 'city', 'AidCode', 'OHC', 'SOCamount', 'EligibilityStatus',
                   'HCplanText', 'ResCounty', 'Govt', 'CountyCaseCode', 'CountyAidCode', 
                   'CountyCaseID', 'MedicareStatus', 'HIC', 'CarrierCode', 
                   'FederalContractNumber', 'PlanID', 'TypeID', 'HCPstatus', 'HCPcode', 
                   'region', 'AidCodeSP1', 'RespCountySP1', 'EligibilityStatusSP1', 'AidCodeSP2', 
                   'RespCountySP2', 'EligibilityStatusSP2', 'AidCodeSP3', 'RespCountySP3', 
                   'EligibilityStatusSP3']

#Create an SPSS .sav file with the columns named in columns_to_save.
mf.create_sav_file(meds_current_uncut_file, df, columns_to_save)
