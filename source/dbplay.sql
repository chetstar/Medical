CREATE TEMP TABLE "staging_attributes" (
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

-- List of CINS that ARE NOT in client_attributes.
SELECT S.cin
FROM "client_attributes" C
    INNER JOIN "staging_attributes" S
    ON C.cin = S.cin

INSERT INTO
