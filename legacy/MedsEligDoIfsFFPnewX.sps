*26 32 38 49 42 44. 
*get file='I:\medicalData\MedsCurrentUncut.sav'.



recode eligibilityStatus eligibilityStatussp1  eligibilityStatussp2 eligibilityStatussp3(" "= "999").
recode RespCounty RespCountysp1  RespCountysp2 RespCountysp3(" "= "99").

 * if eligibilityStatus = " " eligibilityStatus = "999".
 * if eligibilityStatusSP1 = " " eligibilityStatusSP1 = "999".
 * if eligibilityStatusSP2 = " " eligibilityStatusSP2 = "999".
 * if eligibilityStatusSP3 = " " eligibilityStatusSP3 = "999".

 * if respCounty = " " RespCounty = "99".
 * if respCountysp1 = " " RespCountysp1 = "99".
 * if respCountysp2 = " " RespCountysp2 = "99".
 * if respCountysp3 = " " RespCountysp3 = "99".

recode Full FullSP1 fullSP2 fullSP3 Ffp FfpSP1 ffpSP2 ffpSP3(sysmis=99).

do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01" AND full=1 AND FFP=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute slot=1.
compute mcRank=1.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute EligStatusBogus = EligibilityStatus.
compute FFP=100.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5  AND RespCountySP1 = "01" AND fullsp1=1 AND FFPsp1=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=2.
compute mcRank=1.
compute EligStatusBogus = EligibilityStatusSP1.
compute FFP=100.
else if  Number(substr(EligibilityStatusSP2,1,1),f1) lt 5  AND RespCountySP2 = "01" AND fullsp2=1 AND FFPsp2=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=3.
compute mcRank=1.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5  AND RespCountySP3 = "01"  AND fullsp3=1 AND FFPsp3=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=4.
compute mcRank=1.
compute EligStatusBogus = EligibilityStatusSP3.
compute FFP=100.
end if.

do if missing(Mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01" AND full=1 AND FFP=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute slot=5.
compute mcRank=2.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute EligStatusBogus = EligibilityStatus.
compute FFP=65.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5  AND RespCountySP1 = "01" AND fullsp1=1 AND FFPsp1=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=6.
compute mcRank=2.
compute EligStatusBogus = EligibilityStatusSP1.
compute FFP=65.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5 AND  RespCountySP2 = "01" AND fullsp2=1 AND FFPsp2=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=7.
compute mcRank=2.
compute EligStatusBogus = EligibilityStatusSP2.
compute FFP=65.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5 AND   RespCountySP3 = "01"  AND fullsp3=1 AND FFPsp3=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=8.
compute mcRank=2.
compute EligStatusBogus = EligibilityStatusSP3.
compute FFP=65.
end if.
end if.

do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01" AND full=1 AND FFP=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute slot=9.
compute mcRank=3.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5 AND  RespCountySP1 = "01" AND fullsp1=1 AND FFPsp1=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=10.
compute mcRank=3.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5 AND  RespCountySP2 = "01" AND fullsp2=1 AND FFPsp2=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=11.
compute mcRank=3.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5 AND  RespCountySP3 = "01"  AND fullsp3=1 AND FFPsp3=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=12.
compute mcRank=3.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.

do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5   AND full=1 AND FFP=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=13.
compute mcRank=4.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5   AND fullsp1=1 AND FFPsp1=100. 
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=14.
compute mcRank=4.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5   AND fullsp2=1 AND FFPsp2=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=15.
compute mcRank=4.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5   AND fullsp3=1 AND FFPsp3=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=16.
compute mcRank=4.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.

do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5   AND full=1 AND FFP=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=17.
compute mcRank=5.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5  AND fullsp1=1 AND FFPsp1=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=18.
compute mcRank=5.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5   AND fullsp2=1 AND FFPsp2=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=19.
compute mcRank=5.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5   AND fullsp3=1 AND FFPsp3=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=20.
compute mcRank=5.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.


do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5   AND full=1 AND FFP=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=21.
compute mcRank=6.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5   AND fullsp1=1 AND FFPsp1=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=22.
compute mcRank=6.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5  AND fullsp2=1 AND FFPsp2=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=23.
compute mcRank=6.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5   AND fullsp3=1 AND FFPsp3=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=24.
compute mcRank=6.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.


do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01" AND FFP=100 .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=25.
compute mcRank=7.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5 AND RespCountySP1 = "01" AND FFPsp1=100 .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=26.
compute mcRank=7.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5  AND RespCountySP2 = "01"  AND FFPsp2=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=27.
compute mcRank=7.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5  AND RespCountySP3 = "01"  AND FFPsp3=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=28.
compute mcRank=7.
compute EligStatusBogus = EligibilityStatusSP3.
end if .
end if.


do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01"  AND FFP=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=29.
compute mcRank=8.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5 AND  RespCountySP1 = "01"  AND FFPsp1 =65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=30.
compute mcRank=8.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5 AND RespCountySP2 = "01"   AND FFPsp2=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=31.
compute mcRank=8.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5 AND RespCountySP3 = "01"   AND FFPsp3=65 .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=32.
compute mcRank=8.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.


do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01" AND FFP=50 .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=33.
compute mcRank=9.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5 AND  RespCountySP1 = "01" AND FFPsp1=50 .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=34.
compute mcRank=9.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5 AND   RespCountySP2 = "01"  AND FFPsp2=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=35.
compute mcRank=9.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5  AND RespCountySP3 = "01"   AND FFPsp3=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=36.
compute mcRank=9.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.


do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5   AND FFP=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=37.
compute mcRank=10.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5   AND FFPsp1=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=38.
compute mcRank=10.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5   AND FFPsp2=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=39.
compute mcRank=10.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5 AND   FFPsp3=100.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=40.
compute mcRank=10.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.


do if missing(mcrank).
do if Number(substr(EligibilityStatus,1,1),f1) lt 5   AND FFP=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=41.
compute mcRank=11.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5   AND FFPsp1=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=42.
compute mcRank=11.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5 AND FFPsp2=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=43.
compute mcRank=11.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5  AND FFPsp3=65.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=44.
compute mcRank=11.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.

*freq mcRank.
do if missing(mcRank).
do if  Number(substr(EligibilityStatus,1,1),f1) lt 5   AND FFP=50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=45.
compute mcRank=12.
compute EligStatusBogus = EligibilityStatus.
else if  Number(substr(eligibilityStatusSP1,1,1),f1) lt 5 AND FFPsp1 = 50.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=46.
compute mcRank=12.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5 AND FFPsp2=50 .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=47.
compute mcRank=12.
compute EligStatusBogus = EligibilityStatusSP2.
else if  Number(substr(EligibilityStatusSP3,1,1),f1) lt 5 AND FFPsp3=50  .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=48.
compute mcRank=12.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if .
*freq mcRank.

do if missing(mcrank) .
do if Number(substr(EligibilityStatus,1,1),f1) lt 5 AND AidCode ne " " AND  FFP ne 0  .
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCode.
compute ELIGIBILITY_COUNTY_code = RespCounty.
compute slot=49.
compute mcRank=13.
compute EligStatusBogus = EligibilityStatus.
else if Number(substr(EligibilityStatusSP1,1,1),f1) lt 5 AND AidCodesp1 ne " "  AND  FFPsp1 ne 0.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP1.
compute ELIGIBILITY_COUNTY_code = RespCountySP1.
compute slot=50.
compute mcRank=13.
compute EligStatusBogus = EligibilityStatusSP1.
else if Number(substr(EligibilityStatusSP2,1,1),f1) lt 5 AND AidCodesp2 ne " "   AND  FFPsp2 ne 0.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP2.
compute ELIGIBILITY_COUNTY_code = RespCountySP2.
compute slot=51.
compute mcRank=13.
compute EligStatusBogus = EligibilityStatusSP2.
else if Number(substr(EligibilityStatusSP3,1,1),f1) lt 5  AND AidCodesp3 ne " "  AND  FFPsp3 ne 0.
compute eligibility_month= xdate.month(calendar).
compute eligibility_year = xdate.year(calendar).
compute primary_Aid_code = aidCodeSP3.
compute ELIGIBILITY_COUNTY_code = RespCountySP3.
compute slot=52.
compute mcRank=13.
compute EligStatusBogus = EligibilityStatusSP3.
end if.
end if.


















