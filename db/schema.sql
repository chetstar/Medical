CREATE TABLE "aidcodes" (
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

CREATE TABLE "county_codes" (
       --Contains all 58 valid county codes with names for the state of California.
       "id" SMALLSERIAL PRIMARY KEY,
       "county_code" TEXT,
       "county_name" TEXT,
       CONSTRAINT county_codes_CK_county_code CHECK (char_length(county_code) = 2),
       CONSTRAINT county_codes_UQ_county_code UNIQUE (county_code)
);

CREATE TABLE "hcp_statuses" (
       --Contains all valid hcp_status codes with descriptions.
       "id" SMALLSERIAL PRIMARY KEY,
       "code" TEXT NOT NULL,
       "desciption" TEXT NOT NULL,
       CONSTRAINT hcp_statuses_CK_code CHECK (char_length(code) <= 2),
       CONSTRAINT hcp_statuses_UQ_code UNIQUE (code)
);

CREATE TYPE sex_enum AS ENUM ('Male','Female','Intersex','Unknown','Other');

CREATE TABLE "client_attributes" (
       -- cin = client index number
       -- hic = health insurance claim
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "date_of_birth" DATE,
       "meds_id" TEXT,
       "hic_number" TEXT, 
       "hic_suffix" TEXT,
       "ethnicity" TEXT, --Make table to constrain to. Store English term, not code.
       "sex" SEX_ENUM, 
       "primary_language" TEXT, --Make table to constrain to. Store English term, not code.
       CONSTRAINT client_attributes_CK_cin_length CHECK (char_length(cin) <= 9),
       CONSTRAINT client_attributes_CK_meds_id_length CHECK (char_length(meds_id) <= 9),
       CONSTRAINT client_attributes_CK_hic_number_length CHECK (char_length(hic_number) <= 9),
       CONSTRAINT client_attributes_CK_hic_suffix_length CHECK (char_length(hic_suffix) <= 2),
       CONSTRAINT client_attributes_CK_date CHECK 
       		  (date_of_birth > to_date('1895-01-01','YYYY-MM-DD')),
       CONSTRAINT client_attributes_UQ_cin UNIQUE (cin)
);

CREATE TABLE "client_names" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source" TEXT,
       "source_date" DATE,
       "first_name" TEXT,
       "middle_name" TEXT,
       "last_name" TEXT,
       "middle_initial" TEXT,
       "full_name" TEXT,
       "suffix" TEXT,
       CONSTRAINT client_names_FK_cin FOREIGN KEY (cin)
       		  REFERENCES client_attributes (cin) ON DELETE RESTRICT
);

CREATE TABLE "client_addresses" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "street" TEXT,
       "unit" TEXT,
       "city" TEXT,
       "state" TEXT, --Constrain to list?
       "zip" TEXT, --How to deal with zip+4?
       "raw" TEXT, --Unparsed address.
       "source" TEXT,
       CONSTRAINT client_addresses_FK_cin FOREIGN KEY (cin)
       		  REFERENCES client_attributes (cin) ON DELETE RESTRICT       
);

CREATE TABLE "client_eligibility_base" (
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
       CONSTRAINT client_eligibility_base_UQ_cin_date_date UNIQUE
       		  (cin, source_date, eligibility_date),
       CONSTRAINT client_eligibility_base_FK_cin FOREIGN KEY (cin)
       		  REFERENCES client_attributes (cin) ON DELETE RESTRICT,
       CONSTRAINT client_eligiblity_base_FK_resident_county FOREIGN KEY (resident_county)
       		  REFERENCES county_codes (county_code) ON DELETE RESTRICT,
       CONSTRAINT client_eligibility_base_CK_medicare_status CHECK
       		  (char_length(medicare_status) <= 3),
       CONSTRAINT client_eligibility_base_CK_carrier_code CHECK (char_length(carrier_code) <= 4),
       CONSTRAINT client_eligibility_base_CK_federal_contract_number CHECK
       		  (length(federal_contract_number) <= 5)
);

CREATE TABLE "client_hcp_status" (
       --HCP = Health Care Plan
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "eligibility_date" DATE NOT NULL,
       "cardinal" SMALLINT,
       "hcp_status" TEXT,
       "hcp_code" TEXT,
       CONSTRAINT client_hcp_status_FK_cin FOREIGN KEY (cin)
       		  REFERENCES client_attributes (cin) ON DELETE RESTRICT,
       CONSTRAINT client_hcp_status_CK_cardinal CHECK (cardinal IN (0,1,2)),
       CONSTRAINT client_hcp_status_FK_hcp_status FOREIGN KEY (hcp_status)
       		  REFERENCES hcp_statuses (code) ON DELETE RESTRICT,
       CONSTRAINT client_hcp_status_UQ_cin_date_date_cardinal UNIQUE
       		  (cin, source_date, eligibility_date, cardinal)
);

CREATE TABLE "client_eligibility_status" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "eligibility_date" DATE NOT NULL,
       "cardinal" SMALLINT NOT NULL, --eg. sp1,sp2,sp3 or no sp
       "aidcode" TEXT,
       "eligibility_status" TEXT, --Still needs a constraint.(needs table of valid statuses)
       "responsible_county" TEXT,
       CONSTRAINT client_eligibility_status_CK_cardinal_size CHECK (cardinal IN (0,1,2,3)),
       CONSTRAINT client_eligibility_status_FK_aidcode FOREIGN KEY (aidcode) 
       		  REFERENCES aidcodes (aidcode) ON DELETE RESTRICT,
       CONSTRAINT client_eligibility_status_UQ_cin_date_date_cardinal UNIQUE
       		  (cin, source_date, eligibility_date, cardinal),
       CONSTRAINT client_eligibility_status_FK_responsible_county FOREIGN KEY (responsible_county)
       		  REFERENCES county_codes (county_code) ON DELETE RESTRICT,
       CONSTRAINT client_eligibility_status_FK_cin FOREIGN KEY (cin)
       		  REFERENCES client_attributes (cin) ON DELETE RESTRICT
);

CREATE TABLE "client_derived_status" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source_date" DATE NOT NULL,
       "eligibility_date" DATE NOT NULL,
       "rank" SMALLINT NOT NULL,
       "primary_aidcode" TEXT,
       "disabled" BOOLEAN NOT NULL,
       "foster" BOOLEAN NOT NULL,
       "retro" BOOLEAN NOT NULL,
       "ssi" BOOLEAN NOT NULL,
       "ccs" BOOLEAN NOT NULL,
       "ihss" BOOLEAN NOT NULL,
       "soc" BOOLEAN NOT NULL,
       CONSTRAINT client_derived_status_UQ_cin_date_date UNIQUE
       		  (cin, source_date, eligibility_date)
);
       

/*
INSERT INTO client_eligibility_status (cin, "date", cardinal, aidcode) 
VALUES 
       ('999999999', to_date('2012-12-20','YYYY-MM-DD'), 3, '0C')
       ('999999999', to_date('2012-12-20','YYYY-MM-DD'), 2, null)
       ;
*/



       
