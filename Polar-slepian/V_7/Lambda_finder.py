#-------------------------------------------------------------------------------
# Name:       simulation for characterising lambda
# Purpose:    to decide decodability
#
# Author:      soumya
#
# Created:    24/10/2017
"""
Used to findlambda for proof of concept
"""
#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
from datetime import datetime
import json
import polarconstruct as pcon
from pprint import pprint

#-----------------
designbyrate=True
#-----------------

N=32
#actual channel_plist=[0.1,0.2,0.3,0.4]
channel_plist=[0.1,0.2]
channel_plist.sort()
design_p=min(channel_plist) #design agrressively

runsim_th=1000

stamp=datetime.now().strftime("%d-%y-%m_%H-%M-%S")
f1=open("./simresults/lambda_find"+stamp+".txt",'w')

#---------------------------------------------------------------design:
C=pl.CapacityBSC(N,design_p)
deratepercentage=10
tolerable_error= -2

if designbyrate:
	
	
	#K=int((100-deratepercentage)*C/100)
	K=int(0.7*C)
	
	try:
		I=pcon.getGCHsim('ZK',N,design_p,K)
	except:
		(I,E)=pcon.getGChZCK(design_p,N,K)

else:
	
	try:
		I=pcon.getGCHsim('ZL',N,design_p,tolerable_error)
	except:
		(I,E)=pcon.getGChZCL(design_p,N,tolerable_error)



#==========================================================Construction
print "Lambda Finder"
print "---------------------------"
print "N="+str(N)
print "design_p="+str(design_p)
PotGCh=int(ma.floor(pl.CapacityBSC(N,design_p)))
print "Capacity for "+str(N)+"channels:"+str(PotGCh)

if not designbyrate:
	print "tolerable error exponent:"+str(tolerable_error)
else:
	print "design for rate:"+str(K)
	
print "sim ran for LT:"+str(runsim_th)
print "Good Channels:"
print I
print "Number of good channels:"
print len(I)
R=float(len(I))/N
print "R="+str(R)
print "Frozen channels:"
B=list(set(range(N))-set(I))
print len(B)
##########################################file
json.dump( "Lambda_finder",f1) ;f1.write("\n")
json.dump( "---------------------------",f1) ;f1.write("\n")
json.dump( "N="+str(N),f1) ;f1.write("\n")
json.dump( "design_p="+str(design_p),f1) ;f1.write("\n")
json.dump( "Capacity for "+str(N)+"channels:"+str(PotGCh),f1) ;f1.write("\n")

if not designbyrate:
	json.dump("tolerable error exponent:"+str(tolerable_error),f1) ;f1.write("\n")
else:
	json.dump("design for rate:"+str(K),f1) ;f1.write("\n")
	
json.dump("Z Construct--------------------------------------------------------",f1);f1.write("\n")
json.dump( "Good Channels:",f1) ;f1.write("\n")
json.dump( I,f1) ;f1.write("\n")
json.dump( "Number of good channels:",f1) ;f1.write("\n")
json.dump( len(I),f1) ;f1.write("\n")
json.dump( "R="+str(R),f1) ;f1.write("\n")
json.dump( "Frozen channels:",f1) ;f1.write("\n")
json.dump( len(B),f1) ;f1.write("\n")

json.dump("sim ran for LT:"+str(runsim_th),f1) ;f1.write("\n")
#=======================================================Simulation
#Frozen data
D=np.zeros(N-len(I),dtype=int).tolist()

#---------------------------------------------finding lambda-threshold 
#threshold if found for design=channel and design<channel(channel being the second best in compound channel)

lambda_Emindict={}
lambda_minEdict={}



for channel_p in channel_plist:
	lambda_thresholdlist=np.zeros(N)
	lambda_Emin=0

	for i in range(runsim_th):
		UN=np.random.randint(2,size=len(I))
		UN_encoded=ec.polarencodeGR(UN,N,I,list(D))
		YN=pl.BSCN(channel_p,UN_encoded)
			
		(llr,d)=ec.polarSCdecodeG_LLR(YN,N,design_p,I,list(D))
		
		L=abs(llr)/runsim_th
		
		#expected value of min of good channels
		lambda_Emin+=min(ec.getchannel_u(L,I))
		
		#expected Value of all channels(a vector)
		lambda_thresholdlist=lambda_thresholdlist+L
		
		
		

	lambda_Emindict[str(channel_p)]=lambda_Emin
    
	#minimum of expected value of goodchannels
	lambda_minE=min(ec.getchannel_u(lambda_thresholdlist,I))
	lambda_minEdict[str(channel_p)]=lambda_minE
    

	print "channel_p:"+str(channel_p)
	print "Lambda Min(E(LLR))"+ str(lambda_minE)
	print "Lambda E(min(LLR))"+ str(lambda_Emin)
	
	json.dump("channel_p:"+str(channel_p),f1) ;f1.write("\n")
	json.dump("Lambda Min(E(LLR))"+ str(lambda_minE),f1) ;f1.write("\n")
	json.dump("Lambda E(min(LLR))"+str(lambda_Emin),f1) ;f1.write("\n")
	

	





