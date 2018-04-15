#---------------------------------------------------
# Name:       LLRdictWD_sim.py
# Purpose:    Generate LLRdict (not absolute) file with WD sim
#
# Author:      soumya
#
# Created:    15/02/2018
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
design_p=min(channel_plist) #design agrressively

runsim=10

stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
f1=open("./simresults/LLRdictWD_sim"+stamp+".txt",'w')

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
print "LLR dict generation REPORT"
print "---------------------------"
print "N="+str(N)
print "design_p="+str(design_p)
PotGCh=int(ma.floor(pl.CapacityBSC(N,design_p)))
print "Capacity for "+str(N)+"channels:"+str(PotGCh)

if not designbyrate:
	print "tolerable error exponent:"+str(tolerable_error)
else:
	print "design for rate:"+str(K)
	
#print "sim ran for prob:"+str(runsim)

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
json.dump( "LLR dict generation REPORT",f1) ;f1.write("\n")
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
#json.dump("sim ran for prob:"+str(runsim),f1) ;f1.write("\n")

f2name=lmb.get_LLRdictWD(channel_plist,design_p,I,N,runsim,RI)

print ("Outputilename:"+str(f2name))
json.dump ("Outputilename:"+str(f2name),f1) ;f1.write("\n")



			

