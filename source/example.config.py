### Config data common for both explode.py and uncut.py ###

#Location of Medi-Cal file.
medical_file = ''


### Config data for explode.py ###

#County Code in String form. Example: "01"
local_county_code = '01'

#Location of file with aidcode matching information.
aidcodes_file = './aidcodes.csv'

#Location to save medsExplodeNoDupeAidCode or alternate name.
explode_file = ''

#Location of file with information on loading data from Medi-Cal fixed width file.
explode_load_info = './explode_columns_load_info.json'

#Location of file with information on saving data into SPSS .sav format.
explode_save_info = './explode_columns_save_info.json'

#Number of rows to read from Medi-Cal file per chunk.
chunk_size = 10000

### Config data for uncut.py ###

#Location to save medsCurrentUncut.sav or alternate name.
uncut_file = ''

#Location of json file with information loading data from Medi-Cal fixed widht file.
uncut_load_info = './uncut_columns_load_info.json'

#Location of json file with parameters for saving SPSS .sav file.
uncut_save_info = './uncut_columns_save_info.json'

#List of correct city names for spell checking city column.
city_names = './city_names.json'

### Config data for county.py ###

#Location to save CountyCase.sav or alternate name.
county_path = ''

#Location of json file with information loading data from Medi-Cal fixed widht file.
county_load_info = './county_load_info.json'

#Location of json file with parameters for saving SPSS .sav file.
county_save_info = './county_save_info.json'
