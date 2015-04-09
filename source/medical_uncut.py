"""This script will load the Medi-Cal Tape file and create the medsCurrentUncut.sav file."""

import pandas
import medical_functions as mf
from medical_meta import translation_dictionary

#Path to the Medi-Cal Tape file.
medical_file = ''
#Path and file name we want to save medsCurrentUncut.sav to.
meds_current_uncut_file = ''

#Create a pandas dataframe called medical_data from medical_file.
df = mf.load_medical_data(medical_file)

#Drop all rows without a CIN.
df.dropna(subset=['CIN'], inplace=True)

#Remove duplicate rows keeping the row with the best eligibilityStatus. 
df.sort(['CIN','EligibilityStatus'], inplace=True).drop_duplicates(subset='CIN', inplace=True)

#Create HCplanText column and populate with HCPcode data.
df['HCplanText']=df['HCPcode']
#Create language column and populate with the codes from lang.
df['language']=df['lang']
#Uppercase the city column.
df['city']=df['city'].str.upper()
#Replace the numeric codeds in HCplanText and language with their text equivalent.
#Also replace some misspelled city names with the correct spelling.
df.replace(to_replace=translation_dictionary, inplace=True)





