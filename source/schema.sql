CREATE TABLE "client_eligibility_status" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT,
       "date" DATE,
       "cardinal" SMALLINT,
       "aidcode" TEXT,
       "eligibility_status" TEXT, --Still needs a constraint.
       "responsible_county" TEXT,
       CONSTRAINT eligibility_status_CK_cin_length CHECK (char_length(cin) <= 10),
       CONSTRAINT eligibility_status_CK_cardinal_size CHECK (cardinal < 4),
       CONSTRAINT eligibility_status_FK_aidcode REFERENCES aidcodes (aidcode) ON DELETE RESTRICT,
       CONSTRAINT eligibility_status_UQ_cin_date UNIQUE (cin, "date"),
       CONSTRAINT eligibility_status_FK_responsible_county REFERENCES county_codes (county_code)
       		  ON DELETE RESTRICT,
);
/*
CREATE TABLE "client_attributes" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT CHECK attributes_cin_length (char_length(cin) <= 10),
       "date_of_birth" DATE,
       "meds_id" TEXT,
       "hic" TEXT,
       "hic_suffix" TEXT,
       "ethnicity" TEXT, --enum?
       "language" TEXT, --enum
       "gender" TEXT,
);
*/
/*
CREATE TABLE "client_addresses" (
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT CHECK addresses_cin_length (char_length(cin) <= 10),
       "date" DATE,
       "street" TEXT,
       "unit" TEXT,
       "city" TEXT,
       "state" TEXT,
       "zip" TEXT,
       "source" TEXT,
);
*/

CREATE TABLE "aidcodes" (
       "id" SMALLSERIAL PRIMARY KEY,
       "aidcode" TEXT 
       CONSTRAINT aidcodes_CK_aidcode_length CHECK (char_length(aidcode) <= 2),
);

CREATE TABLE "county_codes" (
       "id" SMALLSERIAL PRIMARY KEY,
       "county_code" TEXT,
       CONSTRAINT county_codes_CK_county_code CHECK (char_length(county_code) == 2),
);

       
