import os
from datetime import datetime
import numpy as np
import pandas as pd
from medical_columns import *
#from sqlalchemy import create_engine
#import psycopg2

MedsFolder='/media/decisionsupport/meinzer/pullmedstest/'
medical_tape = '/Users/irisweiss/greg/achs/testmedsx.txt'
csstext_file = '/media/decisionsupport/meinzer/Production/Medical spss files/CCStext.csv'
aidcodes_file = '/media/decisionsupport/meinzer/Production/Medical spss files/AidCodesShort.csv'

#Some pull from demographics table to see who is in it here.
#Save file of who is already in demographics database (file 1)

#import pdb
#pdb.set_trace()

#Read the fixed width medical_tape file into a pandas dataframe object.
df = pd.read_fwf(medical_tape, 
                 colspecs = column_specifications,
                 header = None, 
                 names = column_names, 
                 parse_dates = {'bday':['year','month','day'],'calendar':['eligYear',"eligMonth"]},
                 keep_date_col = True,
                 converters = {'HCPcode':str, 'HCPstatus':str, 'ssn':str})

#This creates a column named "id" that contains a unique integer for each row.
df["id"] = df.index

#Rename several of the dataframes columns inplace to remove some extraneous exes.
#Note this only renames the xAidCode etc. for the first month. The rest of the months still have
#xAidCode1 to #xAidCode15. This was originally done after the wide to long to get all months?
df.rename(columns={'xAidCode':'AidCode','xRespCounty':'RespCounty', 
                   'xEligibilityStatus':'EligibilityStatus'}, inplace=True)

#If there are duplicate CINs in the data at this point, which there shouldn't be because the 
#data is still wide at this point, keep the row with the best EligibilityStatus for the current
#month. This is only looking at EligibilityStatus, not EligibilityStatusSP1 SP2 or SP3.
df.sort(inplace=True)
df.drop_duplicates(subset='CIN', inplace=True)
df.dropna(subset=['CIN'], inplace=True)

#HCP = Health Care Plan
#Populate a HCPlanText Column based on the HCP Code column.
df['HCplanText']=df['HCPcode']
df['language']=df['lang']

df.replace(to_replace=translation_dictionary, inplace=True)

df.ix[df.HCPstatus.isin(["00","10","09","19","40","49","S0","S9"]),'HCplanText']="z No Plan"


#Ethnicity, Language, City replacements go here before we do wide to long.

#uncut month and uncut current file are saved here. (files 2,3)

#Reshape the data.  It is still wide here though with respect to multiple aidcodes etc.
#Its being elongated by months.
df=pd.wide_to_long(df,[ 'eligYear', 'eligMonth','xAidCode','xRespCounty', 'ResCounty',
                        'xEligibilityStatus','SOCamount','MedicareStatus', 'CarrierCode',
                        'FederalContractNumber', 'PlanID', 'TypeID', 'v16','HCPstatus','HCPcode',
                        'OHC','v70','AidCodeSP1', 'RespCountySP1','EligibilityStatusSP1', 
                        'AidCodeSP2', 'RespCountySP2','EligibilityStatusSP2', 'SOCpctSP', 
                        'HFEligDaySP','AidCodeSP3', 'RespCountySP3','EligibilityStatusSP3'],
                   i='id',j='varstocases')

#The index gets rearranged with the wide_to_long, reset it.
df=df.reset_index()

#Wide to long by aidcode.  Sort by j-index.
#If aidcodeN contains ("9K","9M","9N","9R","9U") select that row.

#Why are we multiplying eligYear by 10000 and eligMonth by 100?
#The format='%Y%m%d' takes an eight digit long number and turns it into a datetime object.
#We need to create that eight digit number, so to move the year left by four digits, * by 10000.
df['calendar'] = pd.to_datetime(df['eligYear']*10000 + df['eligMonth']*100 + 1, format='%Y%m%d')

#For each instance of eligibilityStatus create a series of the first digit of elgigbilityStatus.
w = df.EligibilityStatusSP3.dropna().astype(str).str[0].astype(int)
v = df.EligibilityStatusSP2.dropna().astype(str).str[0].astype(int)
u = df.EligibilityStatusSP1.dropna().astype(str).str[0].astype(int)
t = df.EligibilityStatus.dropna().astype(str).str[0].astype(int) 

#If any of the above first digits are less than five, 'MCelig' is set to 1.
df['MCelig'] = ((t < 5)|(u < 5)|(v < 5)|(w < 5)).astype(int)
#If that column is empty, make it have a zero.
df.MCelig = df.MCelig.fillna(0)
df=df.reset_index()

#Create a dataframe x with one instance of a given (CIN, calendar) and the highest MCelig.
x=df.sort(['CIN','calendar',"MCelig"]).groupby(["CIN",'calendar'], as_index=False).last()
x["xid"] = x.index

#Make data shape even longer. AidCode, RespCounty and EligibilityStatus are now their own rows.
y=pd.wide_to_long(x,[ 'AidCode','RespCounty','EligibilityStatus'],i='xid',j='xvarstocases')
y=y.reset_index()

"""
ccstext = pd.read_csv(csstext_file,header=0)
aidcodesshort= pd.read_csv(aidcodes_file,header=0)

#Bring in text form of aid codes.
g=pd.merge(y, ccstext, how='left',left_on='AidCode',right_on='AidCode')
g=pd.merge(g, aidcodesshort, how='left',left_on='AidCode',right_on='aidcode')

#I think this line is broken...Not sure what its trying to do.
g.ix[g.AidCode.isin(["10","20","60"]) & (g.MCelig ==1),'SSI']=1

#get a series of the first digits of non-nan numbers
t = g.EligibilityStatus.dropna().astype(str).str[0].astype(int) 

#The followin two lines of code make columns that combine eligibility status and disabled or
#foster status.
#If first digit of g.EligibilityStatus is less than five and g.Foster==1, then Fosterx is set True.
g['Fosterx'] = ((t < 5).astype(int)) & (g.Foster==1)
#If first digit of g.EligibilityStatus is less than 5 and g.Disabled==1, then Disabledx is set True.
g['Disabledx'] = ((t < 5).astype(int)) & (g.Disabled==1)

#What is going on here?
p=g[['CIN','calendar','Fosterx','Disabledx']]
g.drop(['Fosterx','Disabledx'], axis=1,inplace=True)
g.merge(p,how='left',on=['CIN','calendar'])

#start module

#Fill empty colums
g['EligibilityStatus']=g['EligibilityStatus'].fillna(999)
g['RespCounty']=g['RespCounty'].fillna(99)
g['Full']=g['Full'].fillna(99)
g['FFP']=g['FFP'].fillna(99)

#This line does nothing.
((g.EligibilityStatus.dropna().astype(str).str[0].astype(int) < 5).astype(int)) & (g.RespCounty==1) & (g.Full==1) & (g.FFP==100)

g.ix[1,'EligibilityStatus']=2
g.ix[1,'RespCounty']=1
g.ix[1,'Full']=1
g.ix[1,'FFP']=100

g[['EligibilityStatus','RespCounty','Full','FFP']].head()

g['eligibility_month']=None
g['eligibility_year']=None
g['slot']=None
g['primary_Aid_code']=None
g['mcRank']=None
g['ELIGIBILITY_COUNTY_code']=None


def f(row):
    if (row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1 and (row.Full==1) and (row.FFP==100)):
        row[['eligibility_year', 'eligibility_month','primary_Aid_code','mcRank','ELIGIBILITY_COUNTY_code']] = row['eligYear'],row['eligMonth'],row['aidcode'],1,row['RespCounty']
#fix this at some point!
return row


    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1 & (row.Full==1) & (row.FFP==65):
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1 & (row.Full==1) & (row.FFP==50):
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 & (row.Full==1) & (row.FFP==100):
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 & (row.Full==1) & (row.FFP==65):
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5  & (row.Full==1) & (row.FFP==50):
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1  & (row.FFP==100):

do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01" AND FFP=100 .
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1 & (row.FFP==65):
do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01"  AND FFP=65.
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1 & (row.FFP==50):
do if Number(substr(EligibilityStatus,1,1),f1) lt 5  AND RespCounty = "01" AND FFP=50 .
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1 & (row.FFP==100):
do if Number(substr(EligibilityStatus,1,1),f1) lt 5   AND FFP=100.
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5  & (row.FFP==65):
do if Number(substr(EligibilityStatus,1,1),f1) lt 5   AND FFP=65.
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 & (row.FFP==50):
do if  Number(substr(EligibilityStatus,1,1),f1) lt 5   AND FFP=50.
    if row['EligibilityStatus'] is not None and int(str(row['EligibilityStatus'])[0]) < 5 and row['RespCounty']==1 & (row.Full==1) & (~row.FFP==0):
do if Number(substr(EligibilityStatus,1,1),f1) lt 5 AND AidCode ne " " AND  FFP ne 0  .


g=g.apply(f,axis=1)
g.loc[((g.EligibilityStatus.dropna().astype(str).str[0].astype(int) < 5)) & (g.RespCounty==1) & (g.Full==1) & (g.FFP==100),['eligibility_month',
'primary_Aid_code','slot','mcRank','ELIGIBILITY_COUNTY_code']]=g['eligYear'],1,1,1,1,1

g.sort(['CIN','calendar']).to_csv('dupes')

df['HCplanText']=df['HCPcode'].replace("300","Alliance")
df['HCplanText']=df['HCplanText'].replace("340","Blue Cross")
df['HCplanText']=df['HCplanText'].replace("051","Center for Elders")
df['HCplanText']=df['HCplanText'].replace("056","ONLOK Seniors")
df['HCplanText']=df['HCplanText'].replace("000","z No Plan")
#different in each code whether other or z
df['HCplanText']=df['HCplanText'].replace(np.nan,"z No Plan")

df.ix[df.HCPstatus.isin(["00","10","09","19","40","49","S0","S9"]),'HCplanText']="z No Plan"
df.ix[df.race.isin(["4","7","A","C","H","J","K","M","N","P","R","T","V"]),'ethnicity']="Asian/PI"
df.ix[df.race.isin(["8","9",np.nan,"0"]),'ethnicity']="Unknown"

df['ethnicity']=df['ethnicity'].replace("1","Caucasian")
df['ethnicity']=df['ethnicity'].replace("2","Latino")
df['ethnicity']=df['ethnicity'].replace("3","African American")
df['ethnicity']=df['ethnicity'].replace("5","Native American")
df['ethnicity']=df['ethnicity'].replace("Z","Other")

df['language']=df['lang'].replace("0","American Sign")
df['lang']=df['lang'].replace("1","Spanish")
df['lang']=df['lang'].replace("2","Cantonese")
df['lang']=df['lang'].replace("3","Japanese")
df['lang']=df['lang'].replace("4","Korean")
df['lang']=df['lang'].replace("5","Tagalog")
df['lang']=df['lang'].replace("6","Other")
df['lang']=df['lang'].replace("7","English")
df['lang']=df['lang'].replace("8","Missing")
df['lang']=df['lang'].replace("9","Missing")
df['lang']=df['lang'].replace("A","Other Sign")
df['lang']=df['lang'].replace("B","Chinese")
df['lang']=df['lang'].replace("C","Other Chinese")
df['lang']=df['lang'].replace("D","Cambodian")
df['lang']=df['lang'].replace("E","Armenian")
df['lang']=df['lang'].replace("F","Llacano")
df['lang']=df['lang'].replace("G","Mien")
df['lang']=df['lang'].replace("H","Hmong")
df['lang']=df['lang'].replace("I","Lao")
df['lang']=df['lang'].replace("J","Hebrew")
df['lang']=df['lang'].replace("K","French")
df['lang']=df['lang'].replace("M","Polish")
df['lang']=df['lang'].replace("N","Russian")
df['lang']=df['lang'].replace("P","Portugese")
df['lang']=df['lang'].replace("Q","Italian")
df['lang']=df['lang'].replace("R","Arabic")
df['lang']=df['lang'].replace("S","Samoan")
df['lang']=df['lang'].replace("T","Thai")
df['lang']=df['lang'].replace("U","Farsi")
df['lang']=df['lang'].replace("V","Vietnamese")
df['lang']=df['lang'].replace(np.nan,"Missing")    

df.city=df.city.str.upper()
df.city=df['city'].map(lambda x: x.lstrip(' '))
df['city']=df['city'].replace('MEWARK','NEWARK')
df['city']=df['city'].replace('ERKELEY','BERKELEY')
df['city']=df['city'].replace('NEWARKCITY','NEWARK')
df['city']=df['city'].replace(' NEWARK','NEWARK')
df['city']=df['city'].replace('NEWARIK','NEWARK')
df['city']=df['city'].replace('NEWARKD','NEWARK')
df['city']=df['city'].replace('NEWARKS','NEWARK')
df['city']=df['city'].replace('NEWARKT','NEWARK')
df['city']=df['city'].replace('NEWMARK','NEWARK')
df['city']=df['city'].replace(' NEWWARK','NEWARK')
df['city']=df['city'].replace(' NEWARDK','NEWARK')
df['city']=df['city'].replace('NEWARDK','NEWARK')
df['city']=df['city'].replace('NEWWARK','NEWARK')
df['city']=df['city'].replace(' NEWORK','NEWARK')
df['city']=df['city'].replace('NEWORK','NEWARK')
df['city']=df['city'].replace('CASTRE VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace(' CASTRO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('ALAMADA','ALAMEDA')
df['city']=df['city'].replace('ALAMAEDA','ALAMEDA')
df['city']=df['city'].replace('ALAMDED','ALAMEDA')
df['city']=df['city'].replace('ALAMRDA','ALAMEDA')
df['city']=df['city'].replace('ALEMADA','ALAMEDA')
df['city']=df['city'].replace('ALANDMED','ALAMEDA')
df['city']=df['city'].replace('ALAMEDA CA','ALAMEDA')
df['city']=df['city'].replace('ALABANY','ALBANY')
df['city']=df['city'].replace('ALPANY','ALBANY')
df['city']=df['city'].replace('ALBAY','ALBANY')
df['city']=df['city'].replace('BAERKELEY','BERKELEY')
df['city']=df['city'].replace('BERELEY','BERKELEY')
df['city']=df['city'].replace('BARKELEY','BERKELEY')
df['city']=df['city'].replace('BRKELEY','BERKELEY')
df['city']=df['city'].replace('BVERKELEY','BERKELEY')
df['city']=df['city'].replace('ERKELEY','BERKELEY')
df['city']=df['city'].replace('CA94706','BERKELEY')
df['city']=df['city'].replace('94704','BERKELEY')
df['city']=df['city'].replace('CASTRO VALLEY,','CASTRO VALLEY')
df['city']=df['city'].replace('DYBLIN','DUBLIN')
df['city']=df['city'].replace('DBLN','DUBLIN')
df['city']=df['city'].replace('EMERVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMERY VILLE','EMERYVILLE')
df['city']=df['city'].replace('EMERYVELLIE','EMERYVILLE')
df['city']=df['city'].replace('EMERIVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMORYVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMMERYVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMERYWILLE','EMERYVILLE')
df['city']=df['city'].replace('EMIRYVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMMEYVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMRYVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMEMERY','EMERYVILLE')
df['city']=df['city'].replace('EMERBILLE','EMERYVILLE')
df['city']=df['city'].replace('EMMERYVILE','EMERYVILLE')
df['city']=df['city'].replace('EMORYVILLE','EMERYVILLE')
df['city']=df['city'].replace('94608','EMERYVILLE')
df['city']=df['city'].replace('EMERWILLE','EMERYVILLE')
df['city']=df['city'].replace('EMERVYLLE','EMERYVILLE')
df['city']=df['city'].replace('EMEYVILLE','EMERYVILLE')
df['city']=df['city'].replace('SMERYVILLE','EMERYVILLE')
df['city']=df['city'].replace('EMERVILL                ','EMERYVILLE')
df['city']=df['city'].replace('FREMPNT','FREMONT')
df['city']=df['city'].replace('FEMONT','FREMONT')
df['city']=df['city'].replace('FREMOT','FREMONT')
df['city']=df['city'].replace('FREMNT','FREMONT')
df['city']=df['city'].replace('FREMMONT','FREMONT')
df['city']=df['city'].replace('FRENMONT','FREMONT')
df['city']=df['city'].replace('FRENONT','FREMONT')
df['city']=df['city'].replace('FRIMONT','FREMONT')
df['city']=df['city'].replace('FREAMONT','FREMONT')
df['city']=df['city'].replace('FREMON','FREMONT')
df['city']=df['city'].replace('HAYARD','HAYWARD')
df['city']=df['city'].replace('HARYWARD','HAYWARD')
df['city']=df['city'].replace('HWYWARD','HAYWARD')
df['city']=df['city'].replace('LIVEERMORE','LIVERMORE')
df['city']=df['city'].replace('LIVERSOME','LIVERMORE')
df['city']=df['city'].replace('LIV ERMORE','LIVERMORE')
df['city']=df['city'].replace('LIVORMORE','LIVERMORE')
df['city']=df['city'].replace('LLIVERMORE','LIVERMORE')
df['city']=df['city'].replace('LIVBERMORE','LIVERMORE')
df['city']=df['city'].replace('IVERMORE','LIVERMORE')
df['city']=df['city'].replace('LVMR','LIVERMORE')
df['city']=df['city'].replace('LIVEROMORE','LIVERMORE')
df['city']=df['city'].replace('NEWEARK','NEWARK')
df['city']=df['city'].replace('NEWAR','NEWARK')
df['city']=df['city'].replace('NEWARKK','NEWARK')
df['city']=df['city'].replace('NEWAWRK','NEWARK')
df['city']=df['city'].replace('NEWRAK','NEWARK')
df['city']=df['city'].replace('NEWARKN','NEWARK')
df['city']=df['city'].replace('NEARK','NEWARK')
df['city']=df['city'].replace('NAWARK','NEWARK')
df['city']=df['city'].replace('OAKDLAND','OAKLAND')
df['city']=df['city'].replace('AOKLAND','OAKLAND')
df['city']=df['city'].replace('`OAKLAND','OAKLAND')
df['city']=df['city'].replace('OADLAND','OAKLAND')
df['city']=df['city'].replace('OPAKLAND','OAKLAND')
df['city']=df['city'].replace('\D3KALAND','OAKLAND')
df['city']=df['city'].replace('JOAKLAND','OAKLAND')
df['city']=df['city'].replace('OFAKLAND','OAKLAND')
df['city']=df['city'].replace('`OAKLAND','OAKLAND')
df['city']=df['city'].replace('OAKLDN','OAKLAND')
df['city']=df['city'].replace('RAKLAND','OAKLAND')
df['city']=df['city'].replace('AKALND','OAKLAND')
df['city']=df['city'].replace('OAKALND','OAKLAND')
df['city']=df['city'].replace('OAKLAMD','OAKLAND')
df['city']=df['city'].replace('OAKLAND CA','OAKLAND')
df['city']=df['city'].replace('OALAND','OAKLAND')
df['city']=df['city'].replace('94603','OAKLAND')
df['city']=df['city'].replace('EAST OAKLAND','OAKLAND')
df['city']=df['city'].replace('OQKLQND','OAKLAND')
df['city']=df['city'].replace('OSKLSNF','OAKLAND')
df['city']=df['city'].replace('OAK','OAKLAND')
df['city']=df['city'].replace('94602','OAKLAND')
df['city']=df['city'].replace('94605','OAKLAND')
df['city']=df['city'].replace('94609','OAKLAND')
df['city']=df['city'].replace('94612','OAKLAND')
df['city']=df['city'].replace('94618','OAKLAND')
df['city']=df['city'].replace('SOAKLAND','OAKLAND')
df['city']=df['city'].replace('`AKLAND                 ','OAKLAND')
df['city']=df['city'].replace('2630 EAST 25TH          ','OAKLAND')
df['city']=df['city'].replace('94606','OAKLAND')
df['city']=df['city'].replace('AOKALND                        ','OAKLAND')
df['city']=df['city'].replace('DOAKLAND                ','OAKLAND')
df['city']=df['city'].replace('PLASANTON','PLEASANTON')
df['city']=df['city'].replace('PLEASSANTON','PLEASANTON')
df['city']=df['city'].replace('PLEANSANTON','PLEASANTON')
df['city']=df['city'].replace('PLEAANTON','PLEASANTON')
df['city']=df['city'].replace('PLEASNATON','PLEASANTON')
df['city']=df['city'].replace('PLAEASNTON','PLEASANTON')
df['city']=df['city'].replace('PLEASANON','PLEASANTON')
df['city']=df['city'].replace('PLEANSONTON','PLEASANTON')
df['city']=df['city'].replace('SA, LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAN KEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAN   LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAN LANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SNA LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SSAN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('AND LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAM LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('CAN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SANLORENZO','SAN LORENZO')
df['city']=df['city'].replace('SN LORENZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LOENZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LORENZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LORENZO /','SAN LORENZO')
df['city']=df['city'].replace('SAN LORENZP','SAN LORENZO')
df['city']=df['city'].replace('SAN LORRENZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LORZENO','SAN LORENZO')
df['city']=df['city'].replace('SAN LORANZO','SAN LORENZO')
df['city']=df['city'].replace('YAN LORENZO','SAN LORENZO')
df['city']=df['city'].replace('SAM LORENZO','SAN LORENZO')
df['city']=df['city'].replace('SONOL','SUNOL')
df['city']=df['city'].replace('SANOL','SUNOL')
df['city']=df['city'].replace('UNON CITY','UNION CITY')
df['city']=df['city'].replace('UUNION CITY','UNION CITY')
df['city']=df['city'].replace('UNIOON CITY','UNION CITY')
df['city']=df['city'].replace('UNITON CITY','UNION CITY')
df['city']=df['city'].replace('UNIT CITY','UNION CITY')
df['city']=df['city'].replace('TRANSIENT','HOMELESS')
df['city']=df['city'].replace('HONELESS','HOMELESS')
df['city']=df['city'].replace(' ','UNKNOWN')
df['city']=df['city'].replace('ALADEDA','ALAMEDA')
df['city']=df['city'].replace('ALALMEDA','ALAMEDA')
df['city']=df['city'].replace('ALEMDA','ALAMEDA')
df['city']=df['city'].replace('ALBANY CA','ALBANY')
df['city']=df['city'].replace('CRASTO VALLY','CASTRO VALLEY')
df['city']=df['city'].replace('94546','CASTRO VALLEY')
df['city']=df['city'].replace('CANSTRO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('94552','CASTRO VALLEY')
df['city']=df['city'].replace('DUBIN','DUBLIN')
df['city']=df['city'].replace('DUBLING','DUBLIN')
df['city']=df['city'].replace('DULBIN','DUBLIN')
df['city']=df['city'].replace('DULIN','DUBLIN')
df['city']=df['city'].replace('HAY','HAYWARD')
df['city']=df['city'].replace('CAYWARD','HAYWARD')
df['city']=df['city'].replace('HAWARDD','HAYWARD')
df['city']=df['city'].replace('HAYARWD','HAYWARD')
df['city']=df['city'].replace('HAYWAD','HAYWARD')
df['city']=df['city'].replace('HAYWARDD','HAYWARD')
df['city']=df['city'].replace('HAYWARDF','HAYWARD')
df['city']=df['city'].replace('AOKLAND','OAKLAND')
df['city']=df['city'].replace('SAN LARENZO','SAN LORENZO')
df['city']=df['city'].replace('SAN L0RENZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LORNZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LORENO','SAN LORENZO')
df['city']=df['city'].replace('ALEMEDA','ALAMEDA')
df['city']=df['city'].replace('ALADEDA','ALAMEDA')
df['city']=df['city'].replace('ALAEMDA','ALAMEDA')
df['city']=df['city'].replace('ALAMADA','ALAMEDA')
df['city']=df['city'].replace('ALAMEDA,','ALAMEDA')
df['city']=df['city'].replace('ALEMEDA','ALAMEDA')
df['city']=df['city'].replace('ALMEDA','ALAMEDA')
df['city']=df['city'].replace('94502','ALAMEDA')
df['city']=df['city'].replace('94501','ALAMEDA')
df['city']=df['city'].replace(' BERKELEY','BERKELEY')
df['city']=df['city'].replace('EMVERYVILLE','EMERYVILLE')
df['city']=df['city'].replace('FREMNOT                       ','FREMONT')
df['city']=df['city'].replace('FREONT','FREMONT')
df['city']=df['city'].replace('FERMONT ','FREMONT')
df['city']=df['city'].replace('JLIVERMORE','LIVERMORE')
df['city']=df['city'].replace('LIVEMORE','LIVERMORE')
df['city']=df['city'].replace('LEVERMOARE','LIVERMORE')
df['city']=df['city'].replace('OADLAND','OAKLAND')
df['city']=df['city'].replace('SAN  LENADRO','SAN LEANDRO')
df['city']=df['city'].replace('SAL LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAV LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SA LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('AAN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SANN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('CASRO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASATRO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASTERVALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASTO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('HAYEARD','HAYWARD')
df['city']=df['city'].replace('JHAYWARD','HAYWARD')
df['city']=df['city'].replace('94544','HAYWARD')
df['city']=df['city'].replace('LIVRMORE','LIVERMORE')
df['city']=df['city'].replace('NEWERK','NEWARK')
df['city']=df['city'].replace('  OAKLAND','OAKLAND')
df['city']=df['city'].replace('  OAKLAN','OAKLAND')
df['city']=df['city'].replace('  OAKLAND,','OAKLAND')
df['city']=df['city'].replace('  OAKLANDD','OAKLAND')
df['city']=df['city'].replace('  OAKLANDL','OAKLAND')
df['city']=df['city'].replace('OACKLAND','OAKLAND')
df['city']=df['city'].replace('OAKCLAND','OALAND')
df['city']=df['city'].replace('OAKLNDN','OAKLAND')
df['city']=df['city'].replace('OALANDN','OAKLAND')
df['city']=df['city'].replace('UAKLAND','OAKLAND')
df['city']=df['city'].replace('OAKLDAND','OAKLAND')
df['city']=df['city'].replace('OAKLDND','OAKLAND')
df['city']=df['city'].replace('OAKLKAND','OAKLAND')
df['city']=df['city'].replace('OAKLNADARK','OAKLAND')
df['city']=df['city'].replace('OAKLNDA','OAKLAND')
df['city']=df['city'].replace('OALKLAND','OAKLAND')
df['city']=df['city'].replace('OANLAND      ','OAKLAND')
df['city']=df['city'].replace('OKALAND','OAKLAND')
df['city']=df['city'].replace('OOAKLANDDRO','OAKLAND')
df['city']=df['city'].replace('OQAKLAND','OAKLAND')
df['city']=df['city'].replace('0AKLAND','OAKLAND')
df['city']=df['city'].replace('PLAESANTON','PLEASANTON')
df['city']=df['city'].replace('PLEASANT','PLEASANTON')
df['city']=df['city'].replace('P[LEASANTON','PLEASANTON')
df['city']=df['city'].replace('PLEASANTO','PLEASANTON')
df['city']=df['city'].replace('PLEASABTON','PLEASANTON')
df['city']=df['city'].replace('PLEASATON','PLEASANTON')
df['city']=df['city'].replace('PLEASENTON','PLEASANTON')
df['city']=df['city'].replace('PLEASTON','PLEASANTON')
df['city']=df['city'].replace('PLEACENTON','PLEASANTON')
df['city']=df['city'].replace('PLEASANTN','PLEASANTON')
df['city']=df['city'].replace('PLEASEANTON','PLEASANTON')
df['city']=df['city'].replace('PLEASNTON','PLEASANTON')
df['city']=df['city'].replace('PLEASONTON','PLEASANTON')
df['city']=df['city'].replace('LORENZO','SAN LORENZO')
df['city']=df['city'].replace('SA LORONZO','SAN LORENZO')
df['city']=df['city'].replace('ALAMDA','ALAMEDA')
df['city']=df['city'].replace('LALMEDA','ALAMEDA')
df['city']=df['city'].replace('BWERKELEY','BERKELEY')
df['city']=df['city'].replace('BEREKEY','BERKELEY')
df['city']=df['city'].replace('CATRO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('94538','FREMONT')
df['city']=df['city'].replace('AYWARD','HAYWARD')
df['city']=df['city'].replace('PLESANTON','PLEASANTON')
df['city']=df['city'].replace('SANLORENZO','SAN LORENZO')
df['city']=df['city'].replace('ALLAMEDA','ALAMEDA')
df['city']=df['city'].replace('SAN  LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SANLEANRO','SAN LEANDRO')
df['city']=df['city'].replace('ALBNAY','ALBANY')
df['city']=df['city'].replace('ALBANY CA','ALBANY')
df['city']=df['city'].replace('LIVEMOORE','LIVERMORE')
df['city']=df['city'].replace('NEWARD','NEWARK')
df['city']=df['city'].replace('WEST OAKLAND','OAKLAND')
df['city']=df['city'].replace('PEIDMONT','PIEDMONT')
df['city']=df['city'].replace('PIEDMOND','PIEDMONT')
df['city']=df['city'].replace('SUNOLE','SUNOL')
df['city']=df['city'].replace('SUNOL;','SUNOL')
df['city']=df['city'].replace('BBERKELEYKERKELEY','BERKELEY')
df['city']=df['city'].replace('EEMERYVILLE','EMERYVILLE')
df['city']=df['city'].replace('EVERYVILLE','EMERYVILLE')
df['city']=df['city'].replace('PLEASONTON','PLEASANTON')
df['city']=df['city'].replace('ALMEDA','ALAMEDA')
df['city']=df['city'].replace('ABANY','ALBANY')
df['city']=df['city'].replace('ALBANY,','ALBANY')
df['city']=df['city'].replace('HAWARD','HAYWARD')
df['city']=df['city'].replace('HAYAWRAD','HAYWARD')
df['city']=df['city'].replace('HAYUWARD                                 ','HAYWARD')
df['city']=df['city'].replace('HAUWARD','HAYWARD')
df['city']=df['city'].replace('HAYWORD','HAYWARD')
df['city']=df['city'].replace('SAN  LORENZO','SAN LORENZO')
df['city']=df['city'].replace('LAMEDA','ALAMEDA')
df['city']=df['city'].replace('ALMAEDA                 ','ALAMEDA')
df['city']=df['city'].replace('ALAEMDA','ALAMEDA')
df['city']=df['city'].replace('ALAMDEDA','ALAMEDA')
df['city']=df['city'].replace('DUBLIND','DUBLIN')
df['city']=df['city'].replace('LIVEERMOE','LIVERMORE')
df['city']=df['city'].replace('BECKLEY','BERKELEY')
df['city']=df['city'].replace('BERLELY','BERKELEY')
df['city']=df['city'].replace('DUBLIM','DUBLIN')
df['city']=df['city'].replace('FREMONT CA','FREMONT')
df['city']=df['city'].replace('NEW WARK','NEWARK')
df['city']=df['city'].replace('NEWALK','NEWARK')
df['city']=df['city'].replace('HHWARK                  ','NEWARK')
df['city']=df['city'].replace('HATWARD','HAYWARD')
df['city']=df['city'].replace('CASTRO VALLEU','CASTRO VALLEY')
df['city']=df['city'].replace('CASTR VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASTRO','CASTRO VALLEY')
df['city']=df['city'].replace('CASTRO  VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASTRO CALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASRO  VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASTRO VALEEY','CASTRO VALLEY')
df['city']=df['city'].replace('CASTRO VALEY        ','CASTRO VALLEY')
df['city']=df['city'].replace('CASTRO VALLY','CASTRO VALLEY')
df['city']=df['city'].replace('CASTRO VILLE','CASTRO VALLEY')
df['city']=df['city'].replace('CASTROVALLEY                  ','CASTRO VALLEY')
df['city']=df['city'].replace('PLEASONTON','PLEASANTON')
df['city']=df['city'].replace('OLEASANTON','PLEASANTON')
df['city']=df['city'].replace('SASN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SANLEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('OAKBERKELEY','OAKLAND')
df['city']=df['city'].replace('EMERYBILLE              ','EMERYVILLE')
df['city']=df['city'].replace('SAN LEABDRO             ','SAN LEANDRO')
df['city']=df['city'].replace('SANLEANRO               ','SAN LEANDRO')
df['city']=df['city'].replace('FRAMONT','FREMONT')
df['city']=df['city'].replace('FRMONT','FREMONT')
df['city']=df['city'].replace('DLUBLIN','DUBLIN')
df['city']=df['city'].replace('SUNSOL','SUNOL')
df['city']=df['city'].replace('SANLEANDRO                             ','SAN LEANDRO')
df['city']=df['city'].replace('94621','OAKLAND')
df['city']=df['city'].replace('JFREMONT','FREMONT')
df['city']=df['city'].replace('9AKLAND','OAKLAND')
df['city']=df['city'].replace('SAAN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('     UNION CITY','UNION CITY')
df['city']=df['city'].replace('CASLTRO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('`CASTRO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('3-OAKLAND','OAKLAND')
df['city']=df['city'].replace('LIVIMORE','LIVERMORE')
df['city']=df['city'].replace('SAN LRENZO ','SAN LORENZO')
df['city']=df['city'].replace('CASRTO VALLEY','CASTRO VALLEY')
df['city']=df['city'].replace('SAN LORENXO','SAN LORENZO')
df['city']=df['city'].replace('SA LORENZO','SAN LORENZO')
df['city']=df['city'].replace('RKELEY','BERKELEY')
df['city']=df['city'].replace('`BERKELEY','BERKELEY')
df['city']=df['city'].replace('BEKERLEY','BERKELEY')
df['city']=df['city'].replace('BERKEKLEY','BERKELEY')
df['city']=df['city'].replace('BERKELY','BERKELEY')
df['city']=df['city'].replace('FRRMONT','FREMONT')
df['city']=df['city'].replace(' HARYWARD','HAYWARD')
df['city']=df['city'].replace('HYAYWARD','HAYWARD')
df['city']=df['city'].replace('PLEASNTON','PLEASANTON')
df['city']=df['city'].replace('SN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAN LORENENZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LAEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('AN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('UNIOON CITY','UNION CITY')
df['city']=df['city'].replace('HAYRARD','HAYWARD')
df['city']=df['city'].replace('DAN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAN LORENZI','SAN LORENZO')
df['city']=df['city'].replace('SAN LORONZO','SAN LORENZO')
df['city']=df['city'].replace('SAN LOREZO','SAN LORENZO')
df['city']=df['city'].replace('7ERKELEY','BERKELEY')
df['city']=df['city'].replace('BERKERELY','BERKELEY')
df['city']=df['city'].replace('0AKLAND','OAKLAND')
df['city']=df['city'].replace('QAKLAND','OAKLAND')
df['city']=df['city'].replace('ALAMEDA, CA,','ALAMEDA')
df['city']=df['city'].replace('DUBLLIN','DUBLIN')
df['city']=df['city'].replace('BREKELEY','BERKELEY')
df['city']=df['city'].replace('BEERKELEY','BERKELEY')
df['city']=df['city'].replace('`NEWARK ','NEWARK')
df['city']=df['city'].replace('W. OAKLAND','OAKLAND')
df['city']=df['city'].replace('LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('SAN LOEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('UNIO CITY','UNION CITY')
df['city']=df['city'].replace('BEREKELEY','BERKELEY')
df['city']=df['city'].replace('NWEARK','NEWARK')
df['city']=df['city'].replace('E. OAKLAND','OAKLAND')
df['city']=df['city'].replace('BEREKELY','BERKELEY')
df['city']=df['city'].replace('BEREKLEY','BERKELEY')
df['city']=df['city'].replace("BERKELEY'",'BERKELEY')
df['city']=df['city'].replace('  HAYWARD','HAYWARD')
df['city']=df['city'].replace('PLACENTON','PLEASANTON')
df['city']=df['city'].replace('BEKELEY','BERKELEY')
df['city']=df['city'].replace(' HAYWARD','HAYWARD')
df['city']=df['city'].replace(' OAKLAND','OAKLAND')
df['city']=df['city'].replace('OAJKLAND','OAKLAND')
df['city']=df['city'].replace('OAKKLAND','OAKLAND')
df['city']=df['city'].replace('OAKLLAND','OAKLAND')
df['city']=df['city'].replace('OAKLNAND','OAKLAND')
df['city']=df['city'].replace('OOAKLAND','OAKLAND')
df['city']=df['city'].replace('ALAMDEA','ALAMEDA')
df['city']=df['city'].replace('HAWAYRD','HAYWARD')
df['city']=df['city'].replace('HAWYARD','HAYWARD')
df['city']=df['city'].replace('OAKLSND','OAKLAND')
df['city']=df['city'].replace('OALKAND','OAKLAND')
df['city']=df['city'].replace('HAKLAND','OAKLAND')
df['city']=df['city'].replace('OAKLNAD','OAKLAND')
df['city']=df['city'].replace('PAL;AMD','OAKLAND')
df['city']=df['city'].replace('FREEMONT','FREMONT')
df['city']=df['city'].replace('FREMONT,','FREMONT')
df['city']=df['city'].replace('OAKLND','OAKLAND')
df['city']=df['city'].replace('OKALND','OAKLAND')
df['city']=df['city'].replace('OKLAND','OAKLAND')
df['city']=df['city'].replace('OALAND','OAKLAND')
df['city']=df['city'].replace('AKLAND','OAKLAND')
df['city']=df['city'].replace('NEWARD','NEWARK')
df['city']=df['city'].replace(';PEASANTON','PLEASANTON')
df['city']=df['city'].replace('LAN LEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('PLEASANTON,','PLEASANTON')
df['city']=df['city'].replace('SANLEANDRO','SAN LEANDRO')
df['city']=df['city'].replace('PLEASANTAN','PLEASANTON')
df['city']=df['city'].replace('BERLELEY','BERKELEY')
df['city']=df['city'].replace('UNIN CITY','UNION CITY')
df['city']=df['city'].replace(' UNION CITY','UNION CITY')
df['city']=df['city'].replace('UNIION CITY','UNION CITY')
df['city']=df['city'].replace('UC','UNION CITY')
df['city']=df['city'].replace('UNINON CITY','UNION CITY')
df['city']=df['city'].replace('UNTION CITY','UNION CITY')
df['city']=df['city'].replace('UNUIN CITY','UNION CITY')
df['city']=df['city'].replace('UINION CITY','UNION CITY')
df.ix[df.city.str[0:10].str.contains('SAN LORENZ'),'city']='SAN LORENZO'
df.ix[df.city.str[0:10].str.contains('PLEASANTON'),'city']='PLEASANTON'
df.ix[df.city.str[0:3].str.contains('UNK'),'city']='UNKNOWN'
df.ix[df.city.str[0:4].str.contains('OAKA'),'city']='OAKLAND'
df.ix[df.city.str[0:4].str.contains('HAYW'),'city']='HAYWARD'
df.ix[df.city.str[0:4].str.contains('BERK'),'city']='BERKELEY'
df.ix[df.city.str[0:5].str.contains('CASTO'),'city']='CASTRO VALLEY'
df.ix[df.city.str[0:5].str.contains('SUNOL'),'city']='SUNOL'
df.ix[df.city.str[0:5].str.contains('ALAME'),'city']='ALAMEDA'
df.ix[df.city.str[0:5].str.contains('OAKLA'),'city']='OAKLAND'
df.ix[df.city.str[0:5].str.contains('UNION'),'city']='UNION CITY'
df.ix[df.city.str[0:5].str.contains('FREMO'),'city']='FREMONT'
df.ix[df.city.str[0:6].str.contains('NEWARK'),'city']='NEWARK'
df.ix[df.city.str[0:6].str.contains('DUBLIN'),'city']='DUBLIN'
df.ix[df.city.str[0:6].str.contains('SAN LE'),'city']='SAN LEANDRO'
df.ix[df.city.str[0:6].str.contains('FREMON'),'city']='FREMONT'
df.ix[df.city.str[0:6].str.contains('ALBANY'),'city']='ALBANY'
df.ix[df.city.str[0:7].str.contains('EMEMRY'),'city']='EMERYVILLE'
df.ix[df.city.str[0:7].str.contains('ALAMEDA'),'city']='ALAMEDA'
df.ix[df.city.str[0:7].str.contains('FRMEONT'),'city']='FREMONT'
df.ix[df.city.str[0:7].str.contains('LIVERMO'),'city']='LIVERMORE'
df.ix[df.city.str[0:8].str.contains('EMERYVIL'),'city']='EMERYVILLE'
df.ix[df.city.str[0:8].str.contains('FFREMONT'),'city']='FREMONT'
df.ix[df.city.str[0:8].str.contains('CASTRO V'),'city']='CASTRO VALLEY'
df.ix[df.city.str[4:10].str.contains('LEANDR'),'city']='SAN LEANDRO'

df['OUTCTY']=1
df.ix[df.city.isin(['OAKLAND','SAN LEANDRO','ALAMEDA','HAYWARD','DUBLIN','LIVERMORE','SAN LORENZO','FREMONT','PLEASANTON','EMERYVILLE','PIEDMONT','ALBANY','BERKELEY','UNION CITY','CASTRO VALLEY','NEWARK',\
'HAYWARD','SUNOL','UNKNOWN','HOMELESS']),'OUTCTY']=0

df.ix[df.OUTCTY==1,'Region']='5. Out of County'
df.ix[df.street.str[0:9].str.contains('TRANSIENT') | df.street.str[0:8].str.contains('HOMELESS') | df.street.str[0:5].str.contains('NOMAD'),'homeless']=1
df.ix[df.city.str[0:10].str.contains('TRANSIENT') | df.city.str[0:7].str.contains('HOMELESS') | df.city.str[0:4].str.contains('NOMAD'),'homeless']=1
df.ix[(df.city.isin(["UNKNOWN"]) | df.city.isnull()) & df.street.isin(["TRANSIENT","HOMELESS","NOMAD"]),'city']="HOMELESS"
df.ix[(df.city.isin(["UNKNOWN"]) | df.city.isnull()) & (df.street.str[0:4].str.contains('TRAN')|df.street.str[0:4].str.contains('TRAS')| \
df.street.str[0:4].str.contains('HOM')|df.street.str.contains("(HOMELESS)|")|df.city.str.contains("HOMELESSS") ),["city","homeless"]]="HOMELESS",1
df.ix[df.city.str.contains('HOMELESS'),'Region']="6. Unknown"

engine = create_engine('postgresql://postgres:3Machine@bhcsweb3/postgres')
if AppendDB==1:
    DBAction='replace'
    print DBAction
else:
    DBAction='append'
    print DBAction
df.to_sql("test_pull_meds", engine,if_exists=DBAction)

ccstext = pd.read_csv('/media/decisionsupport/meinzer/Production/Medical spss files/CCStext.csv',header=0)
aidcodesshort= pd.read_csv('/media/decisionsupport/meinzer/Production/Medical spss files/AidCodesShort.csv',header=0)
pd.merge(df, ccstext, how='left',on='AidCode')

"""







