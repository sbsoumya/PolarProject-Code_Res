#-------------------------------------------------------------------------------
# Name:       polarfilesim_FERvsR_rateless_det_Iterretro.py
# Purpose:    FER VS R simulation for given msg_length and varying channel
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
import polarfile as pch

from pprint import pprint
import rateless_file_det as rlf
from timeit import default_timer as timer
#=================================================================simulation		
#------------Number of good channels = capacity
start = timer()
Nlist=[512] #keep this singleton
points=20
channel_p1list=list(np.linspace(0.01,0.2,points))
print channel_p1list
compound_plist=[0.03,0.11,0.17]
compoundcap=[pl.CapacityBSC(Nlist[0],p) for p in compound_plist]
T=9
R_p1=246
F_p1=Nlist[0]-R_p1
error_free_msg_length=F_p1+T #msg to be sent error free
runsim=1000
chp1_i=points
start=timer()
print "RATE Vs FER REPORT Rateless Det Iter retro"
print "------------------------------------------"
print "Compound_plist:"
print compound_plist
print "sim ran :"+str(runsim)
print "T:"+str(T)

fc=0
filenames=[]
achieved_rates=[]
block_errors=[]
for N in Nlist:
	print "N="+str(N)
	for channel_p1 in channel_p1list:
		channel_p2list=list(np.linspace(channel_p1,0.2,chp1_i))
		chp1_i -=1
		fc+=1
		stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
		filename="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_"+str(fc).replace(".",'p')+"_"+str(R_p1)+"in"+str(N)+"_T"+str(T)+"_"+stamp+".txt"
		f1=open(filename,'w')
		filenames.append(filename)
		json.dump( "RATE Vs FER REPORT Rateless Det Iter retro",f1) ;f1.write("\n")
		json.dump( "------------------------------------------",f1) ;f1.write("\n")
		json.dump( "Compound_plist:",f1) ;f1.write("\n")
		json.dump(compound_plist,f1) ;f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		json.dump("T:"+str(T),f1);f1.write("\n")
		
		
		json.dump( "N="+str(N),f1) ;f1.write("\n")
	
		achieved_rate=[]
		FER=[];
		
	
		for channel_p2 in channel_p2list:
		#print "channel_p:"+str(channel_p)
			(ach_rate,block_error)=rlf.send_rateless_file_Iter_retro_det_3_sim(N,T,compound_plist,channel_p1,channel_p2,error_free_msg_length,runsim,False)
			achieved_rate.append(ach_rate) # E{D}/N
			FER.append(block_error) # ep
		

		block_error_exp=np.log10(FER).tolist()	
		block_errors.append(block_error_exp)
		achieved_rates.append(achieved_rate)		
		json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
		json.dump(channel_p1,f1);f1.write("\n")
		json.dump(channel_p2list,f1) ;f1.write("\n")
		json.dump(achieved_rate,f1) ;f1.write("\n")
		json.dump(block_error_exp,f1) ;f1.write("\n")

print filenames		
print channel_p1list    
print achieved_rates
print block_errors
	

end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
			

		    



