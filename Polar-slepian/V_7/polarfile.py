#-------------------------------------------------------------------------------
# Name:       polar file 
# Purpose:    X is sent over channel
#             X is inverse arikan transformed to get U
#             good channels are known
#             Y received and decoded using above knowledge
#             final U is arikan transformed to get X
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

# p is actual flip probability of channel
# design_p is p for whch code is designed

#======================================================polar files

def polarfile(XN,p,I): 
	N=len(XN)
	n=int(ma.log(N,2))
	
	#Tx side
	UN=ec.polarencodeR(XN,N) # reverse arikan (was changed to recursive on 24-10-2017
	
	#picking data from frozen channels
	F=list(set(range(N))-set(I))
	D=ec.getUN_s(UN,F)
	
	YN=pl.BSCN(p,XN)	
	
	#rx side	
	UN_decoded=ec.polarSCdecodeG(YN,N,p,I,D)
	XN_decoded=ec.polarencode(UN_decoded,N)
	
	return XN_decoded
#-----------------------------------------------------sim
"""
N=8
p=0.2
K=4
L=-6
XN=np.random.randint(2,size=N)
try:
	I=pcon.getGCHsim("ZK",N,p,K)
except:
	(I,E)=pcon.getGChZCK(p,N,K)

print XN	
print polarfile(XN,p,I)
"""
"""
#overflow problrm
N=1024
p=0.1
I=pcon.getGCHsim('ZL',N,p,-5)
D=np.zeros(N-len(I),dtype=int).tolist()
UN=np.random.randint(2,size=N)

d=ec.polarSCdecodeG(UN,N,p,I,D)
print d
print ec.getUN_s(d,I)
"""
#----------------------------------------------------------different decode p
def polarfiled(XN,channel_p,design_p,I):
	

	p=channel_p
	N=len(XN)
	n=int(ma.log(N,2))
	
	#Tx side
	UN=ec.polarencode(XN,N) # reverse arikan
	#picking data from frozen channels
	F=list(set(range(N))-set(I))
	D=ec.getUN_s(UN,F)
	
	YN=pl.BSCN(p,XN)	
	
	#rx side	
	UN_decoded=ec.polarSCdecodeG(YN,N,design_p,I,D)
	XN_decoded=ec.polarencode(UN_decoded,N)
	
	return XN_decoded	
#------------------------------------------------------------polarfile known pattern	
def polarfile_known(XN,p,pattern,I):
	
	N=len(XN)
	n=int(ma.log(N,2))
	
	#Tx side
	UN=ec.polarencode(XN,N) # reverse arikan
	#picking data from frozen channels
	F=list(set(range(N))-set(I))
	D=ec.getUN_s(UN,F)
	
	YN=np.logical_xor(XN,pattern)
	
	#rx side	
	UN_decoded=ec.polarSCdecodeG(YN,N,p,I,D)
	XN_decoded=ec.polarencode(UN_decoded,N)
	
	return XN_decoded	

#----------------------------------------------------------function used in sims
def polarfilesim(N,channel_p,design_p,I,runsim,BER_needed):
	    
        
		errcnt=np.zeros(N)
		block_errorcnt=0
		for i in range(runsim):
			
			XN=np.random.randint(2,size=N)
			XN_decoded=polarfiled(XN,channel_p,design_p,I)
			
			if BER_needed:
				errcnt=errcnt+np.logical_xor(XN,XN_decoded)
			
			if XN.tolist()!=XN_decoded.tolist():
				block_errorcnt+=1
				
		if BER_needed:		
			berN=errcnt/runsim
			ber_exp=np.log10(berN).tolist()
				
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
		block_error=float(block_errorcnt)/runsim
		
		if BER_needed:
			return (ber_exp,block_error)
		else:
			return block_error







#-----------------------------------------------------sim
# this combinations show that errors occur
"""
N=8
d_p=0.2
p=0.2

K=4
L=-6
XN=np.random.randint(2,size=N)
try:
	I=pcon.getGCHsim("ZK",N,p,K)
except:
	(I,E)=pcon.getGChZCK(p,N,K)

print XN	
XN_decoded= polarfiled(XN,p,d_p,I)
print XN_decoded
print np.logical_xor(XN,XN_decoded)
print XN.tolist()!=XN_decoded.tolist()

"""
#-----------------------------------------------------------Now in polarfilesim.py
"""
#=================================================================simulation		
#------------Number of good channels = capacity
Nlist=[128,1024]
design_plist=[0.3]
psteps=0.1

tolerable_error= -5 #using ZCL for channel


runsim=100


for N in Nlist:
	for design_p in design_plist:
		p=0
		stamp=datetime.now().strftime("%d-%m-%y_%H-%M-%S")
		f1=open("./simresults/polarfile_"+str(N)+"_"+str(design_p)+"_"+stamp+".txt",'w')
			
		print "MONTE _CARLO FILE REPORT"
		print "---------------------------"
		print "N="+str(N)
		print "p_decode="+str(design_p)
		print "tolerable error exponent:"+str(tolerable_error)# channels selected as per this
		
		json.dump( "MONTE _CARLO FILE REPORT",f1) ;f1.write("\n")
		json.dump( "---------------------------",f1) ;f1.write("\n")
		json.dump( "N="+str(N),f1) ;f1.write("\n")
		json.dump( "p_decode="+str(design_p),f1) ;f1.write("\n")
		json.dump( "tolerable error exponent:"+str(tolerable_error),f1) ;f1.write("\n")
		
		
		
		#-----------------------------------------ZC
		try:
			I=pcon.getGCHsim('ZL',N,design_p,tolerable_error)
		except:
		   (I,E)=pcon.getGChZCL(design_p,N,tolerable_error)
		   
		print "Good Channels:"
		print I
		R=float(len(I))/N
		print "R="+str(R)
		print "Frozen channels:"
		B=list(set(range(N))-set(I))
		print len(B)
		
		json.dump( "Good Channels:",f1) ;f1.write("\n")
		json.dump( I,f1) ;f1.write("\n")
		json.dump( "R="+str(R),f1) ;f1.write("\n")
		json.dump( "Frozen channels:",f1) ;f1.write("\n")
		json.dump( len(B),f1) ;f1.write("\n")
		
		
		
		
		
		while  p<design_p:
			p+=psteps
			json.dump( "p_channel="+str(p),f1) ;f1.write("\n")
			print "p_channel="+str(p)
			errcnt=np.zeros(N)
			block_errorcnt=0
			for i in range(runsim):
				XN=np.random.randint(2,size=N)
				XN_decoded=polarfiled(XN,p,design_p,I)
				errcnt=errcnt+np.logical_xor(XN,XN_decoded)
				if XN.tolist()!=XN_decoded.tolist():
					block_errorcnt+=1
					
			berN=errcnt/runsim
			ber_exp=np.log10(berN).tolist()
			block_error=float(block_errorcnt)/runsim
			
			#print ber_exp
			print block_error
			
			json.dump( "block_error="+str(block_error),f1) ;f1.write("\n")
			json.dump( "BER channelwise:",f1) ;f1.write("\n")
			json.dump( ber_exp,f1) ;f1.write("\n")
		    
"""		




