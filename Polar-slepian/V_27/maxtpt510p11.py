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
import rateless_channel_det as rlc
from timeit import default_timer as timer
#=================================================================simulation		
#------------Number of good channels = capacity
start = timer()
Nlist=[1024]
channel_p=0.11
compound_plist=[0.03,0.11,0.17] #restriction
compoundcap=[pl.CapacityBSC(Nlist[0],p) for p in compound_plist]
maxiters=len(compound_plist)
NR_p1=510
NR_p2=510/2
NR_p3=510/3
Tlist=list(np.arange(1,NR_p2-NR_p3,2))
R_p1=510
runsim=1000

start=timer()
for N in Nlist:
	
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	filename="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt"+str(R_p1)+"in"+str(N)+"_c"+str(channel_p).replace(".","p")+"_"+stamp+".txt"
	f1=open(filename,'w')
	print filename
	
	print "RATE Vs FER REPORT Rateless Det Iter retro"
	print "------------------------------------------"
	print "Compound_plist and their capacities:"
	print compound_plist
	print compoundcap
	print "sim ran :"+str(runsim)
	#print "T:"+str(T)
		
	json.dump( "RATE Vs FER REPORT Rateless Det Iter retro",f1) ;f1.write("\n")
	json.dump( "------------------------------------------",f1) ;f1.write("\n")
	json.dump( "Compound_plist:",f1) ;f1.write("\n")
	json.dump(compound_plist,f1) ;f1.write("\n")
	json.dump(compoundcap,f1) ;f1.write("\n")
	json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
	#json.dump("T:"+str(T),f1);f1.write("\n")
		
	print "N="+str(N)
	json.dump( "N="+str(N),f1) ;f1.write("\n")
	
	used_rate=[];
	achieved_rate=[]
	FER=[];
	Iter_problist=[]
	
	for T in Tlist:
		msg_length=R_p1-T
		print "T:"+str(T)
		(u_rate,ach_rate,block_error,Iter_probdict)=rlc.send_rateless_det_Iter_retro_sim(N,T,compound_plist,channel_p,msg_length,runsim)
		used_rate.append(u_rate)
		achieved_rate.append(ach_rate)
		FER.append(block_error)
		Iter_problist.append(Iter_probdict)


block_error_exp=np.log10(FER).tolist()	    
print channel_p
print Tlist
print achieved_rate
print block_error_exp
print Iter_problist
MeanIters=pl.getMeanIter(Iter_problist,maxiters)
tpt=[float(R_p1-Tlist[i])/(MeanIters[i]*N)*(1-10**block_error_exp[i]) for i in range(len(Tlist))]
print tpt		
json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
json.dump(channel_p,f1) ;f1.write("\n")
json.dump(Tlist,f1) ;f1.write("\n")
json.dump(achieved_rate,f1) ;f1.write("\n")
json.dump(block_error_exp,f1) ;f1.write("\n")
json.dump( "Iter Probabilities=",f1) ;f1.write("\n")
json.dump(Iter_problist,f1) ;f1.write("\n")
json.dump(tpt,f1);f1.write("\n")

end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
			

		    




