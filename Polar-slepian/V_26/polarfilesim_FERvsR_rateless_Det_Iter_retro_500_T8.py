#-------------------------------------------------------------------------------
# Name:       polarfilesim_FERvsR_rateless_det_Iterretro.py
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
import polarfile as pch
from pprint import pprint
import rateless_file_det as rlf
from timeit import default_timer as timer
#=================================================================simulation		
#------------Number of good channels = capacity
start = timer()
Nlist=[1024] #keep this singleton
channel_plist=list(np.linspace(0.05,0.45,10))
compound_plist=[0.044499999999999595, 0.1584999999999997, 0.21649999999999975, 0.2524999999999998, 0.2774999999999998]
#[756, 378, 252, 151]
T=8
F_p1=500
R_p1=Nlist[0]-F_p1
error_free_msg_length=F_p1+T
runsim=10000

start=timer()
for N in Nlist:
	
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	filename="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_"+str(error_free_msg_length)+"in"+str(N)+"_T"+str(T)+"_"+stamp+".txt"
	f1=open(filename,'w')
	print filename
	print "RATE Vs FER REPORT Rateless Det Iter retro"
	print "------------------------------------------"
	print "Compound_plist:"
	print compound_plist
	print "sim ran :"+str(runsim)
	print "T:"+str(T)
		
	json.dump( "RATE Vs FER REPORT Rateless Det Iter retro",f1) ;f1.write("\n")
	json.dump( "------------------------------------------",f1) ;f1.write("\n")
	json.dump( "Compound_plist:",f1) ;f1.write("\n")
	json.dump(compound_plist,f1) ;f1.write("\n")
	json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
	json.dump("T:"+str(T),f1);f1.write("\n")
		
	print "N="+str(N)
	json.dump( "N="+str(N),f1) ;f1.write("\n")
	
	used_rate=[];
	achieved_rate=[]
	FER=[];
	Iter_problist=[]
	
	for channel_p in channel_plist:
		#print "channel_p:"+str(channel_p)
		(u_rate,ach_rate,block_error,Iter_probdict)=rlf.send_rateless_file_Iter_retro_det_sim(N,T,compound_plist,channel_p,error_free_msg_length,runsim)
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
			

		    




