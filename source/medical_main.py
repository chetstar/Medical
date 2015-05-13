import datetime

import pandas as pd

import medical_functions
import config

start_time = datetime.datetime.now()
print('Started at: {}'.format(start_time))

#Create a pandas dataframe (df) from medical_file.
df = medical_functions.load_medical_data(config.medical_file)
print('Medi-Cal file finished loading at: {}'.format(datetime.datetime.now()))
print('Data frame info: ',df.info())

#Drop duplicate row, rows with no CINs, and fix mispelt city names.
df = medical_functions.clean_medical_data(df)
print('clean_medical_data finished at: {}'.format(datetime.datetime.now()))
print('Data frame info: ',df.info())

#Add bday, calendar, HCplanText, ethnicity, language, and region columns.
df = medical_functions.add_supplementary_columns(df)
print('add_supplementary_columns finished at: {}'.format(datetime.datetime.now()))
print('Data frame info: ',df.info())

#Save off medsCurrentUncut.sav file.
medical_functions.create_meds_current_uncut(df)
print('Uncut.sav finished at: {}'.format(datetime.datetime.now()))

#Save off medsExplodeNoDupeAidCode.sav.
medical_functions.create_meds_explode(df)

finished_time = datetime.datetime.now()
print('Finished at: {}'.format(finished_time))
print('Total elapsed time: {}'.format(finished_time - start_time))
