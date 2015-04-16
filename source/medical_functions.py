import numpy as np
import pandas as pd
from medical_meta import (translation_dictionary, 
                          column_names, 
                          column_specifications, 
                          variable_types,
                          variable_formats,
                          converters)
from savReaderWriter import SavWriter

def load_medical_data(file_location):
    df = pd.read_fwf(file_location,
                     colspecs = column_specifications,
                     header = None,
                     names = column_names, 
                     keep_date_col = True,
                     converters = converters)
    return df

def create_sav_file(file_name, dataframe, columns_to_save, new_types, new_formats):

    var_types = variable_types
    var_formats = variable_formats

    #Update dictionaries to merge in meta-data for new columns.
    var_types.update(new_types)
    var_formats.update(new_formats)
    
    #Remove key value pairs where the key is not in columns_to_save. This must be
    #done because SavWriter will choke if there is an item in types/formats dictionaries
    #that is not in the list of columns to save.
    var_types = { column: var_types[column] for column in columns_to_save if 
                       var_types.get(column) != None}
    var_formats = { column: var_formats[column] for column in columns_to_save if 
                         var_formats.get(column) != None}

    with SavWriter(file_name, columns_to_save, var_types, formats = var_formats, 
                   ioUtf8 = True) as writer:

        #Convert from python datetime objects to spssDateTime.
        dataframe['calendar'] = dataframe['calendar'].apply(writer.spssDateTime,args=('%Y-%m-%d',))
        dataframe['bday'] = dataframe['bday'].apply(writer.spssDateTime, args = ('%Y-%m-%d',))

        for row in map(list, dataframe[columns_to_save].values):
            writer.writerow(row)

    print('File {} created.'.format(file_name))

