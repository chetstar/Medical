
insert file='I:\modules\AidCodesShort.sps'.

DEFINE @ThisMonthMEDStext() 
201504
!ENDDEFINE.

DEFINE @ThisMonthsMedsFile() 
Apr15
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
 /1  ssn 0-8 f9
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
 V8 86-127 A47
 street 128-159 A32
 V12 160-177 A18
 city 178-197 A20
 V13 198-199 A2
 zip 200-204 F5.2
 EWcode 205-208 A4
 CIN 209-217 A9
GOVT 218-218 f1
CountyCaseCode 219-220 a2
CountyAidCode 221-222 a2
CountyCaseID 223-229 a7
 v60 230-233 a4 
CMS 234-234 a1
v601 235 - 242 a8
 eligYear 243-246 f4
 eligMonth 247-248 f2
 AidCode 249-250 a2
 RespCounty 251-252 a2
 ResCounty 253-254 a2
 EligibilityStatus 255-257 a3
 SOCamount 258-262 F5
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
 V17 326-335 A10
 eligYear1 336-339 f4
 eligMonth1 340-341 F2
 AidCode1 342-343 A2
 RespCounty1 344-345 a2
 ResCounty1 346-347 a2
 EligibilityStatus1 348-350 a3
 SOCamount1 351-355 f5
 MedicareStatus1 356-358 a3
 CarrierCode1 359-362 a4
 FederalContractNumber1 363-367 A5
 PlanID1 368-370 f3
 TypeID1 371-372 a2
 V20 373-382 A10
 HCPstatus1 383-384 A2
 HCPcode1 385-387 A3
 OHC1  388-388  a1
 V21 389-391 A3
 AidCodeSP1_1 392-393 a2
 RespCountySP1_1 394-395 a2
 EligibilityStatusSP1_1 396-398 a3
 AidCodeSP2_1 399-400 a2
 RespCountySP2_1 401-402 a2
 EligibilityStatusSP2_1 403-405 a3
 SOCpctSP_1 406-407 f2
 HF_EligDay_SP_1 408-411 a4
 AidCodeSP3_1 412-413 a2
 RespCountySP3_1 414-415 a2
 EligibilityStatusSP3_1 416-418 a3
 v22 419-428 a10
 EligYear2  429-432 f4
 EligMonth2 433-434 f2
 AidCode2 435-436 a2
 RespCounty2 437-438 a2
 ResCounty2 439-440 a2
 EligibilityStatus2 441-443 a3
 SocAmount2 444-448 f5
 MedicareStatus2 449-451 a3
 CarrierCode2 452-455 a4
 FederalContractNumber2 456-460 A5
 PlanID2 461-463 f3
 TypeID2 464-465 a2
 v25 466-475  A10
 HCPstatus2 476-477 a2
 HCPcode2  478-480 a3
 OHC2 481-481 a1
 v26 482-484 a3
 AidCodeSP1_2  485-486 a2
 RespCountySP1_2 487-488 a2
 EligibilityStatusSP1_2  489-491 a3
 AidCodeSP2_2 492-493 a2
 RespCountySP2_2  494-495 a2
 EligibilityStatusSP2_2  496-498 a3
 SOCpctSP_2 499-500  f2
 HF_EligDay_SP_2  501-504 a4
 AidCodeSP3_2  505-506 a2
 RespCountySP3_2  507-508 a2
 EligibilityStatusSP3_2  509-511 a3
 v27 512-521 a10
 eligYear3 522-525 f4
 eligMonth3 526-527 f2
 AidCode3 528-529 a2
 RespCounty3 530-531 a2
 ResCounty3 532-533 a2
 EligibilityStatus3 534-536 a3
 SOCamount3 537-541 f5
 MedicareStatus3 542-544 A3
 CarrierCode3 545-548 a4
 FederalContractNumber3 549-553 A5
 PlanID3 554-556 f3
 TypeID3 557-558 a2
 V28 559-568 A10
 HCPstatus3 569-570 a2
 HCPcode3 571-573 a3
 OHC3 574-574 A1
 v29 575-577 A3
 AidCodeSP1_3 578-579 a2
 RespCountySP1_3  580-581 a2
 EligibilityStatusSP1_3  582- 584 a3
 AidCodeSP2_3  585-586 a2
 RespCountySP2_3  587-588 a2
 EligibilityStatusSP2_3  589-591 a3
 SOCpctSP_3  592-593 f2
 HF_EligDay_SP_3  594-597 a4
 AidCodeSP3_3  598-599 a2
 RespCountySP3_3 600-601 a2
 EligibilityStatusSP3_3 602-604 a3
 V66 605-614 a10
 eligYear4 615-618 f4
 eligMonth4 619-620 f2
 AidCode4 621-622 a2
 RespCounty4 623-624 a2
 ResCounty4 625-626 a2
 EligibilityStatus4 627-629 a3
 SOCamount4 630-634 f5
 MedicareStatus4 635-637 a3
 CarrierCode4 638-641 a4
 FederalContractNumber4 642-646 A5
 PlanID4 647-649 f3
 TypeID4 651-651 a2
 v30 652-661 a10
 HCPstatus4 662-663 a2
 HCPcode4 664-666 a3
 OHC4 667-667 a1
 v31 668-670 a3
 AidCodeSP1_4 671-672  a2
 RespCountySP1_4  673-674 a2
 EligibilityStatusSP1_4  675-677 a3
 AidCodeSP2_4  678-679 a2
 RespCountySP2_4  680-681 a2
 EligibilityStatusSP2_4  682-684 a3
 SOCpctSP_4  685-686 f2
 HF_EligDay_SP_4  687-690 a4
 AidCodeSP3_4  691-692 a2
 RespCountySP3_4  693-694 a2
 EligibilityStatusSP3_4  695-697 a3
 v55 698-707 a10
 eligYear5 708-711 f4
 eligMonth5 712-713 f2
 AidCode5 714-715 a2
 RespCounty5 716-717 a2
 ResCounty5 718-719 a2
 EligibilityStatus5 720-722 a3
 SOCamount5 723-727 f5
 MedicareStatus5 728-730 a3
 CarrierCode5 731-734 a4
 FederalContractNumber5 735-739 A5
 PlanID5 740-742 f3
 TypeID5 743-744 a2
 v32 745-754 a10
 HCPstatus5 755-756 a2
 HCPcode5 757-759 a3
 OHC5 760-760 a1
 v33 761-763 a3
 AidCodeSP1_5  764-765 a2
 RespCountySP1_5  766-767 a2
 EligibilityStatusSP1_5  768-770 a3
 AidCodeSP2_5  771-772 a2
 RespCountySP2_5  773-774 a2
 EligibilityStatusSP2_5  775-777 a3
 SOCpctSP_5  778-779 f2
 HF_EligDay_SP_5  780-783 a4
 AidCodeSP3_5  784-785 a2
 RespCountySP3_5  786-787 a2
 EligibilityStatusSP3_5  788-790 a3
 v56 791-800 a10
 eligYear6 801-804 f4
 eligMonth6 805-806 f2
 AidCode6 807-808 a2
 RespCounty6 809-810 a2
 ResCounty6  811-812 a2
 EligibilityStatus6  813-815 a3
 SOCamount6  816-820 f5
 MedicareStatus6 821-823  a3
 CarrierCode6 824-827 a4
 FederalContractNumber6 828-832 A5
 PlanID6 833-835 f3
 TypeID6 836-837 a2
 v34 838-847  a10
 HCPstatus6 848-849 a2
 HCPcode6 850-852 a3
 OHC6 853-853 a1
 v35 854-856 a3
 AidCodeSP1_6  857-858 a2
 RespCountySP1_6 859-860 a2
 EligibilityStatusSP1_6  861-863 a3
 AidCodeSP2_6  864-865 a2
 RespCountySP2_6  866-867 a2
 EligibilityStatusSP2_6  868-870 a3
 SOCpctSP_6  871-872 f2
 HF_EligDay_SP_6  873-876 a4
 AidCodeSP3_6  877-878 a2
 RespCountySP3_6  879-880 a2
 EligibilityStatusSP3_6  881-883 a3
 v68 884-893 a10
 eligYear7 894-897 f4
 eligMonth7  898-899 f2
 AidCode7 900-901 a2
 RespCounty7  902-903 a2
 ResCounty7  904-905 a2
 EligibilityStatus7 906-908 a3
 SOCamount7 909-913 f5
 MedicareStatus7  914-916 a3
 CarrierCode7 917-920 a4
 FederalContractNumber7 921-925 A5
 PlanID7 926-928 f3
 TypeID7 929-930 a2
 v36 931-940  a10
 HCPstatus7 941-942  a2
 HCPcode7  943-945 a3
 OHC7  946-946 a1
 v37 947-949 a3
 AidCodeSP1_7 950-951 a2
 RespCountySP1_7  952-953 a2
 EligibilityStatusSP1_7  954-956 a3
 AidCodeSP2_7  957-958 a2
 RespCountySP2_7  959-960 a2
 EligibilityStatusSP2_7  961-963 a3
 SOCpctSP_7  964-965 f2
 HF_EligDay_SP_7 966-969 a4
 AidCodeSP3_7  970-971 a2
 RespCountySP3_7  972-973 a2
 EligibilityStatusSP3_7  974-976 a3
 v58 977-986 a10
 eligYear8  987-990 f4
 eligMonth8 991-992 f2
 AidCode8 993-994 a2
 RespCounty8  995-996 a2
 ResCounty8 997-998  a2
 EligibilityStatus8 999-1001 a3
 SOCamount8  1002-1006 f5
 MedicareStatus8 1007-1009  a3
 CarrierCode8 1010-1013 a4
 FederalContractNumber8 1014-1018 A5
 PlanID8 1019-1021 f3
 TypeID8 1022-1023 a2
 v38 1024-1033  a10
 HCPstatus8 1034-1035 a2
 HCPcode8 1036-1038 a3
 OHC8 1039-1039 a1
 v39 1040-1042 a3
 AidCodeSP1_8 1043-1044 a2
 RespCountySP1_8  1045-1046 a2
 EligibilityStatusSP1_8 1047-1049 a3
 AidCodeSP2_8  1050-1051 a2
 RespCountySP2_8  1052-1053 a2
 EligibilityStatusSP2_8   1054-1056 a3
 SOCpctSP_8  1057-1058 f2
 HF_EligDay_SP_8  1059-1062 a4
 AidCodeSP3_8  1063-1064 a2
 RespCountySP3_8  1065-1066 a2
 EligibilityStatusSP3_8  1067-1069 a3
 v59 1070-1079 a10
 eligYear9 1080-1083 f4
 eligMonth9  1084-1085 f2
 AidCode9  1086-1087 a2
 RespCounty9  1088-1089 a2
 ResCounty9  1090-1091 a2
 EligibilityStatus9 1092-1094  a3
 SOCamount9  1095-1099 f5
 MedicareStatus9 1100-1102 a3
 CarrierCode9 1103-1106 a4
 FederalContractNumber9 1107-1111 A5
 PlanID9 1112-1114 f3
 TypeID9 1115-1116 a2
 v40 1117-1126  a10
 HCPstatus9 1127-1128 a2
 HCPcode9  1129-1131 a3
 OHC9  1132-1132 a1
 v41 1133-1135 a3
 AidCodeSP1_9  1136-1137 a2
 RespCountySP1_9  1138-1139 a2
 EligibilityStatusSP1_9  1140-1142 a3
 AidCodeSP2_9  1143-1144 a2
 RespCountySP2_9  1145-1146 a2
 EligibilityStatusSP2_9  1147-1149 a3
 SOCpctSP_9  1150-1151 f2
 HF_EligDay_SP_9  1152-1155 a4
 AidCodeSP3_9  1156-1157 a2
 RespCountySP3_9  1158-1159 a2
 EligibilityStatusSP3_9  1160-1162 a3
 v61 1163-1172 a10
 eligYear10 1173-1176 f4
 eligMonth10  1177-1178 f2
 AidCode10 1179-1180 a2
 RespCounty10  1181-1182 a2
 ResCounty10 1183-1184 a2
 EligibilityStatus10  1185-1187 a3
 SOCamount10 1188-1192 f5
 MedicareStatus10 1193-1195 a3
 CarrierCode10 1196-1199 a4
 FederalContractNumber10 1200-1204 A5
 PlanID10 1205-1207 f3
 TypeID10 1208-1209 a2
 v42 1210-1219 a10
 HCPstatus10 1220-1221 a2
 HCPcode10  1222-1224 a3
 OHC10 1225-1225 a1
 v43 1226-1228 a3
 AidCodeSP1_10  1229-1230 a2
 RespCountySP1_10  1231-1232 a2
 EligibilityStatusSP1_10  1233-1235 a3
 AidCodeSP2_10  1236-1237 a2
 RespCountySP2_10  1238-1239 a2
 EligibilityStatusSP2_10  1240-1242 a3
 SOCpctSP_10 1243-1244 f2
 HF_EligDay_SP_10  1245-1248 a4
 AidCodeSP3_10  1249-1250 a2
 RespCountySP3_10  1251-1252 a2
 EligibilityStatusSP3_10  1253-1255 a3
 v61a 1256-1265 a10
 eligYear11 1266-1269 f4
 eligMonth11 1270-1271 f2
 AidCode11  1272-1273 a2
 RespCounty11  1274-1275 a2
 ResCounty11  1276-1277 a2
 EligibilityStatus11  1278-1280 a3
 SOCamount11  1281-1285 f5
 MedicareStatus11 1286-1288 a3
 CarrierCode11 1289-1292 a4
 FederalContractNumber11 1293-1297 A5
 PlanID11 1298-1300 f3
 TypeID11 1301-1302 a2
 v44 1303-1312  a10
 HCPstatus11  1313-1314 a2
 HCPcode11 1315-1317  a3
 OHC11  1318-1318 a1
 v45 1319-1321 a3
 AidCodeSP1_11  1322-1323 a2
 RespCountySP1_11  1324-1325 a2
 EligibilityStatusSP1_11  1326-1328 a3
 AidCodeSP2_11  1329-1330 a2
 RespCountySP2_11  1331-1332 a2
 EligibilityStatusSP2_11  1333-1335 a3
 SOCpctSP_11  1336-1337 f2
 HF_EligDay_SP_11  1338-1341 a4
 AidCodeSP3_11  1342-1343 a2
 RespCountySP3_11  1344-1345 a2
 EligibilityStatusSP3_11  1346-1348 a3
 v69 1349-1358 a10
 eligYear12 1359-1362 f4
 eligMonth12 1363-1364 f2
 AidCode12  1365-1366 a2
 RespCounty12 1367-1368 a2
 ResCounty12 1369-1370 a2
 EligibilityStatus12  1371-1373 a3
 SOCamount12 1374-1378 f5
 MedicareStatus12 1379-1381 a3
 CarrierCode12 1382-1385 a4
 FederalContractNumber12 1386-1390 A5
 PlanID12 1391-1393 f3
 TypeID12 1394-1395 a2
 v46 1396-1405 a10
 HCPstatus12 1406-1407 a2
 HCPcode12  1408-1410 a3
 OHC12 1411-1411 a1
 v47 1412-1414 a3
 AidCodeSP1_12 1415-1416 a2
 RespCountySP1_12  1417-1418 a2
 EligibilityStatusSP1_12 1419-1421 a3
 AidCodeSP2_12  1422-1423 a2
 RespCountySP2_12  1424-1425 a2
 EligibilityStatusSP2_12  1426-1428 a3
 SOCpctSP_12  1429-1430 f2
 HF_EligDay_SP_12  1431-1434 a4
 AidCodeSP3_12  1435-1436 a2
 RespCountySP3_12  1437-1438 a2
 EligibilityStatusSP3_12  1439-1441 a3
 v62 1442-1451 a10
 eligYear13 1452-1455 f4
 eligMonth13 1456-1457 f2
 AidCode13 1458-1459  a2
 RespCounty13 1460-1461  a2
 ResCounty13 1462-1463 a2
 EligibilityStatus13  1464-1466 a3
 SOCamount13 1467-1471 f5
 MedicareStatus13 1472-1474 a3
 CarrierCode13 1475-1478 a4
 FederalContractNumber13 1479-1483 A5
 PlanID13 1484-1486 f3
 TypeID13 1487-1488 a2
 v48 1489-1498 a10
 HCPstatus13 1499-1500  a2
 HCPcode13 1501-1503  a3
 OHC13  1504- 1504 a1
 v49 1505-1507 a3
 AidCodeSP1_13  1508-1509 a2
 RespCountySP1_13  1510-1511 a2
 EligibilityStatusSP1_13 1512-1514 a3
 AidCodeSP2_13  1515-1516 a2
 RespCountySP2_13  1517-1518 a2
 EligibilityStatusSP2_13  1519-1521 a3
 SOCpctSP_13  1522-1523 f2
 HF_EligDay_SP_13  1524-1527 a4
 AidCodeSP3_13  1528-1529 a2
 RespCountySP3_13  1530-1531 a2
 EligibilityStatusSP3_13  1532-1534 a3
 v63 1535-1544 a10
 eligYear14 1545-1548 f4
 eligMonth14 1549-1550 f2
 AidCode14 1551-1552 a2
 RespCounty14 1553-1554  a2
 ResCounty14 1555-1556 a2
 EligibilityStatus14  1557-1559 a3
 SOCamount14 1560-1564 f5
 MedicareStatus14 1565-1567 a3
 CarrierCode14 1568-1571 a4
 FederalContractNumber14 1572-1576 A5
 PlanID14 1577-1579 f3
 TypeID14 1580-1581 a2
 v50 1582-1591 a10
 HCPstatus14 1592-1593  a2
 HCPcode14 1594-1596 a3
 OHC14  1597-1597 a1
 v51 1598-1600 a40
 AidCodeSP1_14 1601-1602 a2
 RespCountySP1_14  1603-1604 a2
 EligibilityStatusSP1_14  1605-1607 a3
 AidCodeSP2_14  1608-1609 a2
 RespCountySP2_14  1610-1611 a2
 EligibilityStatusSP2_14  1612-1614 a3
 SOCpctSP_14  1615-1616 f2
 HF_EligDay_SP_14  1617-1620 a4
 AidCodeSP3_14  1621-1622 a2
 RespCountySP3_14  1623-1624 a2
 EligibilityStatusSP3_14  1625-1627 a3
 v64 1628-1637 a10
 eligYear15 1638-1641 f4
 eligMonth15 1642-1643 f2
 AidCode15 1644-1645 a2
 RespCounty15 1646-1647  a2
 ResCounty15 1648-1649 a2
 EligibilityStatus15  1650-1652 a3
 SOCamount15 1653-1657 f5
 MedicareStatus15 1658-1660 a3
 CarrierCode15 1661-1664 a4
 FederalContractNumber15 1665-1669 A5
 PlanID15 1670-1672 f3
 TypeID15 1673-1674 a2
 v52 1675-1684 a10
 HCPstatus15 1685-1686  a2
 HCPcode15 1687-1689 a3
 OHC15  1690-1690 a1
 v53 1691-1693 a3
 AidCodeSP1_15  1694-1695 a2
 RespCountySP1_15  1696-1697 a2
 EligibilityStatusSP1_15  1698-1700 a3
 AidCodeSP2_15  1701-1702 a2
 RespCountySP2_15  1703-1704 a2
 EligibilityStatusSP2_15  1705-1707 a3
 SOCpctSP_15  1708-1709 f2
 HF_EligDay_SP_15  1710-1713 a4
 AidCodeSP3_15  1714-1715 a2
 RespCountySP3_15  1716-1717 a2
 EligibilityStatusSP3_15  1718-1720 a3
 v65 1721-1778 a58
.
!enddefine.
!getfile fn=@ThisMonthMEDStext.

CACHE.

exe.

COMPUTE calendar  = date.MOYR(eligMonth, eligYear).

DEFINE !savefile (fn=!TOKENS(1))
agg outfile=
!quote(!concat('I:\temp\MedsCaseCodesStaging',!fn,'.sav'))
/break=cin GOVT EWcode CountyCaseCode  CountyCaseID 
/MedsMonth = max(Calendar).
!enddefine.
!savefile fn=@ThisMonthsMedsFile.

 * agg outfile='I:\Temp\MedsCaseCodesStaging.sav' 
/break=cin GOVT EWcode CountyCaseCode  CountyCaseID 
/MedsMonth = max(Calendar).

**OK to here 11/18/11.

*freq eligMonth.
LOOP #cnt=1 to 16.

- DO IF #cnt=1 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth, eligYear).
-   COMPUTE EligibilityStatus = EligibilityStatus.
-   COMPUTE AidCode = AidCode.
-   COMPUTE RespCounty = RespCounty.
-   COMPUTE SOCamount = SOCamount.
-   COMPUTE MedicareStatus = MedicareStatus.
 * -   COMPUTE CarrierCode = CarrierCode.
 * -   COMPUTE FederalContractNumber =FederalContractNumber.
 * -   COMPUTE PlanID=PlanID.
 * -   COMPUTE TypeID=TypeID.
-   COMPUTE HCPStatus = HCPStatus.
-   COMPUTE HCPCode = HCPCode.
-   COMPUTE OHC = OHC.
-   COMPUTE AidCodeSP1=AidCodeSP1. 
-   COMPUTE RespCountySP1=RespCountySP1.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1. 
-   COMPUTE AidCodeSP2=AidCodeSP2.  
-   COMPUTE RespCountySP2=RespCountySP2.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2. 
 * -   COMPUTE SOCpctSP=SOCpctSP.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP.
-   COMPUTE AidCodeSP3=AidCodeSP3.
-   COMPUTE RespCountySP3=RespCountySP3.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3.  
- END IF.

- DO IF #cnt=2 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth1, eligYear1).
-   COMPUTE EligibilityStatus = EligibilityStatus1.
-   COMPUTE AidCode = AidCode1.
-   COMPUTE RespCounty = RespCounty1.
-   COMPUTE SOCamount = SOCamount1.
-   COMPUTE MedicareStatus = MedicareStatus1.
 * -   COMPUTE CarrierCode = CarrierCode1.
 * -   COMPUTE FederalContractNumber =FederalContractNumber1.
 * -   COMPUTE PlanID=PlanID1.
 * -   COMPUTE TypeID=TypeID1.
-   COMPUTE HCPStatus = HCPStatus1.
-   COMPUTE HCPCode = HCPCode1.
-   COMPUTE OHC = OHC1.
-   COMPUTE AidCodeSP1=AidCodeSP1_1. 
-   COMPUTE RespCountySP1=RespCountySP1_1.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_1. 
-   COMPUTE AidCodeSP2=AidCodeSP2_1.  
-   COMPUTE RespCountySP2=RespCountySP2_1.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_1. 
 * -   COMPUTE SOCpctSP=SOCpctSP_1.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_1.
-   COMPUTE AidCodeSP3=AidCodeSP3_1.
-   COMPUTE RespCountySP3=RespCountySP3_1.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_1.  
- END IF.

- DO IF #cnt=3 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth2, eligYear2).
-   COMPUTE EligibilityStatus = EligibilityStatus2.
-   COMPUTE AidCode = AidCode2.
-   COMPUTE RespCounty = RespCounty2.
-   COMPUTE SOCamount = SOCamount2.
-   COMPUTE MedicareStatus = MedicareStatus2.
 * -   COMPUTE CarrierCode = CarrierCode2.
 * -   COMPUTE FederalContractNumber =FederalContractNumber2.
 * -   COMPUTE PlanID=PlanID2.
 * -   COMPUTE TypeID=TypeID2.
-   COMPUTE HCPStatus = HCPStatus2.
-   COMPUTE HCPCode = HCPCode2.
-   COMPUTE OHC = OHC2.
-   COMPUTE AidCodeSP1=AidCodeSP1_2. 
-   COMPUTE RespCountySP1=RespCountySP1_2.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_2. 
-   COMPUTE AidCodeSP2=AidCodeSP2_2.  
-   COMPUTE RespCountySP2=RespCountySP2_2.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_2. 
 * -   COMPUTE SOCm.
-   COMPUTE AidCodeSP3=AidCodeSP3_2.
-   COMPUTE RespCountySP3=RespCountySP3_2.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_2.  
- END IF.

- DO IF #cnt=4 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth3, eligYear3).
-   COMPUTE EligibilityStatus = EligibilityStatus3.
-   COMPUTE AidCode = AidCode3.
-   COMPUTE RespCounty = RespCounty3.
-   COMPUTE SOCamount = SOCamount3.
-   COMPUTE MedicareStatus = MedicareStatus3.
-   COMPUTE CarrierCode = CarrierCode3.
-   COMPUTE FederalContractNumber =FederalContractNumber3.
-   COMPUTE PlanID=PlanID3.
-   COMPUTE TypeID=TypeID3.
-   COMPUTE HCPStatus = HCPStatus3.
-   COMPUTE HCPCode = HCPCode3.
-   COMPUTE OHC = OHC3.
-   COMPUTE AidCodeSP1=AidCodeSP1_3. 
-   COMPUTE RespCountySP1=RespCountySP1_3.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_3. 
-   COMPUTE AidCodeSP2=AidCodeSP2_3.  
-   COMPUTE RespCountySP2=RespCountySP2_3.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_3. 
 * -   COMPUTE SOCpctSP=SOCpctSP_3.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_3.
-   COMPUTE AidCodeSP3=AidCodeSP3_3.
-   COMPUTE RespCountySP3=RespCountySP3_3.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_3.  
- END IF.

- DO IF #cnt=5 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth4, eligYear4).
-   COMPUTE EligibilityStatus = EligibilityStatus4.
-   COMPUTE AidCode = AidCode4.
-   COMPUTE RespCounty = RespCounty4.
-   COMPUTE SOCamount = SOCamount4.
-   COMPUTE MedicareStatus = MedicareStatus4.
 * -   COMPUTE CarrierCode = CarrierCode4.
 * -   COMPUTE FederalContractNumber =FederalContractNumber4.
 * -   COMPUTE PlanID=PlanID4.
 * -   COMPUTE TypeID=TypeID4.
-   COMPUTE HCPStatus = HCPStatus4.
-   COMPUTE HCPCode = HCPCode4.
-   COMPUTE OHC = OHC4.
-   COMPUTE AidCodeSP1=AidCodeSP1_4. 
-   COMPUTE RespCountySP1=RespCountySP1_4.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_4. 
-   COMPUTE AidCodeSP2=AidCodeSP2_4.  
-   COMPUTE RespCountySP2=RespCountySP2_4.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_4. 
 * -   COMPUTE SOCpctSP=SOCpctSP_4.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_4.
-   COMPUTE AidCodeSP3=AidCodeSP3_4.
-   COMPUTE RespCountySP3=RespCountySP3_4.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_4.  
- END IF.

- DO IF #cnt=6 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth5, eligYear5).
-   COMPUTE EligibilityStatus = EligibilityStatus5.
-   COMPUTE AidCode = AidCode5.
-   COMPUTE RespCounty = RespCounty5.
-   COMPUTE SOCamount = SOCamount5.
-   COMPUTE MedicareStatus = MedicareStatus5.
 * -   COMPUTE CarrierCode = CarrierCode5.
 * -   COMPUTE FederalContractNumber =FederalContractNumber5.
 * -   COMPUTE PlanID=PlanID5.
 * -   COMPUTE TypeID=TypeID5.
-   COMPUTE HCPStatus = HCPStatus5.
-   COMPUTE HCPCode = HCPCode5.
-   COMPUTE OHC = OHC5.
-   COMPUTE AidCodeSP1=AidCodeSP1_5. 
-   COMPUTE RespCountySP1=RespCountySP1_5.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_5. 
-   COMPUTE AidCodeSP2=AidCodeSP2_5.  
-   COMPUTE RespCountySP2=RespCountySP2_5.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_5. 
 * -   COMPUTE SOCpctSP=SOCpctSP_5.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_5.
-   COMPUTE AidCodeSP3=AidCodeSP3_5.
-   COMPUTE RespCountySP3=RespCountySP3_5.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_5.  
- END IF.

- DO IF #cnt=7 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth6, eligYear6).
-   COMPUTE EligibilityStatus = EligibilityStatus6.
-   COMPUTE AidCode = AidCode6.
-   COMPUTE RespCounty = RespCounty6.
-   COMPUTE SOCamount = SOCamount6.
-   COMPUTE MedicareStatus = MedicareStatus6.
 * -   COMPUTE CarrierCode = CarrierCode6.
 * -   COMPUTE FederalContractNumber =FederalContractNumber6.
 * -   COMPUTE PlanID=PlanID6.
 * -   COMPUTE TypeID=TypeID6.
-   COMPUTE HCPStatus = HCPStatus6.
-   COMPUTE HCPCode = HCPCode6.
-   COMPUTE OHC = OHC6.
-   COMPUTE AidCodeSP1=AidCodeSP1_6. 
-   COMPUTE RespCountySP1=RespCountySP1_6.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_6. 
-   COMPUTE AidCodeSP2=AidCodeSP2_6.  
-   COMPUTE RespCountySP2=RespCountySP2_6.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_6. 
 * -   COMPUTE SOCpctSP=SOCpctSP_6.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_6.
-   COMPUTE AidCodeSP3=AidCodeSP3_6.
-   COMPUTE RespCountySP3=RespCountySP3_6.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_6.  
- END IF.

- DO IF #cnt=8 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth7, eligYear7).
-   COMPUTE EligibilityStatus = EligibilityStatus7.
-   COMPUTE AidCode = AidCode7.
-   COMPUTE RespCounty = RespCounty7.
-   COMPUTE SOCamount = SOCamount7.
-   COMPUTE MedicareStatus = MedicareStatus7.
 * -   COMPUTE CarrierCode = CarrierCode7.
 * -   COMPUTE FederalContractNumber =FederalContractNumber7.
 * -   COMPUTE PlanID=PlanID7.
 * -   COMPUTE TypeID=TypeID7.
-   COMPUTE HCPStatus = HCPStatus7.
-   COMPUTE HCPCode = HCPCode7.
-   COMPUTE OHC = OHC7.
-   COMPUTE AidCodeSP1=AidCodeSP1_7. 
-   COMPUTE RespCountySP1=RespCountySP1_7.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_7. 
-   COMPUTE AidCodeSP2=AidCodeSP2_7.  
-   COMPUTE RespCountySP2=RespCountySP2_7.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_7. 
 * -   COMPUTE SOCpctSP=SOCpctSP_7.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_7.
-   COMPUTE AidCodeSP3=AidCodeSP3_7.
-   COMPUTE RespCountySP3=RespCountySP3_7.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_7.  
- END IF.

- DO IF #cnt=9 .
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth8, eligYear8).
-   COMPUTE EligibilityStatus = EligibilityStatus8.
-   COMPUTE AidCode = AidCode8.
-   COMPUTE RespCounty = RespCounty8.
-   COMPUTE SOCamount = SOCamount8.
-   COMPUTE MedicareStatus = MedicareStatus8.
 * -   COMPUTE CarrierCode = CarrierCode8.
 * -   COMPUTE FederalContractNumber =FederalContractNumber8.
 * -   COMPUTE PlanID=PlanID8.
 * -   COMPUTE TypeID=TypeID8.
-   COMPUTE HCPStatus = HCPStatus8.
-   COMPUTE HCPCode = HCPCode8.
-   COMPUTE OHC = OHC8.
-   COMPUTE AidCodeSP1=AidCodeSP1_8. 
-   COMPUTE RespCountySP1=RespCountySP1_8.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_8. 
-   COMPUTE AidCodeSP2=AidCodeSP2_8.  
-   COMPUTE RespCountySP2=RespCountySP2_8.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_8. 
 * -   COMPUTE SOCpctSP=SOCpctSP_8.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_8.
-   COMPUTE AidCodeSP3=AidCodeSP3_8.
-   COMPUTE RespCountySP3=RespCountySP3_8.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_8.  
- END IF.

- DO IF #cnt=10.
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth9, eligYear9).
-   COMPUTE EligibilityStatus = EligibilityStatus9.
-   COMPUTE AidCode = AidCode9.
-   COMPUTE RespCounty = RespCounty9.
-   COMPUTE SOCamount = SOCamount9.
-   COMPUTE MedicareStatus = MedicareStatus9.
 * -   COMPUTE CarrierCode = CarrierCode9.
 * -   COMPUTE FederalContractNumber =FederalContractNumber9.
 * -   COMPUTE PlanID=PlanID9.
 * -   COMPUTE TypeID=TypeID9.
-   COMPUTE HCPStatus = HCPStatus9.
-   COMPUTE HCPCode = HCPCode9.
-   COMPUTE OHC = OHC9.
-   COMPUTE AidCodeSP1=AidCodeSP1_9. 
-   COMPUTE RespCountySP1=RespCountySP1_9.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_9. 
-   COMPUTE AidCodeSP2=AidCodeSP2_9.  
-   COMPUTE RespCountySP2=RespCountySP2_9.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_9. 
 * -   COMPUTE SOCpctSP=SOCpctSP_9.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_9.
-   COMPUTE AidCodeSP3=AidCodeSP3_9.
-   COMPUTE RespCountySP3=RespCountySP3_9.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_9.  
- END IF.

- DO IF #cnt=11.
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth10, eligYear10).
-   COMPUTE EligibilityStatus = EligibilityStatus10.
-   COMPUTE AidCode = AidCode10.
-   COMPUTE RespCounty = RespCounty10.
-   COMPUTE SOCamount = SOCamount10.
-   COMPUTE MedicareStatus = MedicareStatus10.
 * -   COMPUTE CarrierCode = CarrierCode10.
 * -   COMPUTE FederalContractNumber =FederalContractNumber10.
 * -   COMPUTE PlanID=PlanID10.
 * -   COMPUTE TypeID=TypeID10.
-   COMPUTE HCPStatus = HCPStatus10.
-   COMPUTE  HCPCode = HCPCode10.
-   COMPUTE OHC = OHC10.
-   COMPUTE AidCodeSP1=AidCodeSP1_10. 
-   COMPUTE RespCountySP1=RespCountySP1_10.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_10. 
-   COMPUTE AidCodeSP2=AidCodeSP2_10.  
-   COMPUTE RespCountySP2=RespCountySP2_10.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_10. 
 * -   COMPUTE SOCpctSP=SOCpctSP_10.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_10.
-   COMPUTE AidCodeSP3=AidCodeSP3_10.
-   COMPUTE RespCountySP3=RespCountySP3_10.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_10.  
- END IF.

- DO IF #cnt=12.
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth11, eligYear11).
-   COMPUTE EligibilityStatus = EligibilityStatus11.
-   COMPUTE AidCode = AidCode11.
-   COMPUTE RespCounty = RespCounty11.
-   COMPUTE SOCamount = SOCamount11.
-   COMPUTE MedicareStatus = MedicareStatus11.
 * -   COMPUTE CarrierCode = CarrierCode11.
 * -   COMPUTE FederalContractNumber =FederalContractNumber11.
 * -   COMPUTE PlanID=PlanID11.
 * -   COMPUTE TypeID=TypeID11.
-   COMPUTE HCPStatus = HCPStatus11.
-   COMPUTE HCPCode = HCPCode11.
-   COMPUTE OHC = OHC11.
-   COMPUTE AidCodeSP1=AidCodeSP1_11. 
-   COMPUTE RespCountySP1=RespCountySP1_11.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_11. 
-   COMPUTE AidCodeSP2=AidCodeSP2_11.  
-   COMPUTE RespCountySP2=RespCountySP2_11.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_11. 
 * -   COMPUTE SOCpctSP=SOCpctSP_11.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_11.
-   COMPUTE AidCodeSP3=AidCodeSP3_11.
-   COMPUTE RespCountySP3=RespCountySP3_11.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_11.  
- END IF.

- DO IF #cnt=13.
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth12, eligYear12).
-   COMPUTE EligibilityStatus = EligibilityStatus12.
-   COMPUTE AidCode = AidCode12.
-   COMPUTE RespCounty = RespCounty12.
-   COMPUTE SOCamount = SOCamount12.
-   COMPUTE MedicareStatus = MedicareStatus12.
 * -   COMPUTE CarrierCode = CarrierCode12.
 * -   COMPUTE FederalContractNumber =FederalContractNumber12.
 * -   COMPUTE PlanID=PlanID12.
 * -   COMPUTE TypeID=TypeID12.
-   COMPUTE HCPStatus = HCPStatus12.
-   COMPUTE HCPCode = HCPCode12.
-   COMPUTE OHC = OHC12.
-   COMPUTE AidCodeSP1=AidCodeSP1_12. 
-   COMPUTE RespCountySP1=RespCountySP1_12.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_12. 
-   COMPUTE AidCodeSP2=AidCodeSP2_12.  
-   COMPUTE RespCountySP2=RespCountySP2_12.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_12. 
 * -   COMPUTE SOCpctSP=SOCpctSP_12.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_12.
-   COMPUTE AidCodeSP3=AidCodeSP3_12.
-   COMPUTE RespCountySP3=RespCountySP3_12.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_12.  
- END IF.


- DO IF #cnt=14.
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth13, eligYear13).
-   COMPUTE EligibilityStatus = EligibilityStatus13.
-   COMPUTE AidCode = AidCode13.
-   COMPUTE RespCounty = RespCounty13.
-   COMPUTE SOCamount = SOCamount13.
-   COMPUTE MedicareStatus = MedicareStatus13.
 * -   COMPUTE CarrierCode = CarrierCode13.
 * -   COMPUTE FederalContractNumber =FederalContractNumber13.
 * -   COMPUTE PlanID=PlanID13.
 * -   COMPUTE TypeID=TypeID13.
-   COMPUTE HCPStatus = HCPStatus13.
-   COMPUTE HCPCode = HCPCode13.
-   COMPUTE OHC = OHC13.
-   COMPUTE AidCodeSP1=AidCodeSP1_13. 
-   COMPUTE RespCountySP1=RespCountySP1_13.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_13. 
-   COMPUTE AidCodeSP2=AidCodeSP2_13.  
-   COMPUTE RespCountySP2=RespCountySP2_13.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_13. 
 * -   COMPUTE SOCpctSP=SOCpctSP_13.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_13.
-   COMPUTE AidCodeSP3=AidCodeSP3_13.
-   COMPUTE RespCountySP3=RespCountySP3_13.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_13.  
- END IF.


- DO IF #cnt=15.
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth14, eligYear14).
-   COMPUTE EligibilityStatus = EligibilityStatus14.
-   COMPUTE AidCode = AidCode14.
-   COMPUTE RespCounty = RespCounty14.
-   COMPUTE SOCamount = SOCamount14.
-   COMPUTE MedicareStatus = MedicareStatus14.
 * -   COMPUTE CarrierCode = CarrierCode14.
 * -   COMPUTE FederalContractNumber =FederalContractNumber14.
 * -   COMPUTE PlanID=PlanID14.
 * -   COMPUTE TypeID=TypeID14.
-   COMPUTE HCPStatus = HCPStatus14.
-   COMPUTE HCPCode = HCPCode14.
-   COMPUTE OHC = OHC14.
-   COMPUTE AidCodeSP1=AidCodeSP1_14. 
-   COMPUTE RespCountySP1=RespCountySP1_14.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_14. 
-   COMPUTE AidCodeSP2=AidCodeSP2_14.  
-   COMPUTE RespCountySP2=RespCountySP2_14.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_14. 
 * -   COMPUTE SOCpctSP=SOCpctSP_14.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_14.
-   COMPUTE AidCodeSP3=AidCodeSP3_14.
-   COMPUTE RespCountySP3=RespCountySP3_14.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_14.  
- END IF.


- DO IF #cnt=16.
-   COMPUTE CIN = CIN.
 * -   COMPUTE GOVT=GOVT.
 * -   COMPUTE CountyCaseCode=CountyCaseCode.
 * -   COMPUTE CountyCaseID=CountyCaseID.
-   COMPUTE calendar  = date.MOYR(eligMonth15, eligYear15).
-   COMPUTE EligibilityStatus = EligibilityStatus15.
-   COMPUTE AidCode = AidCode15.
-   COMPUTE RespCounty = RespCounty15.
-   COMPUTE SOCamount = SOCamount15.
-   COMPUTE MedicareStatus = MedicareStatus15.
 * -   COMPUTE CarrierCode = CarrierCode15.
 * -   COMPUTE FederalContractNumber =FederalContractNumber15.
 * -   COMPUTE PlanID=PlanID15.
 * -   COMPUTE TypeID=TypeID15.
-   COMPUTE HCPStatus = HCPStatus15.
-   COMPUTE HCPCode = HCPCode15.
-   COMPUTE OHC = OHC15.
-   COMPUTE AidCodeSP1=AidCodeSP1_15. 
-   COMPUTE RespCountySP1=RespCountySP1_15.  
-   COMPUTE EligibilityStatusSP1=EligibilityStatusSP1_15. 
-   COMPUTE AidCodeSP2=AidCodeSP2_15.  
-   COMPUTE RespCountySP2=RespCountySP2_15.  
-   COMPUTE EligibilityStatusSP2=EligibilityStatusSP2_15. 
 * -   COMPUTE SOCpctSP=SOCpctSP_15.
 * -   COMPUTE HF_EligDay_SP=HF_EligDay_SP_15.
-   COMPUTE AidCodeSP3=AidCodeSP3_15.
-   COMPUTE RespCountySP3=RespCountySP3_15.  
-   COMPUTE EligibilityStatusSP3=EligibilityStatusSP3_15.  
- END IF.

FORMATS Calendar(MOYR6).

- xsave OUTFILE='I:\temp\MedsEligExplodeX.sav'
	/KEEP CIN Calendar  EligibilityStatus AidCode RespCounty SOCamount MedicareStatus HCPStatus HCPCode OHC  AidCodeSP1    
RespCountySP1 EligibilityStatusSP1  aidCodeSP2  RespCountySP2  EligibilityStatusSP2   AidCodeSP3 RespCountySP3   EligibilityStatusSP3  .
END LOOP.
execute.
*freq calendar.

get FILE="I:\temp\MedsEligExplodeX.sav".

string HCPlanText(a20).
if HCPcode="300" HCplanText="Alliance".
if HCPcode="340" HCplanText="Blue Cross".
if HCPcode="051" HCplanText="Center for Elders".
if HCPcode="056" HCplanText="ONLOK Seniors".
if HCPcode ="000" or HCPcode=" " HCplanText="z No Plan".
if HCplanText=" " HCplanText = "Other Plan".
IF HCPStatus="00" OR HCPStatus="09" OR HCPStatus="10" OR HCPStatus="19" OR HCPStatus="40" OR HCPStatus="49" OR HCPStatus="S0" OR HCPStatus="S9" HCplanText="z No Plan".

if Number(substr(EligibilityStatus,1,1),f1) lt 5  OR 
 Number(substr(EligibilityStatusSP1,1,1),f1) lt 5  OR
 Number(substr(EligibilityStatusSP2,1,1),f1) lt 5  OR
 Number(substr(EligibilityStatusSP3,1,1),f1) lt 5 MCelig=1.

sort cases by cin calendar MCelig .
match files/file=* /by cin calendar/last=cinCal1.
*match files/file=* /by cin /last=cin1.
*freq cinCal1.
select if cinCal1=1 AND  cin  ne " ".
*select if mcelig=1.

sort cases by aidCode.
match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode /drop 
CinCal1 MCelig  .

*disp vars.
rename vars 
   full = fullx   
   FFP = FFPx
   aidCode = AidCodex
   foster=fosterx
   Disabled=Disabledx.

rename vars AidCodeSP1=AidCode.
sort cases by aidCode.
match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode .

rename vars 
   full=fullsp1
   FFP = FFPsp1
   aidCode = aidCodeSP1
   foster=fosterSP1
   disabled=disabledSP1.

rename vars AidCodeSP2=AidCode.
sort cases by aidCode.
match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode .

rename vars 
    full=fullsp2
    FFP = FFPsp2
    aidCode = aidCodeSP2
    foster=fosterSP2
    disabled=disabledSP2.

rename vars AidCodeSP3=AidCode.
sort cases by aidCode.
match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode .

rename vars 
   full=fullsp3
   FFP = FFPsp3
   aidCode = aidCodeSP3
   foster=fosterSP3
   disabled=disabledSP3.

rename vars 
   fullX = full   
   FFPx = FFP
   aidCodeX = AidCode.

if any(AidCode,"10","20","60") And  Number(substr(EligibilityStatus,1,1),f1) lt 5 SSI=1.

if Number(substr(EligibilityStatus,1,1),f1) lt 5 And fosterx=1 OR 
Number(substr(EligibilityStatussp1,1,1),f1) lt 5 And fostersp1=1 OR
Number(substr(EligibilityStatussp2,1,1),f1) lt 5 And fostersp2=1 OR
Number(substr(EligibilityStatussp3,1,1),f1) lt 5 And fostersp3=1 Foster=1.

if  Number(substr(EligibilityStatus,1,1),f1) lt 9 And Disabledx=1 OR 
Number(substr(EligibilityStatussp1,1,1),f1) lt 9 And Disabledsp1=1 OR
Number(substr(EligibilityStatussp2,1,1),f1) lt 9 And Disabledsp2=1 OR
Number(substr(EligibilityStatussp3,1,1),f1) lt 9 And Disabledsp3=1 Disabled=1.

string primary_Aid_Code ELIGIBILITY_COUNTY_code(a2).
string EligStatusBogus(a3).

insert file='I:\Janet\staging\MedsEligDoIfsFFPnewX.sps'.

if any(substr(EligStatusBogus,3,1) ,"2","3","5") RetroMC=1.

*****String SRC(A1).
*****if any(substr(EligStatusBogus,3,1) ,"2","3","5") SRC = "C".

if Number(substr(EligibilityStatus,1,1),f1) = 5  OR 
 Number(substr(EligibilityStatusSP1,1,1),f1) = 5  OR
 Number(substr(EligibilityStatusSP2,1,1),f1) = 5  OR
 Number(substr(EligibilityStatusSP3,1,1),f1) = 5 SOCmc=1.

*6/14 ccs code always in position1 - safety structure below.

string CCSaidCode(a2).

do if Any(AidCodeSP2,"9K","9M","9N","9R","9U","9V","9W").
compute   CCSAidCode  =  AidCodeSP2.
Else if Any(AidCodeSP1,"9K","9M","9N","9R","9U","9V","9W").
compute   CCSAidCode  =  AidCodeSP1.
Else if Any(AidCodeSP3,"9K","9M","9N","9R","9U","9V","9W").
compute  CCSAidCode  =  AidCodeSP3.
Else if Any(AidCode,"9K","9M","9N","9R","9U","9V","9W").
compute  CCSAidCode  =  AidCode.
end if.

string IHSSaidCode(a2).
do if Any(AidCodeSP2,"2L","2M","2N") .
compute   IHSSaidCode  =  AidCodeSP2.
Else if Any(AidCodeSP1,"2L","2M","2N").
compute   IHSSaidCode  =  AidCodeSP1.
Else if Any(AidCodeSP3,"2L","2M","2N").
compute  IHSSaidCode  =  AidCodeSP3.
Else if Any(AidCode,"2L","2M","2N").
compute  IHSSaidCode  =  AidCode.
end if.

sort cases by cin calendar.

agg outfile=* mode=AddVars 
/MedsMonth=Max(Calendar) .

recode eligibilityStatus eligibilityStatussp1  eligibilityStatussp2 eligibilityStatussp3("999"= " ").
recode RespCounty RespCountysp1  RespCountysp2 RespCountysp3("99"= " ").
recode Full FullSP1 fullSP2 fullSP3 Ffp FfpSP1 ffpSP2 ffpSP3(99=sysmis).

formats MEDSmonth(moyr6).

DEFINE !savefile (fn=!TOKENS(1))
save outFILE=
!quote(!concat('I:\MediCalData\meds_',!fn,'_ExplodeNoDupeAidCode.sav'))
/DROP EligStatusBogus SLOT  disabledX disabledSP1 disabledSP2 disabledSP3 fosterX fosterSp1 fostersp2 fosterSP3.

!enddefine.
!savefile fn=@ThisMonthsMedsFile.

saVE outFILE='I:\MedicalData\MedsExplodeCurrentNoDupeAidCode.sav'
 /DROP EligStatusBogus SLOT  disabledX disabledSP1 disabledSP2 disabledSP3 fosterX fosterSp1 fostersp2 fosterSP3.


 * get FILE='I:\MedicalData\MedsExplodeCurrentNoDupeAidCode.sav'.
 * disp vars.

 * get FILE='I:\MedicalData\MedsExplodeCurrent.sav'.

 * get file='I:\Temp\MedsCaseCodesStaging.sav'  .
 * save outfile='I:\Temp\MedsCaseCodesStagingJan11.sav'  .
 * select if cin ne " ".
 * rename vars maxMedsMonth = medsMonth.
 * formats  medsMonth(moyr6).


 * SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'MedsCaseCodes' /MAP/append.

 * disp vars.


GET DATA  /TYPE=ODBC
  /CONNECT='DSN=MHS_CGdecisionSupport;UID=;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=WINSPSSV1;Trusted_Connection=Yes'
  /SQL='SELECT  cin, calendar,SSI as SSIx, SOCmc as SOCmcX, retroMC as RetroMCx, Foster as FosterX , '+ 
' Disabled as DisabledX, mcRank as mcRankX, MedicareStatus as MedicareStatusX  ,ELIGIBILITY_COUNTY_code  as EligCountyX,  Primary_Aid_code as AidCodeX '+
' FROM MedsExplode  where Calendar >= {ts ''2013-07-01 00:00:00''}  ORDER BY cin, calendar, mcRank '
  /ASSUMEDSTRWIDTH=25.

*freq calendar where Calendar >= {ts ''2013-07-01 00:00:00''}.
compute inExplodeDB=1.
match files/file=* /by cin calendar/last=keep.
select if keep=1.
save outfile='I:\temp\MedsExplodeDB.sav' /drop keep.

 * FORMATS CALENDAR(MOYR6).

 * SELECT IF AIDcODEX NE " ".

 * RENAME VARS AIDcODEX = AIDcODE.
 * SORT CASES BY AIDcODE.
 * MATCH FILES/TABLE='i:\AIDcODES.SAV' /FILE=* /BY AIDcODE.


 * TEMP.
 * SELECT IF MISSING(FFP).
 * FREQ AIDCODE.
 
DEFINE @ThisMonthMEDStext() 
201504
!ENDDEFINE.

DEFINE @ThisMonthsMedsFile() 
Apr15
!ENDDEFINE.


*get FILE='I:\MedicalData\MedsExplodeCurrentNoDupeAidCode.sav' .

DEFINE !savefile (fn=!TOKENS(1))
get FILE=
!quote(!concat('I:\MediCalData\meds_',!fn,'_ExplodeNoDupeAidCode.sav'))
 /keep  CIN 
EligibilityStatus
calendar
CCSaidCode
ihssAidCode
SSI
Foster
Disabled
HCPstatus
HCPcode
primary_Aid_Code
ELIGIBILITY_COUNTY_code
mcRank
MedicareStatus
OHC
RetroMC
socMC.

!enddefine.
!savefile fn=@ThisMonthsMedsFile.


*get FILE='I:\MedicalData\MedsExplodeCurrentNoDupeAidCode.sav' .

select if primary_Aid_Code ne " " OR socMC=1  OR (medicareStatus ne " " And MedicareStatus ne "990") OR ccsAidCode ne " " OR disabled=1 OR ihssAidCode ne " ".
rename vars EligibilityStatus = SSIeligStatus.
if missing(SSI) ssiEligStatus=" ".

 * SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'MedsExplode' /MAP/REPLACE.

match files/table='I:\temp\MedsExplodeDB.sav' /file=* /by cin calendar.

*compute disabMediExempt=$sysmis.

temp.
select if missing(inExplodeDB).
save outfile='I:\temp\AppendExplode.sav' /drop SOCmcX retroMCx InExplodeDB ssiX fosterX disabledX mcrankX medicareStatusX eligCountyX AidCodeX.

select if inExplodeDB=1.
recode fosterX disabledX ssiX   (sysmis=0).
if foster=1 and FosterX =0 UpdateFoster=1.
if disabled=1 AND disabledX=0 UpdateDisabled=1.
if ssi=1 and ssiX=0 UpdateSSI=1.
if substr(medicareStatusX,1,1) = "9" AND number(substr(medicareStatus,1,1),f1) lt 9 updateMedicare=1.
if medicareStatusX =" " And medicareStatus ne " " updateMedicare=1.
if mCrank lt mcrankX  OR (missing(McrankX) and not missing(mcrank)) updateMC=1.
if missing(SOCmcX) AND SOCMC =1 updateSOC=1.
if RetroMC =1 AND missing(mcrankX) UpdateRetro=1.  

temp.
select if updateMC=1.
save outfile='I:\temp\UpdateMC.sav' /keep  cin calendar ELIGIBILITY_COUNTY_code  Primary_Aid_code mcrank mcrankX eligCountyX AidCodeX.


temp.
select if updateRetro=1.
save outfile='I:\temp\UpdateRetro.sav' /keep cin calendar RetroMC.


temp.
select if updateSOC=1.
save outfile='I:\temp\UpdateSOC.sav' /keep cin calendar SOCmc.


temp.
select if updateFoster=1.
save outfile='I:\temp\UpdateFoster.sav' /keep cin calendar Foster.

temp.
select if updateDisabled=1.
save outfile='I:\temp\UpdateDisabled.sav' /keep cin calendar Disabled.

temp.
select if updateSSI=1.
save outfile='I:\temp\UpdateSSI.sav' /keep cin calendar SSI ssiEligStatus.

temp.
select if updateMedicare=1.
save outfile='I:\temp\UpdateMedicare.sav' /keep cin calendar MedicareStatus MedicareStatusX.




 * get file='I:\temp\UpdateMedicare.sav'.
 * sort cases by medicareStatusX.
 * split file by MedicareStatusX.
 * freq medicareStatus.

get file='I:\temp\UpdateSSI.sav'.
freq  calendar.
SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'Staging' /MAP /REPLACE
 /SQL=' Update MedsExplode ' +
' SET SSI = stage.SSI , ssiEligStatus= stage.ssiEligStatus  ' +
' From Staging stage, MedsExplode   WHERE MedsExplode.cin = stage.cin AND medsExplode.calendar = stage.Calendar'.


get file='I:\temp\UpdateDisabled.sav'.
freq disabled.
SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'Staging' /MAP /REPLACE
 /SQL=' Update MedsExplode ' +
' SET  Disabled = stage.Disabled  ' +
' From Staging stage, MedsExplode   WHERE MedsExplode.cin = stage.cin AND medsExplode.calendar = stage.Calendar'.


get file='I:\temp\UpdateFoster.sav'.

SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'Staging' /MAP /REPLACE
 /SQL=' Update MedsExplode ' +
' SET  Foster = stage.Foster  ' +
' From Staging stage, MedsExplode   WHERE MedsExplode.cin = stage.cin AND medsExplode.calendar = stage.Calendar'.



get file='I:\temp\UpdateSOC.sav'.

SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'Staging' /MAP /REPLACE
 /SQL=' Update MedsExplode ' +
' SET  SOCmc = stage.SOCmc  ' +
' From Staging stage, MedsExplode   WHERE MedsExplode.cin = stage.cin AND medsExplode.calendar = stage.Calendar'.

get file='I:\temp\UpdateRetro.sav'.

SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'Staging' /MAP /REPLACE
 /SQL=' Update MedsExplode ' +
' SET  Retromc = stage.Retromc  ' +
' From Staging stage, MedsExplode   WHERE MedsExplode.cin = stage.cin AND medsExplode.calendar = stage.Calendar'.


get file='I:\temp\UpdateMC.sav'.
*freq aidCodeX primary_Aid_Code/format=Dfreq.

 * compute eligibility_month = xdate.month(Calendar).
 * compute eligibility_year = xdate.year(calendar).

SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'Staging' /MAP /REPLACE
 /SQL=' Update MedsExplode ' +
' SET primary_aid_code = stage.Primary_aid_Code, ELIGIBILITY_COUNTY_code = stage.ELIGIBILITY_COUNTY_code ' +
' From Staging stage, MedsExplode   WHERE MedsExplode.cin = stage.cin AND medsExplode.calendar = stage.Calendar'.

freq calendar.

get file='I:\temp\AppendExplode.sav'.
freq calendar.
SAVE TRANSLATE /TYPE=ODBC
  /CONNECT='DSN=MHS_CGDecisionSupport;UID=;Trusted_Connection=Yes;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=HP2UA3081880;'
 /table= 'MedsExplode' /MAP/append.

 * get file ='I:\medicalData\MedscurrentUncut.sav' .
 * disp vars.


 * GET DATA  /TYPE=ODBC
  /CONNECT='DSN=MHS_CGdecisionSupport;UID=;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=WINSPSSV1;Trusted_Connection=Yes'
  /SQL='SELECT CIN,calendar,primary_Aid_Code AS AidCode,  ELIGIBILITY_COUNTY_code  AS eligCounty, ' +
 'mcRank,SOCmc FROM MedsExplode where Calendar >= {ts ''2013-12-01 00:00:00''} AND Calendar < {ts ''2014-01-01 00:00:00''} ORDER BY cin, calendar '
  /ASSUMEDSTRWIDTH=25.

 * select if eligCounty = "01"  OR SOCmc=1 .

 * match files/table='I:\medicalData\MedscurrentUncut.sav' /rename calendar = bogus1 aidCode=bogus2 /file=* /by cin.

 * if eligCounty = "01" ACMC=1.

 * agg outfile=* mode=addVars over=yes
 /break=CIN 
   /HasACmc = max(ACMC)
 /minEligCounty = min(EligCounty) 
/maxEligCounty = max(eligCounty).

 * do if  MinEligCounty ne " " AND MaxEligCounty ne " ".
 * compute county = sum(number(minEligCounty,f2),number(maxEligCounty,f2)).
 * end if .

 * if county gt  2 AND SOCmc=1 AND missing(HASacMC)  DropMe=1.
 * if not any(eligCounty, " ", "01")  AND socMC=1 dropMe=1.
 * freq dropMe.
 * select if missing(DropMe).
 * freq rescounty.


*select if keep=1.
 * select if missing(drop).

 * if ACMC=1 AND SOCmc=1 SOCmc=$sysmis.

 * save outfile='I:\temp\MCwork.sav' .


*/drop keep dropMe  HasACmc minEligCounty MaxEligCounty county.

 * get file='I:\temp\MCwork.sav'.
 * if eligCounty="01" AND socMC=1 SOCmc=0.

 * select if ANY(xdate.year(Calendar),2008,2009).
 * sort cases by aidCode.
 * match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode .

 * agg outfile='I:\temp\CalMC1.sav'
   /break=Calendar
   /MCelig=sum(ACmc)
   /unmetSOCmc = sum(SOCmc).

 * get file='I:\temp\CalMC1.sav'.


 * get file='I:\temp\MCwork.sav'.
 * select if ANY(xdate.year(Calendar),2010,2011).
 * sort cases by aidCode.
 * match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode .

 * agg outfile='I:\temp\CalMC2.sav'
   /break=Calendar
   /MCelig=sum(ACmc)
   /Full = sum(full)
   /SOCmc = sum(SOCmc).


 * get file='I:\temp\MCwork.sav'.
 * select if ANY(xdate.year(Calendar),2012,2013).
 * sort cases by aidCode.
 * match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode .

 * agg outfile='I:\temp\CalMC3.sav'
   /break=Calendar
   /MCelig=sum(ACmc)
   /Full = sum(full)
   /SOCmc = sum(SOCmc).



 * get file='I:\temp\MCwork.sav'.
 * select if ANY(xdate.year(Calendar),2014).
 * sort cases by aidCode.
 * match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode .

 * agg outfile='I:\temp\CalMC4.sav'
   /break=Calendar
   /MCelig=sum(ACmc)
   /Full = sum(full)
   /SOCmc = sum(SOCmc).

 * add files
    /file='I:\temp\CalMC1.sav'
    /file='I:\temp\CalMC2.sav'
    /file='I:\temp\CalMC3.sav'
    /file='I:\temp\CalMC4.sav'.

 * sort cases by calendar.
 * split file by calendar.
 * freq MCelig Full SOCmc.



 * freq dropMe County HasACMc.


 * select if keep=1.
 * if eligCounty ="01" AND SOCmc=1 Both=1.
 * freq both.
 * compute drop = $sysmis.
 * freq drop.

 * rename vars Foster=FosterX 
sort cases by aidCode.
 * match files/table='I:\temp\AidCodesShort.sav' /file=* /by AidCode /drop 
CinCal1 MCelig  .


 * freq eligCounty Drop. 

*
*freq calendar.

 * temp.
 * select if OHC ne " ".
 * save outfile=  '//covenas/SPSSdata/MedicalData\MedsExplodeOHC.sav' /keep cin
calendar
OHC.

GET DATA  /TYPE=ODBC
  /CONNECT='DSN=MHS_CGdecisionSupport;UID=;APP=IBM SPSS Products: Statistics '+
    'Common;WSID=WINSPSSV1;Trusted_Connection=Yes'
  /SQL='SELECT * FROM MedsExplode  where Calendar >= {ts ''2012-01-01 00:00:00''} ORDER BY cin, calendar '
  /ASSUMEDSTRWIDTH=25.

rename vars primary_Aid_Code = AidCode ELIGIBILITY_COUNTY_code =eligCounty.
select if aidCode ne " " .
formats calendar(moyr6).
 * sort cases by cin calendar.
 * match files/file=* /by cin calendar/first=calCase1.
 * freq  calCase1.
 * select if calCase1=1.
save outfile=  '//covenas/decisionsupport/temp\MedsExplodeDB.sav' /keep cin
calendar
SSI
Foster
Disabled
EligCounty
AidCode
HCPstatus
HCPcode.

*get file=  '//covenas/decisionsupport/temp\MedsExplodeDB.sav' .
select if dateDiff($time, Calendar,"months") lt 37.
select if foster=1.
AGG OUTfile='I:\fostermc.sav'
   /BREAK=CIN
   /fOSTERmc = MAX(foster).

 * get file=  '//covenas/decisionsupport/temp\MedsExplodeDB.sav' .
*get file=  '//covenas/decisionsupport/temp\MedsExplodeDB.sav'.



 * get file='I:\temp\MedicalTable.sav' .
 * select if xdate.year(calendar) = 2014.
 * rename vars insystPrimAidCode= AidCode.
 * sort cases by aidCode.
 * match files/table='I:\aidCodes.sav' /file=* /by AidCode.
 * sort cases by FFP.
 * split file by FFP.
 * freq AidCode.


get file =  '//covenas/decisionsupport/temp\MedsExplodeDB.sav'
   /keep cin calendar SSI Foster Disabled EligCounty AidCode.

select if EligCounty ne " ".

compute counter=1.
aggregate outfile =  '//covenas/decisionsupport/temp\MaxMedsInDB.sav'
  /break=counter   
 /calendar = max(calendar).

sort cases by cin calendar.
match files /file=* /by cin /last=keep.
select if keep=1.

rename variables aidCode = LastAidCode.

aggregate outfile =  '//covenas/decisionsupport/temp\MedsExplodeDBWithMaxCalendar.sav'
   /break = cin LastAidCode
   /MaxMediCal = max(calendar).


