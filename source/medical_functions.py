import numpy as np
import pandas as pd
from column_info import translation_dictionary, column_names, column_specifications

def load_medical_data(file_location):
    df = pd.read_fwf(file_location, 
                 colspecs = column_specifications,
                 header = None, 
                 names = column_names, 
                 parse_dates = {'bday':['year','month','day'],'calendar':['eligYear',"eligMonth"]},
                 keep_date_col = True,
                 converters = {'HCPcode':str, 'HCPstatus':str, 'ssn':str})
    return df

