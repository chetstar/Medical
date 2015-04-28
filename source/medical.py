import os
from datetime import datetime
import numpy as np
import pandas as pd
from medical_meta import translation_dictionary, column_names, column_specifications
import config
#from sqlalchemy import create_engine
#import psycopg2

MedsFolder='/media/decisionsupport/meinzer/pullmedstest/'
medical_tape = config.medical_file
csstext_file = '../legacy/CCStext.csv'
aidcodes_file = '../legacy/AidCodesShort.csv'

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
df['city']=df['city'].str.upper()
df.replace(to_replace=translation_dictionary, inplace=True)

#If HCPstatus is one of the listed codes, the the 'HCplanText for that row is "z No Plan"
#I understand what this is doing technically but not the rational for it.
df.ix[df.HCPstatus.isin(["00","10","09","19","40","49","S0","S9"]),'HCplanText']="z No Plan"

#Ethnicity, Language, City replacements go here before we do wide to long.

#uncut month and uncut current file are saved here. (files 2,3)

#Reshape the data.  It is still wide here though with respect to multiple aidcodes etc.
#Its being elongated by months.
df=pd.wide_to_long(df,[ 'eligYear', 'eligMonth','AidCode','RespCounty', 'ResCounty',
                        'EligibilityStatus','SOCamount','MedicareStatus', 'CarrierCode',
                        'FederalContractNumber', 'PlanID', 'TypeID', 'v16','HCPstatus','HCPcode',
                        'OHC','v70','AidCodeSP1', 'RespCountySP1','EligibilityStatusSP1', 
                        'AidCodeSP2', 'RespCountySP2','EligibilityStatusSP2', 'SOCpctSP', 
                        'HFEligDaySP','AidCodeSP3', 'RespCountySP3','EligibilityStatusSP3'],
                   i='id',j='varstocases')

#Why are we multiplying eligYear by 10000 and eligMonth by 100?
#The format='%Y%m%d' takes an eight digit long number and turns it into a datetime object.
#We need to create that eight digit number, so to move the year left by four digits, * by 10000.
df['calendar'] = pd.to_datetime(df['eligYear']*10000 + df['eligMonth']*100 + 1, format='%Y%m%d')

#The index gets rearranged with the wide_to_long, reset it.
df=df.reset_index()

#Wide to long by aidcode.  Sort by j-index.
#If aidcodeN contains ("9K","9M","9N","9R","9U") select that row.
#return to previous df.

#For each instance of eligibilityStatus create a series of the first digit of elgigbilityStatus.
#The index for these matches that of df but with numbers missing for the dropped rows.
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
#Wide to long by aidcode
y=pd.wide_to_long(x,[ 'AidCode','RespCounty','EligibilityStatus'],i='xid',j='xvarstocases')
y=y.reset_index()

#Bring in text form of aid codes.
ccstext = pd.read_csv(csstext_file,header=0)
aidcodesshort= pd.read_csv(aidcodes_file,header=0)

#Merge in text form of aid codes. Why change from y to g as our dataframe name here?
g=pd.merge(y, ccstext, how='left',left_on='AidCode',right_on='AidCode')
g=pd.merge(g, aidcodesshort, how='left',left_on='AidCode',right_on='aidcode')

#Save file (4) medCSS%month.sav (only about six columns)
#return to original df.

#Make small demographics files
#Update if there, insert if not.

#Everything after this is in explode.

#if aidcode is in list and mcelig is one, SSI is one.
g.ix[g.AidCode.isin(["10","20","60"]) & (g.MCelig ==1),'SSI']=1

#get a series of the first digits of non-nan numbers
t = g.EligibilityStatus.dropna().astype(str).str[0].astype(int) 

#The followin two lines of code make columns that combine eligibility status and disabled or
#foster status.
#If first digit of g.EligibilityStatus is less than five and g.Foster==1, then Fosterx is set True.
g['Fosterx'] = ((t < 5).astype(int)) & (g.Foster==1)
#If first digit of g.EligibilityStatus is less than 5 and g.Disabled==1, then Disabledx is set 
#to True.
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
g['FFP']=g['FFP'].fillna(99)#Does it make sense to do this?

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


g=g.apply(f,axis=1)
g.loc[((g.EligibilityStatus.dropna().astype(str).str[0].astype(int) < 5)) & (g.RespCounty==1) & (g.Full==1) & (g.FFP==100),['eligibility_month',
'primary_Aid_code','slot','mcRank','ELIGIBILITY_COUNTY_code']]=g['eligYear'],1,1,1,1,1

g.sort(['CIN','calendar']).to_csv('dupes')
df.ix[df.OUTCTY==1,'Region']='5. Out of County'
df.ix[df.street.str[0:9].str.contains('TRANSIENT') | df.street.str[0:8].str.contains('HOMELESS') | df.street.str[0:5].str.contains('NOMAD'),'homeless']=1
df.ix[df.city.str[0:10].str.contains('TRANSIENT') | df.city.str[0:7].str.contains('HOMELESS') | df.city.str[0:4].str.contains('NOMAD'),'homeless']=1
df.ix[(df.city.isin(["UNKNOWN"]) | df.city.isnull()) & df.street.isin(["TRANSIENT","HOMELESS","NOMAD"]),'city']="HOMELESS"
df.ix[(df.city.isin(["UNKNOWN"]) | df.city.isnull()) & (df.street.str[0:4].str.contains('TRAN')|df.street.str[0:4].str.contains('TRAS')| \
df.street.str[0:4].str.contains('HOM')|df.street.str.contains("(HOMELESS)|")|df.city.str.contains("HOMELESSS") ),["city","homeless"]]="HOMELESS",1
df.ix[df.city.str.contains('HOMELESS'),'Region']="6. Unknown"

ccstext = pd.read_csv('/media/decisionsupport/meinzer/Production/Medical spss files/CCStext.csv',
                      header=0)
aidcodesshort= pd.read_csv('/media/decisionsupport/meinzer/Production/Medical spss files/AidCodesShort.csv',header=0)
pd.merge(df, ccstext, how='left',on='AidCode')








