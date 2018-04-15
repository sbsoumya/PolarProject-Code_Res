#-------------------------------------------------------------------------------
# Name:       polar channel
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

def polarchannelsim(N,p,design_p,I,runsim,BER_needed):
	
	G=len(I) #number of good channels
	D=np.zeros(N-G,dtype=int).tolist()#frozen data
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	
	for i in range(runsim):
		UN=np.random.randint(2,size=G)
		XN=ec.polarencodeGR(UN,N,I,list(D))
		
		YN=pl.BSCN(p,XN)
		UN_hat=ec.polarSCdecodeG(YN,N,design_p,I,list(D))
		UN_decoded=ec.getUN_s(UN_hat,I)
		if BER_needed:
			errcnt=errcnt+np.logical_xor(UN,UN_decoded)
						
		if UN.tolist()!=UN_decoded.tolist():
			block_errorcnt+=1
		
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (ber_exp,block_error)
	else:
		return block_error

