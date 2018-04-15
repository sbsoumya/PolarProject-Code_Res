#-------------------------------------------------------------------------------
# Name:       polarchannel.py
# Purpose:    polarcodes for channelcoding 
#             two types of simulation
#            
#
# Author:      soumya
#
# Created:     19/08/2017
# modified:    20/12/2017- 1/1/2018 week
#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
import polarconstruct as pcon
from datetime import datetime
import json
import matlib as ml
#p is channel_p

#==================Polar channel sim 
#FD and I decides outside runsim
#I sent from calling function
def polarchannelsim(N,channel_p,design_p,I,runsim,BER_needed):
	p=channel_p
	G=len(I) #number of good channels
	FD=np.zeros(N-G,dtype=int).tolist()#frozen data
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	#print float(len(I))/N
	#UN=np.random.randint(2,size=G)
	#print UN
	for i in range(runsim):
		#print i
		UN=np.random.randint(2,size=G)
		
		XN=ec.polarencodeG(UN,N,I,list(FD),False)
		
		YN=pl.BSCN(p,XN)
		UN_hat=ec.polarSCdecodeG(YN,N,design_p,I,list(FD),False)
		UN_decoded=ec.getUN(UN_hat,I,False)
		if BER_needed:
			errcnt=errcnt+np.logical_xor(UN,UN_decoded)
						
		if UN.tolist()!=UN_decoded.tolist():
			block_errorcnt+=1
		#print UN,YN,UN_decoded
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (ber_exp,block_error)
	else:
		return block_error
def polarchannelsim_FDin(N,channel_p,design_p,I,runsim,BER_needed):
	p=channel_p
	G=len(I) #number of good channels

	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	#print float(len(I))/N
	#UN=np.random.randint(2,size=G)
	#print UN
	for i in range(runsim):
		#print i
		UN=np.random.randint(2,size=G)
		FD=np.zeros(N-G,dtype=int).tolist()#frozen data
		XN=ec.polarencodeG(UN,N,I,list(FD),False)
		
		YN=pl.BSCN(p,XN)
		UN_hat=ec.polarSCdecodeG(YN,N,design_p,I,list(FD),False)
		UN_decoded=ec.getUN(UN_hat,I,False)
		if BER_needed:
			errcnt=errcnt+np.logical_xor(UN,UN_decoded)
						
		if UN.tolist()!=UN_decoded.tolist():
			block_errorcnt+=1
		#print UN,YN,UN_decoded
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (ber_exp,block_error)
	else:
		return block_error	
#=========================================polar channel sim derate
#0.04 debug 20-12-2017
#These are for simulations to match rateless style
#uses derating from capacity
	
#===================================================encode and decode UN
    
def polarchannel_derate_sim(N,channel_p,design_p,derate,runsim,BER_needed):
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
		UN=np.random.randint(2,size=G)
		FD=np.zeros(N-G,dtype=int).tolist()#frozen data
		XN=ec.polarencodeG(UN,N,I,list(FD),False)
		YN=pl.BSCN(p,XN)
		UN_hat=ec.polarSCdecodeG(YN,N,design_p,I,list(FD),False)
		UN_decoded=ec.getUN(UN_hat,I,False)
	
		if BER_needed:
			errcnt=errcnt+np.logical_xor(UN,UN_decoded)
						
		if UN.tolist()!=UN_decoded.tolist():
			block_errorcnt+=1
		#print UN,YN,UN_decoded
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (ber_exp,float(G)/N,block_error)
	else:
		return (float(G)/N,block_error)
