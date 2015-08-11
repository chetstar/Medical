/*
SELECT ES.aidcode, fully_covered AS "full", disabled, foster, federal_financial_participation AS ffp 
FROM client_eligibility_status ES
     LEFT JOIN aidcodes AC
     ON ES.aidcode = AC.aidcode
*/
/*
SELECT * --ES0.aidcode AS aidcode, ES1.aidcode AS aidcode_sp1, ES2.aidcode AS aidcode_sp2
FROM client_eligibility_status ES0
     INNER JOIN client_eligibility_status ES1
     ON ES0.cin = ES1.cin
     	AND ES0.source_date = ES1.source_date
	AND ES0.eligibility_date = ES1.eligibility_date
	AND ES0.cardinal < ES1.cardinal
WHERE ES1.cardinal < 2 ;
*/

WITH sp0 AS
     (SELECT *
     FROM client_eligibility_status ES
     	  LEFT JOIN aidcodes AC
	  ON ES.aidcode = AC.aidcode)
SELECT * FROM sp0;
