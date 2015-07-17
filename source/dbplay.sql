CREATE TEMP TABLE "staging_attributes" (
       -- (Tested, works)
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
       CONSTRAINT staging_attributes_CK_cin_length CHECK (char_length(cin) <= 9),
       CONSTRAINT staging_attributes_CK_meds_id_length CHECK (char_length(meds_id) <= 9),
       CONSTRAINT staging_attributes_CK_hic_number_length CHECK (char_length(hic_number) <= 9),
       CONSTRAINT staging_attributes_CK_hic_suffix_length CHECK (char_length(hic_suffix) <= 2),
       CONSTRAINT staging_attributes_CK_date CHECK 
       		  (date_of_birth > to_date('1895-01-01','YYYY-MM-DD')),
       CONSTRAINT staging_attributes_UQ_cin UNIQUE (cin)
);

CREATE TEMP TABLE "staging_names" (
       -- (Tested, works)
       "id" BIGSERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL,
       "source" TEXT,
       "date" DATE,
       "first_name" TEXT,
       "middle_name" TEXT,
       "last_name" TEXT,
       "middle_initial" TEXT,
       "full_name" TEXT,
       CONSTRAINT staging_names_FK_cin FOREIGN KEY (cin)
       		  REFERENCES staging_attributes (cin) ON DELETE RESTRICT
);

CREATE TEMP TABLE "staging_addresses" (
       -- (Tested, works)
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
       CONSTRAINT staging_addresses_FK_cin FOREIGN KEY (cin)
       		  REFERENCES staging_attributes (cin) ON DELETE RESTRICT       
);

--Create table for CINs that aren't in the database.
CREATE TEMP TABLE new_cins (
       "id" SERIAL PRIMARY KEY,
       "cin" TEXT NOT NULL UNIQUE
);

--Populate new_cins table. (Tested, works)
INSERT INTO new_cins (cin)
SELECT S.cin
FROM client_attributes C
    RIGHT OUTER JOIN staging_attributes S
    ON C.cin = S.cin
WHERE C.id IS NULL
;

--Insert attributes for new clients
INSERT INTO client_attributes
       (cin, date_of_birth, meds_id, hic_number, hic_suffix, ethnicity, sex, primary_language)
SELECT S.cin, S.date_of_birth, S.meds_id, S.hic_number, S.hic_suffix, 
       S.ethnicity, S.sex, S.primary_language
FROM new_cins N
     INNER JOIN staging_attributes S
     ON N.cin = S.cin
;

--Insert names for new clients
INSERT INTO client_names
       (cin, source, date, first_name, middle_initial, last_name)
FROM new_cins N
     INNER JOIN staging_names S
     ON N.cin = S.cin
;

--Insert address for new clients.
INSERT INTO client_addresses
       (cin, source, date, street, unit, city, state, zip, raw)
FROM new_cins
     INNER JOIN staging_addresses S
     ON N.cin = S.cin
;

/*There are three main tables with information about the client themselves: attributes, names,
and addresses.  

client_attributes:
The data in the attribute table should be MOSTLY static. Date of Birth should 
only change if it was wrong or empty to start with, same for meds_id and hic_number. Sex is
static in the vast majority of cases, same with primary_language and ethnicity.  On any change to
those fields we should keep the new data and drop the old data as long as the new data is valid.
(eg, isn't an empty field replacing actual data.)

client_names and client_addresses:
If there is a change between the old data and the new data for the same source, add a new
entry with the new data.
*/

WITH cins_in_both AS 
     --List of cins that are in both client_attributes and staging_attributes.
     (
     SELECT S.cin
     FROM client_attributes C
     	  INNER JOIN staging_attributes S
     	  ON S.cin = C.cin
     WHERE C.id IS NOT NULL
      	  AND S.id IS NOT NULL
     ),
     union_no_dupes AS
     --All non dupe rows of staging and client attributes where cin is in both.
     (
     SELECT * FROM staging_attributes S WHERE S.cin IN (SELECT cin FROM cins_in_both)
     UNION
     SELECT * FROM client_attributes C WHERE c.cin IN (SELECT cin FROM cins_in_both)
     ),
     union_all AS 
     --All rows of staging_attributes and client_attributes where the cin is in both.
     (
     SELECT * FROM staging_attributes S WHERE S.cin IN (SELECT cin FROM cins_in_both)
     UNION ALL
     SELECT * FROM client_attributes C WHERE c.cin IN (SELECT cin FROM cins_in_both)
     ),
     dupes AS 
     --Rows that are the same in client_attributes and staging_attributes.
     (
     SELECT * FROM union_all
     EXCEPT
     SELECT * FROM union_no_dupes
     ),
     changed AS
     --Rows where cin is in both client and staging but there is a difference between the two.
     (
     SELECT * FROM staging_attributes S WHERE S.cin IN (SELECT cin FROM cins_in_both)
     EXCEPT
     SELECT * FROM dupes
     )
SELECT *
FROM changed
;

WITH cins_in_both AS 
     --List of cins that are in both client_attributes and staging_attributes.
     (
     SELECT S.cin
     FROM client_attributes C
     	  INNER JOIN staging_attributes S
     	  ON S.cin = C.cin
     WHERE C.id IS NOT NULL
      	  AND S.id IS NOT NULL
     ),

----Code below here is for testing.

--copy from client to staging.
INSERT INTO staging_attributes
       (cin, date_of_birth, meds_id, hic_number, hic_suffix, ethnicity, sex, primary_language)
SELECT S.cin, S.date_of_birth, S.meds_id, S.hic_number, S.hic_suffix, 
       S.ethnicity, S.sex, S.primary_language
FROM client_attributes S
WHERE S.id in (15,16,17,18,19,20)
;

update staging_attributes                                                                
set cin='00000000A'
where id = 1;

update staging_attributes                                                                
set cin='00000000B'
where id = 2; 

update staging_attributes                                                                
set cin='00000000C'
where id = 3; 

update staging_attributes
set cin='00000000C'
where id = 3; 
