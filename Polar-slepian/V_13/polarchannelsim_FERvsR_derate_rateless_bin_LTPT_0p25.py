#-------------------------------------------------------------------------------
# Name:       polarchannelsim_FERvsR_derate_rateless_LTPT.py
# Purpose:    FER VS R simulation for given P and different rates
#             for rateless with BINNING
#             IN BINNING
#             all achieved rates and error cnt for a given sent rate in NOT averaged
#             achieved rates are are  
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

#=================================================================simulation		
#------------Number of good channels = capacity
Nlist=[1024]
#Nlist=[2048]
#Nlist=[4096]
channel_plist=[0.25]
compound_plist=[0.04,0.15,0.2,0.25]
LTPTdict={'0.04':[30,71],'0.15':[30,50.5],'0.2':[30,44],'0.25':[0,0]}
design_p=0.04
deratelist=np.arange(0.1,1.1,0.1) #using ZCK

FER_dict={}


runsim=10000

for N in Nlist:
	for channel_p in channel_plist:
		C=pl.CapacityBSC(N,design_p)
		stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
		f1=open("./simresults/polarchannel_FERvsR_derate_rateless_bin_LTPT"+str(N)+"_"+str(channel_p)+"_"+stamp+".txt",'w')
			
		print "RATE Vs FER REPORT Rateless LTPT"
		print "--------------------------------"
		print "N="+str(N)
		print "p_design="+str(design_p)
		print "p_channel="+str(channel_p)
		print "capacity*N:"+str(C)
		print "sim ran :"+str(runsim)
		print "LTPT:"
		pprint(LTPTdict)
		
		json.dump( "RATE Vs FER REPORT Rateless LTPT",f1) ;f1.write("\n")
		json.dump( "--------------------------------",f1) ;f1.write("\n")
		json.dump( "N="+str(N),f1) ;f1.write("\n")
		json.dump( "p_design="+str(design_p),f1) ;f1.write("\n")
		json.dump( "p_channel="+str(channel_p),f1) ;f1.write("\n")
		json.dump( "capacity*N:"+str(C),f1) ;f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		json.dump("LTPTdict:",f1) ;f1.write("\n")
		json.dump(LTPTdict,f1);f1.write("\n")
		
		try:
			I_order=pcon.getGCHsim('ZK',N,design_p,N)
		except:
			(I_order,E)=pcon.getGChZCK(design_p,N,N)			
		
		ERR_DICT={}
		DP=2
		#derate * capacity of design_p is used as rate
		for derate in deratelist:
			ERR_DICT=rlc.send_rateless_LTPT_sim_bin(ERR_DICT,DP,N,compound_plist,channel_p,derate,LTPTdict,runsim)
		
		achieved_rate=[float(key) for key in ERR_DICT.keys()]
		achieved_rate.sort()
		FER=[]
		for ar in achieved_rate:
			r=format(ar,'.'+str(DP)+'f')
			FER.append(float(ERR_DICT[r][1])/ERR_DICT[r][0])
				
		block_error_exp=np.log10(FER).tolist()	    
		#FER_dict[N]=(used_rate,block_error_exp)
		print achieved_rate
		print block_error_exp
		
		json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
		
		#json.dump(used_rate,f1) ;
		f1.write("\n")
		json.dump(achieved_rate,f1) ;f1.write("\n")
		json.dump(block_error_exp,f1) ;f1.write("\n")
		json.dump(ERR_DICT,f1) ;f1.write("\n")
		

			

		    




