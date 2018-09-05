#-------------------------------------------------------------------------------
# Name:       polarchannelsim_FERvsR_rateless_det_Iterretro.py
# Purpose:    FER VS R simulation for given msg_length and varying channel
#
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
import rateless_channel as rlc
from timeit import default_timer as timer
#=================================================================simulation		
#------------Number of good channels = capacity
start = timer()
Nlist=[2048]
channel_plist=list(np.linspace(0.01,0.2,20))
print channel_plist
compound_plist=[0.03,0.11,0.17]
compoundcap=[pl.CapacityBSC(Nlist[0],p) for p in channel_plist]
R_p1=1020
msg_length=R_p1
runsim=1000

LTPTdict={'0.03':[40,80],'0.11':[30,80],'0.17':[0,0]}

start=timer()
for N in Nlist:
	
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	filename="./simresults/polarchannel_FERvsR_rateless_Det_LTPT_"+str(R_p1)+"in"+str(N)+"_"+stamp+".txt"
	f1=open(filename,'w')
	print filename
	print "RATE Vs FER REPORT Rateless LTPT"
	print "------------------------------------------"
	print "Compound_plist and their capacities:"
	print compound_plist
	print compoundcap
	print "sim ran :"+str(runsim)
	print "LTPT:"
	pprint(LTPTdict)
		
	json.dump( "RATE Vs FER REPORT Rateless LTPT",f1) ;f1.write("\n")
	json.dump( "------------------------------------------",f1) ;f1.write("\n")
	json.dump( "Compound_plist:",f1) ;f1.write("\n")
	json.dump(compound_plist,f1) ;f1.write("\n")
	json.dump(compoundcap,f1) ;f1.write("\n")
	json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
	json.dump("LTPTdict:",f1) ;f1.write("\n")
	json.dump(LTPTdict,f1);f1.write("\n")
		
	print "N="+str(N)
	json.dump( "N="+str(N),f1) ;f1.write("\n")
	
	used_rate=[];
	achieved_rate=[]
	FER=[];
	Iter_problist=[]
	
	for channel_p in channel_plist:
		#print "channel_p:"+str(channel_p)
		(u_rate,ach_rate,block_error,Iter_probdict)=rlc.send_rateless_LTPT_new_sim(N,LTPTdict,compound_plist,channel_p,msg_length,runsim)
		used_rate.append(u_rate)
		achieved_rate.append(ach_rate)
		FER.append(block_error)
		Iter_problist.append(Iter_probdict)

block_error_exp=np.log10(FER).tolist()	    
print channel_plist
print achieved_rate
print block_error_exp
print Iter_problist
		
json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
json.dump(channel_plist,f1) ;f1.write("\n")
json.dump(achieved_rate,f1) ;f1.write("\n")
json.dump(block_error_exp,f1) ;f1.write("\n")
json.dump( "Iter Probabilities=",f1) ;f1.write("\n")
json.dump(Iter_problist,f1) ;f1.write("\n")

end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
			

		    




