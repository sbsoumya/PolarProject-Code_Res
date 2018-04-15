#-------------------------------------------------------------------------------
# Name:       monte-carlo for charaterising channel/ code construction
# Purpose:    related to prob and channel
#
# Author:      soumya
#
# Created:     04/08/2017
#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
from datetime import datetime
import json


#=================================================Code construction
#NOTE:Zconstruct is good for BEC,but gives similar results for BSC
def Zconstruct(Z,n):
	ZN1=[]
	ZN2=[]
	ZN1.append(Z)
	for i in range(n):
		for z in ZN1:
			ZN2.append(2*z-z**2)
			ZN2.append(z**2)
		
		ZN1=list(ZN2)
		#print ZN1
		ZN2=[]
		
	return ZN1

#ZN=Zconstruct(pl.ZBSC(0.3),2)
#print ZN,len(ZN) 

#note the channels from Zconstruct are taken as bit reversed order
def getGChZCK(design_p,N,K):
	p=design_p
	#actually here the p is not neccessary
	print "ZC(K)..."
	n=int(ma.log(N,2))
	Z=pl.ZBSC(p)	
	ZN=Zconstruct(pl.ZBSC(p),n)
	aZN=np.array(ZN)
	sZN=np.sort(aZN)
	good_channels=aZN.argsort().tolist()[:K]
	ber_exp=np.log10(sZN).tolist()
	rgood_channels=ec.bitreverseorder(good_channels,n)
	
	f2=open("./simresults/GCZK_"+str(N)+"_"+str(p).replace(".","p")+"_"+str(K)+".txt",'w')
	json.dump(rgood_channels,f2)
	
	
	return (rgood_channels,ber_exp[:K])

		
def getGChZCL(design_p,N,L):#L is error exponent
	p=design_p
	print "ZC(error)..."
	n=int(ma.log(N,2))
	Z=pl.ZBSC(p)	
	ZN=Zconstruct(pl.ZBSC(p),n)
	aZN=np.array(ZN)
	sZN=np.sort(aZN)
	ber_exp=np.log10(sZN).tolist()
	#print ber_exp
	K=0
	for i in ber_exp:
		if i<=L:
			K+=1
	
	good_channels=aZN.argsort().tolist()[:K]
	rgood_channels=ec.bitreverseorder(good_channels,n)
	
	
	f2=open("./simresults/GCZL_"+str(N)+"_"+str(p).replace(".","p")+"_"+str(L)+".txt",'w')
	json.dump(rgood_channels,f2)
	
	return (rgood_channels,ber_exp[:K])


#---------------------------------Monte Carlo

def getGChMCK(design_p,N,K,runsim):
	p=design_p
	n=int(ma.log(N,2))
	err=np.zeros(N)
	print "MC(K)..."+str(runsim)
	for i in range(runsim):
		UN=np.random.randint(2,size=N)
		UN_decoded=ec.polarSCdecode(pl.BSCN(p,ec.polarencode(UN,len(UN))),len(UN),p)
		err=err+np.logical_xor(UN,UN_decoded)
	
	aZN=err/runsim
	sZN=np.sort(aZN)
	good_channels_all=aZN.argsort().tolist()[:K]
	good_channels=good_channels_all[:K]
	ber_exp=np.log10(sZN).tolist()
	rgood_channels=ec.bitreverseorder(good_channels,n)
	rgood_channels_all=ec.bitreverseorder(good_channels_all,n)
	
	f2=open("./simresults/GCMK_"+str(N)+"_"+str(p).replace(".","p")+"_"+str(K)+".txt",'w')
	json.dump(rgood_channels,f2)
	
	f3=open("./simresults/GCMK_ALL"+str(N)+".txt",'w')
	json.dump(rgood_channels_all,f3)
	
	return (rgood_channels,ber_exp[:K],ber_exp)
	
def getGChMCL(design_p,N,L,runsim):
	p=design_p
	n=int(ma.log(N,2))
	err=np.zeros(N)
	print "MC(error)..."+str(runsim)
	for i in range(runsim):
		UN=np.random.randint(2,size=N)
		UN_decoded=ec.polarSCdecode(pl.BSCN(p,ec.polarencode(UN,len(UN))),len(UN),p)
		err=err+np.logical_xor(UN,UN_decoded)
	
	aZN=err/runsim
	sZN=np.sort(aZN)
	ber_exp=np.log10(sZN).tolist()
	#print ber_exp
	K=0
	for i in ber_exp:
		if i<=L:
			K+=1
	
	
	good_channels_all=aZN.argsort().tolist()[:K]
	good_channels=good_channels_all[:K]
	
	rgood_channels=ec.bitreverseorder(good_channels,n)
	rgood_channels_all=ec.bitreverseorder(good_channels_all,n)
	
	f2=open("./simresults/GCML_"+str(N)+"_"+str(p).replace(".","p")+"_"+str(L)+".txt",'w')
	json.dump(rgood_channels,f2)
	
	f3=open("./simresults/GCML_ALL"+str(N)+".txt",'w')
	json.dump(rgood_channels_all,f3)
	
	#print ber_exp
	return (rgood_channels,ber_exp[:K],ber_exp)

def getGChMZ(design_p,N,L,runsim):
	p=design_p
	#Uses param to find number of good channels from Z and then produces same number by M
	(Zgood_channels,Zber_exp)=getGChZCL(p,N,L)
	Zgoodcount=len(Zgood_channels)
	(Mgood_channels,Mber_exp,dummy)=getGChMCK(p,N,Zgoodcount,runsim)
	
	f2=open("./simresults/GCMZ_"+str(N)+"_"+str(p).replace(".","p")+"_"+str(L)+".txt",'w')
	json.dump(Mgood_channels,f2)
	
	#print Zgood_channels #,Zber_exp
	#print Mgood_channels #,Mber_exp
	
	print "Difference:%"
	print float(len((set(Zgood_channels)-set(Mgood_channels)))*100)/Zgoodcount
	
	return (Mgood_channels,Mber_exp,dummy)
	
	
	
	
#----------------------------------------------------------load sim results
def getGCHsim(tsim,N,design_p,param): # tsim = ML / MK/ ZL/ ZK/ MZ/ MK_ALL
		p=design_p
	    # param for getting channel model K channels or L error exponent
		#=====================clean the mess below
		if tsim=="MK_ALL" or tsim == "ML_ALL":
			
			filename="./simresults/GC"+str(tsim)+str(N)+".txt"
			f1=open(filename,'r')
		    
			return json.load(f1)[:param]
		else:
			filename="./simresults/GC"+str(tsim)+"_"+str(N)+"_"+str(p).replace(".","p")+"_"+str(param)+".txt"
			f1=open(filename,'r')
			return json.load(f1)
		
#--------------------------------------------------------------llr based
def getRI_LLR(absllr,I,N):
	good_channels_all_Iind=absllr.argsort().tolist();
	#print I
	llr_I=[I[i] for i in good_channels_all_Iind[::-1]]
	#print llr_I
	#print absllr
	f2=open("./simresults/GCLLR_"+str(N)+".txt",'w')
	json.dump(llr_I,f2)
	return llr_I
"""	
llr=[3,5,2,3,4,4,7,8]
I=[8,7,6,5,4,3,2,1]
llr_I= getRI_LLR(np.array(llr),I,8)
print llr_I
print [i for i in I]
llr_I.index


llr_index=[I.index(i) for i in llr_I]
print llr_index
print [llr[k] for k in llr_index]
"""	
def getRI_LLRsim(N):
	f2=open("./simresults/GCLLR_"+str(N)+".txt",'r')
	return json.load(f2)
	
	
	
#=================================================================simulation	




#print getGChMZ(0.01,1024,-6,1000)	

"""
#reliability ordering
N=128
plist=[0.01,0.1,0.2,0.3]
print "N="+str(N)+"\n"

for p in plist:
	print "p="+str(p)+"\n"
	print getGChZCK(p,N,N)

"""
#getGChMCK(0.1,32,32,1000)
"""
#=================================================traceback V_2
runsim=1000
print "MONTE _CARLO CHANNEL REPORT"
print "---------------------------"
N=32
p=0.1
print "N="+str(N)
print "p="+str(p)
PotGCh=int(ma.floor(pl.CapacityBSC(N,p)))
print "Capacity for "+str(N)+"channels:"+str(PotGCh)

K=4
tolerable_error= -6
print "No of good channels needed :"+str(K)+"(valid if used)"
print "tolerable error exponent:"+str(tolerable_error)
#-----------------------------------------ZC
(I,E)=getGChZCK(p,N,N)
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
		
#-------------------------------------MC

(I,E,AE)=getGChMCK(p,N,N,runsim)
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
"""

#=============================Now in polarconstructsim.py

"""	
#------------Number of good channels = capacity
Nlist=[128,256,1024]
plist=[0.05,0.1,0.2]
K=5
tolerable_error= -5
runsim=(10**(-tolerable_error))*2

for N in Nlist:
	for p in plist:
	
		
		

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
		(I,E)=getGChZCL(p,N,tolerable_error)
		#(I,E)=getGChZCK(p,N,K)
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

		(I,E,FE)=getGChMCL(p,N,tolerable_error,runsim)
		#(I,E,FE)=getGChMCK(p,N,K,runsim)
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
		

"""
