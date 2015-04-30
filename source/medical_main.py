import pandas as pd

import medical_functions
import config

#Create a pandas dataframe (df) from medical_file.
df = medical_functions.load_medical_data(config.medical_file)

#Drop duplicate row, rows with no CINs, and fix mispelt city names.
df = medical_functions.clean_medical_data(df)

#Add bday, calendar, HCplanText, ethnicity, language, and region columns.
df = medical_functions.add_supplementary_columns(df)

#Save off medsCurrentUncut.sav file.
medical_functions.create_meds_current_uncut(df)

#Change the shape of the dataframe.  Make it longer by making each month its own row.
df = medical_functions.wide_to_long_by_month(df)

#Create a single column, MCelig, with a boolean eligibility status.
df = df.apply(medical_functions.create_mcelig, axis = 1)

#Drop months where there is no eligibility.
df = medical_functions.drop_ineligible_months(df)

#Change the shape of the dataframe.  Make it longer by taking each set of four (aidcode,status,
#respcounty) and breaking them into their own row.
#df = medical_functions.wide_to_long_by_aidcode(df)

#Creates a Medi-Cal rank based on EligibilityStatus, RespCounty, Full and FFP columns.
df = df.apply(medical_functions.create_medical_rank_from_wide_data, axis = 1)

#Create SSI, Fosterx and Disabledx Columns.
df = medical_functions.create_statuses(df)

