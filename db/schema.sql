CREATE TABLE "rules_aidcodes" (
       "id" SMALLSERIAL PRIMARY KEY,
       "aidcode" TEXT NOT NULL,
       "federal_financial_participation" SMALLINT NOT NULL,
       "fully_covered" BOOLEAN NOT NULL,
       "disabled" BOOLEAN NOT NULL,
       "foster" BOOLEAN NOT NULL,
       CONSTRAINT aidcodes_CK_aidcode_length CHECK (char_length(aidcode) <= 2),
       CONSTRAINT aidcodes_CK_aidcode_not_empty CHECK (aidcode <> ''),
       CONSTRAINT aidcodes_UQ_aidcode_unique UNIQUE (aidcode),
       CONSTRAINT aidcodes_CK_federal_financial_participation CHECK
       		  (federal_financial_participation IN (0,50,65,100))
);

CREATE TABLE "rules_county_codes" (
       --Contains all 58 valid county codes with names for the state of California.
       "id" SMALLSERIAL PRIMARY KEY,
       "county_code" TEXT,
       "county_name" TEXT,
       CONSTRAINT county_codes_CK_county_code CHECK (char_length(county_code) = 2),
       CONSTRAINT county_codes_UQ_county_code UNIQUE (county_code)
);

CREATE TABLE "rules_hcp_status_codes" (
       --Contains all valid hcp_status codes with descriptions.
       "id" SMALLSERIAL PRIMARY KEY,
       "code" TEXT NOT NULL,
       "desciption" TEXT NOT NULL,
       CONSTRAINT hcp_status_codes_CK_code CHECK (char_length(code) <= 2),
       CONSTRAINT hcp_status_codes_UQ_code UNIQUE (code)
);

CREATE TYPE sex_enum AS ENUM ('Male','Female','Intersex','Unknown','Other');

CREATE TABLE "medi_cal_attributes" (
       -- cin = client index number
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "date_of_birth" DATE,
       "meds_id" TEXT,
       "health_insurance_claim_number" TEXT, 
       "health_insurance_claim_suffix" TEXT,
       "ethnicity" TEXT, --Make table to constrain to.
       		   	 --Store English term, not code.
       "sex" SEX_ENUM, 
       "primary_language" TEXT, --Make table to constrain to.
       			  	--Store English term, not code.
       				--Or use enums for lang/ethnicity?
       CONSTRAINT medi_cal_attributes_CK_cin_length CHECK (char_length(cin) <= 9),
       CONSTRAINT medi_cal_attributes_CK_meds_id_length CHECK
       		  (char_length(meds_id) <= 9),
       CONSTRAINT medi_cal_attributes_CK_hic_number_length CHECK
       		  (char_length(health_insurance_claim_number) <= 9),
       CONSTRAINT medi_cal_attributes_CK_hic_suffix_length CHECK
       		  (char_length(health_insurance_claim_suffix) <= 2),
       CONSTRAINT medi_cal_attributes_CK_date CHECK 
       		  (date_of_birth > to_date('1895-01-01','YYYY-MM-DD')),
       CONSTRAINT medi_cal_attributes_UQ_cin_date UNIQUE (cin, source_date)
);

CREATE TABLE "medi_cal_names" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "first_name" TEXT,
       "middle_initial" TEXT,
       "last_name" TEXT,
       "suffix" TEXT,
       CONSTRAINT medi_cal_names_FK_cin_date FOREIGN KEY (cin, source_date)
       		  REFERENCES medi_cal_attributes (cin, source_date) ON DELETE RESTRICT
);

CREATE TABLE "medi_cal_addresses" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "street_address" TEXT,
       "city" TEXT,
       "state" TEXT, --Constrain to list?
       "zip" TEXT, --Constrain length, digits only.
       CONSTRAINT medi_cal_addresses_FK_cin_date FOREIGN KEY (cin, source_date)
       		  REFERENCES medi_cal_attributes (cin, source_date) ON DELETE RESTRICT
);

CREATE TABLE "medi_cal_eligibility_base" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "eligibility_date" DATE NOT NULL,
       "resident_county" TEXT,
       "soc_amount" TEXT,
       "medicare_status" TEXT,
       "carrier_code" TEXT,
       "federal_contract_number" TEXT,
       "plan_id" TEXT,
       "plan_type" TEXT,
       "surs_code" TEXT,
       "special_obligation" TEXT,
       "healthy_families_date" DATE,
       "other_health_coverage" TEXT, --Constrain to list, constrain by length.
       CONSTRAINT medi_cal_eligibility_base_UQ_cin_date_date UNIQUE
       		  (cin, source_date, eligibility_date),
       CONSTRAINT medi_cal_eligibility_base_FK_cin_date FOREIGN KEY (cin, source_date)
       		  REFERENCES medi_cal_attributes (cin, source_date) ON DELETE RESTRICT,
       CONSTRAINT medi_cal_eligiblity_base_FK_resident_county FOREIGN KEY (resident_county)
       		  REFERENCES rules_county_codes (county_code) ON DELETE RESTRICT,
       CONSTRAINT medi_cal_eligibility_base_CK_medicare_status CHECK
       		  (char_length(medicare_status) <= 3),
       CONSTRAINT medi_cal_eligibility_base_CK_carrier_code CHECK (char_length(carrier_code) <= 4),
       CONSTRAINT medi_cal_eligibility_base_CK_federal_contract_number CHECK
       		  (length(federal_contract_number) <= 5)
);

CREATE TABLE "medi_cal_hcp_status" (
       --HCP = Health Care Plan
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "eligibility_date" DATE NOT NULL,
       "cardinal" SMALLINT,
       "hcp_status_code" TEXT,
       "hcp_code" TEXT,
       CONSTRAINT medi_cal_hcp_status_FK_cin_date FOREIGN KEY (cin, source_date)
       		  REFERENCES medi_cal_attributes (cin, source_date) ON DELETE RESTRICT,
       CONSTRAINT medi_cal_hcp_status_CK_cardinal CHECK (cardinal IN (0,1,2)),
       CONSTRAINT medi_cal_hcp_status_FK_hcp_status FOREIGN KEY (hcp_status_code)
       		  REFERENCES rules_hcp_status_codes (code) ON DELETE RESTRICT,
       CONSTRAINT medi_cal_hcp_status_UQ_cin_date_date_cardinal UNIQUE
       		  (cin, source_date, eligibility_date, cardinal)
);

CREATE TABLE "medi_cal_eligibility_status" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "eligibility_date" DATE NOT NULL,
       "cardinal" SMALLINT NOT NULL, --eg. sp1,sp2,sp3 or no sp
       "aidcode" TEXT,
       "eligibility_status" TEXT, --Still needs a constraint.(needs table of valid statuses)
       "responsible_county" TEXT,
       CONSTRAINT medi_cal_eligibility_status_CK_cardinal_size CHECK (cardinal IN (0,1,2,3)),
       /*CONSTRAINT medi_cal_eligibility_status_FK_aidcode FOREIGN KEY (aidcode) 
       		  REFERENCES rules_aidcodes (aidcode) ON DELETE RESTRICT,*/
       CONSTRAINT medi_cal_eligibility_status_UQ_cin_date_date_cardinal UNIQUE
       		  (cin, source_date, eligibility_date, cardinal),
       CONSTRAINT medi_cal_eligibility_status_FK_responsible_county FOREIGN KEY (responsible_county)
       		  REFERENCES rules_county_codes (county_code) ON DELETE RESTRICT,
       CONSTRAINT medi_cal_eligibility_status_FK_cin_date FOREIGN KEY (cin, source_date)
       		  REFERENCES medi_cal_attributes (cin, source_date) ON DELETE RESTRICT
);

CREATE TABLE "medi_cal_derived_status" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "eligibility_date" DATE NOT NULL,
       "rank" SMALLINT NOT NULL,
       "primary_aidcode" TEXT,
       "primary_county_code" TEXT,
       "disabled" BOOLEAN NOT NULL,
       "foster" BOOLEAN NOT NULL,
       "retro" BOOLEAN NOT NULL,
       "ssi" BOOLEAN NOT NULL,
       "ccs" BOOLEAN NOT NULL,
       "ihss" BOOLEAN NOT NULL,
       "soc" BOOLEAN NOT NULL,
       CONSTRAINT medi_cal_derived_status_UQ_cin_date_date UNIQUE
       		  (cin, source_date, eligibility_date)
);
       
CREATE TABLE "rules_hcp_codes" (
       "id" SMALLSERIAL PRIMARY KEY,
       "plan_code" TEXT NOT NULL,
       "plan_name" TEXT NOT NULL
);

CREATE TABLE "rules_city_names" (
       "id" SMALLSERIAL PRIMARY KEY,
       "city_name" TEXT NOT NULL
);

CREATE TABLE "medi_cal_duplicates" (
       "id" SMALLSERIAL PRIMARY KEY,
       "row_text" TEXT
);

CREATE TABLE "rules_ethnicity_codes" (
       "id" SMALLSERIAL PRIMARY KEY,
       "ethnicity_code" TEXT,
       "ethnicity_text" TEXT
);
       
