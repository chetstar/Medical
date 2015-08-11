CREATE TABLE  language_codes (
       "id" SMALLSERIAL PRIMARY KEY,
       "language_code" TEXT,
       "language_text" TEXT NOT NULL
);

COPY language_codes (language_code, language_text)
FROM '/Users/greg/code/medical/db/language_codes.csv'
WITH CSV;
