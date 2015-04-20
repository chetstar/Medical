import pandas as pd

import medical_functions
import config

#Create a pandas dataframe (df) from medical_file.
df = medical_functions.load_medical_data(config.medical_file)

#Drop duplicate row, rows with no CINs, and fix mispelt city names.
df = medical_functions.clean_medical_data(df)

#Add bday, calendar, HCplanText, ethnicity, language, and language columns.
df = medical_functions.add_supplementary_columns(df)

#Save off medsCurrentUncut.sav file.
medical_functions.create_meds_current_uncut(df)

#Change the shape of the dataframe.  Make it longer by making each month its own row.
df = medical_functions.wide_to_long_by_month(df)


