import numpy as np
import pandas as pd
from column_info import translation_dictionary, column_names, column_specifications
from savReaderWriter import SavWriter

def load_medical_data(file_location):
    df = pd.read_fwf(file_location, 
                 colspecs = column_specifications,
                 header = None, 
                 names = column_names, 
                 parse_dates = {'bday':['year','month','day'],'calendar':['eligYear',"eligMonth"]},
                 keep_date_col = True,
                 converters = {'HCPcode':str, 'HCPstatus':str, 'ssn':str})
    return df

def create_sav_file(file_name, dataframe, columns_to_save):
    length_dictionary = {'bday':10,'calendar':10}
    for name in columns_to_save:
        if name in column_lengths:
            length_dictionary = column_lengths[name]
        if name in translation_dictionary:
            length_dictionary = translation_lengths[name]
    
    with SavWriter(file_name, columns_to_save, length_dictionary) as writer:
        for row in map(list, dataframe[columns_to_save].values):
            writer.writerow(row)

    print('File {} created.'.format(file_name))

