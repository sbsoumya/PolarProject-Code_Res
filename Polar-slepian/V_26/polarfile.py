#-------------------------------------------------------------------------------
# Name:       polarfile.py 
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

#----------------------------------------------------------different decode p
def polarfile(XN,channel_p,design_p,I):
	

	p=channel_p
	N=len(XN)
	n=int(ma.log(N,2))
	
	#Tx side
	UN=ec.polarencode(XN,N) # reverse arikan
	#picking data from frozen channels
	F=list(set(range(N))-set(I))
	FD=ec.getUN(UN,F,True)
	
	YN=pl.BSCN(p,XN)	
	
	#rx side	
	UN_decoded=ec.polarSCdecodeG(YN,N,design_p,I,FD,False)
	XN_decoded=ec.polarencode(UN_decoded,N)
	
	return XN_decoded	

def polarfile_list(pc1,XN,channel_p,design_p,I,list_size):
	

	p=channel_p
	N=len(XN)
	n=int(ma.log(N,2))
	G=len(I)
	
	
	#Tx side
	UN=pc1.arikan(XN.tolist())
	
	#picking data from frozen channels
	F=pc1.channel_ordering[G:]
	print F
	FD=ec.getUN(UN,F,True)
	
	print FD
	YN=pl.BSCN(p,XN)	
	
	#rx side	
	UN_decoded=ec.polarSCdecodeG_C(pc1,YN,channel_p,list(FD),list_size)
	XN_decoded=ec.polarencodeG_C(pc1,UN_decoded.tolist(),list(FD))
	
	return XN_decoded	
#------------------------------------------------------------polarfile known pattern	
def polarfile_known(XN,p,pattern,I):
	
	N=len(XN)
	n=int(ma.log(N,2))
	
	#Tx side
	UN=ec.polarencode(XN,N) # reverse arikan
	#picking data from frozen channels
	F=list(set(range(N))-set(I))
	FD=ec.getUN(UN,F,True)
	
	YN=np.logical_xor(XN,pattern)
	
	#rx side	
	UN_decoded=ec.polarSCdecodeG(YN,N,p,I,FD,False)
	XN_decoded=ec.polarencode(UN_decoded,N)
	
	return XN_decoded	

#----------------------------------------------------------function used in sims
def polarfilesim(N,channel_p,design_p,I,runsim,BER_needed):
	    
        
		errcnt=np.zeros(N)
		block_errorcnt=0
		for i in range(runsim):
			
			XN=np.random.randint(2,size=N)
			XN_decoded=polarfile(XN,channel_p,design_p,I)
			
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
			
#=========================================polar file sim derate
#27-12-2017
#These are for simulations to match rateless style
#uses derating from capacity
	
#===================================================encode and decode UN
    
def polarfile_derate_sim(N,channel_p,design_p,derate,runsim,BER_needed):
	p=channel_p
	I_ord=pcon.getreliability_order(N)
	R=pl.getRatelist([channel_p],derate)[0]  #calculates rate for given channel
	G=int(R*N)
	I=I_ord[:G]
	
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	#print float(len(I))/N
	#UN=np.random.randint(2,size=G)
	#print UN
	for i in range(runsim):
		#print i
		XN=np.random.randint(2,size=N)
		XN_decoded=polarfile(XN,channel_p,design_p,I)
			
		if BER_needed:
			errcnt=errcnt+np.logical_xor(XN,XN_decoded)
			
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
				
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (ber_exp,float(G)/N,block_error)
	else:
		return (float(G)/N,block_error)


def polarfilesim_FR(N,channel_p,design_p,msg_length,runsim,BER_needed):
	p=channel_p
	I_ord=pcon.getreliability_order(N)
	G=msg_length
	I=I_ord[:G]
	
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	#print float(len(I))/N
	#UN=np.random.randint(2,size=G)
	#print UN
	for i in range(runsim):
		#print i
		XN=np.random.randint(2,size=N)
		XN_decoded=polarfile(XN,channel_p,design_p,I)
			
		if BER_needed:
			errcnt=errcnt+np.logical_xor(XN,XN_decoded)
			
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
				
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (ber_exp,float(G)/N,block_error)
	else:
		return block_error
		
def polarfilesim_FR_list(N,channel_p,design_p,msg_length,runsim,BER_needed,list_size):
	p=channel_p
	G=msg_length
	
	
	pc1=ec.polarcode_init(N,G,design_p,0)
	I_ord=pc1.channel_ordering
	I=I_ord[:G]
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	#print float(len(I))/N
	#UN=np.random.randint(2,size=G)
	#print UN
	for i in range(runsim):
		#print i
		XN=np.random.randint(2,size=N)
		#AN=np.random.randint(2,size=G)
		#FD=np.zeros(N-G,dtype=int).tolist()#frozen data
		#XN=ec.polarencodeG_C(pc1,AN.tolist(),list(FD))
		XN_decoded=polarfile_list(pc1,XN,channel_p,design_p,I,list_size)
			
		if BER_needed:
			errcnt=errcnt+np.logical_xor(XN,XN_decoded)
			
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
				
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (ber_exp,float(G)/N,block_error)
	else:
		return block_error
