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
import rateless_file_det_4G as rlf
from timeit import default_timer as timer
#=================================================================simulation		
#------------Number of good channels = capacity
start = timer()
Nlist=[512] #keep this singleton
points2=20
compound_plist=[0.03,0.11,0.17]
channel_p0=0.07
channel_p1list=[0.03]#,0.11,0.17]
compoundcap=[pl.CapacityBSC(Nlist[0],p) for p in compound_plist]
T=50
R_p1=246
F_p1=Nlist[0]-R_p1
error_free_msg_length=F_p1+T #msg to be sent error free
runsim=1000
#\=points
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
Empirical_comps=[]
block_errors=[]
MC=False
#print "MC2"
for N in Nlist:
	print "N="+str(N)
	for channel_p1 in channel_p1list:
		channel_p2_start=0.01
		channel_p2list=list(np.linspace(channel_p2_start,0.2,points2))
		#channel_p2list=[0.11]
		

		
		fc+=1
		stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
		if MC:
			filename="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_MC2_"+str(fc).replace(".",'p')+"_"+str(R_p1)+"in"+str(N)+"_T"+str(T)+"_"+stamp+".txt"
		else:
			filename="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_Tree_"+str(fc).replace(".",'p')+"_"+str(R_p1)+"in"+str(N)+"_T"+str(T)+"_"+stamp+".txt"
		filename2="./simresults/polarfile_FT4G_"+str(fc).replace(".",'p')+"_"+str(R_p1)+"in"+str(N)+"_T"+str(T)+"_"+stamp+".txt"
		f1=open(filename,'w')
		f2=open(filename2,'w')
		filenames.append(filename)
		json.dump( "RATE Vs FER REPORT Rateless Det Iter retro",f1) ;f1.write("\n")
		json.dump( "------------------------------------------",f1) ;f1.write("\n")
		json.dump( "Compound_plist:",f1) ;f1.write("\n")
		json.dump(compound_plist,f1) ;f1.write("\n")
		json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
		json.dump("T:"+str(T),f1);f1.write("\n")
		
		
		json.dump( "N="+str(N),f1) ;f1.write("\n")
	
		achieved_rate=[]
		Empirical_comp=[]
		FER=[];

	
		for channel_p2 in channel_p2list:
		#print "channel_p:"+str(channel_p)
			(ach_rate,block_error,decoded,Emp_comp)=rlf.send_rateless_file_Iter_retro_det_4G_sim(N,T,compound_plist,[channel_p0,channel_p1,channel_p2],error_free_msg_length,runsim,False,MC)

			achieved_rate.append(ach_rate) # E{D}/N
			Empirical_comp.append(Emp_comp)
			FER.append(block_error) # ep
	
			json.dump("channel:"+str(channel_p0)+","+str(channel_p1)+","+str(channel_p2),f2);f2.write("\n")
			json.dump("Sample FT",f2) ;f2.write("\n")
			json.dump(decoded,f2);f2.write("\n")
			print decoded
		

		block_error_exp=np.log10(FER).tolist()	
		block_errors.append(block_error_exp)
		achieved_rates.append(achieved_rate)	
		Empirical_comps.append(Empirical_comp)	
		json.dump( "Rate vs Block_error=",f1) ;f1.write("\n")
		json.dump([channel_p0,channel_p1],f1);f1.write("\n")
		json.dump(channel_p2list,f1) ;f1.write("\n")
		json.dump(achieved_rate,f1) ;f1.write("\n")
		json.dump(block_error_exp,f1) ;f1.write("\n")
		json.dump(Empirical_comp,f1) ;f1.write("\n")




print "Channel"
print channel_p0
print channel_p1list
print channel_p2list
print "Output"
print achieved_rates
print block_errors
print Empirical_comps
print filenames	
	

end = timer()
TC=(end-start)
print "Time taken:"+str(TC)	
json.dump("Time taken:"+str(TC)	,f1) ;f1.write("\n")
			

		    




