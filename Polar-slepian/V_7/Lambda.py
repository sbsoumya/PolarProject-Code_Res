#-------------------------------------------------------------------------------
# Name:       simulation for characterising lambda
# Purpose:    to decide decodability
#
# Author:      soumya
#
# Created:    30/08/2017
#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
from datetime import datetime
import json
import polarconstruct as pcon
from pprint import pprint

llr_dict={}
good_channels={}
degenerate_channels={}

N=32
plist=[0.05,0.07,0.1,0.2,0.3,0.4]
p=0.05 #design agrressively
tolerable_error= -1
K=16

runsim=10000

stamp=datetime.now().strftime("%d-%y-%m_%H-%M-%S")
f1=open("./simresults/lambda_avg"+stamp+".txt",'w')

#==========================================================Construction
print "LLR Lambda REPORT"
print "---------------------------"
print "N="+str(N)
print "design_p="+str(p)
PotGCh=int(ma.floor(pl.CapacityBSC(N,p)))
print "Capacity for "+str(N)+"channels:"+str(PotGCh)
print "tolerable error exponent:"+str(tolerable_error)
print "sim ran :"+str(runsim)
#-----------------------------------------ZC
#(I,E)=pcon.getGChZCL(p,N,tolerable_error)
#(I,E)=pcon.getGChZCK(p,N,K)
I=pcon.getGCHsim("MK_ALL",N,p,K)
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
json.dump( "design_p="+str(p),f1) ;f1.write("\n")
json.dump( "Capacity for "+str(N)+"channels:"+str(PotGCh),f1) ;f1.write("\n")
json.dump( "tolerable error exponent:"+str(tolerable_error),f1) ;f1.write("\n")
#-----------------------------------------ZC
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

for psim in plist:
	print "running for "+str(psim)+"...\n"
	#(psimI,psimE)=pcon.getGChZCL(psim,N,tolerable_error)
	#(psimI,psimE)=pcon.getGChZCK(psim,N,int(K*p/psim))
	psimI=pcon.getGCHsim("MK_ALL",N,psim,int(K*p/psim))
	good_channels[psim]=psimI
	print psimI
	psim_llr_sum=np.zeros(N)
	for i in range(runsim):
		UN=np.random.randint(2,size=len(I))
		UN_encoded=ec.polarencodeG(UN,N,I,list(D))
		YN=pl.BSCN(psim,UN_encoded)
		(L,d)=ec.polarSCdecodeG_LLR(YN,N,p,I,list(D))
		#print abs(L)/runsim
		psim_llr_sum+=abs(L)/runsim
	
	#psim_llr=[float(x)/runsim for x in psim_llr_sum]
	psim_llr=psim_llr_sum.tolist()
	print psim_llr
	if p==psim:
		 #sets the threshold of lambda as the min of goodchannels 
		 #for the highest rate channel  
				
		lambda_threshold=min(ec.getchannel_u(psim_llr,I))
		print ec.getchannel_u(psim_llr,I)

	llr_dict[psim]=psim_llr
	
print lambda_threshold

#---------------------------------------------------decodable condition
# all bad channels are within lambda threshold

HiBad=[]
for ch in B:
	if llr_dict[psim][ch]>=lambda_threshold:
		HiBad.append(ch)
		
print "Decodable Condition:"
print "-"*20
print HiBad

json.dump("Decodable Condition:",f1) ;f1.write("\n")
json.dump("---------------------",f1);f1.write("\n")
json.dump("Bad Channels above threshold:",f1);f1.write("\n")
json.dump(HiBad,f1);f1.write("\n")

LoGood=[]
for ch in I:
	if llr_dict[psim][ch]<=lambda_threshold:
		LoGood.append(ch)


json.dump("Good channels below threshold:",f1);f1.write("\n")
json.dump(HiBad,f1);f1.write("\n")
#----------------------------------------------------------undecodable
#good channels in design p
# that are actually bad in real p fall below threshold
print "Undecodable Condition:"
print "-"*20



for psim in plist:
	degenerate_channels[psim]=[]
	for ch in I:
		if llr_dict[psim][ch]<lambda_threshold:
			degenerate_channels[psim].append(ch)
			
print "Degenerate channels:\n"
pprint(degenerate_channels)	
print "Lambda threshold:"+str(lambda_threshold)		
pprint(llr_dict)



json.dump("Undecodable Condition:",f1) ;f1.write("\n")
json.dump("---------------------",f1);f1.write("\n")
json.dump("Lambda Threshold:"+str(lambda_threshold),f1) ;f1.write("\n")
json.dump("Good_channels for other p:",f1) ;f1.write("\n")
json.dump(good_channels,f1,indent=2);f1.write("\n")
json.dump("LLRs:",f1) ;f1.write("\n")
json.dump(llr_dict,f1,indent=2);f1.write("\n")
json.dump("degenerate channels:",f1) ;f1.write("\n")
json.dump(degenerate_channels,f1,indent=2);f1.write("\n")


