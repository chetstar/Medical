def drop_summary_row(df):
    """Code to delete the last row if its a summary row."""
    df.drop(df.index[-1], inplace = True)
    return df

def drop_cinless_rows(df):
    """Drop all rows without a CIN."""
    df.dropna(subset = ['cin'], inplace = True)
    return df

def drop_duplicate_rows(df):
    """Remove duplicate rows keeping the row with the best eligibilityStatus."""
    df.sort(['cin','eligibilitystatus'], inplace = True)
    df.drop_duplicates(subset = 'cin', inplace = True)
    return df

def fix_hcplantext(df):
    """If someone has an HCplanText but their HCPstatus is such that it is invalidated, change
    HCplanText to 'z No Plan'"""
    df.ix[df.hcpstatus.isin(["00","10","09","19","40","49","S0","S9"]),'hcplantext'] = "z No Plan"
    df['hcplantext'] = df['hcplantext'].fillna('z No Plan')
    return df
