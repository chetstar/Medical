import pandas as pd
from medical_meta import (translation_dictionary, 
                          column_names, 
                          column_specifications, 
                          column_lengths,
                          translation_lengths,
                          column_converters)
from savReaderWriter import SavWriter

def load_medical_data(file_location):
    df = pd.read_fwf(file_location,
                     colspecs = column_specifications,
                     header = None,
                     names = column_names, 
                     parse_dates = {'bday':['year','month','day'],
                                    'calendar':['eligYear',"eligMonth"]},
                     keep_date_col = True,
                     converters = column_converters)
    return df

def create_sav_file(file_name, dataframe, columns_to_save):
    length_dictionary = {'bday':10,'calendar':10}
    for name in columns_to_save:
        if name in column_lengths:
            length_dictionary[name] = column_lengths[name]
        if name in translation_dictionary:
            length_dictionary[name] = translation_lengths[name]

    print(length_dictionary)
    with SavWriter(file_name, columns_to_save, length_dictionary) as writer:
        for row in map(list, dataframe[columns_to_save].values):
            writer.writerow(row)

    print('File {} created.'.format(file_name))

