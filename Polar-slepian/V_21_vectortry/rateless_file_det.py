#-------------------------------------------
# Name:       Ratelesschannel
# Purpose:    Rx knows channel
#             or lambda_threshold
#
# Author:      soumya
#
# Created:    18/09/2017
# Uses recursive encoding
#-------------------------------------------

#-----------------------------------------------------------

import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
from datetime import datetime
import json
import polarconstruct as pcon
from pprint import pprint
import matlib as ml
import copy
#import lambdathreshold as lmb
#plist=[0.04,0.15,0.2,0.25] #16 12 6 4 3
plist=[0.04,0.15,0.2,0.25] #16 12 6 4 3
#~ #deltaplist=[0.057,0.083,0.113,0.149,0.245,0.315]
#~ #deltaGlist=[700,600,500,400,300,200]
#~ deltaplist=[0.083,0.113,0.149,0.245]
#~ deltaGlist=[600,500,400,300]
#~ delta=100
	
#----------------------------------------adjusts Glist for R,R/2.. 
#===================================Glist generation	

def getGlist(MaxG,lenG): 
	lcm=ml.get_lcm_for(range(1,lenG+1))
	return [int(MaxG/lcm)*(lcm/(i+1)) for i in range(lenG)]
	
def getGlistfile(MaxG,lenG): 
	return [int(MaxG/(i+1)) for i in range(lenG)]

def getdeltaGlist(MaxG,lenG,deltaG):
	if MaxG >= 2*(lenG-1)*deltaG:
		return range(MaxG,MaxG-lenG*deltaG,-deltaG)
	else:
		print "Error: R< 2(K-1)*delta" 
		print MaxG,lenG,deltaG
		return 0

#=======================================================================Detection bits
"""
Error free rate:
The rate of communication required on error-free channel
It includes the frozen bits and T bits for checking
Let Fp1 be the assumed frozen bits on first iteration
N-Fp1 is the number of goodchannels needed.
N-Fp1-T is number of info bits transferred if channel coding is considered.
this was considered as msg_length in channel coding.
error free msg_length will be Fp1+T.
N-(error_free_msg_length-T) should be number of good channels required.
"""


def is_mismatch(lock,key):	
	return list(lock)!=list(key)

def send_rateless_file_Iter_retro(XN,N,I_ord,channel_p,compound_plist,Glist,T): 
	# T < deltaG
	#compound channel
    #----------------------------------------------------Iterations start
	decoded=False
	maxiter=len(compound_plist)-1
	#------------------for filing Tx side
	# reverse arikan :: THIS IS OF SIZE N 
	UN_N=ec.polarencode(XN,N) 
	Iter_XN=XN
	Iter_YN=pl.BSCN(channel_p,Iter_XN)
	Iter=0
	#-------------------------------------------Forward decoding	
  	while not decoded:
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		
		
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(UN_N,Iter_T,False)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		Iter_UN_decoded_key=ec.getUN(Iter_UN_hat,Iter_T,False)
				
		Iter_errorfree=len(Iter_D)+len(Iter_lock)
				
		if Iter<maxiter and is_mismatch(Iter_lock,Iter_UN_decoded_key):
			Iter+=1
		else:
			decoded= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			Iter_I=I_ord[:Iter_G-T] # including the T bits as frozen
			Iter_F=list(set(range(N))-set(Iter_I))
			Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
			Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)
			
				
	final_Iter=Iter	
	if is_mismatch(Iter_lock,Iter_UN_decoded_key): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	
	#print Iter_errorfree
	final_XN=ec.polarencode(Iter_UN_hat,N)
	errorfree_rate=float(Iter_errorfree)/N #corrected
	return (errorfree_rate,return_iter,np.array(final_XN))
	
#R R/2 R/3 R/4.....		
def send_rateless_file_Iter_retro_det_sim(N,T,compound_plist_u,channel_p,error_free_msg_length,runsim):
	#error_free_msg_length is the initial error_free_msg_length, that is the frozen bits considered+T.
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlistfile(N- (error_free_msg_length-T),lenG)
	
	Fp1=N-Glist[0]
	print "channel_p:"+str(channel_p)
	print "error_free_msg:"+str(Fp1+T)
	block_errorcnt=0
	Iter_probdict={}
	errorfree_rate=0
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		(errorfreerate_sim,Iter,XN_decoded)=send_rateless_file_Iter_retro(XN,N,I_ord,channel_p,compound_plist_u,Glist,T)
		errorfree_rate+=float(errorfreerate_sim)/runsim
						
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1	
	
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
	Fp1=N-Glist[0]	
	used_rate=float(Fp1+T)/N	
	block_error=float(block_errorcnt)/runsim
	
	
	
	return (used_rate,errorfree_rate,block_error,Iter_probdict)
	
