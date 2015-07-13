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
       "id" SMALLSERIAL PRIMARY KEY,
       "county_code" TEXT,
       "county_name" TEXT,
       CONSTRAINT county_codes_CK_county_code CHECK (char_length(county_code) = 2),
       CONSTRAINT county_codes_UQ_county_code UNIQUE (county_code)
);

CREATE TYPE sex_enum AS ENUM ('Male','Female','Intersex','Unknown','Other');

CREATE TABLE "client_attributes" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "date_of_birth" DATE,
       "meds_id" TEXT,
       "hic" TEXT,
       "hic_suffix" TEXT,
       "race" TEXT, --Constrain
       "language" TEXT, --Constrain
       "sex" SEX_ENUM,
       CONSTRAINT client_attributes_CK_cin_length CHECK (length(cin) <= 9),
       CONSTRAINT client_attributes_CK_meds_id_length CHECK (length(meds_id) <= 9),
       CONSTRAINT client_attributes_CK_hic_length CHECK (length(hic) <= 9),
       CONSTRAINT client_attributes_CK_hic_suffix_length CHECK (length(hic_suffix) <= 2),
       CONSTRAINT client_attributes_CK_date CHECK 
       		  (date_of_birth > to_date('1895-01-01','YYYY-MM-DD')
);

CREATE TABLE "client_eligibility_status" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "date" DATE NOT NULL,
       "cardinal" SMALLINT NOT NULL, --eg. sp1,sp2,sp3 or no sp
       "aidcode" TEXT,
       "eligibility_status" TEXT, --Still needs a constraint.(needs table of valid statuses)
       "responsible_county" TEXT,
       CONSTRAINT client_eligibility_status_CK_cardinal_size CHECK (cardinal IN (0,1,2,3)),
       CONSTRAINT client_eligibility_status_FK_aidcode FOREIGN KEY (aidcode) 
       		  REFERENCES aidcodes (aidcode) ON DELETE RESTRICT,
       CONSTRAINT client_eligibility_status_UQ_cin_date_cardinal UNIQUE (cin, "date", cardinal),
       CONSTRAINT client_eligibility_status_FK_responsible_county FOREIGN KEY (responsible_county)
       		  REFERENCES county_codes (county_code) ON DELETE RESTRICT,
       CONSTRAINT client_eligibility_status_FK_cin FOREIGN KEY (cin)
       		  REFERENCES client_attributes (cin) ON DELETE RESTRICT
);

CREATE TABLE "client_addresses" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "date" DATE NOT NULL,
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
       "date" DATE NOT NULL,
       "resident_county" TEXT,
       "soc_amount" TEXT,
       "medicare_status" TEXT,
       "carrier_code" TEXT,
       "federal_contract_number" TEXT,
       "plan_id" TEXT,
       "hcp_status" TEXT,
       "hcp_code" TEXT,
       "surs_code" TEXT,
       "special_obligation" TEXT,
       "healthy_families_date" DATE,
       CONSTRAINT client_eligibility_base_FK_cin FOREIGN KEY (cin)
       		  REFERENCES client_attributes (cin) ON DELETE RESTRICT,
       CONSTRAINT client_eligiblity_base_FK_resident_county FOREIGN KEY (resident_county)
       		  REFERENCES county_codes (county_code) ON DELETE RESTRICT,
       CONSTRAINT client_eligibility_base_CK_medicare_status CHECK (length(medicare_status) <= 3),
       CONSTRAINT client_eligibility_base_CK_carrier_code CHECK (length(carrier_code) <= 4),
       CONSTRAINT client_eligibility_base_CK_federal_contract_number CHECK
       		  (length(federal_contract_number) <= 4),
);

/*
INSERT INTO client_eligibility_status (cin, "date", cardinal, aidcode) 
VALUES 
       ('999999999', to_date('2012-12-20','YYYY-MM-DD'), 3, '0C')
       ('999999999', to_date('2012-12-20','YYYY-MM-DD'), 2, null)
       ;
*/



       
