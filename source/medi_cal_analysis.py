def make_eligibility_bitmask(dw):
    elig = dw['eligibility_status'].dropna().str[0].astype(int).le(5).reindex(
        index = dw.index, fill_value = False)
    return elig

def make_local_bitmask(dw):
    return dw['responsible_county'].dropna().eq('01').reindex(index = dw.index, fill_value = False)

def make_covered_bitmask(dw):
    return dw['full'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def make_disabled_bitmask(dw):
    return dw['disabled'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def make_foster_bitmask(dw):
    return dw['foster'].dropna().eq(1).reindex(index = dw.index, fill_value = False)

def merge_aidcode_info(dw, df_aidcodes):
    """Merge in aidcode based info: foster, disabled, full, ffp."""
    dw = dw.merge(df_aidcodes, how = 'left')
    return dw

def mcrank(dw, elig, local, covered):
    """Create Medi-Cal ranks."""
    #Done in this order so worse ranks don't overwrite better ones.
    dw['mcrank'] = ((dw['aidcode'].notnull()) & (dw['ffp'] >= 1)).map({True:13})
    dw.loc[elig,'mcrank'] = dw['ffp'][elig].map({100:10, 65:11, 50:12})
    dw.loc[(elig & local), 'mcrank'] = dw['ffp'][elig & local].map({100:7, 65:8, 50:9})
    dw.loc[(elig & covered), 'mcrank'] = dw['ffp'][elig & covered].map({100:4, 65:5, 50:6})
    dw.loc[(elig & local & covered), 'mcrank'] = dw['ffp'][elig & local & covered].\
                                                 map({100:1, 65:2, 50:3})
    dw['mcrank'] = dw['mcrank'].fillna(14)
    return dw

def make_primary_codes(dw, elig):
    """Set primary_aid_code equal to aidcode and eligibility_county_code 
    equal to respcounty."""
    
    dw.loc[elig, 'primary_aidcode'] = dw['aidcode'][elig]
    dw.loc[elig, 'eligibility_county_code'] = dw['responsible_county'][elig]
    return dw

def make_disabled_column(dw, elig, disabled):
    dw['disabled'] = (elig & disabled)
    dw.loc[:,'disabled'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['disabled'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'disabled_r']
    return dw

def make_foster_column(dw, elig, foster):
    dw['foster'] = (elig & foster)
    dw.loc[:,'foster'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['foster'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'foster_r']
    return dw

def make_retromc_column(dw):
    """If the last character of the primary_Aid_Code is 2,3, or 5 set RetroMC to 1."""
    dw['retromc'] = dw['primary_aidcode'].dropna().str[-1].isin(['2','3','5'])
    dw.loc[:,'retromc'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['retromc'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'retromc_r']
    return dw

def make_ssi_column(dw, ssicodes):
    """If any aidcode in row is in ssicodes set ssi to '1'."""
    dw['ssi'] = dw['aidcode'].isin(ssicodes)
    dw.loc[:,'ssi'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['ssi'], 
                              on=['cin','eligibility_date'], rsuffix='_r').loc[:,'ssi_r']
    return dw

def make_ccsaidcode_column(dw, ccscodes):
    """If any aidcode in row is in ccscodes set ccsaidcode to '1'."""
    dw['ccsaidcode'] = dw['aidcode'].isin(ccscodes)
    dw.loc[:,'ccsaidcode'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['ccsaidcode'], 
                                     on=['cin','eligibility_date'], rsuffix='_r').loc[:,'ccsaidcode_r']
    return dw

def make_ihssaidcode_column(dw, ihsscodes):
    """If any aidcode in row is in ihsscodes set ihssaidcode to '1'."""
    dw['ihssaidcode'] = dw['aidcode'].isin(ihsscodes)
    dw.loc[:,'ihssaidcode'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['ihssaidcode'], 
                                      on=['cin','eligibility_date'], rsuffix='_r').loc[:,'ihssaidcode_r']
    return dw

def make_socmc_column(dw):
    """If the last character of any eligibility status in row is 1, set socmc to '1'."""
    dw['socmc'] = dw['eligibility_status'].dropna().str[-1].astype(int).eq(1)
    dw.loc[:,'socmc'] = dw.join(dw.groupby(['cin','eligibility_date']).max()['socmc'], 
                                   on=['cin','eligibility_date'], rsuffix='_r').loc[:,'socmc_r']
    return dw
        
def keep_best_mcrank(dw):
    """Groupby cin and calendar and keep only the row with the best mcrank 
    for each group."""
    dw = dw.sort('mcrank', ascending = True).groupby(['cin', 'eligibility_date']).first()
    dw['cin'] = dw.index.get_level_values('cin')
    dw['eligibility_date'] = dw.index.get_level_values('eligibility_date')
    return dw

def no_nulls(dw):
    no_null_cols = ['disabled', 'foster', 'retromc', 'ssi', 'ccsaidcode',
                    'ihssaidcode', 'socmc']
    dw.loc[:,no_null_cols] = dw[no_null_cols].fillna(False)
    return dw

def medi_cal_analysis(df, df_aidcodes, ssicodes, ccscodes, ihsscodes):

    df = merge_aidcode_info(df, df_aidcodes)

    elig = make_eligibility_bitmask(df)
    local = make_local_bitmask(df)
    covered = make_covered_bitmask(df)
    disabled = make_disabled_bitmask(df)
    foster = make_foster_bitmask(df)

    df = mcrank(df, elig, local, covered)    
    
    df = make_primary_codes(df, elig)
    df = make_disabled_column(df, elig, disabled)
    df = make_foster_column(df, elig, foster)
    df = make_retromc_column(df)
    df = make_ssi_column(df, ssicodes)
    df = make_ccsaidcode_column(df, ccscodes)
    df = make_ihssaidcode_column(df, ihsscodes)
    df = make_socmc_column(df)

    df = keep_best_mcrank(df)
    df = no_nulls(df)
    
    return df
