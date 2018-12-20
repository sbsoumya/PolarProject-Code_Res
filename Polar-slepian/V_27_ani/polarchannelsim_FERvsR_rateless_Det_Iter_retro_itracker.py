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
channel_plist=list(np.linspace(0.05,0.45,10))
compound_plist=[0.08349999999999963, 0.19249999999999973, 0.24549999999999977, 0.2784999999999998, 0.3009999999999998]
compoundcap=[600, 300, 200, 150, 120]
T=8
R_p1high=601
R_p1low=100
msg_lengthhigh=R_p1high-T
msg_lengthlow=R_p1low-T
step=50
runsim=10000

start=timer()
for N in Nlist:
	
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	filename="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_itracker"+str(N)+"_T"+str(T)+"_"+stamp+".txt"
	f1=open(filename,'w')
	print filename
	
	print "RATE Vs FER REPORT Rateless Det Iter retro"
	print "------------------------------------------"
	print "Compound_plist and their capacities:"
	print compound_plist
	print compoundcap
	print "sim ran :"+str(runsim)
	print "T:"+str(T)
	print "Rp1high:"+str(R_p1high)
	print "Rp1low:"+str(R_p1low)
	print "step:"+str(step)
		
	json.dump( "RATE Vs FER REPORT Rateless Det Iter retro",f1) ;f1.write("\n")
	json.dump( "------------------------------------------",f1) ;f1.write("\n")
	json.dump( "Compound_plist:",f1) ;f1.write("\n")
	json.dump(compound_plist,f1) ;f1.write("\n")
	json.dump(compoundcap,f1) ;f1.write("\n")
	json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
	json.dump("T:"+str(T),f1);f1.write("\n")
	json.dump("Rp1high:"+str(R_p1high),f1);f1.write("\n")
	json.dump("Rp1low:"+str(R_p1low),f1);f1.write("\n")
	json.dump("step:"+str(step),f1);f1.write("\n")
		
	print "N="+str(N)
	json.dump( "N="+str(N),f1) ;f1.write("\n")
	

	achieved_rate=[]
	FER=[];
	
	
	for channel_p in channel_plist:
		#print "channel_p:"+str(channel_p)
		(ach_rate,block_error)=rlc.send_rateless_det_Iter_retro_itracker_sim(N,T,compound_plist,channel_p,msg_lengthhigh,msg_lengthlow,step,runsim)
		achieved_rate.append(ach_rate)
		FER.append(block_error)
		

block_error_exp=np.log10(FER).tolist()	    
print channel_plist
print achieved_rate
print block_error_exp

		
json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
json.dump(channel_plist,f1) ;f1.write("\n")
json.dump(achieved_rate,f1) ;f1.write("\n")
json.dump(block_error_exp,f1) ;f1.write("\n")


end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
			

		    




