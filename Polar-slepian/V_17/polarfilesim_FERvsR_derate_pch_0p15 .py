#-------------------------------------------------------------------------------
# Name:       polarfilesim_FERvsR_derate_pch.py
# Purpose:    FER VS R simulation for given P and different rates
#             uses polar channel sim , derate is done in caller
# Author:      soumya
#
# Created:     2/1/2018
#----------------------------------------

import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
import polarconstruct as pcon
from datetime import datetime
import json
import polarfile as pf
from pprint import pprint

#=================================================================simulation		
#------------Number of good channels = capacity
Nlist=[1024]
#Nlist=[2048]
#Nlist=[4096]
design_plist=[0.15]#,0.15,0.2,0.25]
deratelist=np.arange(0.1,1.1,0.1) #using ZCK

FER_dict={}


runsim=100000

for N in Nlist:
	for design_p in design_plist:
		C=pl.CapacityBSC(N,design_p)
		stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
		f1=open("./simresults/polarFile_FERvsR_"+str(N)+"_"+str(design_p)+"_"+stamp+".txt",'w')
			
		print "RATE Vs FER REPORT FILE"
		print "-----------------------------"
		print "N="+str(N)
		print "p_design="+str(design_p)
		print "capacity*N:"+str(C)
		print "sim ran :"+str(runsim)
		
		json.dump( "RATE Vs FER REPORT FILE",f1) ;f1.write("\n")
		json.dump( "-----------------------------",f1) ;f1.write("\n")
		json.dump( "N="+str(N),f1) ;f1.write("\n")
		json.dump( "p_decode="+str(design_p),f1) ;f1.write("\n")
		json.dump( "capacity*N:"+str(C),f1) ;f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		
		try:
			I_order=pcon.getGCHsim('ZK',N,design_p,N)
		except:
			(I_order,E)=pcon.getGChZCK(design_p,N,N)			
		
		used_rate=[];
		FER=[];
		Ratelist=[i*float(C)/N for i in deratelist]
		for R in Ratelist:
			if R<=(C/N):
				
				
				K=int(R*N)
				I=I_order[:K]
				#print R					
				block_error=pf.polarfilesim(N,design_p,design_p,I,runsim,False)
				used_rate.append(R)
				FER.append(block_error)

		
		block_error_exp=np.log10(FER).tolist()	    
		#FER_dict[N]=(used_rate,block_error_exp)
		print used_rate
		print block_error_exp
		json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
		
		json.dump(used_rate,f1) ;f1.write("\n")
		json.dump(block_error_exp,f1) ;f1.write("\n")

			

		    




