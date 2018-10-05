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
N-(error_free_msg_length-T) should be number of good channels required.#same as channel coding
THERE IS NO CONCEPT OF TOP HERE.
THE LOCK IS SENT OVER THE ERROR FREE CHANNEL
THE KEY IS DECODED AND MATCHED
"""


def is_mismatch(lock,key):	
	return list(lock)!=list(key)

def send_rateless_file_Iter_retro(XN,N,I_ord,channel_p,compound_plist,Glist,T,final_boost): 
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
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(UN_N,Iter_T,False)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_UN_decoded_key=ec.getUN(Iter_UN_hat,Iter_T,False)
				
		Iter_errorfree=len(Iter_D)+len(Iter_lock)
				
		if Iter<maxiter and is_mismatch(Iter_lock,Iter_UN_decoded_key):
			Iter+=1
		else:
			decoded= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			if final_boost:
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
	errorfree_ach_rate=float(Iter_errorfree)/N 
	return (errorfree_ach_rate,return_iter,np.array(final_XN))
	
#R R/2 R/3 R/4.....		
def send_rateless_file_Iter_retro_det_sim(N,T,compound_plist_u,channel_p,error_free_msg_length,runsim,final_boost):
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
	errorfree_ach_rate=0
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		(errorfreerate_sim,Iter,XN_decoded)=send_rateless_file_Iter_retro(XN,N,I_ord,channel_p,compound_plist_u,Glist,T,final_boost)
		errorfree_ach_rate+=float(errorfreerate_sim)/runsim
						
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1	
	
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
	Fp1=N-Glist[0]	
	errorfree_used_rate=float(Fp1+T)/N	
	block_error=float(block_errorcnt)/runsim
	
	
	
	return (errorfree_used_rate,errorfree_ach_rate,block_error,Iter_probdict)

#=======================================================================UK
def send_rateless_file_Iter_retro_UK(XN,N,I_ord,channel_p,compound_plist,Glist): 
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
		#No extra T bits for checking sent over error free channel 
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		

				
		Iter_errorfree=len(Iter_D)
				
		if Iter<maxiter and is_mismatch(UN_N,Iter_UN_hat): #U is known to decoder ( both could have been reverse arikaned for comparison, not required)
			Iter+=1
		else:
			decoded= True
			
			
				
	final_Iter=Iter	
	if is_mismatch(UN_N,Iter_UN_hat): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	
	#print Iter_errorfree
	final_XN=ec.polarencode(Iter_UN_hat,N)
	errorfree_ach_rate=float(Iter_errorfree)/N 
	return (errorfree_ach_rate,return_iter,np.array(final_XN))
	
#R R/2 R/3 R/4.....		
def send_rateless_file_Iter_retro_det_UK_sim(N,compound_plist_u,channel_p,error_free_msg_length,runsim):
	#error_free_msg_length is the initial error_free_msg_length, that is the frozen bits considered+T.
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlistfile(N- (error_free_msg_length),lenG)
	
	Fp1=N-Glist[0]
	print "channel_p:"+str(channel_p)
	print "error_free_msg:"+str(Fp1)
	block_errorcnt=0
	Iter_probdict={}
	errorfree_ach_rate=0
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		(errorfreerate_sim,Iter,XN_decoded)=send_rateless_file_Iter_retro_UK(XN,N,I_ord,channel_p,compound_plist_u,Glist)
		errorfree_ach_rate+=float(errorfreerate_sim)/runsim
						
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1	
	
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
	Fp1=N-Glist[0]	
	errorfree_used_rate=float(Fp1)/N	
	block_error=float(block_errorcnt)/runsim
	
	
	
	return (errorfree_used_rate,errorfree_ach_rate,block_error,Iter_probdict)
	
#==============================================================================CRC8
	
def send_rateless_file_Iter_retro_CRC8(XN,N,I_ord,channel_p,compound_plist,Glist,T,final_boost): 
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
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(UN_N,Iter_T,False)
		UN_N_int=[int(u) for u in UN_N]
		Iter_lock_CRC=ml.getCRC(list(UN_N_int),8)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_UN_decoded_key=ec.getUN(Iter_UN_hat,Iter_T,False)
		Iter_UN_decoded_key_CRC=ml.getCRC(list(Iter_UN_hat),8)	
		Iter_errorfree=len(Iter_D)+len(Iter_lock_CRC)
				
		if Iter<maxiter and is_mismatch(Iter_lock_CRC,Iter_UN_decoded_key_CRC):
			Iter+=1
		else:
			decoded= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			if final_boost:
				Iter_I=I_ord[:Iter_G-T] # including the T bits as frozen
				Iter_F=list(set(range(N))-set(Iter_I))
				Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
				Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)
			
				
	final_Iter=Iter	
	if is_mismatch(Iter_lock_CRC,Iter_UN_decoded_key_CRC): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	
	#print Iter_errorfree
	final_XN=ec.polarencode(Iter_UN_hat,N)
	errorfree_ach_rate=float(Iter_errorfree)/N
	return (errorfree_ach_rate,return_iter,np.array(final_XN))
	
#R R/2 R/3 R/4.....		
def send_rateless_file_Iter_retro_det_CRC8_sim(N,T,compound_plist_u,channel_p,error_free_msg_length,runsim,final_boost):
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
	errorfree_ach_rate=0
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		(errorfreerate_sim,Iter,XN_decoded)=send_rateless_file_Iter_retro_CRC8(XN,N,I_ord,channel_p,compound_plist_u,Glist,T,final_boost)
		errorfree_ach_rate+=float(errorfreerate_sim)/runsim
						
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1	
	
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
	Fp1=N-Glist[0]	
	errorfree_used_rate=float(Fp1+T)/N	
	block_error=float(block_errorcnt)/runsim
	
	
	
	return (errorfree_used_rate,errorfree_ach_rate,block_error,Iter_probdict)
	
#==============================================================================CRC32
	
def send_rateless_file_Iter_retro_CRC32(XN,N,I_ord,channel_p,compound_plist,Glist,T,final_boost): 
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
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(UN_N,Iter_T,False)
		UN_N_int=[int(u) for u in UN_N]
		Iter_lock_CRC=ml.getCRC(list(UN_N_int),32)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_UN_decoded_key=ec.getUN(Iter_UN_hat,Iter_T,False)
		Iter_UN_decoded_key_CRC=ml.getCRC(list(Iter_UN_hat),32)	
		Iter_errorfree=len(Iter_D)+len(Iter_lock_CRC)
				
		if Iter<maxiter and is_mismatch(Iter_lock_CRC,Iter_UN_decoded_key_CRC):
			Iter+=1
		else:
			decoded= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			if final_boost:
				Iter_I=I_ord[:Iter_G-T] # including the T bits as frozen
				Iter_F=list(set(range(N))-set(Iter_I))
				Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
				Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)
			
				
	final_Iter=Iter	
	if is_mismatch(Iter_lock_CRC,Iter_UN_decoded_key_CRC): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	
	#print Iter_errorfree
	final_XN=ec.polarencode(Iter_UN_hat,N)
	errorfree_ach_rate=float(Iter_errorfree)/N
	return (errorfree_ach_rate,return_iter,np.array(final_XN))
	
#R R/2 R/3 R/4.....		
def send_rateless_file_Iter_retro_det_CRC32_sim(N,T,compound_plist_u,channel_p,error_free_msg_length,runsim,final_boost):
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
	errorfree_ach_rate=0
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		(errorfreerate_sim,Iter,XN_decoded)=send_rateless_file_Iter_retro_CRC32(XN,N,I_ord,channel_p,compound_plist_u,Glist,T,final_boost)
		errorfree_ach_rate+=float(errorfreerate_sim)/runsim
						
		if XN.tolist()!=XN_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1	
	
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
	Fp1=N-Glist[0]	
	errorfree_used_rate=float(Fp1+T)/N	
	block_error=float(block_errorcnt)/runsim
	
	
	
	return (errorfree_used_rate,errorfree_ach_rate,block_error,Iter_probdict)
	
	
#=======================================================================3 party

def send_rateless_file_Iter_retro_3(XN,N,I_ord,channel_p1,channel_p2,compound_plist,Glist,T,final_boost): 
	# T < deltaG
	#compound channel
    #----------------------------------------------------Iterations start
	decodedX2Y=False
	decodedY2X=False
	decodedX2Z=False
	decodedZ2X=False
	decodedY2Z=False
	decodedZ2Y=False
	maxiter=len(compound_plist)-1
	#------------------for filing Tx side
	# reverse arikan :: THIS IS OF SIZE N 
	UN_N=ec.polarencode(XN,N) 
	Iter_XN=XN
	
	YN=pl.BSCN(channel_p1,Iter_XN)
	Iter_YN=YN
	VN_N=ec.polarencode(Iter_YN,N)
	
	ZN=pl.BSCN(channel_p2,Iter_YN)
	Iter_ZN=ZN
	WN_N=ec.polarencode(Iter_ZN,N)
	
	Iter=0
	#Y decoding X
	#-------------------------------------------Forward decoding	
	 
  	while not decodedX2Y:
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		
		
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(UN_N,Iter_T,False)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_UN_decoded_key=ec.getUN(Iter_UN_hat,Iter_T,False)
				
		Iter_errorfree=len(Iter_D)+len(Iter_lock)
				
		if Iter<maxiter and is_mismatch(Iter_lock,Iter_UN_decoded_key):
			Iter+=1
		else:
			decodedX2Y= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			if final_boost:
				Iter_I=I_ord[:Iter_G-T] # including the T bits as frozen
				Iter_F=list(set(range(N))-set(Iter_I))
				Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
				Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)
			
				
	final_Iter_X2Y=Iter	
	final_Iter_F_X2Y=Iter_F
	final_Iter_p_X2Y=Iter_p
	final_Iter_I_X2Y=Iter_I
	D_X2Y=ec.getUN(UN_N,Iter_F,True) # this is transmitted to Y and Z
	final_X2Y=ec.polarencode(Iter_UN_hat,N) # should match XN at Y
	
	Iter_errorfree_X2Y=len(D_X2Y)
	err_X2Y = (final_X2Y.tolist() != XN.tolist())
	
	#X decoding Y(lock key checking not required)(channel symmetry is used)
	D_Y2X=ec.getUN(VN_N,final_Iter_F_X2Y,True) # this is transmitted to X and Z
	Y2X_VN_hat=ec.polarSCdecodeG(XN,N,final_Iter_p_X2Y,final_Iter_I_X2Y,list(D_Y2X),False)
	final_Y2X=ec.polarencode(Y2X_VN_hat,N)
	
	Iter_errorfree_Y2X=len(D_Y2X)
	err_Y2X = (final_Y2X.tolist() != YN.tolist())
	
	decodedY2X=True
	
	#Z decoding Y 
	Iter=final_Iter_X2Y 
	#-------------------------------------------Forward decoding	 
  	while not decodedY2Z:
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		
		
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(VN_N,Iter_T,False)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(VN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_VN_hat=ec.polarSCdecodeG(Iter_ZN,N,Iter_p,Iter_I,list(Iter_D),False)		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_VN_decoded_key=ec.getUN(Iter_VN_hat,Iter_T,False)
				
		Iter_errorfree=len(Iter_D)+len(Iter_lock)
				
		if Iter<maxiter and is_mismatch(Iter_lock,Iter_VN_decoded_key):
			Iter+=1
		else:
			decodedY2Z= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			if final_boost:
				Iter_I=I_ord[:Iter_G-T] # including the T bits as frozen
				Iter_F=list(set(range(N))-set(Iter_I))
				Iter_D=ec.getUN(VN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
				Iter_VN_hat=ec.polarSCdecodeG(Iter_ZN,N,Iter_p,Iter_I,list(Iter_D),False)
				
	final_Iter_Y2Z=Iter	
	final_Iter_F_Y2Z=Iter_F
	final_Iter_p_Y2Z=Iter_p
	final_Iter_I_Y2Z=Iter_I
	D_Y2Z=Iter_D
	final_Y2Z=ec.polarencode(Iter_VN_hat,N) # should match YN at Z
	
	Iter_errorfree_Y2Z=len(D_Y2Z)-len(D_Y2X) # only the extra bits transmitted, i.e, in the loop above all bits frozen for z is considered, here we subtract the bits sent from y to X
	err_Y2Z = (final_Y2Z.tolist() != YN.tolist())
	
	#Z decoding X(lock key checking not required)(it has Y now, also has previous communication from X)
	X2Z_UN_hat=ec.polarSCdecodeG(final_Y2Z,N,final_Iter_p_X2Y,final_Iter_I_X2Y,list(D_X2Y),False)
	final_X2Z=ec.polarencode(X2Z_UN_hat,N)
	
	Iter_errorfree_X2Z=0 #Nothing new is communicated , decoding uses final estimation of Y from Z and error free com sent by X for decoding at Y
	err_X2Z = (final_X2Z.tolist() != XN.tolist())
	
	decodedX2Z=True
	
	#Decoding at Z over -------------------------------------------------------
	
	#Y decoding Z(lock key checking not required)(channel symmetry is used)
	D_Z2Y=ec.getUN(WN_N,final_Iter_F_Y2Z,True) # this is transmitted to X and Y
	Z2Y_WN_hat=ec.polarSCdecodeG(YN,N,final_Iter_p_Y2Z,final_Iter_I_Y2Z,list(D_Z2Y),False)
	final_Z2Y=ec.polarencode(Z2Y_WN_hat,N)
	
	Iter_errorfree_Z2Y=len(D_Z2Y)
	err_Z2Y = (final_Z2Y.tolist() != ZN.tolist())
	
	#Decoding at Y over-------------------------------------------------------
	
	#X decoding Z
	Z2X_WN_hat=ec.polarSCdecodeG(final_Y2X,N,final_Iter_p_Y2Z,final_Iter_I_Y2Z,list(D_Z2Y),False)
	final_Z2X=ec.polarencode(Z2X_WN_hat,N)
	
	Iter_errorfree_Z2X=0 #Nothing new is communicated , decoding uses final estimation of Y from X and error free com sent by Z for decoding at Y
	err_Z2X = (final_Z2X.tolist() != ZN.tolist())
	
	decodedZ2X=True
	
	
	
	Total_error_free= (Iter_errorfree_X2Y+Iter_errorfree_Y2X)+(Iter_errorfree_Y2Z+Iter_errorfree_X2Z)+(Iter_errorfree_Z2Y+Iter_errorfree_Z2X)
	# decoding of X and Y, decoding at Z, decoding OF Z at X and Y)
	error=0
	error= (err_X2Y+err_Y2X+err_Y2Z+err_X2Z+err_Z2Y+err_Z2X) >0 
	#print error
	
	
	return (Total_error_free,error)
	
def send_rateless_file_Iter_retro_det_3_sim(N,T,compound_plist_u,channel_p1,channel_p2,error_free_msg_length,runsim,final_boost):
	#error_free_msg_length is the initial error_free_msg_length, that is the frozen bits considered+T.
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlistfile(N- (error_free_msg_length-T),lenG)
	
	Fp1=N-Glist[0] #initial errorfree (simulation monitoring param)
	print "channel_p:"+str(channel_p1)+","+str(channel_p2)
	print "error_free_msg:"+str(Fp1+T)
	block_errorcnt=0
	Iter_probdict={}
	errorfree_ach_rate=0
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		(Total_error_free,error)=send_rateless_file_Iter_retro_3(XN,N,I_ord,channel_p1,channel_p2,compound_plist_u,Glist,T,final_boost)
		errorfree_ach_rate+=float(Total_error_free)/(N*runsim) # calculates E{D}/N
						
		block_errorcnt+=error
		
	#print block_errorcnt
	block_error=float(block_errorcnt)/runsim
		
	return (errorfree_ach_rate,block_error)
	
#=======================================================================3 party general
def send_rateless_file_Iter_retro_3G(XN,N,I_ord,channel_p1,channel_p2,compound_plist,Glist,T,final_boost): 
	# T < deltaG
	#compound channel
    #----------------------------------------------------Iterations start
    #The 
    decoded={}
    decodedX2Y=False
	decodedY2X=False
	decodedX2Z=False
	decodedZ2X=False
	decodedY2Z=False
	decodedZ2Y=False
    decoded["atX"]=[decodedY2X,decodedZ2X]
    decoded["atY"]=[decodedX2Y,decodedZ2Y]
    decoded["atZ"]=[decodedX2Z,decodedY2Z]

	maxiter=len(compound_plist)-1
	#------------------for filing Tx side
	# reverse arikan :: THIS IS OF SIZE N 
	UN_N=ec.polarencode(XN,N) 
	Iter_XN=XN
	
	YN=pl.BSCN(channel_p1,Iter_XN)
	Iter_YN=YN
	VN_N=ec.polarencode(Iter_YN,N)
	
	ZN=pl.BSCN(channel_p2,Iter_YN)
	Iter_ZN=ZN
	WN_N=ec.polarencode(Iter_ZN,N)
	
	Iter=0
	#Y decoding X
	#-------------------------------------------Forward decoding	
	 
  	while not decodedX2Y:
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		
		
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(UN_N,Iter_T,False)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_UN_decoded_key=ec.getUN(Iter_UN_hat,Iter_T,False)
				
		Iter_errorfree=len(Iter_D)+len(Iter_lock)
				
		if Iter<maxiter and is_mismatch(Iter_lock,Iter_UN_decoded_key):
			Iter+=1
		else:
			decodedX2Y= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			if final_boost:
				Iter_I=I_ord[:Iter_G-T] # including the T bits as frozen
				Iter_F=list(set(range(N))-set(Iter_I))
				Iter_D=ec.getUN(UN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
				Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)
			
				
	final_Iter_X2Y=Iter	
	final_Iter_F_X2Y=Iter_F
	final_Iter_p_X2Y=Iter_p
	final_Iter_I_X2Y=Iter_I
	D_X2Y=ec.getUN(UN_N,Iter_F,True) # this is transmitted to Y and Z
	final_X2Y=ec.polarencode(Iter_UN_hat,N) # should match XN at Y
	
	Iter_errorfree_X2Y=len(D_X2Y)
	err_X2Y = (final_X2Y.tolist() != XN.tolist())
	
	#X decoding Y(lock key checking not required)(channel symmetry is used)
	D_Y2X=ec.getUN(VN_N,final_Iter_F_X2Y,True) # this is transmitted to X and Z
	Y2X_VN_hat=ec.polarSCdecodeG(XN,N,final_Iter_p_X2Y,final_Iter_I_X2Y,list(D_Y2X),False)
	final_Y2X=ec.polarencode(Y2X_VN_hat,N)
	
	Iter_errorfree_Y2X=len(D_Y2X)
	err_Y2X = (final_Y2X.tolist() != YN.tolist())
	
	decodedY2X=True
	
	#Z decoding Y 
	Iter=final_Iter_X2Y 
	#-------------------------------------------Forward decoding	 
  	while not decodedY2Z:
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		
		
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_T=I_ord[Iter_G-T:Iter_G] 	
		Iter_lock=ec.getUN(VN_N,Iter_T,False)
		#bits frozen sent over errorrfree channel
		Iter_F=list(set(range(N))-set(Iter_I)) 
		Iter_D=ec.getUN(VN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
		Iter_VN_hat=ec.polarSCdecodeG(Iter_ZN,N,Iter_p,Iter_I,list(Iter_D),False)		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_VN_decoded_key=ec.getUN(Iter_VN_hat,Iter_T,False)
				
		Iter_errorfree=len(Iter_D)+len(Iter_lock)
				
		if Iter<maxiter and is_mismatch(Iter_lock,Iter_VN_decoded_key):
			Iter+=1
		else:
			decodedY2Z= True
			#TPT booster
			#reuse the check bits in final decoding
			#could have shown including the T-bits as frozen explicitly, this is equivalent for simulation
			if final_boost:
				Iter_I=I_ord[:Iter_G-T] # including the T bits as frozen
				Iter_F=list(set(range(N))-set(Iter_I))
				Iter_D=ec.getUN(VN_N,Iter_F,True) # Note while decoding the data is assumed to be in sorted order
				Iter_VN_hat=ec.polarSCdecodeG(Iter_ZN,N,Iter_p,Iter_I,list(Iter_D),False)
				
	final_Iter_Y2Z=Iter	
	final_Iter_F_Y2Z=Iter_F
	final_Iter_p_Y2Z=Iter_p
	final_Iter_I_Y2Z=Iter_I
	D_Y2Z=Iter_D
	final_Y2Z=ec.polarencode(Iter_VN_hat,N) # should match YN at Z
	
	Iter_errorfree_Y2Z=len(D_Y2Z)-len(D_Y2X) # only the extra bits transmitted, i.e, in the loop above all bits frozen for z is considered, here we subtract the bits sent from y to X
	err_Y2Z = (final_Y2Z.tolist() != YN.tolist())
	
	#Z decoding X(lock key checking not required)(it has Y now, also has previous communication from X)
	X2Z_UN_hat=ec.polarSCdecodeG(final_Y2Z,N,final_Iter_p_X2Y,final_Iter_I_X2Y,list(D_X2Y),False)
	final_X2Z=ec.polarencode(X2Z_UN_hat,N)
	
	Iter_errorfree_X2Z=0 #Nothing new is communicated , decoding uses final estimation of Y from Z and error free com sent by X for decoding at Y
	err_X2Z = (final_X2Z.tolist() != XN.tolist())
	
	decodedX2Z=True
	
	#Decoding at Z over -------------------------------------------------------
	
	#Y decoding Z(lock key checking not required)(channel symmetry is used)
	D_Z2Y=ec.getUN(WN_N,final_Iter_F_Y2Z,True) # this is transmitted to X and Y
	Z2Y_WN_hat=ec.polarSCdecodeG(YN,N,final_Iter_p_Y2Z,final_Iter_I_Y2Z,list(D_Z2Y),False)
	final_Z2Y=ec.polarencode(Z2Y_WN_hat,N)
	
	Iter_errorfree_Z2Y=len(D_Z2Y)
	err_Z2Y = (final_Z2Y.tolist() != ZN.tolist())
	
	#Decoding at Y over-------------------------------------------------------
	
	#X decoding Z
	Z2X_WN_hat=ec.polarSCdecodeG(final_Y2X,N,final_Iter_p_Y2Z,final_Iter_I_Y2Z,list(D_Z2Y),False)
	final_Z2X=ec.polarencode(Z2X_WN_hat,N)
	
	Iter_errorfree_Z2X=0 #Nothing new is communicated , decoding uses final estimation of Y from X and error free com sent by Z for decoding at Y
	err_Z2X = (final_Z2X.tolist() != ZN.tolist())
	
	decodedZ2X=True
	
	
	
	Total_error_free= (Iter_errorfree_X2Y+Iter_errorfree_Y2X)+(Iter_errorfree_Y2Z+Iter_errorfree_X2Z)+(Iter_errorfree_Z2Y+Iter_errorfree_Z2X)
	# decoding of X and Y, decoding at Z, decoding OF Z at X and Y)
	error=0
	error= (err_X2Y+err_Y2X+err_Y2Z+err_X2Z+err_Z2Y+err_Z2X) >0 
	#print error
	
	
	return (Total_error_free,error)
	
def send_rateless_file_Iter_retro_det_3_sim(N,T,compound_plist_u,channel_p1,channel_p2,error_free_msg_length,runsim,final_boost):
	#error_free_msg_length is the initial error_free_msg_length, that is the frozen bits considered+T.
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlistfile(N- (error_free_msg_length-T),lenG)
	
	Fp1=N-Glist[0] #initial errorfree (simulation monitoring param)
	print "channel_p:"+str(channel_p1)+","+str(channel_p2)
	print "error_free_msg:"+str(Fp1+T)
	block_errorcnt=0
	Iter_probdict={}
	errorfree_ach_rate=0
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		(Total_error_free,error)=send_rateless_file_Iter_retro_3(XN,N,I_ord,channel_p1,channel_p2,compound_plist_u,Glist,T,final_boost)
		errorfree_ach_rate+=float(Total_error_free)/(N*runsim) # calculates E{D}/N
						
		block_errorcnt+=error
		
	#print block_errorcnt
	block_error=float(block_errorcnt)/runsim
		
	return (errorfree_ach_rate,block_error)
	
