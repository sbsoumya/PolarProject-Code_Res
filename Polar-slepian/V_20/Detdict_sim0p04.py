#---------------------------------------------------
# Name:       Detdict_sim.py
# Purpose:    generate ditection bit dict
#
# Author:      soumya
#
# Created:    17/03/2018
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
import detectionbits as dd


#-----------------
designbyrate=True
#-----------------

N=1024

channel_plist=[0.04,0.15]
design_p=0.04
runsim=1
deratelist=np.arange(0.2,1.2,0.2)


Worst_p=max(channel_plist)
C=pl.CapacityBSC(N,design_p)
C_w=pl.CapacityBSC(N,Worst_p)

runfor_channel=[0.04]


stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
f1=open("./simresults/Detdict_sim"+stamp+".txt",'w')
print "Detdict generation REPORT"
print "---------------------------"
print "N="+str(N)
print "Design_p:"+str(design_p)
print "Capacity of design:"+str(C)
print "Worst_p:"+str(Worst_p)
print "Capacity of Worst:"+str(C_w)


json.dump( "Detdict generation REPORT",f1) ;f1.write("\n")
json.dump( "---------------------------",f1) ;f1.write("\n")
json.dump( "N="+str(N),f1) ;f1.write("\n")
json.dump( "Design_p:"+str(design_p),f1) ;f1.write("\n")
json.dump( "Capacity of design:"+str(C),f1) ;f1.write("\n")


for channel_p in runfor_channel:
	C_ch=pl.CapacityBSC(N,channel_p)
	print "Next Channel:======================================================================"
	print "Channel_p:"+str(channel_p)
	json.dump( "Channel_p:"+str(channel_p),f1) ;f1.write("\n")
	print "Capacity of channel:"+str(C_ch)
	json.dump( "Capacity of channel:"+str(C_ch),f1) ;f1.write("\n")
	for derate in deratelist:
		Tstart=10
		dC=int(derate*C)
		dC_w=int(derate*C_w)
		Tend=int(dC)-int(dC_w)
		#print Tend
		step=int(Tend/3)
		Tlist=range(Tstart,Tend,step)
		
		#---------------------------------------------------------------design:
		if designbyrate:
			
			
			K=dC
			#K=int(C)
			
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

		G=len(I)
		print "Derate:"+str(derate)
		print "Sent Rate*N including detection bits:"+str(G)
		print "Derated capacity of Worst_p:"+str(dC_w)
		print "Detection Length"
		print Tlist
		
		
		json.dump("Derate:"+str(derate),f1) ;f1.write("\n")
		json.dump("Sent Rate*N including detection bits:"+str(G),f1) ;f1.write("\n")
		json.dump("Derated capacity of Worst_p:"+str(dC_w),f1) ;f1.write("\n")
		json.dump("Detection length:",f1);f1.write("\n")
		json.dump(Tlist,f1);f1.write("\n")
		
		
		
		print "simran:"+str(runsim)
		json.dump( "simran:"+str(runsim),f1) ;f1.write("\n")
		
		f2name=dd.get_Detdict(channel_p,design_p,I,Tlist,N,runsim,RI)
		print ("Outputilename:"+str(f2name))
		json.dump ("Outputilename:"+str(f2name),f1) ;f1.write("\n")



			

