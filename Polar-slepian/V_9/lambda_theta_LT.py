#---------------------------------------------------
# Name:       lambda_theta_LT.py
# Purpose:    Probability of theta fraction goodchannels above a threshold LT
#
# Author:      soumya
#
# Created:    24/10/2017
#---------------------------------------------

#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
from datetime import datetime
import json
import polarconstruct as pcon
from pprint import pprint
import csv
import matplotlib.pyplot as plt
import lambdathreshold as lmb


#-----------------
designbyrate=True
#-----------------

N=1024
channel_plist=[0.04,0.15,0.2,0.25]
channel_plist.sort()
lesser_channel_p=channel_plist[1]
design_p=min(channel_plist) #design agrressively

runsim=1000


LT=30
theta1=59
theta2=59


stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
f1=open("./simresults/lambda_theta_LT"+stamp+".txt",'w')

#---------------------------------------------------------------design:
C=pl.CapacityBSC(N,design_p)
deratepercentage=10
tolerable_error= -2

if designbyrate:
	
	
	#K=int((100-deratepercentage)*C/100)
	K=int(C)
	
	try:
		I=pcon.getGCHsim('ZK',N,design_p,K)
		RI=pcon.getGChsim('ZK',design_p,N,N)

		
	except:
		(I,E)=pcon.getGChZCK(design_p,N,K)
		(RI,E)=pcon.getGChZCK(design_p,N,N)

else:
	
	try:
		I=pcon.getGCHsim('ZL',N,design_p,tolerable_error)
	except:
		(I,E)=pcon.getGChZCL(design_p,N,tolerable_error)




#==========================================================Construction
print "LLR Lambda Channel REPORT"
print "---------------------------"
print "N="+str(N)
print "design_p="+str(design_p)
PotGCh=int(ma.floor(pl.CapacityBSC(N,design_p)))
print "Capacity for "+str(N)+"channels:"+str(PotGCh)

if not designbyrate:
	print "tolerable error exponent:"+str(tolerable_error)
else:
	print "design for rate:"+str(K)
	
print "sim ran for prob:"+str(runsim)

print "Good Channels:"
print I
print "R order:"
print I
print "Number of good channels:"
print len(I)
R=float(len(I))/N
print "R="+str(R)
print "Frozen channels:"
F=list(set(range(N))-set(I))
print len(F)
#-------------------------------------------------------------file
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
json.dump( "R order:",f1) ;f1.write("\n")
json.dump( RI,f1) ;f1.write("\n")
json.dump( "Number of good channels:",f1) ;f1.write("\n")
json.dump( len(I),f1) ;f1.write("\n")
json.dump( "R="+str(R),f1) ;f1.write("\n")
json.dump( "Frozen channels:",f1) ;f1.write("\n")
json.dump( len(F),f1) ;f1.write("\n")
json.dump("sim ran for prob:"+str(runsim),f1) ;f1.write("\n")

print ("Lambdathreshold:"+str(LT))
print ("Theta1 (fraction of goodchannels above LT for design channel):"+str(theta1))
print ("Theta2 (fraction of goodchannels above LT for other channel):"+str(theta2))
json.dump("Lambdathreshold:"+str(LT),f1) ;f1.write("\n")
json.dump("Theta1 (fraction of goodchannels above LT for design channel):"+str(theta1),f1) ;f1.write("\n")
json.dump ("Theta2 (fraction of goodchannels above LT for other channel):"+str(theta2),f1) ;f1.write("\n")


#=======================================================Simulation

json.dump("{p:Fraction of good channels abov LT...}",f1);f1.write("\n")
#-----------------------------------------checking channel
#calculating P_all good could have been seperated for llrdict , but that takes longer time
Fdict=lmb.frac_goodchannel(channel_plist,design_p,I,N,LT,runsim,RI,False)

Pperdict=lmb.PrOffracaboveFT(Fdict,channel_plist,theta1,runsim)

pprint(Fdict)
pprint(Pperdict)
json.dump(Fdict,f1)
json.dump(Pperdict,f1)



			

