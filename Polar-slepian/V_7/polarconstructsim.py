#-------------------------------------------------------------------------------
# Name:       simulation for monte-carlo for charaterising channel/ code construction
# Purpose:    related to prob and channel
#
# Author:      soumya
#
# Created:     01/09/2017
#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
import polarconstruct as pcon
from datetime import datetime
import json



#------------Number of good channels = capacity
Nlist=[128,256,1024]
design_plist=[0.05,0.1,0.2]
K=5
tolerable_error= -5
runsim=(10**(-tolerable_error))*2

for N in Nlist:
	for p in design_plist:
	
		
		

		#runsim for K
		#runsim=1000

		#-----------------------
		stamp=datetime.now().strftime("%d-%y-%m_%H-%M-%S")
		f1=open("./simresults/polarconstruct"+stamp+".txt",'w')



		print "MONTE _CARLO CHANNEL REPORT"
		print "---------------------------"

		print "N="+str(N)
		print "p="+str(p)
		PotGCh=int(ma.floor(pl.CapacityBSC(N,p)))
		print "Capacity for "+str(N)+"channels:"+str(PotGCh)



		print "No of good channels needed :"+str(K)+"(valid if used)"
		print "tolerable error exponent:"+str(tolerable_error)
		#-----------------------------------------ZC
		(I,E)=pcon.getGChZCL(p,N,tolerable_error)
		#(I,E)=pcon.getGChZCK(p,N,K)
		print "Good Channels:"
		print I
		print "Corresponding Error Exponents:"
		print E
		print "Number of good channels:"
		print len(I)
		R=float(len(I))/N
		print "R="+str(R)
		print "Frozen channels:"
		B=list(set(range(N))-set(I))
		print len(B)

##########################################file
		json.dump( "MONTE _CARLO CHANNEL REPORT",f1) ;f1.write("\n")
		json.dump( "---------------------------",f1) ;f1.write("\n")
		json.dump( "N="+str(N),f1) ;f1.write("\n")
		json.dump( "p="+str(p),f1) ;f1.write("\n")
		json.dump( "Capacity for "+str(N)+"channels:"+str(PotGCh),f1) ;f1.write("\n")
		json.dump( "No of good channels needed :"+str(K)+"(valid if used)",f1) ;f1.write("\n")
		json.dump( "tolerable error exponent:"+str(tolerable_error),f1) ;f1.write("\n")
#-----------------------------------------ZC
		json.dump("Z Construct--------------------------------------------------------",f1);f1.write("\n")
		json.dump( "Good Channels:",f1) ;f1.write("\n")
		json.dump( I,f1) ;f1.write("\n")
		json.dump( "Corresponding Error Exponents:",f1) ;f1.write("\n")
		json.dump( E,f1) ;f1.write("\n")
		json.dump( "Number of good channels:",f1) ;f1.write("\n")
		json.dump( len(I),f1) ;f1.write("\n")
		json.dump( "R="+str(R),f1) ;f1.write("\n")
		json.dump( "Frozen channels:",f1) ;f1.write("\n")
		json.dump( len(B),f1) ;f1.write("\n")
		
	
		#-------------------------------------MC

		(I,E,FE)=pcon.getGChMCL(p,N,tolerable_error,runsim)
		#(I,E,FE)=pcon.getGChMCK(p,N,K,runsim)
		#print "sim ran :"+str(runsim)
		print "Good Channels:"
		print I
		print "Corresponding Error Exponents:"
		print E
		print "Number of good channels:"
		print len(I)
		R=float(len(I))/N
		print "R="+str(R)
		print "Frozen channels:"
		B=list(set(range(N))-set(I))
		print len(B)
		###################################file
		json.dump("Monte Carlo--------------------------------------------------------",f1);f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		json.dump( "Good Channels:",f1) ;f1.write("\n")
		json.dump( I,f1) ;f1.write("\n")
		json.dump( "Corresponding Error Exponents:",f1) ;f1.write("\n")
		json.dump( E,f1) ;f1.write("\n")
		json.dump( FE,f1);f1.write("\n")
		json.dump( "Number of good channels:",f1) ;f1.write("\n")
		json.dump( len(I),f1) ;f1.write("\n")
		json.dump( "R="+str(R),f1) ;f1.write("\n")
		json.dump( "Frozen channels:",f1) ;f1.write("\n")
		json.dump( len(B),f1) ;f1.write("\n")
		


