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
N=512

design_plist=list(np.linspace(0.01,0.2,10))
msg_length=256
L=4
runsim=100
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
print "L:"+str(L)
		
json.dump( "P Vs FER REPORT derate",f1) ;f1.write("\n")
json.dump( "---------------------------",f1) ;f1.write("\n")
json.dump( "N="+str(N),f1) ;f1.write("\n")
json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")		
json.dump("msg_length:"+str(msg_length),f1) ;f1.write("\n")	
json.dump("L:"+str(L),f1) ;f1.write("\n")		

FER=[];
FERL=[];
start=timer()
for design_p in design_plist:
	print design_p
	block_error=pch.polarchannelsim_FR(N,design_p,design_p,msg_length,runsim,False)
	#~ if block_error==0:
		#block_error=pch.polarchannelsim_FR(N,design_p,design_p,msg_length,runsim,False)
	block_errorL=pch.polarchannelsim_FR_list(N,design_p,design_p,msg_length,runsim,False,L)
	
	
	FER.append(block_error)
	FERL.append(block_errorL)
block_error_exp=np.log10(FER).tolist()
block_error_expL=np.log10(FERL).tolist()
	
print design_plist
print block_error_exp
print block_error_expL
		
json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
json.dump(design_plist,f1) ;f1.write("\n")
json.dump(block_error_exp,f1) ;f1.write("\n")	
json.dump(block_error_expL,f1) ;f1.write("\n")	


end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
				

		    




