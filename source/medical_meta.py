"""This file contains the column_names and column_specifications for the Medi-Cal Tape along
with data dictionaries to tranlate numeric codes into English"""

import json

hcpcode_translation = {"300":"Alliance", "340":"Blue Cross", "051":"Center for Elders",
                       "056":"ONLOK Seniors", "000":"z No Plan", None:"z No Plan"}

language_translation = {'B': 'Chinese', 'P': 'Portugese', 'A': 'Other Sign', 'D': 'Cambodian', 
                        '2': 'Cantonese', 'N': 'Russian', None: 'Missing', '1': 'Spanish', 
                        '3': 'Japanese', 'G': 'Mien', '4': 'Korean', '5': 'Tagalog', 
                        'C': 'Other Chinese', 'V': 'Vietnamese', '0': 'American Sign', 
                        '7': 'English', 'S': 'Samoan', 'J': 'Hebrew', 'U': 'Farsi', 
                        'R': 'Arabic', 'Q': 'Italian', 'M': 'Polish', 'F': 'Llacano', 
                        '9': 'Missing', '8': 'Missing', 'I': 'Lao', 'H': 'Hmong', '6': 'Other', 
                        'T': 'Thai', 'K': 'French', 'E': 'Armenian'}

ethnicity_translation = {'A': 'Asian/PI', 'C': 'Asian/PI', '0': 'Unknown', 'H': 'Asian/PI', 
                         'K': 'Asian/PI', 'J': 'Asian/PI', 'M': 'Asian/PI', 'N': 'Asian/PI', 
                         'P': 'Asian/PI', 'R': 'Asian/PI', '4': 'Asian/PI', '7': 'Asian/PI', 
                         'V': 'Asian/PI', '9': 'Unknown', '8': 'Unknown', 'T': 'Asian/PI',
                         '1': 'Caucasian', '2': 'Latino', '3': 'Aftrican American',
                         '5': 'Native American', 'Z': 'Other'}

with open('city_names.json', 'r') as f:
    city_translation = json.load(f)

translation_dictionary = {"HCplanText":hcpcode_translation,
                          "language":language_translation,
                          "city":city_translation,
                          "ethnicity":ethnicity_translation}

column_names = ('ssn','HIC','V2', 'year', 'month','day','sex','race', 'lang', 'V4', 'CaseName', 'lname','fname','suffix', 'street', 'V12','city', 'state','zip','EWcode', 'CIN','GOVT', 'CountyCaseCode', 
    'CountyAidCode','CountyCaseID', 'v60','CMS','v601', 'eligYear', 'eligMonth','xAidCode','RespCounty', 'ResCounty','xEligibilityStatus','SOCamount','MedicareStatus', 'CarrierCode','FederalContractNumber',
    'PlanID', 'TypeID', 'v16','HCPstatus','HCPcode','OHC','v70','AidCodeSP1', 'RespCountySP1','EligibilityStatusSP1', 'AidCodeSP2', 'RespCountySP2','EligibilityStatusSP2', 'SOCpctSP', 'HFEligDaySP',
    'AidCodeSP3', 'RespCountySP3','EligibilityStatusSP3', 'V17','eligYear1','eligMonth1', 'xAidCode1', 'xRespCounty1','ResCounty1', 'xEligibilityStatus1', 'SOCamount1', 'MedicareStatus1','CarrierCode1', 
    'FederalContractNumber1', 'PlanID1','TypeID1','V20','HCPstatus1', 'HCPcode1', 'OHC1', 'V21','AidCodeSP11', 'RespCountySP11','EligibilityStatusSP11', 'AidCodeSP21', 'RespCountySP21',
    'EligibilityStatusSP21', 'SOCpctSP1', 'HFEligDaySP1','AidCodeSP31', 'RespCountySP31','EligibilityStatusSP31', 'v22','eligYear2','eligMonth2', 'xAidCode2', 'xRespCounty2','ResCounty2', 
    'xEligibilityStatus2', 'SOCamount2', 'MedicareStatus2','CarrierCode2', 'FederalContractNumber2', 'PlanID2','TypeID2','v25','HCPstatus2', 'HCPcode2', 'OHC2', 'v26','AidCodeSP12', 'RespCountySP12',
    'EligibilityStatusSP12', 'AidCodeSP22', 'RespCountySP22','EligibilityStatusSP22', 'SOCpctSP2', 'HFEligDaySP2','AidCodeSP32', 'RespCountySP32','EligibilityStatusSP32', 'v27','eligYear3',
    'eligMonth3', 'xAidCode3', 'xRespCounty3','ResCounty3', 'xEligibilityStatus3', 'SOCamount3', 'MedicareStatus3','CarrierCode3', 'FederalContractNumber3', 'PlanID3','TypeID3','V28','HCPstatus3', 'HCPcode3',
     'OHC3', 'v29','AidCodeSP13', 'RespCountySP13','EligibilityStatusSP13', 'AidCodeSP23', 'RespCountySP23','EligibilityStatusSP23', 'SOCpctSP3', 'HFEligDaySP3','AidCodeSP33', 'RespCountySP33',
     'EligibilityStatusSP33', 'V66','eligYear4','eligMonth4', 'xAidCode4', 'xRespCounty4','ResCounty4', 'xEligibilityStatus4', 'SOCamount4', 'MedicareStatus4','CarrierCode4', 'FederalContractNumber4', 
     'PlanID4','TypeID4','v30','HCPstatus4', 'HCPcode4', 'OHC4', 'v31','AidCodeSP14', 'RespCountySP14','EligibilityStatusSP14', 'AidCodeSP24', 'RespCountySP24','EligibilityStatusSP24', 'SOCpctSP4', 
     'HFEligDaySP4','AidCodeSP34', 'RespCountySP34','EligibilityStatusSP34', 'v55','eligYear5','eligMonth5', 'xAidCode5', 'xRespCounty5','ResCounty5', 'xEligibilityStatus5', 'SOCamount5', 
     'MedicareStatus5','CarrierCode5', 'FederalContractNumber5', 'PlanID5','TypeID5','v32','HCPstatus5', 'HCPcode5', 'OHC5', 'v33','AidCodeSP15', 'RespCountySP15','EligibilityStatusSP15', 
     'AidCodeSP25', 'RespCountySP25','EligibilityStatusSP25', 'SOCpctSP5', 'HFEligDaySP5','AidCodeSP35', 'RespCountySP35','EligibilityStatusSP35', 'v56','eligYear6','eligMonth6', 'xAidCode6', 
     'xRespCounty6','ResCounty6', 'xEligibilityStatus6', 'SOCamount6', 'MedicareStatus6','CarrierCode6', 'FederalContractNumber6', 'PlanID6','TypeID6','v34','HCPstatus6', 'HCPcode6', 'OHC6', 'v35',
     'AidCodeSP16', 'RespCountySP16','EligibilityStatusSP16', 'AidCodeSP26', 'RespCountySP26','EligibilityStatusSP26', 'SOCpctSP6', 'HFEligDaySP6','AidCodeSP36', 'RespCountySP36',
     'EligibilityStatusSP36', 'v68','eligYear7','eligMonth7', 'xAidCode7', 'xRespCounty7','ResCounty7', 'xEligibilityStatus7', 'SOCamount7', 'MedicareStatus7','CarrierCode7', 'FederalContractNumber7', 
     'PlanID7','TypeID7','v36','HCPstatus7', 'HCPcode7', 'OHC7', 'v37','AidCodeSP17', 'RespCountySP17','EligibilityStatusSP17', 'AidCodeSP27', 'RespCountySP27','EligibilityStatusSP27', 'SOCpctSP7', 
     'HFEligDaySP7','AidCodeSP37', 'RespCountySP37','EligibilityStatusSP37', 'v58','eligYear8','eligMonth8', 'xAidCode8', 'xRespCounty8','ResCounty8', 'xEligibilityStatus8', 'SOCamount8', 
     'MedicareStatus8','CarrierCode8', 'FederalContractNumber8', 'PlanID8','TypeID8','v38','HCPstatus8', 'HCPcode8', 'OHC8', 'v39','AidCodeSP18', 'RespCountySP18','EligibilityStatusSP18', 
     'AidCodeSP28', 'RespCountySP28','EligibilityStatusSP28', 'SOCpctSP8', 'HFEligDaySP8','AidCodeSP38', 'RespCountySP38','EligibilityStatusSP38', 'v59','eligYear9','eligMonth9', 'xAidCode9', 
     'xRespCounty9','ResCounty9', 'xEligibilityStatus9', 'SOCamount9', 'MedicareStatus9','CarrierCode9', 'FederalContractNumber9', 'PlanID9','TypeID9','v40','HCPstatus9', 'HCPcode9', 'OHC9', 'v41',
     'AidCodeSP19', 'RespCountySP19','EligibilityStatusSP19', 'AidCodeSP29', 'RespCountySP29','EligibilityStatusSP29', 'SOCpctSP9', 'HFEligDaySP9','AidCodeSP39', 'RespCountySP39',
     'EligibilityStatusSP39', 'v61','eligYear10', 'eligMonth10','xAidCode10','xRespCounty10', 'ResCounty10','xEligibilityStatus10','SOCamount10','MedicareStatus10', 'CarrierCode10','FederalContractNumber10',
     'PlanID10', 'TypeID10', 'v42','HCPstatus10','HCPcode10','OHC10','v43','AidCodeSP110','RespCountySP110', 'EligibilityStatusSP110','AidCodeSP210','RespCountySP210', 'EligibilityStatusSP210',
     'SOCpctSP10','HFEligDaySP10', 'AidCodeSP310','RespCountySP310', 'EligibilityStatusSP310','v61a', 'eligYear11', 'eligMonth11','xAidCode11','xRespCounty11', 'ResCounty11','xEligibilityStatus11',
     'SOCamount11','MedicareStatus11', 'CarrierCode11','FederalContractNumber11','PlanID11', 'TypeID11', 'v44','HCPstatus11','HCPcode11','OHC11','v45','AidCodeSP111','RespCountySP111', 
     'EligibilityStatusSP111','AidCodeSP211','RespCountySP211', 'EligibilityStatusSP211','SOCpctSP11','HFEligDaySP11', 'AidCodeSP311','RespCountySP311', 'EligibilityStatusSP311','v69',
     'eligYear12', 'eligMonth12','xAidCode12','xRespCounty12', 'ResCounty12','xEligibilityStatus12','SOCamount12','MedicareStatus12', 'CarrierCode12','FederalContractNumber12','PlanID12', 'TypeID12', 
     'v46','HCPstatus12','HCPcode12','OHC12','v47','AidCodeSP112','RespCountySP112', 'EligibilityStatusSP112','AidCodeSP212','RespCountySP212', 'EligibilityStatusSP212','SOCpctSP12',
     'HFEligDaySP12', 'AidCodeSP312','RespCountySP312', 'EligibilityStatusSP312','v62','eligYear13', 'eligMonth13','xAidCode13','xRespCounty13', 'ResCounty13','xEligibilityStatus13','SOCamount13',
     'MedicareStatus13', 'CarrierCode13','FederalContractNumber13','PlanID13', 'TypeID13', 'v48','HCPstatus13','HCPcode13','OHC13','v49','AidCodeSP113','RespCountySP113', 'EligibilityStatusSP113',
     'AidCodeSP213','RespCountySP213', 'EligibilityStatusSP213','SOCpctSP13','HFEligDaySP13', 'AidCodeSP313','RespCountySP313', 'EligibilityStatusSP313','v63','eligYear14', 'eligMonth14',
     'xAidCode14','xRespCounty14', 'ResCounty14','xEligibilityStatus14','SOCamount14','MedicareStatus14', 'CarrierCode14','FederalContractNumber14','PlanID14', 'TypeID14', 'v50','HCPstatus14','HCPcode14',
     'OHC14','v51','AidCodeSP114','RespCountySP114', 'EligibilityStatusSP114','AidCodeSP214','RespCountySP214', 'EligibilityStatusSP214','SOCpctSP14','HFEligDaySP14', 'AidCodeSP314',
     'RespCountySP314', 'EligibilityStatusSP314','v64','eligYear15', 'eligMonth15','xAidCode15','xRespCounty15', 'ResCounty15','xEligibilityStatus15','SOCamount15','MedicareStatus15', 'CarrierCode15',
     'FederalContractNumber15','PlanID15', 'TypeID15', 'v52','HCPstatus15','HCPcode15','OHC15','v53','AidCodeSP115','RespCountySP115', 'EligibilityStatusSP115','AidCodeSP215','RespCountySP215', 
     'EligibilityStatusSP215','SOCpctSP15','HFEligDaySP15', 'AidCodeSP315','RespCountySP315', 'EligibilityStatusSP315','v65')

column_specifications = [(0,9),(9,19), (19,21),(21,25),(25,27),(27,29),(29,30),(30,31),(31,32),(32,33),(33,51),(51,71),(71,86),(86,128), (128,160),(160,178),(178,198),(198,200),(200,205),(205,209),(209,218),(218,219),(219,221),(221,223),(223,230),(230,234),(234,235),(235,243),(243,247),(247,249),(249,251),(251,253),(253,255),(255,258),(258,263),(263,266),(266,270),(270,275),(275,278),(278,280),(280,290),(290,292),(292,295),(295,296),(296,299),(299,301),(301,303),(303,306),(306,308),(308,310),(310,313),(313,315),(315,319),(319,321),(321,323),(323,326),(326,336),(336,340),(340,342),(342,344),(344,346),(346,348),(348,351),(351,356),(356,359),(359,363),(363,368),(368,371),(371,373),(373,383),(383,385),(385,388),(388,389),(389,392),(392,394),(394,396),(396,399),(399,401),(401,403),(403,406),(406,408),(408,412),(412,414),(414,416),(416,419),(419,429),(429,433),(433,435),(435,437),(437,439),(439,441),(441,444),(444,449),(449,452),(452,456),(456,461),(461,464),(464,466),(466,476),(476,478),(478,481),(481,482),(482,485),(485,487),(487,489),(489,492),(492,494),(494,496),(496,499),(499,501),(501,505),(505,507),(507,509),(509,512),(512,522),(522,526),(526,528),(528,530),(530,532),(532,534),(534,537),(537,542),(542,545),(545,549),(549,554),(554,557),(557,559),(559,569),(569,571),(571,574),(574,575),(575,578),(578,580),(580,582),(582,585),(585,587),(587,589),(589,592),(592,594),(594,598),(598,600),(600,602),(602,605),(605,615),(615,619),(619,621),(621,623),(623,625),(625,627),(627,630),(630,635),(635,638),(638,642),(642,647),(647,650),(651,652),(652,662),(662,664),(664,667),(667,668),(668,671),(671,673),(673,675),(675,678),(678,680),(680,682),(682,685),(685,687),(687,691),(691,693),(693,695),(695,698),(698,708),(708,712),(712,714),(714,716),(716,718),(718,720),(720,723),(723,728),(728,731),(731,735),(735,740),(740,743),(743,745),(745,755),(755,757),(757,760),(760,761),(761,764),(764,766),(766,768),(768,771),(771,773),(773,775),(775,778),(778,780),(780,784),(784,786),(786,788),(788,791),(791,801),(801,805),(805,807),(807,809),(809,811),(811,813),(813,816),(816,821),(821,824),(824,828),(828,833),(833,836),(836,838),(838,848),(848,850),(850,853),(853,854),(854,857),(857,859),(859,861),(861,864),(864,866),(866,868),(868,871),(871,873),(873,877),(877,879),(879,881),(881,884),(884,894),(894,898),(898,900),(900,902),(902,904),(904,906),(906,909),(909,914),(914,917),(917,921),(921,926),(926,929),(929,931),(931,941),(941,943),(943,946),(946,947),(947,950),(950,952),(952,954),(954,957),(957,959),(959,961),(961,964),(964,966),(966,970),(970,972),(972,974),(974,977),(977,987),(987,991),(991,993),(993,995),(995,997),(997,999),(999,1002), (1002,1007),(1007,1010),(1010,1014),(1014,1019),(1019,1022),(1022,1024),(1024,1034),(1034,1036),(1036,1039),(1039,1040),(1040,1043),(1043,1045),(1045,1047),(1047,1050),(1050,1052),(1052,1054),(1054,1057),(1057,1059),(1059,1063),(1063,1065),(1065,1067),(1067,1070),(1070,1080),(1080,1084),(1084,1086),(1086,1088),(1088,1090),(1090,1092),(1092,1095),(1095,1100),(1100,1103),(1103,1107),(1107,1112),(1112,1115),(1115,1117),(1117,1127),(1127,1129),(1129,1132),(1132,1133),(1133,1136),(1136,1138),(1138,1140),(1140,1143),(1143,1145),(1145,1147),(1147,1150),(1150,1152),(1152,1156),(1156,1158),(1158,1160),(1160,1163),(1163,1173),(1173,1177),(1177,1179),(1179,1181),(1181,1183),(1183,1185),(1185,1188),(1188,1193),(1193,1196),(1196,1200),(1200,1205),(1205,1208),(1208,1210),(1210,1220),(1220,1222),(1222,1225),(1225,1226),(1226,1229),(1229,1231),(1231,1233),(1233,1236),(1236,1238),(1238,1240),(1240,1243),(1243,1245),(1245,1249),(1249,1251),(1251,1253),(1253,1256),(1256,1266),(1266,1270),(1270,1272),(1272,1274),(1274,1276),(1276,1278),(1278,1281),(1281,1286),(1286,1289),(1289,1293),(1293,1298),(1298,1301),(1301,1303),(1303,1313),(1313,1315),(1315,1318),(1318,1319),(1319,1322),(1322,1324),(1324,1326),(1326,1329),(1329,1331),(1331,1333),(1333,1336),(1336,1338),(1338,1342),(1342,1344),(1344,1346),(1346,1349),(1349,1359),(1359,1363),(1363,1365),(1365,1367),(1367,1369),(1369,1371),(1371,1374),(1374,1379),(1379,1382),(1382,1386),(1386,1391),(1391,1394),(1394,1396),(1396,1406),(1406,1408),(1408,1411),(1411,1412),(1412,1415),(1415,1417),(1417,1419),(1419,1422),(1422,1424),(1424,1426),(1426,1429),(1429,1431),(1431,1435),(1435,1437),(1437,1439),(1439,1442),(1442,1452),(1452,1456),(1456,1458),(1458,1460),(1460,1462),(1462,1464),(1464,1467),(1467,1472),(1472,1475),(1475,1479),(1479,1484),(1484,1487),(1487,1489),(1489,1499),(1499,1501),(1501,1504),(1504,1505),(1505,1508),(1508,1510),(1510,1512),(1512,1515),(1515,1517),(1517,1519),(1519,1522),(1522,1524),(1524,1528),(1528,1530),(1530,1532),(1532,1535),(1535,1545),(1545,1549),(1549,1551),(1551,1553),(1553,1555),(1555,1557),(1557,1560),(1560,1565),(1565,1568),(1568,1572),(1572,1577),(1577,1580),(1580,1582),(1582,1592),(1592,1594),(1594,1597),(1597,1598),(1598,1601),(1601,1603),(1603,1605),(1605,1608),(1608,1610),(1610,1612),(1612,1615),(1615,1617),(1617,1621),(1621,1623),(1623,1625),(1625,1628),(1628,1638),(1638,1642),(1642,1644),(1644,1646),(1646,1648),(1648,1650),(1650,1653),(1653,1658),(1658,1661),(1661,1665),(1665,1670),(1670,1673),(1673,1675),(1675,1685),(1685,1687),(1687,1690),(1690,1691),(1691,1694),(1694,1696),(1696,1698),(1698,1701),(1701,1703),(1703,1705),(1705,1708),(1708,1710),(1710,1714),(1714,1716),(1716,1718),(1718,1721),(1721,1779)]

column_lengths = {}
for tuple_ in zip(column_names, column_specifications):
    column_length = tuple_[1][1] - tuple_[1][0]
    column_lengths[tuple_[0]] = column_length

translation_lengths = {}
for key in translation_dictionary:
    max_value_length = 0
    for value in translation_dictionary[key].values():
        if len(value) > max_value_length:
            max_value_length = len(value)
    translation_lengths[key] = max_value_length

column_converters = {}
for name in column_names:
    column_converters[name]=str
