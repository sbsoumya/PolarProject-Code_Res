#-------------------------------------------------------------------------------
# Name:       simulation for characterising lambda
# Purpose:    to decide decodability
#
# Author:      soumya
#
# Created:    30/08/2017
"""
for the Rate for lowest p its rate is found out as R_design
This is used to design channel
The LLRs are simulated for this channel
Lambda_goodmin = min(LLR(i):i is a good channel)
Lambda_frozenmax=min(LLR(i):i is a frozen channel)

#assuming 
lambda threshold= (Lambda_goodmin+lambda_frozenmax)/2 across all simulations

P(decodable)=
P(all good channels outside lambda)


P(all bad channels inside lambda threshold)=
P(Lambda_threshold-Lambda_frozenmax>0)
This should be high if the rate is supported by the given channel

for a worse channel J
P(undecodable_J)=
P(atleast one good channel inside threshold)=
P(Lamda_threshold - LambdaJ_Gmin<0)
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
channel_plist=[0.1,0.2,0.3,0.4]
channel_plist.sort()
design_p=min(channel_plist) #design agrressively

runsim=10000
runsim_th=10000

stamp=datetime.now().strftime("%d-%y-%m_%H-%M-%S")
f1=open("./simresults/lambda_prob"+stamp+".txt",'w')

#---------------------------------------------------------------design:
C=pl.CapacityBSC(N,design_p)
deratepercentage=10
tolerable_error= -2

if designbyrate:
	
	
	#K=int((100-deratepercentage)*C/100)
	K=N/2
	
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
print "LLR Lambda REPORT"
print "---------------------------"
print "N="+str(N)
print "design_p="+str(design_p)
PotGCh=int(ma.floor(pl.CapacityBSC(N,design_p)))
print "Capacity for "+str(N)+"channels:"+str(PotGCh)

if not designbyrate:
	print "tolerable error exponent:"+str(tolerable_error)
else:
	print "design for rate:"+str(K)
	
print "sim ran :"+str(runsim)
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
json.dump( "LLR Lambda CHANNEL REPORT",f1) ;f1.write("\n")
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
json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
#=======================================================Simulation
#Frozen data
D=np.zeros(N-len(I),dtype=int).tolist()

#---------------------------------------------finding lambda-threshold
lambda_thresholdlist=np.zeros(N)
lambda_threshold1list=np.zeros(N)
lambda_threshold2list=np.zeros(N)
for i in range(runsim_th):
	UN=np.random.randint(2,size=len(I))
	UN_encoded=ec.polarencodeG(UN,N,I,list(D))
	YN=pl.BSCN(design_p,UN_encoded)
	(llr,d)=ec.polarSCdecodeG_LLR(YN,N,design_p,I,list(D))
	L=abs(llr)/runsim_th
	lambda_thresholdlist=lambda_thresholdlist+L
	



lambda_threshold1=min(ec.getchannel_u(lambda_thresholdlist,I))
lambda_threshold2=max(ec.getchannel_u(lambda_thresholdlist,B))
lambda_threshold=(lambda_threshold1+lambda_threshold2)/2


print [lambda_threshold1,lambda_threshold2,lambda_threshold]
json.dump([lambda_threshold1,lambda_threshold2,lambda_threshold],f1);f1.write("\n")


used_lambda_threshold=lambda_threshold1
print used_lambda_threshold
json.dump("used_lambda_threshold"+str(used_lambda_threshold),f1);f1.write("\n")




json.dump("p,Pr(Gmin>thr),Pr(Fmax<thr)::Pr(gmin>Fmax)",f1);f1.write("\n")
#-----------------------------------------checking channels



for channel_p in channel_plist:
	print "\nrunning for "+str(channel_p)+"..."
	
	Count_Dec=0
	Count_Dec2=0
	Count_Ord=0
		
	for i in range(runsim):
		
		
		UN=np.random.randint(2,size=len(I))
		UN_encoded=ec.polarencodeG(UN,N,I,list(D))
		YN=pl.BSCN(channel_p,UN_encoded)
		(llr,d)=ec.polarSCdecodeG_LLR(YN,N,design_p,I,list(D))
		L=abs(llr)
		llr_Gmin=min(ec.getchannel_u(L,I))
		llr_Fmax=max(ec.getchannel_u(L,B))
		
		#if(llr_Gmin<llr_Fmax):
			#print llr
		

		#print L
		Count_Dec+=((llr_Gmin-used_lambda_threshold)>=0)
		Count_Dec2+=((llr_Fmax-used_lambda_threshold)<0)
		Count_Ord+=((llr_Gmin-llr_Fmax)>=0)
	
	#print "specimen:"
	#print ec.getchannel_u(L,I)
	#print ec.getchannel_u(L,B)
	
	print [channel_p,float(Count_Dec)/runsim,float(Count_Dec2)/runsim,float(Count_Ord)/runsim]
	json.dump([channel_p,float(Count_Dec)/runsim,float(Count_Dec2)/runsim,float(Count_Ord)/runsim],f1);f1.write("\n")	

