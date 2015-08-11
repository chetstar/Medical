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

WITH sp0 AS (
     SELECT ES.cin, ES.source_date, ES.eligibility_date, ES.aidcode,
     	    ES.eligibility_status, ES.responsible_county, AC.fully_covered,
	    AC.federal_financial_participation
     FROM client_eligibility_status ES
     	  LEFT JOIN aidcodes AC
	  ON ES.aidcode = AC.aidcode
     WHERE cardinal = 0),

     sp1 AS (
     SELECT ES.cin, ES.source_date, ES.eligibility_date, ES.aidcode,
     	    ES.eligibility_status, ES.responsible_county, AC.fully_covered,
	    AC.federal_financial_participation
     FROM client_eligibility_status ES
     	  LEFT JOIN aidcodes AC
	  ON ES.aidcode = AC.aidcode
     WHERE cardinal = 1),

     sp2 AS (
     SELECT ES.cin, ES.source_date, ES.eligibility_date, ES.aidcode,
     	    ES.eligibility_status, ES.responsible_county, AC.fully_covered,
	    AC.federal_financial_participation
     FROM client_eligibility_status ES
     	  LEFT JOIN aidcodes AC
	  ON ES.aidcode = AC.aidcode
     WHERE cardinal = 2),

     sp3 AS (
     SELECT ES.cin, ES.source_date, ES.eligibility_date, ES.aidcode,
     	    ES.eligibility_status, ES.responsible_county, AC.fully_covered,
	    AC.federal_financial_participation
     FROM client_eligibility_status ES
     	  LEFT JOIN aidcodes AC
	  ON ES.aidcode = AC.aidcode
     WHERE cardinal = 3)

SELECT sp0.cin,
       sp0.source_date AS calendar,
       sp0.eligibility_date AS medsmonth,

       sp0.aidcode,
       sp0.eligibility_status,
       sp0.responsible_county,
       sp0.fully_covered AS full,
       sp0.federal_financial_participation AS ffp,

       sp1.aidcode AS aidcode_sp1,
       sp1.eligibility_status AS eligibility_status_sp1,
       sp1.responsible_county AS responsible_county_sp1,
       sp1.fully_covered AS full_sp1,
       sp1.federal_financial_participation AS ffp_sp1,

       sp2.aidcode AS aidcode_sp2,
       sp2.eligibility_status AS eligibility_status_sp2,
       sp2.responsible_county AS responsible_county_sp2,
       sp2.fully_covered AS full_sp2,
       sp2.federal_financial_participation AS ffp_sp2,

       sp3.aidcode AS aidcode_sp3,
       sp3.eligibility_status AS eligibility_status_sp3,
       sp3.responsible_county AS responsible_county_sp3,
       sp3.fully_covered AS full_sp3,
       sp3.federal_financial_participation AS ffp_sp3,

       CDS.primary_aidcode,
       CDS.ssi,
       CDS.rank AS mcrank,
       CDS.ccs,
       CDS.ihss,
       CDS.foster,
       CDS.disabled,
       CDS.soc,
       CDS.retro AS retromc
       
FROM sp0
     INNER JOIN sp1
     ON sp0.cin = sp1.cin
     AND sp0.eligibility_date = sp1.eligibility_date
     AND sp0.source_date = sp1.source_date
     INNER JOIN sp2
     ON sp0.cin = sp2.cin
     AND sp0.eligibility_date = sp2.eligibility_date
     AND sp0.source_date = sp2.source_date
     INNER JOIN sp3
     ON sp0.cin = sp3.cin
     AND sp0.eligibility_date = sp3.eligibility_date
     AND sp0.source_date = sp3.source_date
     INNER JOIN client_derived_status CDS
     ON sp0.cin = CDS.cin
     AND sp0.eligibility_date = CDS.eligibility_date
     AND sp0.source_date = CDS.source_date
