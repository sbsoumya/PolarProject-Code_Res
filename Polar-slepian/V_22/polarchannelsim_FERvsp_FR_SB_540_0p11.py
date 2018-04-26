#-------------------------------------------------------------------------------
# Name:       polarchannelsim_FERvsR_derate.py
# Purpose:    FER VS R simulation for given code and different rates
#             p
# Author:      soumya
#
# Created:     19/08/2017
#----------------------------------------

import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
import polarconstruct as pcon
from datetime import datetime
import json
import polarchannel as pch
from pprint import pprint
from timeit import default_timer as timer

#=================================================================simulation		
#------------Number of good channels = capacity
N=1024

# parameters from rateless for reference
compound_plist=[0.08349999999999963, 0.19249999999999973, 0.24549999999999977, 0.2784999999999998, 0.3009999999999998]
#compoundcap=[600, 300, 200, 150, 120]
#~ [540.0, 270.0, 180.0, 135.0, 108.0]
#~ [0.10099999999999965, 0.20699999999999974, 0.2579999999999998, 0.2894999999999998, 0.31099999999999983]
#~ [508, 238, 148, 103, 76]

design_p=0.03
channel_p=0.03
R_p=510
Tlist=[1,2,4,8,16,32,64,128]
runsim=10000
runsimhigh=100000

stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
filename="./simresults/polarchannel_FERvsp_FRSB"+str(channel_p).replace(".","p")+"_"+str(R_p1)+"in"+str(N)+"_"+stamp+".txt"
f1=open(filename,'w')
print filename
print "P Vs FER REPORT derate"
print "---------------------------"
print "N="+str(N)
print "sim ran :"+str(runsim)
print "R_p1:"+str(R_p1)
		
json.dump( "P Vs FER REPORT derate",f1) ;f1.write("\n")
json.dump( "---------------------------",f1) ;f1.write("\n")
json.dump( "N="+str(N),f1) ;f1.write("\n")
json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")		
json.dump("R_p1:"+str(R_p1),f1) ;f1.write("\n")		

FER=[];
start=timer()
for T in Tlist:
	print T,channel_p
	block_error=pch.polarchannelsim_FR_SB(N,channel_p,design_p,R_p1,runsim,T,False)
	#~ if block_error==0:
		#block_error=pch.polarchannelsim_FR(N,design_p,design_p,R_p1,runsim,False)
	
	
	FER.append(block_error)
	    

block_error_exp=np.log10(FER).tolist()	
correctness=[1-er for er in FER]
print design_p
print channel_p
print Tlist
print block_error_exp
print correctness
		
json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
json.dump(design_p,f1) ;f1.write("\n")
json.dump(channel_p,f1) ;f1.write("\n")
json.dump(Tlist,f1) ;f1.write("\n")
json.dump(block_error_exp,f1) ;f1.write("\n")	
json.dump(correctness,f1) ;f1.write("\n")	


end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
				

		    




