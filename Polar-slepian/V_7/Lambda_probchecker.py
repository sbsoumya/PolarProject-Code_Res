#-------------------------------------------------------------------------------
# Name:       simulation for characterising lambda
# Purpose:    to decide decodability
#
# Author:      soumya
#
# Created:    24/10/2017
"""

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
import csv
import matplotlib.pyplot as plt


#-----------------
designbyrate=True
#-----------------

N=1024
channel_plist=[0.1,0.2,0.3,0.4]
channel_plist.sort()
lesser_channel_p=channel_plist[1]
design_p=min(channel_plist) #design agrressively

runsim=1000


LT=float(np.log2(N)/N)


stamp=datetime.now().strftime("%d-%y-%m_%H-%M-%S")
f1=open("./simresults/lambda_prob_checker"+stamp+".txt",'w')

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
json.dump( "R order:",f1) ;f1.write("\n")
json.dump( RI,f1) ;f1.write("\n")
json.dump( "Number of good channels:",f1) ;f1.write("\n")
json.dump( len(I),f1) ;f1.write("\n")
json.dump( "R="+str(R),f1) ;f1.write("\n")
json.dump( "Frozen channels:",f1) ;f1.write("\n")
json.dump( len(B),f1) ;f1.write("\n")
json.dump("sim ran for prob:"+str(runsim),f1) ;f1.write("\n")

print ("Lambdathreshold:"+str(LT))
json.dump("Lambdathreshold:"+str(LT),f1) ;f1.write("\n")



#=======================================================Simulation
#Frozen data
D=np.zeros(N-len(I),dtype=int).tolist()

json.dump("p,Pr(Gmin>LT)",f1);f1.write("\n")
#-----------------------------------------checking channels
LLRdict={}



for channel_p in channel_plist:
	print "\nrunning for "+str(channel_p)+"..."
	
	Count_all_good=0
	LLRdict[str(channel_p)]=[]
		
	for i in range(runsim):
		
		
		UN=np.random.randint(2,size=len(I))
		UN_encoded=ec.polarencodeG(UN,N,I,list(D))
		YN=pl.BSCN(channel_p,UN_encoded)
		(llr,d)=ec.polarSCdecodeG_LLR(YN,N,design_p,I,list(D))
		L=abs(llr)
		llr_Gmin=min(ec.getchannel_u(L,I))
		LLRdict[str(channel_p)].append(ec.getchannel_u(L,RI))
		Count_all_good+=(llr_Gmin>=LT)

	
	print [channel_p,float(Count_all_good)/runsim]
	json.dump([channel_p,float(Count_all_good)/runsim],f1);f1.write("\n")
	
pprint(LLRdict)

json.dump(LLRdict,f1)

for channel_p in channel_plist:
	with open("./simresults/llr"+str(channel_p).replace(".","p")+"_lambda_prob_checker"+stamp+".csv",'wb') as resultFile:
		wr = csv.writer(resultFile, dialect='excel')
		wr.writerow(RI)	
		wr.writerows(LLRdict[str(channel_p)])


			

