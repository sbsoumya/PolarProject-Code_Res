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
Nlist=[128]
p=0.1
Rate=[0.1,0.2,0.3,0.5]

#tolerable_error= -6 #using ZCL for channel


runsim=5*10**6


for N in Nlist:
	for R in Rate:
		K=int(R*N) 
		stamp=datetime.now().strftime("%d-%m-%y_%H-%M-%S")
		f1=open("./simresults/polarfileR_"+str(R)+"_"+str(N)+"_"+str(p)+"_"+stamp+".txt",'w')
			
		print "MONTE _CARLO FILE REPORT"
		print "---------------------------"
		print "N="+str(N)
		print "p="+str(p)
		print "RequiredRate="+str(R)
		print "sim ran :"+str(runsim)

			
		json.dump( "MONTE _CARLO FILE REPORT",f1) ;f1.write("\n")
		json.dump( "---------------------------",f1) ;f1.write("\n")
		json.dump( "N="+str(N),f1) ;f1.write("\n")
		json.dump( "p="+str(p),f1) ;f1.write("\n")
		json.dump( "Rate="+str(R),f1) ;f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		
		
		
		#-----------------------------------------ZC
		try:
			I=pcon.getGCHsim('ZK',N,p,K)
		except:
		   (I,E)=pcon.getGChZCK(p,N,K)
		   
		print "Good Channels:"
		print I
		aR=float(len(I))/N
		print "Achieved Rate="+str(aR)
		print "Frozen channels:"
		B=list(set(range(N))-set(I))
		print len(B)
		
		json.dump( "Good Channels:",f1) ;f1.write("\n")
		json.dump( I,f1) ;f1.write("\n")
		json.dump( "Achieved ="+str(aR),f1) ;f1.write("\n")
		json.dump( "Frozen channels:",f1) ;f1.write("\n")
		json.dump( len(B),f1) ;f1.write("\n")
		
		
		(ber_exp,block_error)=pf.polarfilesim(N,p,p,I,runsim)
			
		print ber_exp
		print block_error
		
		json.dump( "block_error="+str(block_error),f1) ;f1.write("\n")
		json.dump( "BER channelwise:",f1) ;f1.write("\n")
		json.dump( ber_exp,f1) ;f1.write("\n")
		    





