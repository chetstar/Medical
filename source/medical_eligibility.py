local_county_code = "01"

def is_eligible():
    if s['eligibility_status'][0] < 5:
        return True

def is_local():
    if s['RespCounty'] == local_county_code:
        return True

def is_covered():
    if s['Full'] == 1:
        return True

def ffp_ge_than(percentage):
    if s['Ffp'] >= percentage:
        return True

def create_medical_rank(s):
"""This function creates and populates a rank column depending on the eligibilityStatus, 
RespCounty, full and ffp columns of the Medi-Cal data."""
    if   is_eligible() and is_local() and is_covered() and ffp_ge_than(100): s['rank'] = 1
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(65 ): s['rank'] = 2
    elif is_eligible() and is_local() and is_covered() and ffp_ge_than(50 ): s['rank'] = 3

    elif is_eligible() and is_covered() and ffp_ge_than(100): s['rank'] = 4
    elif is_eligible() and is_covered() and ffp_ge_than(65 ): s['rank'] = 5
    elif is_eligible() and is_covered() and ffp_ge_than(50 ): s['rank'] = 6

    elif is_eligible() and is_local() and ffp_ge_than(100): s['rank'] = 7
    elif is_eligible() and is_local() and ffp_ge_than(65 ): s['rank'] = 8
    elif is_eligible() and is_local() and ffp_ge_than(50 ): s['rank'] = 9

    elif is_eligible() and ffp_ge_than(100): s['rank'] = 10
    elif is_eligible() and ffp_ge_than(65 ): s['rank'] = 11
    elif is_eligible() and ffp_ge_than(50 ): s['rank'] = 12

    elif is_eligible() and AidCode and ffp_ge_than(1): s['rank'] = 13

    return s


"""
#Alternate method of creating MCrank.  Should test them speed wise.
medical_rank_dictionary = {('5','01',1,100):1,
                           ('5','01',1,65 ):2,
                           ('5','01',1,50 ):3,
                           ('5',    ,1,100):4,
                           ('5',    ,1,65 ):5,
                           ('5',    ,1,50 ):6,}

def create_medical_rank(s):
    factors = tuple(s['eligibilityStatus'][0],s['RespCounty'],s['Full'],s['Ffp'])
    return s['MCrank'] = medical_rank_dictionary[factor]
"""
