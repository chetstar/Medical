*IMPORT  FILE='//covenas/spssdata/case_addrs.por'.
*import file='//covenas/spssdata/AddressAOD.POR'.
*import file='//covenas/spssdata/AOD_CASE_ADDRS.POR'.

*compute number = ltrim(number).
*compute street = ltrim(street).

compute city=upcas(city).
compute city = ltrim(city).

if substr(city,1,5) = "ALAME"  city = "ALAMEDA".                                        
if city = "ALAMDEA" city = "ALAMEDA".                                                   
if city = "ALAMEDA, CA," city = "ALAMEDA".                                              
if city = "ALMEDA" city = "ALAMEDA".        
if city = "ALAMADA" city = "ALAMEDA".
if city = "ALAMDA"              city = "ALAMEDA".    
if city = "LALMEDA"              city = "ALAMEDA".    
if city = "LAMEDA"              city = "ALAMEDA".         
if city = "ALADEDA"              city = "ALAMEDA". 
if city = "ALMAEDA                 "              city = "ALAMEDA".         
if city = "ALAEMDA"              city = "ALAMEDA".         
if city = "ALAMDEDA"              city = "ALAMEDA".         
if city = "ALEMEDA"              city = "ALAMEDA".  
if city = "ALADEDA"              city = "ALAMEDA".  
if city = "ALAEMDA"              city = "ALAMEDA".  
if city = "ALAMADA"              city = "ALAMEDA".  
if city = "ALAMEDA,"              city = "ALAMEDA".  
if city = "ALEMEDA"              city = "ALAMEDA".  
if city = "ALMEDA"              city = "ALAMEDA".  
if city = "ALLAMEDA"          city = "ALAMEDA".     
if substr(city,1,7) = "ALAMEDA"              city = "ALAMEDA".  
if city = "ALAMAEDA" city = "ALAMEDA".
if city = "ALAMDED" city = "ALAMEDA".
if city = "ALAMRDA" city = "ALAMEDA".
if city = "ALEMADA" city = "ALAMEDA".
if city = "ALANDMED" city = "ALAMEDA".
if city = "ALAMEDA CA" city = "ALAMEDA".
if city = "94502"              city = "ALAMEDA".  
if city = "94501"              city = "ALAMEDA".  
if city = "ALALMEDA"          city = "ALAMEDA". 
if city = "ALEMDA"          city = "ALAMEDA". 
                
                  


if city = "ALBANY CA" city = "ALBANY". 
if substr(city,1,6) = "ALBANY" city = "ALBANY".                     
if city = "ABANY" city = "ALBANY".        
if city = "ALBANY," city = "ALBANY".        
if city = "ALABANY" city = "ALBANY".
if city = "ALPANY" city = "ALBANY".
if city = "ALBNAY" city = "ALBANY".      
if city = "ALBANY CA"  city = "ALBANY".      
if city = "ALBAY" city = "ALBANY".



if city = "RKELEY" city = "BERKELEY".                                        
if city = "`BERKELEY"  city = "BERKELEY".                                        
if city = "BEKERLEY" city = "BERKELEY".                                        
if city = "BERKEKLEY" city = "BERKELEY".                                        
if city = "BERKELY" city = "BERKELEY".                                        
if city = "7ERKELEY" city = "BERKELEY".                                             
if substr(city,1,4) = "BERK"  city = "BERKELEY".                                        
if city = "BEKELEY" city = "BERKELEY".                                                  
if city = "BEREKELEY" city = "BERKELEY".                                                
if city = "BECKLEY" city = "BERKELEY".          
if city = "BERKERELY"      city = "BERKELEY".                                             
if city = "BEREKELY" city = "BERKELEY".                                                 
if city="BERLELEY" city = "BERKELEY".                                                   
if city = " BERKELEY" city = "BERKELEY".  
if city = "BREKELEY" city = "BERKELEY".                                               
if city = "BEERKELEY" city = "BERKELEY".                                               
if city = "BEREKLEY" city = "BERKELEY".                                                 
if city = "BERLELY" city = "BERKELEY".          
if city = "BERKELEY'" city = "BERKELEY".                                                 
if city = "BAERKELEY" city = "BERKELEY".
if city = "BERELEY" city = "BERKELEY".
if city = "BWERKELEY"   city = "BERKELEY".    
if city = "BEREKEY"   city = "BERKELEY".    
if city = "BBERKELEYKERKELEY" city= "BERKELEY".       
if city = "BARKELEY" city = "BERKELEY".
if city = "BRKELEY" city = "BERKELEY".
if city = "BVERKELEY" city = "BERKELEY".
if city = "ERKELEY" city = "BERKELEY".
if city = "CA94706" city = "BERKELEY".
if city = "94704" city = "BERKELEY".

                 
       
                          
if substr(city,1,5) = "CASTO" city = "CASTRO VALLEY". 
if city = "CASTRO VALLEY," city = "CASTRO VALLEY".
if city = "CASLTRO VALLEY" city = "CASTRO VALLEY".                                  
if city ="CASTRE VALLEY" city = "CASTRO VALLEY".                                       
if city = "`CASTRO VALLEY" city = "CASTRO VALLEY".                                  
if city =" CASTRO VALLEY" city = "CASTRO VALLEY".                                       
if city = "CASRTO VALLEY" city = "CASTRO VALLEY".                                       
if city = "CASTRO VALLEU" city = "CASTRO VALLEY".             
if city = "CASTR VALLEY" city = "CASTRO VALLEY".             
if substr(city,1,8) = "CASTRO V" city = "CASTRO VALLEY".             
if city = "CASRO VALLEY" city = "CASTRO VALLEY".   
if city = "CASTRO" city = "CASTRO VALLEY".             
if city = "CASTRO  VALLEY" city = "CASTRO VALLEY".             
if city = "CASTRO CALLEY" city = "CASTRO VALLEY".             
if city = "CASRO  VALLEY" city = "CASTRO VALLEY".             
if city = "CASTRO VALEEY" city = "CASTRO VALLEY".             
if city = "CASTRO VALEY        " city = "CASTRO VALLEY".             
if city = "CASTRO VALLY" city = "CASTRO VALLEY".             
if city = "CASTRO VILLE" city = "CASTRO VALLEY".             
if city = "CASTROVALLEY                  " city = "CASTRO VALLEY".             
if city = "CATRO VALLEY" city   = "CASTRO VALLEY".    
if city = "CASATRO VALLEY" city   = "CASTRO VALLEY".   
if city = "CASTERVALLEY" city   = "CASTRO VALLEY".   
if city = "CASTO VALLEY"  city   = "CASTRO VALLEY".   
if city = "CRASTO VALLY"  city   = "CASTRO VALLEY". 
if city = "94546"  city   = "CASTRO VALLEY". 
if city = "CANSTRO VALLEY"  city   = "CASTRO VALLEY". 
if city = "94552"  city   = "CASTRO VALLEY". 
          


If substr(city,1,6) = "DUBLIN" city = "DUBLIN" .        
If city = "DUBIN" city = "DUBLIN". 
If city = "DUBLIND" city = "DUBLIN".         
If city = "DUBLLIN" city = "DUBLIN".                                              
if city = "DUBLIM" city = "DUBLIN".          
If city = "DUBLING" city = "DUBLIN". 
If city = "DULBIN" city = "DUBLIN". 
If city = "DULIN" city = "DUBLIN". 
If city = "DLUBLIN" city = "DUBLIN".                    
if city = "DYBLIN" city = "DUBLIN".
if city = "DBLN" city = "DUBLIN".



if substr(city,1,8 ) = "EMERYVIL" city = "EMERYVILLE".                                  
if city = "EEMERYVILLE" city = "EMERYVILLE".       
if city = "EVERYVILLE" city = "EMERYVILLE".       
if city = "EMERVILLE" city = "EMERYVILLE".
if city = "EMERY VILLE" city = "EMERYVILLE".
if city = "EMERYVELLIE" city = "EMERYVILLE".
if city = "EMERIVILLE" city = "EMERYVILLE".
if city = "EMORYVILLE" city = "EMERYVILLE".
if city = "EMMERYVILLE" city = "EMERYVILLE".
if city = "EMERYWILLE" city = "EMERYVILLE".
if city = "EMIRYVILLE" city = "EMERYVILLE".
if city = "EMMEYVILLE" city = "EMERYVILLE".
if city = "EMRYVILLE" city = "EMERYVILLE".
if city = "EMVERYVILLE" city = "EMERYVILLE".  
if city = "EMEMERY" city = "EMERYVILLE".
if city = "EMERBILLE" city = "EMERYVILLE".
if city = "EMMERYVILE" city = "EMERYVILLE".
if city = "EMORYVILLE" city = "EMERYVILLE".
if city = "94608" city = "EMERYVILLE".
if city = "EMERWILLE" city = "EMERYVILLE".
if substr(city,1,7 ) = "EMEMRY" city = "EMERYVILLE".                                  
if city = "EMERVYLLE" city = "EMERYVILLE".
if city = "EMEYVILLE" city = "EMERYVILLE".
if city = "SMERYVILLE" city = "EMERYVILLE".
if city = "EMERVILL                " city = "EMERYVILLE".
if city = "EMERYBILLE              " city = "EMERYVILLE".               
               

if substr(city,1,6) = "FREMON" city="FREMONT".                   
if city = "FRMONT" city="FREMONT".                   
if city = "FREMPNT" city="FREMONT".
if city = "FREMNOT                       " city="FREMONT".  
if city = "FREONT"     city="FREMONT".  
if city = "FRAMONT"     city="FREMONT".                
if city = "94538"     city="FREMONT".    
if city = "FERMONT "     city="FREMONT".  
                
   
if substr(city,1,5) = "FREMO" city="FREMONT".                                           
if city = "FREEMONT" city="FREMONT".                                                    
if city = "FREMONT CA" city="FREMONT".          
if city = "FRRMONT" city = "FREMONT".                                        
if city = "FREMONT," city="FREMONT".                                                    
if city = "FEMONT" city="FREMONT".
if city = "FREMOT" city="FREMONT".
if city = "FREMNT" city="FREMONT".
if city = "FREMMONT" city="FREMONT".
if city = "FRENMONT" city="FREMONT".
if city = "FRENONT" city="FREMONT".
if city = "FRIMONT" city ="FREMONT".
if city = "FREAMONT" city = "FREMONT".
if city = "FREMON" city = "FREMONT".
if substr(city,1,8) = "FFREMONT" city="FREMONT".  
if substr(city,1,7) = "FRMEONT" city="FREMONT".  
if city = "JFREMONT" city = "FREMONT".                                
  


                      
if substr(city,1,4) = "HAYW"  city = "HAYWARD".        
if city = "HAWARD"  city = "HAYWARD".        
if city = "HAYAWRAD"  city = "HAYWARD".        
if city = "HAYUWARD                                 "  city = "HAYWARD".        
if city = "HATWARD" city = "HAYWARD".            
if city = " HARYWARD" city = "HAYWARD".                                         
if city = " HAYWARD" city = "HAYWARD".                                                  
if city = "HAWAYRD" city = "HAYWARD".                                                   
if city = "HAYARD" city = "HAYWARD".
if city = "HAUWARD" city = "HAYWARD".        
if city = "HARYWARD" city = "HAYWARD".
if city = "HAYWORD" city = "HAYWARD".        
if city = "AYWARD" city = "HAYWARD".    
if city = "HWYWARD" city = "HAYWARD".
if city = "HYAYWARD" city = "HAYWARD".                                         
if city = "HAWYARD" city = "HAYWARD".                                                   
if city = "  HAYWARD" city = "HAYWARD".                                                 
if city = "HAYEARD" city = "HAYWARD".   
if city = "HAY" city = "HAYWARD". 
if city = "CAYWARD" city = "HAYWARD". 
if city = "HAWARDD" city = "HAYWARD". 
if city = "HAYARWD" city = "HAYWARD". 
if city = "HAYWAD"  city = "HAYWARD". 
if city = "HAYWARDD" city = "HAYWARD". 
if city = "HAYWARDF" city = "HAYWARD". 
if city = "HAYRARD" city = "HAYWARD".                                           
if city = "JHAYWARD" city = "HAYWARD".   
if city = "94544" city = "HAYWARD".   

     
if substr(city,1,7) = "LIVERMO" city = "LIVERMORE".      
if city = "LIVEERMORE" city = "LIVERMORE".      
if city = "LIVEMOORE" city = "LIVERMORE".      
if city = "LIVIMORE" city = "LIVERMORE".                                     
if city = "JLIVERMORE" city = "LIVERMORE".  
if city = "LIVEMORE" city = "LIVERMORE".  
if city = "LEVERMOARE" city = "LIVERMORE".  
if city = "LIVERSOME" city = "LIVERMORE".
if city = "LIV ERMORE" city = "LIVERMORE".
if city = "LIVORMORE"  city = "LIVERMORE".
if city = "LLIVERMORE" city = "LIVERMORE".
if city = "LIVBERMORE" city = "LIVERMORE".
if city = "IVERMORE" city = "LIVERMORE".
if city = "LVMR" city = "LIVERMORE".
if city = "LIVEROMORE" city = "LIVERMORE".

  
if city = "NEWARD" city = "NEWARK".                                                     
if city  = " NEWARDK" city = "NEWARK".                                                  
if city  = " NEWARK" city = "NEWARK".    
if city = "`NEWARK " city = "NEWARK".                                               
if city  = "NEWARDK" city = "NEWARK".                                                   
if city  = "NEWARKCITY" city = "NEWARK".  
if city = "NEWEARK" city = "NEWARK".
if city = "NEWAR" city= "NEWARK".
if city = "NEWARKK" city= "NEWARK".
if city = "NEWAWRK" city= "NEWARK".
if city = "NEWRAK" city= "NEWARK".
if city = "NEWARKN" city= "NEWARK".
if city = "NEARK" city= "NEWARK".
if city = "NAWARK" city= "NEWARK".
if substr(city,1,6)  = "NEWARK" city = "NEWARK".                                                   
if city = "NWEARK" city = "NEWARK".                                                
if city  = "NEWORK" city = "NEWARK".                                                    
if city  = "NEWWARK" city = "NEWARK".                                                   
if city  = "MEWARK" city = "NEWARK".
if city  = " NEWORK" city = "NEWARK".                                                   
if city  = " NEWWARK" city = "NEWARK".          
if city  = "NEWARIK" city = "NEWARK".     
if city  = "NEWARKD" city = "NEWARK".     
if city  = "NEWARKS" city = "NEWARK".     
if city  = "NEWARKT" city = "NEWARK".     
if city  = "NEWMARK" city = "NEWARK".      
if city = "NEW WARK" city = "NEWARK".          
if city = "NEWALK" city = "NEWARK".          
if city = "NEWARD" city = "NEWARK".      
if city = "HHWARK                  " city = "NEWARK".          
             

                          
if city = "E. OAKLAND" city = "OAKLAND".                                                
if city = "  OAKLAND"    city = "OAKLAND".   
if city = "OACKLAND"    city = "OAKLAND".   
if city = "OAKCLAND"    city = "OALAND".   
if city = "OAKDLAND"    city = "OAKLAND".
if city = "OAKLNDN"    city = "OAKLAND".   
if city = "OALANDN"    city = "OAKLAND".   
if city = "AOKLAND" city = "OAKLAND".
if city = "`OAKLAND" city = "OAKLAND".
if city = "UAKLAND"    city = "OAKLAND".   
if city = "OAKLDAND"    city = "OAKLAND".   
if city = "OAKLDND"    city = "OAKLAND".   
if city = "OAKLKAND"    city = "OAKLAND".   
if city = "OAKLNADARK"    city = "OAKLAND".   
if city = "OAKLNDA"    city = "OAKLAND".   
if city = "OALKLAND"    city = "OAKLAND".   
if city = "OANLAND      "    city = "OAKLAND".   
if city = "OKALAND"    city = "OAKLAND".   
if city = "OADLAND" city = "OAKLAND".
if city = "OOAKLANDDRO"    city = "OAKLAND".   
if city = "OPAKLAND"    city = "OAKLAND".
if city = "OADLAND" city = "OAKLAND".  
if city = "AOKLAND" city = "OAKLAND". 
if city = "WEST OAKLAND"    city = "OAKLAND".      
if city = "9AKLAND" city = "OAKLAND".                                
if city = " OAKLAND" city = "OAKLAND".                                                  
if city = "0AKLAND"       city = "OAKLAND".                                             
if city = "OAJKLAND" city = "OAKLAND".                                                  
if city = "OAKBERKELEY"  city = "OAKLAND".              
if city = "ÓKALAND" CITY = "OAKLAND".
if city = "OAKKLAND" city = "OAKLAND".                                                  
if city = "OAKLND" city = "OAKLAND".                                                    
if city = "OAKLLAND" city = "OAKLAND".                                                  
if city = "OAKLSND" city = "OAKLAND".                                                   
if city = "OALKAND" city = "OAKLAND".                                                   
if city = "OKALND" city = "OAKLAND".                                                    
if city = "OKLAND" city = "OAKLAND".                                                    
if substr(city,1,5) = "OAKLA"  city = "OAKLAND".                                        
if substr(city,1,4) = "OAKA"  city = "OAKLAND".       
if city = "JOAKLAND" city = "OAKLAND".
if city = "3-OAKLAND" city = "OAKLAND".                                  
if city = "HAKLAND" city = "OAKLAND".                                                   
if city = "OAKLNAD" city = "OAKLAND".                                                   
if city = "OAKLNAND" city = "OAKLAND".                                                  
if city = "OALAND" city = "OAKLAND".                                                    
if city = "AKLAND" city = "OAKLAND".                                                    
if city = "PAL;AMD" city = "OAKLAND".                                                   
if city = "QAKLAND"       city = "OAKLAND".                                             
if city = "W. OAKLAND"  city = "OAKLAND".                                               
if city = "OOAKLAND" city = "OAKLAND".                                                  
if city = "OQAKLAND" city = "OAKLAND".   
if city = "0AKLAND" city = "OAKLAND".   
if city = "OFAKLAND" city="OAKLAND".
if city = "`OAKLAND" city="OAKLAND".
if city = "OAKLDN"    city="OAKLAND".
if city = "RAKLAND" city = "OAKLAND".
if city = "AKALND" city = "OAKLAND".
if city = "OAKALND" city = "OAKLAND".
if city = "OAKLAMD" city = "OAKLAND".
if city = "OAKLAND CA" city = "OAKLAND".
if city = "OALAND" city = "OAKLAND".
if city = "94603" city = "OAKLAND".
if city = "EAST OAKLAND" city = "OAKLAND".
if city = "OQKLQND" city = "OAKLAND".
if city = "OSKLSNF" city = "OAKLAND".
if city = "OAK" city = "OAKLAND".
if city = "94602" city = "OAKLAND".
if city = "94605" city = "OAKLAND".
if city = "94609" city = "OAKLAND".
if city = "94612" city = "OAKLAND".
if city = "94618" city = "OAKLAND".
if city = "SOAKLAND" city = "OAKLAND".
if city = "`AKLAND                 " city = "OAKLAND".
if city = "2630 EAST 25TH          "  city = "OAKLAND".
if city = "94606         "  city = "OAKLAND".
if city = "AOKALND                        "  city = "OAKLAND".
if city = "DOAKLAND                "  city = "OAKLAND".

if city = "PEIDMONT" city = "PIEDMONT".      
if city = "PIEDMOND"  city = "PIEDMONT".      



if substr(city,1,10) = "PLEASANTON" city = "PLEASANTON".                                                                                          
if city = "PLEASONTON" city="PLEASANTON".             
if city = "OLEASANTON" city="PLEASANTON".             
if city = "PLACENTON"    city="PLEASANTON".                                                 
if city = ";PEASANTON"  city="PLEASANTON".                                                                                      
if city="PLEASANTAN" city="PLEASANTON".                                                 
if city="PLEASANTON," city="PLEASANTON".                                                
if city = "PLEASONTON" city = "PLEASANTON".       
if city = "PLEASNTON" city = "PLEASANTON".                                         
if city = "PLESANTON" city = "PLEASANTON".    
if city = "PLAESANTON" city = "PLEASANTON".   
if city = "PLASANTON" city = "PLEASANTON".
if city = "PLEASSANTON" city = "PLEASANTON".
if city = "PLEANSANTON" city = "PLEASANTON".
if city = "PLEAANTON" city = "PLEASANTON".
if city = "PLEASANT" city = "PLEASANTON".   
if city = "P[LEASANTON" city = "PLEASANTON".   
if city = "PLEASANTO" city = "PLEASANTON".   
if city = "PLEASABTON" city ="PLEASANTON".   
if city = "PLEASATON" city = "PLEASANTON".   
if city = "PLEASENTON" city = "PLEASANTON".   
if city = "PLEASNATON" city = "PLEASANTON".
if city = "PLAEASNTON" city = "PLEASANTON".
if city = "PLEASANON" city = "PLEASANTON".
if city = "PLEANSONTON" city = "PLEASANTON".
if city = "PLEASTON" city = "PLEASANTON".   
if city = "PLEACENTON" city = "PLEASANTON".   
if city = "PLEASANTN"  city = "PLEASANTON".   
if city = "PLEASEANTON"  city = "PLEASANTON".   
if city = "PLEASNTON" city = "PLEASANTON".   
if city = "PLEASONTON" city = "PLEASANTON".   



if city = "SAN  LEANDRO" city = "SAN LLEADRO".     
if city = "SAN  LEANDRO" city = "SAN LEANDRO".     
if city = "SA, LEANDRO" city = "SAN LEANDRO".
if city = "SAN KEANDRO" city = "SAN LEANDRO".
if city = "SAN   LEANDRO" city = "SAN LEANDRO".
if city = "SAN  LENADRO" city = "SAN LEANDRO".  
if city = "SAL LEANDRO" city = "SAN LEANDRO".  
if city = "SAV LEANDRO" city = "SAN LEANDRO".  
if city = "LEANDRO" city = "SAN LEANDRO".                                               
if city = "SAN LOEANDRO" city = "SAN LEANDRO".                                               
if city = "SAN LAEANDRO" city = "SAN LEANDRO".                                          
if city = "DAN LEANDRO" city = "SAN LEANDRO".                                           
if city = "AN LEANDRO" city = "SAN LEANDRO".                                          
if city = "SANLEANRO"      city="SAN LEANDRO".     
if city = "SAN LEABDRO             " city =   "SAN LEANDRO".               
if city = "SANLEANRO               " city =              "SAN LEANDRO".               
if city = "SANLEANDRO                             " city =              "SAN LEANDRO".                           
if city="LAN LEANDRO" city="SAN LEANDRO".                                               
if city = "SN LEANDRO"      city="SAN LEANDRO".                                         
if substr(city,1,6) = "SAN LE" city="SAN LEANDRO".     
if city = "SAAN LEANDRO" city = "SAN LEANDRO".                                 
if city="SANLEANDRO" city="SAN LEANDRO".                                                
if city = "SA LEANDRO" city = "SAN LEANDRO".  
if city = "AAN LEANDRO" city = "SAN LEANDRO".  
if city = "SANN LEANDRO" city = "SAN LEANDRO".  
if city = "SAN LANDRO" city = "SAN LEANDRO".
if substr(city,5,10) = "LEANDR" city= "SAN LEANDRO".
if city = "SNA LEANDRO" city = "SAN LEANDRO".
if city = "SSAN LEANDRO" city = "SAN LEANDRO".
if city = "AND LEANDRO" city = "SAN LEANDRO".
if city = "SAM LEANDRO" city = "SAN LEANDRO".
if city = "CAN LEANDRO" city = "SAN LEANDRO".
if city = "SASN LEANDRO" city = "SAN LEANDRO".             




if city = "SN LORENZO" city = "SAN LORENZO".
if substr(city,1,10) = "SAN LORENZ" city = "SAN LORENZO".
if city = "SAN LOENZO" city = "SAN LORENZO".
if city = "SAN LORENZO" city = "SAN LORENZO".
if city = "SAN LORENZO /" city = "SAN LORENZO".
if city = "SAN LORENZP" city = "SAN LORENZO".
if city = "SAN LORRENZO" city = "SAN LORENZO".
if city = "SAN LORZENO" city = "SAN LORENZO".
if city = "SAN LRENZO " city = "SAN LORENZO".                                      
if city = "SAN LORENENZO" city = "SAN LORENZO".                                         
if city = "SAN  LORENZO" city = "SAN LORENZO".        
if city = "LORENZO" city = "SAN LORENZO".                                         
if city = "SAN LORENZI" city = "SAN LORENZO".                                           
if city = "SAN LOREZO" city = "SAN LORENZO".                                            
if city = "SAN LORONZO" city = "SAN LORENZO".                                           
if city = "SA LORONZO" city = "SAN LORENZO".   
if city = "SA LORENZO"      city = "SAN LORENZO".                                       
if city = "SANLORENZO" city ="SAN LORENZO".    
if city = "SAN LARENZO" city="SAN LORENZO". 
if city = "SAN L0RENZO"   city="SAN LORENZO". 
if city = "SAN LORNZO"   city="SAN LORENZO". 
if city = "SAN LORENO" city="SAN LORENZO". 
if city = "SAN LORANZO" city="SAN LORENZO".
if city = "YAN LORENZO" city="SAN LORENZO".
if city = "SAM LORENZO" city="SAN LORENZO".

if city = "SUNOLE" city = "SUNOL".      
if city = "SUNOL;" city = "SUNOL".      
if substr(city,1,5) = "SUNOL" city = "SUNOL". 
if city = "SUNSOL" city = "SUNOL".                         
if city = "SONOL" city = "SUNOL".
if city = "SANOL" city = "SUNOL".
                      

 
if substr(city,1,5) = "UNION" city="UNION CITY".                                        
if city= " UNION CITY" city="UNION CITY".            
if city= "UC" city="UNION CITY".                                          
if city= "UINION CITY" city="UNION CITY".                                               
if city= "UNIION CITY" city="UNION CITY".                   
if city = "     UNION CITY"    city="UNION CITY".                                 
if city= "UNIN CITY" city="UNION CITY".   
if city = "UNIO CITY" city="UNION CITY".                                               
if city= "UNINON CITY" city="UNION CITY".                                          
if city= "UNTION CITY" city="UNION CITY".                                          
if city= "UNUIN CITY" city="UNION CITY".                                          
if city = "UNIOON CITY" city="UNION CITY".                                          
if city = "UNON CITY" city = "UNION CITY".
if city = "UUNION CITY" city = "UNION CITY".
if city = "UNIOON CITY" city = "UNION CITY".
if city = "UNITON CITY" city = "UNION CITY".
if city = "UNIT CITY" city = "UNION CITY".


if substr(city,1,3) = "UNK" city= "UNKNOWN".

if city = "TRANSIENT" city  = "HOMELESS".
if city = "HONELESS" city  = "HOMELESS".
if city = " " city= "UNKNOWN".

*FREQ City.


*********STOP********************.

COMPUTE OUTCTY=1.
IF CITY = "OAKLAND" OUTCTY=0.
IF CITY="SAN LEANDRO" OUTCTY=0.
IF CITY="ALAMEDA" OUTCTY=0.
IF CITY="HAYWARD" OUTCTY=0.
IF CITY="DUBLIN" OUTCTY=0.
IF CITY="LIVERMORE" OUTCTY=0.
IF CITY="SAN LORENZO" OUTCTY=0.
IF CITY="FREMONT" OUTCTY=0.
IF CITY="PLEASANTON" OUTCTY=0.
IF CITY="EMERYVILLE" OUTCTY=0.
IF CITY="PIEDMONT" OUTCTY=0.
IF CITY="ALBANY" OUTCTY=0.
IF CITY="BERKELEY" OUTCTY=0.
IF CITY="UNION CITY" OUTCTY=0.
IF CITY="CASTRO VALLEY" OUTCTY=0.
IF CITY="NEWARK" OUTCTY=0.
IF CITY="HAYWARD" OUTCTY=0.
IF CITY = "SUNOL" OUTCTY=0.
IF CITY = "UNKNOWN" OUTCTY=0.
IF CITY = "HOMELESS"     OUTCTY=0.

*IF OUTCTY=1 CITY = "z. Out of County".

execute.

string Region(a18).

if city = "ALAMEDA" Region="1. North".
if city = "ALBANY" Region="1. North".
if city = "BERKELEY" Region="1. North".
if city = "OAKLAND" Region="1. North".
if city = "EMERYVILLE" Region="1. North".
if city = "PIEDMONT" Region="1. North".         

if city = "HAYWARD" Region="2. Central".         
if city = "SAN LEANDRO" Region="2. Central".         
if city = "SAN LORENZO" Region="2. Central".       
if city  = "CASTRO VALLEY" Region="2. Central".

if city = "PLEASANTON" Region="4. East".         
if city = "LIVERMORE" Region="4. East".         
if city = "SUNOL" Region="4. East".         
if city = "DUBLIN" Region="4. East". 
               
if city = "UNION CITY" Region="3. South".         
if city = "FREMONT" Region="3. South".         
if city = "NEWARK" Region="3. South".                 

if city = "UNKNOWN" Region="6. Unknown".         
do if OUTCTY = 1.
compute  Region="5. Out of County".
end if.


if substr(street,1,9) = "TRANSIENT" OR substr(street,1,8) = "HOMELESS" OR substr(street,1,5) = "NOMAD" homeless=1.
if substr(city,1,9) = "TRANSIENT" OR substr(city,1,8) = "HOMELESS" OR substr(city,1,5) = "NOMAD" homeless=1.

  
do if city = " " OR city= "UNKNOWN".
do if substr(street,1,9) = "TRANSIENT" OR substr(street,1,8) = "HOMELESS" OR substr(street,1,5) = "NOMAD". 
compute city  = "HOMELESS".
end if.
end if.

do if city = " " OR city= "UNKNOWN".
do if substr(street,1,4) = "TRAN" OR substr(street,1,4) = "TRAS" OR substr(street,1,3) = "HOM" OR street = "(HOMELESS)" OR city = "HOMELESSS".
compute city  = "HOMELESS".
compute homeless=1.
end if.
end if.

IF CITY = "HOMELESS"     Region="6. Unknown".    

*save outFILE='//covenas/spssdata/AddressAOD.SAV'.

*save outFILE='//covenas/spssdata/AOD\AOD_CASE_ADDRESS.SAV'.

