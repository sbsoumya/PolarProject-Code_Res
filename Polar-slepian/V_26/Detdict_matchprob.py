#---------------------------------------------------
# Name:       Detdict_match.py
# Purpose:    generate ditection bit match probabilities for detdict
#
# Author:      soumya
#
# Created:    17/03/2018
#---------------------------------------------
# all the large 
#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
from datetime import datetime
import json
import polarconstruct as pcon
from pprint import pprint
import csv
import matplotlib.pyplot as plt
import lambdathreshold as lmb
import detectionbits as dd


#------------------Detdict files
Detdictfiledict={"155":["Detdict-G-155of1024-des-0p04-ch0p04-18-03-18_01-30-28.txt"
,"Detdict-G-155of1024-des-0p04-ch0p15-18-03-18_01-30-44.txt"],
"310":["Detdict-G-310of1024-des-0p04-ch0p04-18-03-18_01-36-03.txt"
,"Detdict-G-310of1024-des-0p04-ch0p15-18-03-18_01-36-11.txt"],
"465":["Detdict-G-465of1024-des-0p04-ch0p04-18-03-18_01-41-40.txt"
,"Detdict-G-465of1024-des-0p04-ch0p15-18-03-18_01-41-38.txt"],
"620":["Detdict-G-620of1024-des-0p04-ch0p04-18-03-18_01-47-18.txt"
,"Detdict-G-620of1024-des-0p04-ch0p15-18-03-18_01-47-08.txt"],
"775":["Detdict-G-775of1024-des-0p04-ch0p04-18-03-18_01-52-58.txt"
,"Detdict-G-775of1024-des-0p04-ch0p15-18-03-18_01-52-39.txt"]}
#-------------------------------------------
Ratelist=["155","310","465","620","775"]
runsim=1000
N=1024
prob_matchdict={}
design_p=0.04
channel_plist=[0.04,0.15]
header_write=1
with open("./simresults/Dectditreport-"+str(N)+"-des"+str(design_p).replace(".","p")+".csv",'wb') as resultFile:
			wr = csv.writer(resultFile, dialect='excel')
			wr.writerow(["Detectionbits Report"])
			wr.writerow(["N",N])
			wr.writerow(["Design_p",design_p])
			wr.writerow(["Runsim",runsim])
			for r in Ratelist:
				for p in range(2):
					Detdict=dd.load_Detdict("./simresults/"+Detdictfiledict[r][p])
					(Tlist,prob_detmatch)=dd.prob_detmatch(Detdict,runsim)
					print prob_detmatch,Tlist
					if p==0:
						wr.writerow(["Rate",r])
						wr.writerow(["Repeat"]+Tlist)
					
					wr.writerow(["ch_p="+str(channel_plist[p])]+[prob_detmatch[T] for T in Tlist])
					
					
	#~ print prob_detmatch


		#~ wr.writerow(["Sent"]+["Decoded"]+["DetectionKey"]+["Detectionbits"])
		#~ for sim in range(runsim):	
		#~ wr.writerow([str('"')+Detdictcsv[str(T)][sim][0]+str('"')]+[str('"')+Detdictcsv[str(T)][sim][1]+str('"')]+[str('"')+Detdictcsv[str(T)][sim][2]+str('"')]+[str('"')+Detdictcsv[str(T)][sim][3]+str('"')])
#~ return fname+".txt"
			

