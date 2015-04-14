def is_eligible(eligibility_status):
    if eligibility_status[0] < 5:
        return True
    else:
        return False

local_county_code = "01"

def is_local(responsible_county):
    if responsible_county == "01":
        return True
    else:
        return False

def create_medical_rank(dataframe):
    if
