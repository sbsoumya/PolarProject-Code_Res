#-------------------------------------------------------------------------------
# Name:       simulation for polar channel
# Purpose:    U is msg
#             X is code
#             good channels are known
#             Y received and decoded using above knowledge
#             U_decoded is decoded and compared with U
#
#              simulation done for given p and a set of better channels
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
import matplotlib.pyplot as plt

#=================================================================simulation		
#------------Number of good channels = capacity
Nlist=[128,1024]
channel_plist=[0.1]
channel_p=channel_plist[0] #this is a rate based design, so design_p is not used and channel_p is used for decoding
Ratelist=np.arange(0.1,0.6,0.05) #using ZCK

FER_dict={}


runsim=10

for N in Nlist:
	
	C=pl.CapacityBSC(N,channel_p)
	stamp=datetime.now().strftime("%d-%m-%y_%H-%M-%S")
	f1=open("./simresults/polarchannel_FERvsR_"+str(N)+"_"+str(channel_p)+"_"+stamp+".txt",'w')
			
	print "RATE Vs FER REPORT"
	print "---------------------------"
	print "N="+str(N)
	print "p_channel="+str(channel_p)
	print "capacity*N:"+str(C)
	print "sim ran :"+str(runsim)
	
	json.dump( "RATE Vs FER REPORT",f1) ;f1.write("\n")
	json.dump( "---------------------------",f1) ;f1.write("\n")
	json.dump( "N="+str(N),f1) ;f1.write("\n")
	json.dump( "p_decode="+str(channel_p),f1) ;f1.write("\n")
	json.dump( "capacity*N:"+str(C),f1) ;f1.write("\n")
	json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		
	try:
		I_order=pcon.getGCHsim('ZK',N,channel_p,N)
	except:
		(I_order,E)=pcon.getGChZCK(channel_p,N,N)			
		
	used_rate=[];
	FER=[];
	for R in Ratelist:
		if R<=(C/N):
			
				
			K=int(R*N)
			I=I_order[:K]
								
			block_error=pch.polarchannelsim(N,channel_p,I,runsim,False)
			
			used_rate.append(float(K)/N)
			FER.append(block_error)
	
	block_error_exp=np.log10(FER).tolist()	    
	#FER_dict[N]=(used_rate,block_error_exp)
	print used_rate
	print block_error_exp
	json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
	
	json.dump(used_rate,f1) ;f1.write("\n")
	json.dump(block_error_exp,f1) ;f1.write("\n")

			

		    




