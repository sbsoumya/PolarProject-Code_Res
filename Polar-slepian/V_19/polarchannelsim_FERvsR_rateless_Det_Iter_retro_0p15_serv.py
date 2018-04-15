#-------------------------------------------------------------------------------
# Name:       polarchannelsim_FERvsR_derate_rateless_Det.py
# Purpose:    FER VS R simulation for given P and different rates
#             for rateless
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
channel_plist=[0.15]
compound_plist=[0.04,0.15,0.2,0.25]
T=20
msg_lengthlist=range(50,600,50)

runsim=100000

for N in Nlist:
	for channel_p in channel_plist:
		C=pl.CapacityBSC(N,channel_p)
		stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
		f1=open("./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro"+str(N)+"_"+str(channel_p)+"_"+stamp+".txt",'w')
			
		print "RATE Vs FER REPORT Rateless Det Iter retro"
		print "------------------------------------------"
		print "N="+str(N)
		print "Compound_plist:"
		print compound_plist
		print "p_channel="+str(channel_p)
		print "capacity*N:"+str(C)
		print "sim ran :"+str(runsim)
		print "T:"+str(T)
	
		
		json.dump( "RATE Vs FER REPORT Rateless Det Iter retro",f1) ;f1.write("\n")
		json.dump( "--------------------------------------------",f1) ;f1.write("\n")
		json.dump( "N="+str(N),f1) ;f1.write("\n")
		json.dump( "p_channel="+str(channel_p),f1) ;f1.write("\n")
		json.dump( "capacity*N:"+str(C),f1) ;f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		json.dump("T:"+str(T),f1);f1.write("\n")
		json.dump( "Compound_plist:",f1) ;f1.write("\n")
		json.dump(compound_plist,f1) ;f1.write("\n")
		
		used_rate=[];
		achieved_rate=[]
		FER=[];
		Iter_problist=[]
	
		for msg_length in msg_lengthlist:
			print "msg_length:"+str(msg_length)
			
			(u_rate,ach_rate,block_error,Iter_probdict)=rlc.send_rateless_det_Iter_retro_sim(N,T,compound_plist,channel_p,msg_length,runsim)
		
				
			used_rate.append(u_rate)
			achieved_rate.append(ach_rate)
			FER.append(block_error)
			Iter_problist.append(Iter_probdict)
		
		block_error_exp=np.log10(FER).tolist()	    
		
		print used_rate
		print achieved_rate
		print block_error_exp
		print Iter_problist
		
		json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
		json.dump(msg_lengthlist,f1) ;f1.write("\n")
		json.dump(used_rate,f1) ;f1.write("\n")
		json.dump(achieved_rate,f1) ;f1.write("\n")
		json.dump(block_error_exp,f1) ;f1.write("\n")
		
		json.dump( "Iter Probabilities=",f1) ;f1.write("\n")
		json.dump(Iter_problist,f1) ;f1.write("\n")
		end = timer()
		TC=(end-start)

		print "Time taken:"+str(TC)	
		json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
			
			

		    




