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
start = timer()
Nlist=[512]
N=Nlist[0]
channel_plist=list(np.linspace(0.01,0.2,20))
design_plist=channel_plist
L=np.log10(0.05)
Rlist=[len(pcon.getGChZCL(p,N,L)[0]) for p in design_plist]
print Rlist
print design_plist

runsim=10

start=timer()

stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
filename="./simresults/polarchannel_FERvsp_FR"+str(L).replace(".","e")+"in"+str(N)+"_"+stamp+".txt"
f1=open(filename,'w')
print filename
print "P Vs FER REPORT derate"
print "---------------------------"
print "N="+str(N)
print "sim ran :"+str(runsim)

		
json.dump( "P Vs FER REPORT derate",f1) ;f1.write("\n")
json.dump( "---------------------------",f1) ;f1.write("\n")
json.dump( "N="+str(N),f1) ;f1.write("\n")
json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")		
	

FER=[];
start=timer()
for i in range(len(design_plist)):
	print design_plist[i];
	print Rlist[i]
	block_error=pch.polarchannelsim_FR(N,design_plist[i],design_plist[i],Rlist[i],runsim,False)
	#~ if block_error==0:
		#block_error=pch.polarchannelsim_FR(N,design_p,design_p,msg_length,runsim,False)
	
	
	FER.append(block_error)
	    
print "Z max :"+str(L)
block_error_exp=np.log10(FER).tolist()	
print design_plist
print Rlist
print block_error_exp
		
json.dump("Z max :"+str(L),f1) ;f1.write("\n")
json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
json.dump(design_plist,f1) ;f1.write("\n")
json.dump(Rlist,f1) ;f1.write("\n")
json.dump(block_error_exp,f1) ;f1.write("\n")	


end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
				

		    




