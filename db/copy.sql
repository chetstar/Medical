COPY aidcodes (federal_financial_participation, aidcode, disabled, fully_covered, foster)
FROM '/Users/greg/code/medical/db/db_aidcodes.csv'
WITH CSV HEADER;

COPY county_codes (county_code, county_name)
FROM '/Users/greg/code/medical/db/db_county_codes.csv'
WITH CSV;

COPY hcp_statuses (code, desciption)
FROM '/Users/greg/code/medical/db/db_hcp_status_codes.csv'
WITH CSV;

COPY info_hcp_codes (plan_code, plan_name)
FROM '/Users/greg/code/medical/db/db_hcp_text.csv'
WITH CSV;
