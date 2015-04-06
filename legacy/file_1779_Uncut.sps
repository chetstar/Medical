GET DATA  /TYPE=ODBC
  /CONNECT='DSN=MHS_CGdecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: '+
    'Statistics Common;WSID=HP2UA3081880'
  /SQL='SELECT *  FROM MedsDemographics ORDER BY CIN'
  /ASSUMEDSTRWIDTH=255.
CACHE.

*FREQ MEDSMONTH.
compute inDB=1.
save outfile='I:\temp\CinsInDB.sav' /keep cin inDB .


DEFINE @ThisMonthMEDStext() 
201412
!ENDDEFINE.

DEFINE @ThisMonthsMedsFile() 
Dec14
!ENDDEFINE.


DEFINE !getfile (fn=!TOKENS(1))
GET DATA  /TYPE = TXT
 /FILE = 
!quote(!concat('\\Covenas\mis_dwnld\STATE_MEDS FILES\MEDS_',!fn,'_1779.TXT'))
 /FIXCASE = 1
 /ARRANGEMENT = FIXED
 /FIRSTCASE = 1
 /IMPORTCASE = ALL
 /VARIABLES =
 /1  ssn 0-8 f9.0
 HIC 9 -18 A10 
 V2 19-20 F2.1
 year 21-24 A4
 month 25-26 A2
 day 27-28 A2
 sex 29-29 A2
 race 30-30 A2
 lang 31-31 A2
 V4 32-32 A1
 CaseName 33-50 A18
 lname 51-70 A20
 fname 71-85 A15
 middleInitial 86-86 A1
 suffix 87-89 A3
 V15 90-127 A37
 street 128-177 A50
 city 178-197 A20
 state 198-199 A2
 zip 200-204 F5.0
 EWcode 205-208 A6
 CIN 209-217 A9
 GOVT 218-218 f1
CountyCaseCode 219-220 a2
CountyAidCode 221-222 a2
CountyCaseID 223-229 a7
 v60 230-233 a4 
CMS 234-234 a1
v601 235 - 242 a8
 eligYear 243-246 A4
 eligMonth 247-248 a2
 AidCode 249-250 a2
 RespCounty 251-252 a2
 ResCounty 253-254 a2
 EligibilityStatus 255-257 a3
 SOCamount 258-262 a7
 MedicareStatus 263-265 a3
 CarrierCode 266-269 a4
 FederalContractNumber 270-274 A5
 PlanID 275-277 f3
 TypeID 278-279 a2
 v16 280-289 a11
 HCPstatus 290-291 a2
 HCPcode 292-294 a3
 OHC 295-295 a1
 v70 296-298 a3
 AidCodeSP1 299-300 a2
 RespCountySP1 301-302 a2
 EligibilityStatusSP1 303-305 a3
 AidCodeSP2 306-307 a2
 RespCountySP2 308-309 a2
 EligibilityStatusSP2 310-312 a3
 SOCpctSP 313-314 f2
 HF_EligDay_SP 315-318 a4
 AidCodeSP3 319-320 a2
 RespCountySP3 321-322 a2
 EligibilityStatusSP3 323-325 a3
 V17 326-327 A2
 V71 328-330 a3
 V72 331-332 a2
 V73 333-335 a3
 V18 336-338 A3
 V19 339-341 A3
 AidCode1 342-343 A2
 RespCounty1 344-345 a2
 V19A 346-347 a2
 EligibilityStatus1 348-350 a3
 V20 351-387 A37
 OHC1  388-388  a1
 V21 389-406 A18
 V22 407-446 A50
 v67 447-496 a50
 v68 497-521 a27
 eligYear4 522-525 A4
 eligMonth4 526-527 a2
 AidCode4 528-529 a2
 RespCounty4 530-531 a2
 ResCounty4 532-533 a2
 EligibilityStatus4 534-536 a3
 V27 537-542 A6
 V28 543-569 A27
 HCPstatus4 569-570 a2
 HCPcode4 571-573 a3
 v29 574-604 A32
 V30 605-610 A6
 V31 611-660 A50
 V32 661-672 A12
 V33 673-678 A6
 V34 679-728 A50
 V35 729-740 A12
 V36 741-746 A6
 V37 747-796 A50
 V38 797-808 A12
 V39 809-814 A6
 V40 815-864 A50
 V41 865-876 A12
 V42 877-882 A6
 V43 883-932 A50
 V44 933-944 A12
 V45 945-950 A6
 V46 951-1000 A50
 V47 1001-1012 A12
 V48 1013-1018 A6
 V49 1019-1068 A50
 V50 1069-1080 A12
 V51 1081-1086 A6
 V52 1087-1136 A50
 V53 1137-1148 A12
 V54 1149-1154 A6
 V55 1155-1216 A62
 V56 1217-1222 A6
 V57 1223-1284 A62
 V58 1285-1290 A6
 V59 1291-1338 A48
 .
!enddefine.
!getfile fn=@ThisMonthMEDStext.

CACHE.
exe.

if eligibilityStatus = " " eligibilityStatus = "889".
sort cases by CIN eligibilityStatus.
match files /file=* /by cin /first=Cin1.
*freq cin1.

if eligibilityStatus = "889" eligibilityStatus = " ".
select if cin1=1.
select if cin ne " " .
COMPUTE bday=NUMBER(concat(month,"/",day, "/", year),ADATE10).
FORMATS bday (date11).

string HCPlanText(a20).
if HCPcode="300" HCplanText="Alliance".
if HCPcode="340" HCplanText="Blue Cross".
if HCPcode="051" HCplanText="Center for Elders".
if HCPcode="056" HCplanText="ONLOK Seniors".
if HCPcode ="000" or HCPcode=" " HCplanText="z No Plan".
if HCplanText=" " HCplanText = "Other Plan".
IF HCPStatus="00" OR HCPStatus="09" OR HCPStatus="10" OR HCPStatus="19" OR HCPStatus="40" OR HCPStatus="49" OR HCPStatus="S0" OR HCPStatus="S9" HCplanText="z No Plan".

*COMPUTE ssn=NUMBER(ssn1,f9.0).

include 'I:\MedicalData\MedsEthnicity.sps'.
include 'I:\MedicalData\MedsLanguage.sps'.
include 'I:\Cities.sps'.

compute calendar = date.MOYR(Number(eligMonth,f2),Number(eligYear,f4)).
formats calendar(MOYR6).
*freq calendar.

DEFINE !savefile (fn=!TOKENS(1))
SAVE OUTFILE=
!quote(!concat('I:\MediCalData\meds_',!fn,'_uncut.sav'))
    /keep CaseName   respCounty   language calendar ssn  sex ethnicity street state zip CIN bday fname lname city  
	AidCode OHC SOCamount  EligibilityStatus HCplanText  ResCounty Govt CountyCaseCode CountyAidCode CountyCaseID 
	MedicareStatus HIC CarrierCode FederalContractNumber PlanID TypeID HCPstatus HCPcode region
	AidCodeSP1 RespCountySP1 EligibilityStatusSP1 AidCodeSP2 RespCountySP2 EligibilityStatusSP2  
 	 AidCodeSP3 RespCountySP3 EligibilityStatusSP3. 
!enddefine.
!savefile fn=@ThisMonthsMedsFile.

SAVE OUTFILE='I:\MediCalData\medsCurrentUncut.sav'
    /keep CaseName   respCounty   language calendar ssn  sex ethnicity street state zip CIN bday fname lname suffix middleInitial  city  
	AidCode OHC SOCamount  EligibilityStatus HCplanText  ResCounty Govt CountyCaseCode CountyAidCode CountyCaseID 
	MedicareStatus HIC CarrierCode FederalContractNumber PlanID TypeID HCPstatus HCPcode region
	AidCodeSP1 RespCountySP1 EligibilityStatusSP1 AidCodeSP2 RespCountySP2 EligibilityStatusSP2  
 	 AidCodeSP3 RespCountySP3 EligibilityStatusSP3. 

select if Any(AidCodeSP2,"9K","9M","9N","9R","9U") OR Any(AidCodeSP1,"9K","9M","9N","9R","9U") 
  OR Any(AidCodeSP3,"9K","9M","9N","9R","9U")
  or Any(AidCode,"9K","9M","9N","9R","9U").
*freq calendar.

rename vars AidCode = bob RespCounty = RespCountyBOB.

String RespCounty AidCode(a2).
if Any(AidCodeSP2,"9K","9M","9N","9R","9U")  AidCode  =  AidCodeSP2.
if Any(AidCodeSP2,"9K","9M","9N","9R","9U")  RespCounty =  RespCountySP2.
if Any(AidCodeSP1,"9K","9M","9N","9R","9U")  AidCode  =  AidCodeSP1.
if Any(AidCodeSP1,"9K","9M","9N","9R","9U")  RespCounty =  RespCountySP1.
if Any(AidCodeSP3,"9K","9M","9N","9R","9U")  AidCode  =  AidCodeSP3.
if Any(AidCodeSP3,"9K","9M","9N","9R","9U")  RespCounty =  RespCountySP3.
if Any(bob,"9K","9M","9N","9R","9U")  AidCode  =  bob.
if Any(bob,"9K","9M","9N","9R","9U")  RespCounty =  RespCountybob.
exe.

sort cases by aidCode.
match files/table='I:\CCStext.sav' /file=* /by aidCOde.

sort cases by cin.
rename vars aidCode = CCSaidCode RespCounty = CCSrespCounty.

DEFINE !savefile (fn=!TOKENS(1))
SAVE OUTFILE=
!quote(!concat('I:\MedicalData\medsCCS_',!fn,'.sav'))
/keep cin CCSAidCode CCStype CCStext calendar CCSrespCounty.
!enddefine.
!savefile fn=@ThisMonthsMedsFile.


get FILE='I:\MediCalData\medsCurrentUncut.sav'.
save outfile='K:\MediCalData\medsCurrentUncut.sav'.


get FILE='I:\MediCalData\medsCurrentUncut.sav'  /keep
CIN
ethnicity
language
sex
ssn
bday
fname
lname
street
city
state
zip calendar. 

rename vars
ethnicity = ethnicityMEDS
language = languageMEDS
sex = sexMEDS
ssn = SSNMeds
bday = bdayMEDS
fname = FnameMEDS
lname = LnameMEDS
street = StreetMeds
city = cityMEDS
state = StateMEDS
zip = zipMeds
calendar = MedsMonth.


 * SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'MedsDemographics' /MAP/REPLACE.


match files/table='I:\temp\CinsInDB.sav' /file=* /by cin.

temp.
select if missing(inDB).
save outfile='I:\temp\MedsAppend.sav' /drop inDB.

select if inDB=1.

*save outfile='I:\bob.sav'.

*get file='I:\bob.sav'.
*select if $casenum lt 100.

SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'Staging' /MAP /REPLACE
 /SQL=' Update MedsDemographics ' +
' SET ethnicityMEDS = stage.ethnicityMEDS , languageMEDS = stage.languageMEDS , sexMEDS = stage.sexMEDS ,  ' +
'  SSNMeds = stage.SSNMeds , bdayMEDS = stage.bdayMEDS ,FnameMEDS = stage.FnameMEDS , '  +
'   cityMeds = stage.CityMeds , StreetMEDS = stage.StreetMEDS , lnameMEDS = stage.lnameMEDS , '  +
'   StateMeds = stage.StateMeds , zipMEDS = stage.zipMEDS , MedsMonth = stage.MedsMonth  ' +
' From Staging stage, MedsDemographics   WHERE MedsDemographics.cin = stage.cin'.


get file='I:\temp\MedsAppend.sav'.

SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'MedsDemographics' /MAP /append.



GET DATA  /TYPE=ODBC
  /CONNECT='DSN=MHS_CGdecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: '+
    'Statistics Common;WSID=HP2UA3081880'
  /SQL='SELECT *  FROM MedsDemographics ORDER BY CIN'
  /ASSUMEDSTRWIDTH=255.


save outfile='I:\temp\MedsInfo.sav' 
/keep cin LnameMeds FnameMEDS bdayMEDS ssnMEDS sexMEDS streetMEds cityMEDS stateMEDS ssnMEDS languageMEDS ethnicityMEDS zipMEDS MedsMonth.

*FREQ MEDSMONTH.
compute inDB=1.
save outfile='I:\temp\CinsInDB.sav' /keep cin inDB .
save outfile='I:\temp\MedsDemographics.sav'.
save outfile='K:\MedsDemographics.sav'.

rename vars  LnameMEDS= Client_Last_Name fnameMEDS = client_First_Name bdayMEDS = Birth_date SexMEDS = sex 
StreetMEDS = street CityMEds = city ZipMEDS=zip StateMEDS = state.
save outfile='I:\temp\MedsBillingDemographics.sav' /keep cin  Client_Last_Name  Client_first_Name birth_Date sex street city state zip. 





