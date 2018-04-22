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
import rateless_channel_det_maxiter as rlc
from timeit import default_timer as timer
#=================================================================simulation		
#------------Number of good channels = capacity
start = timer()
Nlist=[1024] #keep this singleton
compound_plist=[0.08349999999999963, 0.19249999999999973, 0.24549999999999977, 0.2784999999999998, 0.3009999999999998]
#[600, 300, 200, 150, 120]
#~ [540.0, 270.0, 180.0, 135.0, 108.0]
#~ [0.10099999999999965, 0.20699999999999974, 0.2579999999999998, 0.2894999999999998, 0.31099999999999983]
#~ [508, 238, 148, 103, 76]
doiter=2
channel_plist=list(np.linspace(0.1,0.2,10))
T=0
msg_length=540
runsim=10000
runsimhigh=100000

start=timer()
for N in Nlist:
	
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	filename="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_"+str(msg_length)+"in"+str(N)+"_T"+str(T)+"_doiter"+str(doiter)+"_"+stamp+".txt"
	f1=open(filename,'w')
	print filename
	print "RATE Vs FER REPORT Rateless Det Iter retro"
	print "------------------------------------------"
	print "Compound_plist:"
	print compound_plist
	print "sim ran :"+str(runsim)
	print "T:"+str(T)
	print "doiter:"+str(doiter)
		
	json.dump( "RATE Vs FER REPORT Rateless Det Iter delta",f1) ;f1.write("\n")
	json.dump( "------------------------------------------",f1) ;f1.write("\n")
	json.dump( "Compound_plist:",f1) ;f1.write("\n")
	json.dump(compound_plist,f1) ;f1.write("\n")
	json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
	json.dump("T:"+str(T),f1);f1.write("\n")
	json.dump("doiter:"+str(doiter),f1);f1.write("\n")
		
	print "N="+str(N)
	json.dump( "N="+str(N),f1) ;f1.write("\n")
	
	used_rate=[];
	achieved_rate=[]
	FER=[];
	Iter_problist=[]
	
	for channel_p in channel_plist:
		#print "channel_p:"+str(channel_p)
		(u_rate,ach_rate,block_error,Iter_probdict)=rlc.send_rateless_det_Iter_retro_doiter_sim(N,T,compound_plist,channel_p,msg_length,doiter,runsim)
		used_rate.append(u_rate)
		#~ if block_error==0:
			#~ (u_rate,ach_rate,block_error,Iter_probdict)=rlc.send_rateless_det_Iter_retro_doiter_sim(N,T,compound_plist,channel_p,msg_length,doiter,runsimhigh)
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
			

		    




