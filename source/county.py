import json
from datetime import datetime
import sys

from savReaderWriter import SavWriter #For saving SPSS .sav files.
import pandas as pd

import common
import config

if __name__ == "__main__":
    program_start_time = datetime.now()
    
    medical_file = common.set_medical_file_location(sys.argv)

    #column_names and column_specifications are used by pandas.read_fwf to read Medi-Cal file.
    with open(config.county_load_info) as fp:
        column_names, column_specifications = zip(*json.load(fp))

    #All columns should be brought in as strings.
    converters = {name:str for name in column_names}

    df = pd.read_fwf(medical_file,
                     colspecs = column_specifications,
                     header = None,
                     names = column_names, 
                     converters = converters )

    df = common.drop_summary_row(df)
    df = common.drop_cinless_rows(df)

    with open(config.county_save_info) as fp:
        save_info = json.load(fp)

    with SavWriter(config.county_file, 
                   save_info['column_names'], 
                   save_info['types'], 
                   measureLevels = save_info['measure_levels'],
                   alignments = save_info['alignments'],
                   columnWidths = save_info['column_widths']) as writer:

        writer.writerows(df[save_info['column_names']].values)

    print('Program finished in: {}.'.format(str(datetime.now()-program_start_time)))    
