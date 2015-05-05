import datetime

import pandas as pd

import medical_functions
import config

start_time = datetime.datetime.now()
print('Started at: {}'.format(start_time))

#Create a pandas dataframe (df) from medical_file.
df = medical_functions.load_medical_data(config.medical_file)
print('Medi-Cal file finished loading at: {}'.format(datetime.datetime.now()))

#Drop duplicate row, rows with no CINs, and fix mispelt city names.
df = medical_functions.clean_medical_data(df)
print('clean_medical_data finished at: {}'.format(datetime.datetime.now()))

#Add bday, calendar, HCplanText, ethnicity, language, and region columns.
df = medical_functions.add_supplementary_columns(df)
print('add_supplementary_columns finished at: {}'.format(datetime.datetime.now()))

#Save off medsCurrentUncut.sav file.
medical_functions.create_meds_current_uncut(df)
print('Uncut.sav finished at: {}'.format(datetime.datetime.now()))

#Change the shape of the dataframe.  Make it longer by making each month its own row.
#df = medical_functions.wide_to_long_by_month(df)
df = medical_functions.wide_to_long(df)
print('wide_to_long finished at: {}'.format(datetime.datetime.now()))

#Create a single column, MCelig, with a boolean eligibility status.
df = df.apply(medical_functions.create_mcelig, axis = 1)
print('MCelig created at: {}'.format(datetime.datetime.now()))

#Drop months where there is no eligibility.
df = medical_functions.drop_ineligible_months(df)
print('Ineligible months dropped at: {}'.format(datetime.datetime.now()))

#Creates a Medi-Cal rank based on EligibilityStatus, RespCounty, Full and FFP columns.
df = df.apply(medical_functions.create_medical_rank_from_wide_data, axis = 1)
print('mcRank created at: {}'.format(datetime.datetime.now()))

#Create SSI, Fosterx and Disabledx Columns.
df = medical_functions.create_statuses(df)
print('Statuses created at: {}'.format(datetime.datetime.now()))

#Save off medsExplodeNoDupeAidCode.sav.
medical_functions.create_meds_explode(df)

finished_time = datetime.datetime.now()
print('Finished at: {}'.format(finished_time))
print('Total elapsed time: {}'.format(finished_time - start_time))
