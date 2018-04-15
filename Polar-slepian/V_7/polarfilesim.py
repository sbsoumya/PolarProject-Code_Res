#-------------------------------------------------------------------------------
# Name:       simulation for polar file 
# Purpose:    X is sent over channel
#             X is inverse arikan transformed to get U
#             good channels are known
#             Y received and decoded using above knowledge
#             final U is arikan transformed to get X
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
import polarfile as pf
#=================================================================simulation		
#------------Number of good channels = capacity
Nlist=[128,1024]
design_plist=[0.1,0.2]
psteps=0.02

tolerable_error= -6 #using ZCL for channel


runsim=5*10**6


for N in Nlist:
	for design_p in design_plist:
		p=0
		stamp=datetime.now().strftime("%d-%m-%y_%H-%M-%S")
		f1=open("./simresults/polarfile_"+str(N)+"_"+str(design_p)+"_"+stamp+".txt",'w')
			
		print "MONTE _CARLO FILE REPORT"
		print "---------------------------"
		print "N="+str(N)
		print "p_decode="+str(design_p)
		print "tolerable error exponent:"+str(tolerable_error)# channels selected as per this
		print "sim ran :"+str(runsim)
		
		json.dump( "MONTE _CARLO FILE REPORT",f1) ;f1.write("\n")
		json.dump( "---------------------------",f1) ;f1.write("\n")
		json.dump( "N="+str(N),f1) ;f1.write("\n")
		json.dump( "p_decode="+str(design_p),f1) ;f1.write("\n")
		json.dump( "tolerable error exponent:"+str(tolerable_error),f1) ;f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		
		
		
		#-----------------------------------------ZC
		try:
			I=pcon.getGCHsim('ZL',N,design_p,tolerable_error)
		except:
		   (I,E)=pcon.getGChZCL(design_p,N,tolerable_error)
		   
		print "Good Channels:"
		print I
		R=float(len(I))/N
		print "R="+str(R)
		print "Frozen channels:"
		B=list(set(range(N))-set(I))
		print len(B)
		
		json.dump( "Good Channels:",f1) ;f1.write("\n")
		json.dump( I,f1) ;f1.write("\n")
		json.dump( "R="+str(R),f1) ;f1.write("\n")
		json.dump( "Frozen channels:",f1) ;f1.write("\n")
		json.dump( len(B),f1) ;f1.write("\n")
		
		
		
		
		
		while  p<design_p:
			p+=psteps
			json.dump( "p_channel="+str(p),f1) ;f1.write("\n")
			print "p_channel="+str(p)
			
			
			(ber_exp,block_error)=pf.polarfilesim(N,p,design_p,I,runsim)
			
			
			print "block_error="+str(block_error)
								
			json.dump( "block_error="+str(block_error),f1) ;f1.write("\n")
			json.dump( "BER channelwise:",f1) ;f1.write("\n")
			json.dump(ber_exp,f1) ;f1.write("\n")
		    





