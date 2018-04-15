#-------------------------------------------------------------------------------
# Name:       simulation for polar file 
# Purpose:    X is sent over channel
#             X is inverse arikan transformed to get U
#             good channels are known
#             Y received and decoded using above knowledge
#             final U is arikan transformed to get X
#
#              simulation done for given p and different rates <= C
#              Note the rate achieved for 1e-6 tolerable error can be 
#              found from polarfilesim files
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
import polarfile as pf
#=================================================================simulation		
#------------Number of good channels = capacity
Nlist=[4096]
design_plist=[0.1]
Rate=[0.1,0.2,0.3,0.5]

Ratelist=np.arange(0.1,0.6,0.05) #using ZCK

FER_dict={}


runsim=10000

#tolerable_error= -6 #using ZCL for channel


#runsim=5*10**6


for N in Nlist:
	for design_p in design_plist:
		C=pl.CapacityBSC(N,design_p)
		stamp=datetime.now().strftime("%d-%m-%y_%H-%M-%S")
		#f1=open("/home/soumya/Project/code/Polar-slepian/V_5/simresults/polarchannel_FERvsR_"+str(N)+"_"+str(design_p)+"_"+stamp+".txt",'w')
		f1=open("./simresults/polarFile_FERvsR_"+str(N)+"_"+str(design_p)+"_"+stamp+".txt",'w')
			
		print "RATE Vs FER REPORT FOR FILE TX"
		print "---------------------------"
		print "N="+str(N)
		print "p_design="+str(design_p)
		print "capacity*N:"+str(C)
		print "sim ran :"+str(runsim)
		
		json.dump( "RATE Vs FER REPORT FOR FILE TX",f1) ;f1.write("\n")
		json.dump( "---------------------------",f1) ;f1.write("\n")
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
		
		for R in Ratelist:
			if R<=(C/N):
				
				
				K=int(R*N)
				I=I_order[:K]
									
				block_error=pf.polarfilesim(N,design_p,design_p,I,runsim,False)
				
				
				
				used_rate.append(float(K)/N)
				FER.append(block_error)
		
		block_error_exp=np.log10(FER).tolist()	    
		#FER_dict[N]=(used_rate,block_error_exp)
		print used_rate
		print block_error_exp
		json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
		
		json.dump(used_rate,f1) ;f1.write("\n")
		json.dump(block_error_exp,f1) ;f1.write("\n")
