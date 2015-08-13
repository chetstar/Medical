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
     WHERE cardinal = 3),

     plantext AS (
     SELECT CHS.cin, CHS.source_date, CHS.eligibility_date, IHC.plan_name
     FROM client_hcp_status CHS
     	  LEFT JOIN info_hcp_codes IHC
	  ON CHS.hcp_code = IHC.plan_code
     WHERE cardinal = 0)

SELECT sp0.cin,
       sp0.source_date AS medsmonth,
       sp0.eligibility_date AS calendar,
       to_char(sp0.eligibility_date, 'MON') AS elig_month,
       to_char(sp0.eligibility_date, 'YYYY') AS elig_year,

       CAST(sp0.aidcode AS varchar(3)),
       CAST(sp0.eligibility_status AS varchar(3)),
       CAST(sp0.responsible_county AS varchar(2)),
       boolean_to_smallint(sp0.fully_covered) AS full,
       sp0.federal_financial_participation AS ffp,

       CAST(sp1.aidcode AS varchar(3)) AS aidcode_sp1,
       CAST(sp1.eligibility_status AS varchar(3)) AS eligibility_status_sp1,
       CAST(sp1.responsible_county AS varchar(2)) AS responsible_county_sp1,
       boolean_to_smallint(sp1.fully_covered) AS full_sp1,
       sp1.federal_financial_participation AS ffp_sp1,

       CAST(sp2.aidcode AS varchar(3)) AS aidcode_sp2,
       CAST(sp2.eligibility_status AS varchar(3)) AS eligibility_status_sp2,
       CAST(sp2.responsible_county AS varchar(2)) AS responsible_county_sp2,
       boolean_to_smallint(sp2.fully_covered) AS full_sp2,
       sp2.federal_financial_participation AS ffp_sp2,

       CAST(sp3.aidcode AS varchar(3)) AS aidcode_sp3,
       CAST(sp3.eligibility_status AS varchar(3)) AS eligibility_status_sp3,
       CAST(sp3.responsible_county AS varchar(2)) AS responsible_county_sp3,
       boolean_to_smallint(sp3.fully_covered) AS full_sp3,
       sp3.federal_financial_participation AS ffp_sp3,

       CDS.primary_aidcode,
       boolean_to_smallint(CDS.ssi),
       CDS.rank AS mcrank,
       boolean_to_varchar(CDS.ccs) AS ccsaidcode,
       boolean_to_varchar(CDS.ihss) AS ihssaidcode,
       boolean_to_smallint(CDS.foster),
       boolean_to_smallint(CDS.disabled),
       boolean_to_smallint(CDS.soc) AS socmc,
       boolean_to_smallint(CDS.retro) AS retromc,
       CDS.primary_county_code AS eligibility_county_code,

       CEB.soc_amount AS socamount,
       CEB.medicare_status,
       CEB.other_health_coverage AS ohc,

       CHS.hcp_code,
       CHS.hcp_status,

       PT.plan_name AS hcplantext
     
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
     INNER JOIN client_eligibility_base CEB
     ON sp0.cin = CEB.cin
     AND sp0.eligibility_date = CEB.eligibility_date
     AND sp0.source_date = CEB.source_date
     INNER JOIN client_hcp_status CHS
     ON sp0.cin = CHS.cin
     AND sp0.eligibility_date = CHS.eligibility_date
     AND sp0.source_date = CHS.source_date
     INNER JOIN plantext PT
     ON sp0.cin = PT.cin
     AND sp0.eligibility_date = PT.eligibility_date
     AND sp0.source_date = PT.source_date

WHERE CHS.cardinal = 0
