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


