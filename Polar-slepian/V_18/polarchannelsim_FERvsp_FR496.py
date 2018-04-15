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
#~ [496, 430, 364, 298, 232]
#~ [0.10499999999999965, 0.12699999999999967, 0.1509999999999997, 0.17849999999999971, 0.20999999999999974]
#~ 66

design_plist=list(np.linspace(0.01,0.12,8))
msg_length=496

runsim=10000
runsimhigh=100000

stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
filename="./simresults/polarchannel_FERvsp_FR"+str(msg_length)+"in"+str(N)+"_"+stamp+".txt"
f1=open(filename,'w')
print filename
print "P Vs FER REPORT derate"
print "---------------------------"
print "N="+str(N)
print "sim ran :"+str(runsim)
print "msg_length:"+str(msg_length)
		
json.dump( "P Vs FER REPORT derate",f1) ;f1.write("\n")
json.dump( "---------------------------",f1) ;f1.write("\n")
json.dump( "N="+str(N),f1) ;f1.write("\n")
json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")		
json.dump("msg_length:"+str(msg_length),f1) ;f1.write("\n")		

FER=[];
start=timer()
for design_p in design_plist:
	print design_p
	block_error=pch.polarchannelsim_FR(N,design_p,design_p,msg_length,runsim,False)
	#~ if block_error==0:
		#block_error=pch.polarchannelsim_FR(N,design_p,design_p,msg_length,runsim,False)
	
	
	FER.append(block_error)
	    

block_error_exp=np.log10(FER).tolist()	
print design_plist
print block_error_exp
		
json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
json.dump(design_plist,f1) ;f1.write("\n")
json.dump(block_error_exp,f1) ;f1.write("\n")	


end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
				

		    




