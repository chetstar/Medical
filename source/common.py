import pandas as pd

import config

def drop_duplicate_rows(df, chunknum, chunksize, dupemask):
    """Drop duplicate rows and rows without CINs."""
    df.index = range(chunknum*chunksize, chunknum*chunksize + len(df.index))
    df = df[dupemask[df.index]]
    return df

def wide_to_long_by_month(df, stubs):
    df = pd.wide_to_long(df, stubs, 'cin', 'j')
    df = df.reset_index()
    return df

def make_duplicates_bitmask(medical_file):
    """Use CIN and eligibility status for entire file to make bitmask
    of duplicate and cinless rows."""
    df = pd.read_fwf(medical_file, colspecs = [(209,218),(255,258)], names = ['cin','elig'])
    cinless = df['cin'].isnull()
    df = df.sort(columns = ['cin','elig'], ascending = True, na_position = 'last')
    dupemask = df.duplicated(subset = ['cin'])
    dropmask = ~(cinless | dupemask) 
    return dropmask

def drop_summary_row(df):
    """Code to delete the last row if its a summary row."""
    df.drop(df.index[-1], inplace = True)
    return df

def drop_cinless_rows(df):
    """Drop all rows without a CIN."""
    df.dropna(subset = ['cin'], inplace = True)
    return df

def make_hcplantext_column(df):
    """Create hcplantext column and populate with hcpcode data."""
    hcpcode_map = {'300':'Alliance', '340':'Blue Cross', '051':'Center for Elders',
                   '056':'ONLOK Seniors', '000':'z No Plan', None:'z No Plan'}
    df['hcplantext'] = df['hcpcode'].map(hcpcode_map)    

    def fix_hcplantext(df):
        """If someone has an HCplanText but their HCPstatus is such that it is invalidated, change
        HCplanText to 'z No Plan'"""
        df.ix[df.hcpstatus.isin(["00","10","09","19","40","49","S0","S9"]),
              'hcplantext'] = "z No Plan"
        df['hcplantext'] = df['hcplantext'].fillna('z No Plan')
        return df
        
    df = fix_hcplantext(df)
    return df

def format_string_columns(df, save_info):
    """  SavWriter will translate NaNs in string columns to output the string 'NaN'. Since that
    isn't the desired output, replace each NaN in a string column with an empty string."""
    string_cols = [x for x in save_info['types'] if save_info['types'][x] > 0]
    df[string_cols] = df[string_cols].fillna('')
    return df

def set_medical_file_location(argv):
    if len(argv) == 2:
        return argv[1]
    else:
        return config.medical_file
