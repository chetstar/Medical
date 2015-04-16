"""This module contains the column_names and column_specifications for the Medi-Cal Tape along
with data dictionaries to tranlate numeric codes into English"""

import numpy as np
import json

#Load a list of valid city names that will be used to set misspelled city names from the
#Medi-Cal file.
with open('city_names.json') as f:
    city_names = json.load(f)

#Load column_info.json into column_info.  This is a list of lists.
with open('column_info.json') as f:
    column_info = json.load(f)

#Split column_info into its four component lists.
#column_names and column_specifications are used by pandas.read_fwf to read in the Medi-Cal file.
column_names, column_specifications, types_list, formats_list = zip(*column_info)

#Converters are used by dataframe.read_fwf to set the type of objects in a column.
#Here we are creating a converter for every name in column_names that has a matching value in
#types_list that isn't 0 which is all the ones that are strings.
converters = {key: str for key, value in zip(column_names, types_list) if value}

#variable_types and variable_formats are used by savReaderWriter. Create them here.
variable_types = {key: value for key, value in zip(column_names, types_list)}
variable_formats = {key: value for key, value in zip(column_names, formats_list) if value}

#These dictionaries are used to translate numeric codes into their English equivalents.
#Health care plan codes and names.
hcpcode_translation = {'300':'Alliance', '340':'Blue Cross', '051':'Center for Elders',
                       '056':'ONLOK Seniors', '000':'z No Plan', None:'z No Plan'}

#Language codes and their respective languages.
language_translation = {'B': 'Chinese', 'P': 'Portugese', 'A': 'Other Sign', 'D': 'Cambodian', 
                        '2': 'Cantonese', 'N': 'Russian', None: 'Missing', '1': 'Spanish', 
                        '3': 'Japanese', 'G': 'Mien', '4': 'Korean', '5': 'Tagalog', 
                        'C': 'Other Chinese', 'V': 'Vietnamese', '0': 'American Sign', 
                        '7': 'English', 'S': 'Samoan', 'J': 'Hebrew', 'U': 'Farsi', 
                        'R': 'Arabic', 'Q': 'Italian', 'M': 'Polish', 'F': 'Llacano', 
                        '9': 'Missing', '8': 'Missing', 'I': 'Lao', 'H': 'Hmong', '6': 'Other', 
                        'T': 'Thai', 'K': 'French', 'E': 'Armenian'}

#Ethnicity codes and their respective catagories.
ethnicity_translation = {'A': 'Asian/PI', 'C': 'Asian/PI', '0': 'Unknown', 'H': 'Asian/PI', 
                         'K': 'Asian/PI', 'J': 'Asian/PI', 'M': 'Asian/PI', 'N': 'Asian/PI', 
                         'P': 'Asian/PI', 'R': 'Asian/PI', '4': 'Asian/PI', '7': 'Asian/PI', 
                         'V': 'Asian/PI', '9': 'Unknown', '8': 'Unknown', 'T': 'Asian/PI',
                         '1': 'Caucasian', '2': 'Latino', '3': 'African American',
                         '5': 'Native American', 'Z': 'Other'}

#Dictionary to set blank, NaN and Transient city values.
city_translation = {'TRANSIENT':'HOMELESS', '':'UNKNOWN', np.nan:'UNKNOWN'}

#Match city names to their respective regions.
region_translation = {'ALAMEDA' :'1. North', 'ALBANY' :'1. North', 'BERKELEY' :'1. North',
                      'OAKLAND' :'1. North', 'EMERYVILLE' :'1. North', 'PIEDMONT' :'1. North',
                      'HAYWARD' :'2. Central', 'SAN LEANDRO' :'2. Central', 
                      'SAN LORENZO' :'2. Central', 'CASTRO VALLEY' :'2. Central',
                      'PLEASANTON' :'4. East', 'LIVERMORE' :'4. East', 'SUNOL' :'4. East',     
                      'DUBLIN' :'4. East', 'UNION CITY' :'3. South', 'FREMONT' :'3. South', 
                      'NEWARK' :'3. South', 'UNKNOWN' :'6. Unknown'}

#This dictionary of dictionaries is passed to a .replace method on the dataframe and then all 
#replacements are done in a single pass.
translation_dictionary = {'HCplanText':hcpcode_translation,
                          'language':language_translation,
                          'ethnicity':ethnicity_translation,
                          'city':city_translation,
                          'region':region_translation}

