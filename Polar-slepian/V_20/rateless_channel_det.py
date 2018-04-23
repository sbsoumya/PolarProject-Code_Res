#-------------------------------------------
# Name:       Ratelesschannel_detection bits
# Purpose:    Detection bits
#
# Author:      soumya
#
# Created:    22/03/2018
#NOTE this library has hard coded rates and p's to alter use
#derate style coding 
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

#===================================Glist generation	
#adjusts Glist for R,R/2.. 
#Max G in Glist might not be a part of output
#msglength must be max of the output
def getGlist(MaxG,lenG): 
	lcm=ml.get_lcm_for(range(1,lenG+1))
	return [int(MaxG/lcm)*(lcm/(i+1)) for i in range(lenG)]

#print getGlist(540,5)
#adjusts Glist for delta
#max G is a part of the output 
#hence msglength=max G is ok
def getdeltaGlist(MaxG,lenG,deltaG):
	if MaxG >= 2*(lenG-1)*deltaG:
		return range(MaxG,MaxG-lenG*deltaG,-deltaG)
	else:
		print "Error: R< 2(K-1)*delta" 
		print MaxG,lenG,deltaG
		return 0
		
#print getdeltaGlist(70,7,10)

#=======================================================================Detectionbits	

def is_mismatch(lock,key):	
	return lock!=key
	
def send_rateless_det(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist): 
    
    #Adding detection bits
    # T is lock and Key length
   	UN_lock=list(UN_msg)[:T]
   	key_ind=range(Glist[0]-T,Glist[0])
	UN=np.array(list(UN_msg)+UN_lock) # lock added as key
	#print UN
	
	
	maxiter=len(compound_plist)-1
  
	#----------------------------------------------------Iterations start
	Iterhistory={} #contains indexes of UN sent in each iteration
	decoded=False
	
	# for first Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(len(UN))
	
    
	#print "Forward decoding"		
	while not decoded :
		
		Iter_UN=[UN[i] for i in Iter_UN_ind]
		 
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeG(Iter_UN,N,Iter_I,list(Iter_D),False)   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		Iter_UN_decoded=ec.getUN(Iter_UN_hat,Iter_I,False)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		#print Iterhistory
		
		#Extracting Lock (in first iter only)
		if Iter==0:
			UN_decoded_lock=list(Iter_UN_decoded)[:T] # received lock
		
		#print UN_decoded_lock
		#picking det
		Iter_det_pat=np.zeros(Glist[0])-1 #(is of length UN)
		for i in range(Iter+1):
			for t in key_ind:
				
				if t in Iter_UN_ind:
					
					Iter_det_pat[t]=Iterhistory[i][1][Iter_UN_ind.index(t)]
				
		#print Iter_det_pat
		Iter_UN_decoded_key=list(Iter_det_pat)[-T:]		
		
		
		#print Iter_UN_decoded_key
		if is_mismatch(UN_decoded_lock,Iter_UN_decoded_key) and Iter<maxiter:
			
			
			# picking out all the channels that are suspected to be bad in past
			# iterations and putting them for next iteration.
			# Note first iteration Whole UN is sent
			# in next only suspected bad channels are sent
			prev_I=Iter_I
			Iter+=1
			
			#New channel params
			Iter_p=compound_plist[Iter]
			Iter_G=Glist[Iter]
			Iter_I=I_ord[:Iter_G]
			
			tosend_ind=[]
			for i in range(Iter):
				
				#picking out the bad channels from prev iterations
				sent_ind=Iterhistory[i][0]
				sent_ind_last_iter=sent_ind[:Glist[Iter-1]]
				bad_ind=sent_ind_last_iter[Iter_G:]
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind=list(set(tosend_ind))
			Iter_UN_ind.sort()
			
			
			
		else:
			#the final reliable good channels is that of last iteration
			final_Iter=Iter
			final_G=Iter_G
			#channel_p is already updated
			final_p=Iter_p
			final_I=I_ord[:final_G]
			decoded= True
			
	#pprint(Iterhistory)
	#-----------------------------------------Retro decoding
	for Iter in range(final_Iter-1,-1,-1):
			
			# note INC_FREEZE and FROZEN zeroes are treated seperately
			Prev_correct_ind=Iterhistory[Iter+1][0]
			Prev_correct_data=Iterhistory[Iter+1][1]
			
			#PICKING INC FROZEN NEEDED FOR THIS ITERATION
			IncFreeze_ind_UN=[i for i in Prev_correct_ind if i in Iterhistory[Iter][0]] #picking the indexes of the prev iter frozen data needed FOR DECODING in this iter i.e, 12
			#picking the data i.e. u12
			IncFreeze_ind_ind=[Prev_correct_ind.index(j) for j in IncFreeze_ind_UN]
			IncFreeze_data=[Prev_correct_data[k] for k in IncFreeze_ind_ind]
			
			#finding the channels where 12 went in this iter 16 15 14 "13"<--- here
			#i.e, removing the top channel_G channels (as they are good) from top Iter_i_G channels
			Iter_G=Glist[Iter]
			IncFreeze_ind=I_ord[:Iter_G][final_G:]
		
			#print "Frozen zeroes"
			Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data as per iteration
							
			Iter_YN=Iterhistory[Iter][2]
			Iter_UN_hat=ec.polarIncFrzSCdecodeG(Iter_YN,N,final_p,final_I,list(Iter_D),IncFreeze_ind,IncFreeze_data,False)
			Iter_UN_decoded=ec.getUN(Iter_UN_hat,final_I,False)
			
			#print Iter_UN_decoded
			
			#history update
			Iterhistory_ind_upd=list(Prev_correct_ind)
			Iterhistory_ind_upd.extend(Iterhistory[Iter][0][:final_G]) #ie adding 5,6,11 to 4,10,12
			Iterhistory_data_upd=np.hstack((Prev_correct_data,Iter_UN_decoded)) #same as extend
			(Iterhistory[Iter][0],Iterhistory[Iter][1])=ml.sortAextend(Iterhistory_ind_upd,Iterhistory_data_upd.tolist())
		
	#pprint(Iterhistory)
	final_decoded= Iterhistory[0][1]
	#return_iter=final_Iter+1
	if is_mismatch(UN_decoded_lock,Iter_UN_decoded_key): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	
	final_UN_msg=final_decoded[:Glist[0]-T]
	achieved_rate=float(len(UN_msg))/((final_Iter+1)*N)
	return (achieved_rate,return_iter,np.array(final_UN_msg))
	
#R R/2 R/3 R/4.....		
def send_rateless_det_sim(N,T,compound_plist_u,channel_p,msg_length,runsim): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlist(msg_length+T,lenG)
	
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	print "msg_length:"+str(Glist[0]-T)
	print "channel_p:"+str(channel_p)
	
	for i in range(runsim):
		UN_msg=np.random.randint(2,size=Glist[0]-T)
		(achievedrate_sim,Iter,UN_msg_decoded)=send_rateless_det(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist)
		achievedrate+=float(achievedrate_sim)/runsim
		if UN_msg.tolist()!=UN_msg_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1
			
	used_rate=float(Glist[0]-T)/N	
	block_error=float(block_errorcnt)/runsim
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
		
	return (used_rate,achievedrate,block_error,Iter_probdict)


#=====================================================================================================step_retro	
def Iter_retro_decode(Iterhistory_original,this_Iter,N,I_ord,Glist,this_Iter_G,this_Iter_p,this_Iter_I):	
	Iterhistory=copy.deepcopy(Iterhistory_original)
	#-----------------------------------------Retro decoding
	for Iter in range(this_Iter-1,-1,-1):
			
			# note INC_FREEZE and FROZEN zeroes are treated seperately
			Prev_correct_ind=Iterhistory[Iter+1][0]
			Prev_correct_data=Iterhistory[Iter+1][1]
			
			#PICKING INC FROZEN NEEDED FOR THIS ITERATION
			IncFreeze_ind_UN=[i for i in Prev_correct_ind if i in Iterhistory[Iter][0]] #picking the indexes of the prev iter frozen data needed FOR DECODING in this iter i.e, 12
			#picking the data i.e. u12
			IncFreeze_ind_ind=[Prev_correct_ind.index(j) for j in IncFreeze_ind_UN]
			IncFreeze_data=[Prev_correct_data[k] for k in IncFreeze_ind_ind]
			
			#finding the channels where 12 went in this iter 16 15 14 "13"<--- here
			#i.e, removing the top channel_G channels (as they are good) from top Iter_i_G channels
			Iter_G=Glist[Iter]
			IncFreeze_ind=I_ord[:Iter_G][this_Iter_G:]
		
			#print "Frozen zeroes"
			Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data as per iteration
							
			Iter_YN=Iterhistory[Iter][2]
			Iter_UN_hat=ec.polarIncFrzSCdecodeG(Iter_YN,N,this_Iter_p,this_Iter_I,list(Iter_D),IncFreeze_ind,IncFreeze_data,False)
			Iter_UN_decoded=ec.getUN(Iter_UN_hat,this_Iter_I,False)
			
			#print Iter_UN_decoded
			
			#history update
			Iterhistory_ind_upd=list(Prev_correct_ind)
			Iterhistory_ind_upd.extend(Iterhistory[Iter][0][:this_Iter_G]) #ie adding 5,6,11 to 4,10,12
			Iterhistory_data_upd=np.hstack((Prev_correct_data,Iter_UN_decoded)) #same as extend
			(Iterhistory[Iter][0],Iterhistory[Iter][1])=ml.sortAextend(Iterhistory_ind_upd,Iterhistory_data_upd.tolist())
	#print "retro decode"
	#print Iterhistory
	return Iterhistory[0][1]
	
def send_rateless_det_Iter_retro(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist): 
    
    #Adding detection bits
    # T is lock and Key length
   	UN_lock=list(UN_msg)[:T]
   	key_ind=range(Glist[0]-T,Glist[0])
	UN=np.array(list(UN_msg)+UN_lock) # lock added as key
	#print UN
	
	
	maxiter=len(compound_plist)-1
    #the rate considered for the true channel
	#G=Glist[compound_plist.index(channel_p)]
	#----------------------------------------------------Iterations start
	Iterhistory={} #contains indexes of UN sent in each iteration
	decoded=False
	
	# for first Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(len(UN))
	
    
	#print "Forward decoding"		
	while not decoded :
		
		Iter_UN=[UN[i] for i in Iter_UN_ind]
		 
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeG(Iter_UN,N,Iter_I,list(Iter_D),False)   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		Iter_UN_decoded=ec.getUN(Iter_UN_hat,Iter_I,False)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		#print Iterhistory
		
		
		
		Iter_UN_retro_decoded=Iter_retro_decode(Iterhistory,Iter,N,I_ord,Glist,Iter_G,Iter_p,Iter_I)
		#print Iterhistory
		#Extracting Lock lock and key
		Iter_UN_decoded_lock=list(Iter_UN_retro_decoded)[:T] # updated lock
		Iter_UN_decoded_key=list(Iter_UN_retro_decoded)[-T:]		
		
		#print Iter_UN_retro_decoded 
		#print Iter_UN_decoded_lock
		#print Iter_UN_decoded_key
		
		#print Iter_UN_decoded_key
		if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key) and Iter<maxiter:
			
			
			# picking out all the channels that are suspected to be bad in past
			# iterations and putting them for next iteration.
			# Note first iteration Whole UN is sent
			# in next only suspected bad channels are sent
			prev_I=Iter_I
			Iter+=1
			
			#New channel params
			Iter_p=compound_plist[Iter]
			Iter_G=Glist[Iter]
			Iter_I=I_ord[:Iter_G]
			
			tosend_ind=[]
			for i in range(Iter):
				
				#picking out the bad channels from prev iterations
				sent_ind=Iterhistory[i][0]
				sent_ind_last_iter=sent_ind[:Glist[Iter-1]]
				bad_ind=sent_ind_last_iter[Iter_G:]
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind=list(set(tosend_ind))
			Iter_UN_ind.sort()
			
			
			
		else:
			decoded= True
			
			
	
	#final==================================
	final_Iter=Iter
	if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	final_decoded=Iter_UN_retro_decoded
	final_UN_msg=final_decoded[:Glist[0]-T]
	achieved_rate=float(len(UN_msg))/((final_Iter+1)*N)
	return (achieved_rate,return_iter,np.array(final_UN_msg))

def send_rateless_det_Iter_retro_sim(N,T,compound_plist_u,channel_p,msg_length,runsim): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlist(msg_length+T,lenG)
	
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	print "msg_length:"+str(Glist[0]-T)
	print "channel_p:"+str(channel_p)
	
	for i in range(runsim):
		UN_msg=np.random.randint(2,size=Glist[0]-T)
		(achievedrate_sim,Iter,UN_msg_decoded)=send_rateless_det_Iter_retro(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist)
		achievedrate+=float(achievedrate_sim)/runsim
		if UN_msg.tolist()!=UN_msg_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1
			
	used_rate=float(Glist[0]-T)/N	
	block_error=float(block_errorcnt)/runsim
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
		
	return (used_rate,achievedrate,block_error,Iter_probdict)
	
def getGGlist(msglengthhigh,msglengthlow,step,lenG,T):
	#print  [msg_length+T for msg_length in np.arange(msglengthlow,msglengthhigh,step)]
	return [getGlist(msg_length+T,lenG) for msg_length in np.arange(msglengthlow,msglengthhigh,step)]


def send_rateless_det_Iter_retro_itracker_sim(N,T,compound_plist_u,channel_p,msglengthhigh,msglengthlow,step,runsim): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	GGlist=getGGlist(msglengthhigh,msglengthlow,step,lenG,T)
	#print GGlist
	Gears=len(GGlist)-1
	gear=Gears
	
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	#print "msg_length:"+str(Glist[0]-T)
	print "channel_p:"+str(channel_p)
	gearcnt=0
	for i in range(runsim):
		Glist=GGlist[gear]
		gearcnt=gearcnt+Glist[0]	
		UN_msg=np.random.randint(2,size=Glist[0]-T)
		(achievedrate_sim,Iter,UN_msg_decoded)=send_rateless_det_Iter_retro(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist)
		achievedrate+=float(achievedrate_sim)/runsim
		if UN_msg.tolist()!=UN_msg_decoded.tolist():
			block_errorcnt+=1
		if Iter==0:
			if gear>0:
				gear-=1
		else:
			if gear<Gears:
				gear+=1
	print float(gearcnt)/runsim	
			
	#used_rate=float(Glist[0]-T)/N	
	block_error=float(block_errorcnt)/runsim
			
	return (achievedrate,block_error)


#================================================================================Delta with step retro
def Iter_retro_decode_delta(Iterhistory_original,this_Iter,N,I_ord,Glist,this_Iter_G,this_Iter_p,this_Iter_I):	
	Iterhistory=copy.deepcopy(Iterhistory_original)
	#-----------------------------------------Retro decoding
	for Iter in range(this_Iter-1,-1,-1):
			
			# note INC_FREEZE and FROZEN zeroes are treated seperately
			Prev_correct_ind=Iterhistory[Iter+1][0]
			Prev_correct_data=Iterhistory[Iter+1][1]
			
			#PICKING INC FROZEN NEEDED FOR THIS ITERATION
			IncFreeze_ind_UN=[i for i in Prev_correct_ind if i in Iterhistory[Iter][0]] #picking the indexes of the prev iter frozen data needed FOR DECODING in this iter i.e, 12
			#picking the data i.e. u12
			IncFreeze_ind_ind=[Prev_correct_ind.index(j) for j in IncFreeze_ind_UN]
			IncFreeze_data=[Prev_correct_data[k] for k in IncFreeze_ind_ind]
			
			#finding the channels where 12 went in this iter 16 15 14 "13"<--- here
			#i.e, removing the top channel_G channels (as they are good) from top Iter_i_G channels
			Iter_G=Glist[Iter]
			IncFreeze_ind=I_ord[:Iter_G][this_Iter_G:]
		
			#print "Frozen zeroes"
			Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data as per iteration
							
			Iter_YN=Iterhistory[Iter][2]
			Iter_UN_hat=ec.polarIncFrzSCdecodeG(Iter_YN,N,this_Iter_p,this_Iter_I,list(Iter_D),IncFreeze_ind,IncFreeze_data,False)
			Iter_UN_decoded=ec.getUN(Iter_UN_hat,this_Iter_I,False)
			
			#print Iter_UN_decoded
			
			#history update
			Iterhistory_ind_upd=list(Prev_correct_ind)
			Iterhistory_ind_upd.extend(Iterhistory[Iter][0][:this_Iter_G]) #ie adding 5,6,11 to 4,10,12
			Iterhistory_data_upd=np.hstack((Prev_correct_data,Iter_UN_decoded)) #same as extend
			(Iterhistory[Iter][0],Iterhistory[Iter][1])=ml.sortAextend(Iterhistory_ind_upd,Iterhistory_data_upd.tolist())
	#~ print "retro decode"
	#~ print Iterhistory

	return (Iterhistory[0][0],Iterhistory[0][1])

def send_rateless_det_Iter_retro_delta(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist,deltaG):
	#delta G need not be mentioned.explicit argument for readability
    
    #Adding detection bits
    # T is lock and Key length
	UN_msg=list(UN_msg)
   	UN_lock=UN_msg[:T]
   	key_ind=range(Glist[0]-T,Glist[0])
   	UN=np.array(UN_msg+UN_lock) # lock added as key
   	UN_msg_length=len(UN_msg)
   	UN_msg_ind=range(UN_msg_length)
	#~ print UN
	
	maxiter=len(compound_plist)-1

	#----------------------------------------------------Iterations start
	Iterhistory={} #contains indexes of UN sent in each iteration
	decoded=False
	
	# for first Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(Glist[0])
	Iter_key_ind=key_ind
    
	while not decoded :
		#~ print Iter_G
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeG(Iter_UN,N,Iter_I,list(Iter_D),False)   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		Iter_UN_decoded=ec.getUN(Iter_UN_hat,Iter_I,False)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		
		#~ print "forward"
		#~ print Iterhistory
		
		#updating decoded UN wrt results of present iteration
		(Iter_UN_retro_decoded_ind,Iter_UN_retro_decoded)=Iter_retro_decode_delta(Iterhistory,Iter,N,I_ord,Glist,Iter_G,Iter_p,Iter_I)
		
		
		#Extracting Lock lock and key
		Iter_UN_decoded_lock=list(Iter_UN_retro_decoded)[:T] # updated lock
		Iter_UN_decoded_key=ml.extract_data(Iter_UN_retro_decoded_ind,Iter_UN_retro_decoded,key_ind)	
		
		#~ print Iter_UN_retro_decoded 
		#~ print Iter_UN_decoded_lock
		#~ print Iter_UN_decoded_key
	
		if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key) and Iter<maxiter:
			
			
			# picking out all the channels that are suspected to be bad in past
			# iterations and putting them for next iteration.
			# Note first iteration Whole UN is sent
			# in next only suspected bad channels are sent
			prev_I=Iter_I
			Iter+=1
			prev_Iter_key_ind=list(Iter_key_ind)
			
			#New channel params
			Iter_p=compound_plist[Iter]
			Iter_G=Glist[Iter]
			Iter_I=I_ord[:Iter_G]
			
			tosend_ind=[]
			for i in range(Iter):
			
				#picking out the bad channels from prev iterations
				sent_ind=Iterhistory[i][0]
				sent_ind_last_iter=sent_ind[:Glist[Iter-1]]
				bad_ind=sent_ind_last_iter[Iter_G:]
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind_retran=list(set(tosend_ind))
			Iter_UN_ind_retran.sort()
			Iter_key_ind=[]
			
			#construction of Iter_UN
			#removing Key indices from retran indices
			for t in prev_Iter_key_ind:
				try:
					Iter_UN_ind_retran.remove(t)
					Iter_key_ind.append(t)
				except:
					pass
			
					
			#picking retran data
			#~ print len(UN_msg)
			#~ print Iter_UN_ind_retran
			Iter_UN_retran=ml.extract_data(UN_msg_ind,UN_msg,Iter_UN_ind_retran)
			
			
			#filler
			Iter_filler_length=Iter_G-Iter*deltaG
			Iter_UN_ind_filler=range(UN_msg_length+T,UN_msg_length+Iter_filler_length+T)
			Iter_UN_filler=list(np.random.randint(2,size=Iter_G-Iter*deltaG))
			
			#~ print "indices"
			#~ print Iter_UN_ind_retran
			#~ print Iter_UN_ind_filler
			#~ print Iter_key_ind
			
			#~ print "retran and new data"			
			#~ print Iter_UN_retran
			#~ print Iter_UN_filler
			
			

			#Iter_UN
			Iter_UN=list(Iter_UN_retran)+list(Iter_UN_filler)+list(UN_lock) # adding lock at end
			Iter_UN_ind=list(Iter_UN_ind_retran)+list(Iter_UN_ind_filler)+list(Iter_key_ind)
			#print Iter_UN_ind
			#~ print "Present UN"
			#~ print UN_msg_ind
			#~ print UN_msg
			#~ print Iter_UN_filler
			#~ print "Iter_UN"
			#~ print Iter_UN
			#update UN_msg, will be returned for error checking
			UN_msg.extend(Iter_UN_filler)
			UN_msg_ind.extend(Iter_UN_ind_filler)
			#~ print "new UN_msg_ind"
			#~ print UN_msg_ind
			#~ print UN_msg
			#~ print Iter_UN_filler
			UN_msg_length=len(UN_msg)
				
		else:
			decoded= True
	
	#final==================================
	final_Iter=Iter
	if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
			return_iter=final_Iter+1
	final_decoded=Iter_UN_retro_decoded
	final_indices=Iter_UN_retro_decoded_ind
	final_UN_msg=ml.extract_otherdata(final_indices,final_decoded,key_ind) #The data in Iter 0 is sorted
	achieved_rate=float(UN_msg_length)/((final_Iter+1)*N)
	return (achieved_rate,return_iter,np.array(UN_msg),np.array(final_UN_msg))

def send_rateless_det_Iter_retro_delta_sim(N,T,compound_plist_u,channel_p,msg_length,deltaG,runsim): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getdeltaGlist(msg_length+T,lenG,deltaG)
	
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	
	print "msg_length:"+str(msg_length)
	print "channel_p:"+str(channel_p)
	for i in range(runsim):
		UN_msg=np.random.randint(2,size=msg_length)
		(achievedrate_sim,Iter,UN_msg_sent,UN_msg_decoded)=send_rateless_det_Iter_retro_delta(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist,deltaG)
		achievedrate+=float(achievedrate_sim)/runsim
		if UN_msg_sent.tolist()!=UN_msg_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1
			
	used_rate=float(len(UN_msg_sent))/N	# has no meaning
	block_error=float(block_errorcnt)/runsim
	
	#print block_errorcnt
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
		
	return (used_rate,achievedrate,block_error,Iter_probdict)
	
#=============================================================================CRC
"""
For CRC , a CRC of the UN_nsg it transmitted as key
At every iteration this is extracted, The CRC is calculated and both are matched
with Iter retro UN_msg is retro decoded and CRC is calculated
"""
def send_rateless_det_Iter_retro_CRC(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist): 
    
    #Adding detection bits
    # T is lock and Key length
   	UN_lock=ml.getCRC(UN_msg,T)
   	key_ind=range(Glist[0]-T,Glist[0])
	UN=np.array(list(UN_msg)+UN_lock) # lock added as key
	#print UN
	
	
	maxiter=len(compound_plist)-1
    #the rate considered for the true channel
	#G=Glist[compound_plist.index(channel_p)]
	#----------------------------------------------------Iterations start
	Iterhistory={} #contains indexes of UN sent in each iteration
	decoded=False
	
	# for first Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(len(UN))
	
    
	#print "Forward decoding"		
	while not decoded :
		
		Iter_UN=[UN[i] for i in Iter_UN_ind]
		 
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeG(Iter_UN,N,Iter_I,list(Iter_D),False)   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		Iter_UN_decoded=ec.getUN(Iter_UN_hat,Iter_I,False)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		#print Iterhistory
		
		
		
		Iter_UN_retro_decoded=Iter_retro_decode(Iterhistory,Iter,N,I_ord,Glist,Iter_G,Iter_p,Iter_I)
		#print Iterhistory
		#Extracting Lock lock and key
		Iter_UN_decoded_lock=ml.getCRC(list(Iter_UN_retro_decoded)[:Glist[0]-T],T) # calculating CRC
		Iter_UN_decoded_key=list(Iter_UN_retro_decoded)[-T:] #received CRC	
		
		#print Iter_UN_retro_decoded 
		#print Iter_UN_decoded_lock
		#print Iter_UN_decoded_key
		
		#print Iter_UN_decoded_key
		if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key) and Iter<maxiter:
			
			
			# picking out all the channels that are suspected to be bad in past
			# iterations and putting them for next iteration.
			# Note first iteration Whole UN is sent
			# in next only suspected bad channels are sent
			prev_I=Iter_I
			Iter+=1
			
			#New channel params
			Iter_p=compound_plist[Iter]
			Iter_G=Glist[Iter]
			Iter_I=I_ord[:Iter_G]
			
			tosend_ind=[]
			for i in range(Iter):
				
				#picking out the bad channels from prev iterations
				sent_ind=Iterhistory[i][0]
				sent_ind_last_iter=sent_ind[:Glist[Iter-1]]
				bad_ind=sent_ind_last_iter[Iter_G:]
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind=list(set(tosend_ind))
			Iter_UN_ind.sort()
			
			
			
		else:
			decoded= True
			
			
	
	#final==================================
	final_Iter=Iter
	if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	final_decoded=Iter_UN_retro_decoded
	final_UN_msg=final_decoded[:Glist[0]-T]
	achieved_rate=float(len(UN_msg))/((final_Iter+1)*N)
	return (achieved_rate,return_iter,np.array(final_UN_msg))

def send_rateless_det_Iter_retro_CRC_sim(N,T,compound_plist_u,channel_p,msg_length,runsim): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlist(msg_length+T,lenG)
	
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	
	print "msg_length:"+str(Glist[0]-T)
	print "channel_p:"+str(channel_p)
	
	for i in range(runsim):
		UN_msg=np.random.randint(2,size=Glist[0]-T)
		(achievedrate_sim,Iter,UN_msg_decoded)=send_rateless_det_Iter_retro_CRC(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist)
		achievedrate+=float(achievedrate_sim)/runsim
		if UN_msg.tolist()!=UN_msg_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1
			
	used_rate=float(Glist[0]-T)/N	
	block_error=float(block_errorcnt)/runsim
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
		
	return (used_rate,achievedrate,block_error,Iter_probdict)
#================================================================================CRC-delta
def send_rateless_det_Iter_retro_delta_CRC(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist,deltaG):
	#delta G need not be mentioned.explicit argument for readability
    
    #Adding detection bits
    # T is lock and Key length
	UN_msg=list(UN_msg)
   	UN_lock=ml.getCRC(UN_msg,T)
   	key_ind=range(Glist[0]-T,Glist[0])
   	UN=np.array(UN_msg+UN_lock) # lock added as key
   	UN_msg_length=len(UN_msg)
   	UN_msg_ind=range(UN_msg_length)
	#~ print UN
	#CRC is always calculated on the first msg
	InputtoCRC_ind=range(UN_msg_length)
	
	maxiter=len(compound_plist)-1

	#----------------------------------------------------Iterations start
	Iterhistory={} #contains indexes of UN sent in each iteration
	decoded=False
	
	# for first Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(Glist[0])
	Iter_key_ind=key_ind
    
	while not decoded :
		#~ print Iter_G
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeG(Iter_UN,N,Iter_I,list(Iter_D),False)   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),False)		
		Iter_UN_decoded=ec.getUN(Iter_UN_hat,Iter_I,False)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		
		#~ print "forward"
		#~ print Iterhistory
		
		#updating decoded UN wrt results of present iteration
		(Iter_UN_retro_decoded_ind,Iter_UN_retro_decoded)=Iter_retro_decode_delta(Iterhistory,Iter,N,I_ord,Glist,Iter_G,Iter_p,Iter_I)
		
		
		#Extracting Lock and key
		Iter_UN_decoded_lock=list(Iter_UN_retro_decoded)[:T] # updated lock
		
		
		#Extracting Lock lock and key
		Iter_UN_decoded_lock=ml.getCRC(ml.extract_data(Iter_UN_retro_decoded_ind,Iter_UN_retro_decoded,InputtoCRC_ind),T) # calculating CRC
		Iter_UN_decoded_key=ml.extract_data(Iter_UN_retro_decoded_ind,Iter_UN_retro_decoded,key_ind)	#received CRC
		
		#~ print Iter_UN_retro_decoded 
		#~ print Iter_UN_decoded_lock
		#~ print Iter_UN_decoded_key
	
		if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key) and Iter<maxiter:
			
			
			# picking out all the channels that are suspected to be bad in past
			# iterations and putting them for next iteration.
			# Note first iteration Whole UN is sent
			# in next only suspected bad channels are sent
			prev_I=Iter_I
			Iter+=1
			prev_Iter_key_ind=list(Iter_key_ind)
			
			#New channel params
			Iter_p=compound_plist[Iter]
			Iter_G=Glist[Iter]
			Iter_I=I_ord[:Iter_G]
			
			tosend_ind=[]
			for i in range(Iter):
			
				#picking out the bad channels from prev iterations
				sent_ind=Iterhistory[i][0]
				sent_ind_last_iter=sent_ind[:Glist[Iter-1]]
				bad_ind=sent_ind_last_iter[Iter_G:]
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind_retran=list(set(tosend_ind))
			Iter_UN_ind_retran.sort()
			Iter_key_ind=[]
			
			#construction of Iter_UN
			#removing Key indices from retran indices
			for t in prev_Iter_key_ind:
				try:
					Iter_UN_ind_retran.remove(t)
					Iter_key_ind.append(t)
				except:
					pass
			
					
			#picking retran data
			#~ print len(UN_msg)
			#~ print Iter_UN_ind_retran
			Iter_UN_retran=ml.extract_data(UN_msg_ind,UN_msg,Iter_UN_ind_retran)
			
			
			#filler
			Iter_filler_length=Iter_G-Iter*deltaG
			Iter_UN_ind_filler=range(UN_msg_length+T,UN_msg_length+Iter_filler_length+T)
			Iter_UN_filler=list(np.random.randint(2,size=Iter_G-Iter*deltaG))
			
			#~ print "indices"
			#~ print Iter_UN_ind_retran
			#~ print Iter_UN_ind_filler
			#~ print Iter_key_ind
			
			#~ print "retran and new data"			
			#~ print Iter_UN_retran
			#~ print Iter_UN_filler
			
			

			#Iter_UN
			Iter_UN=list(Iter_UN_retran)+list(Iter_UN_filler)+list(UN_lock) # adding lock at end
			Iter_UN_ind=list(Iter_UN_ind_retran)+list(Iter_UN_ind_filler)+list(Iter_key_ind)
			#print Iter_UN_ind
			#~ print "Present UN"
			#~ print UN_msg_ind
			#~ print UN_msg
			#~ print Iter_UN_filler
			#~ print "Iter_UN"
			#~ print Iter_UN
			#update UN_msg, will be returned for error checking
			UN_msg.extend(Iter_UN_filler)
			UN_msg_ind.extend(Iter_UN_ind_filler)
			#~ print "new UN_msg_ind"
			#~ print UN_msg_ind
			#~ print UN_msg
			#~ print Iter_UN_filler
			UN_msg_length=len(UN_msg)
				
		else:
			decoded= True
	
	#final==================================
	final_Iter=Iter
	if is_mismatch(Iter_UN_decoded_lock,Iter_UN_decoded_key): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
			return_iter=final_Iter+1
	final_decoded=Iter_UN_retro_decoded
	final_indices=Iter_UN_retro_decoded_ind
	final_UN_msg=ml.extract_otherdata(final_indices,final_decoded,key_ind) #The data in Iter 0 is sorted
	achieved_rate=float(UN_msg_length)/((final_Iter+1)*N)
	return (achieved_rate,return_iter,np.array(UN_msg),np.array(final_UN_msg))

def send_rateless_det_Iter_retro_delta_CRC_sim(N,T,compound_plist_u,channel_p,msg_length,deltaG,runsim): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getdeltaGlist(msg_length+T,lenG,deltaG)
	
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	print "msg_length:"+str(msg_length)
	print "channel_p:"+str(channel_p)
	for i in range(runsim):
		UN_msg=np.random.randint(2,size=msg_length)
		(achievedrate_sim,Iter,UN_msg_sent,UN_msg_decoded)=send_rateless_det_Iter_retro_delta_CRC(UN_msg,N,T,I_ord,channel_p,compound_plist,Glist,deltaG)
		achievedrate+=float(achievedrate_sim)/runsim
		if UN_msg_sent.tolist()!=UN_msg_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1
			
	used_rate=float(len(UN_msg_sent))/N	# has no meaning
	block_error=float(block_errorcnt)/runsim
	
	#print block_errorcnt
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
		
	return (used_rate,achievedrate,block_error,Iter_probdict)
	
#==============================================================================Sample runs

#~ #------------------------Iter_delta
#~ UN_msg=np.random.randint(2,size=21)
#~ print UN_msg
#~ I_ord=pcon.getreliability_order(32)
#~ deltaG=4
#~ (achieved_rate,Iter,sent,Rec)=send_rateless_det_Iter_retro_delta(UN_msg,32,3,I_ord,0.1,deltaplist,[24,20,16,12],deltaG)
#~ print Iter
#~ print sent
#~ print Rec
#~ print sent.tolist()==Rec.tolist()


#~ for i in range(10):
	#~ UN_msg=np.random.randint(2,size=268)
	#~ #print UN_msg
	
	#~ I_ord=pcon.getreliability_order(1024)
	#~ (achieved_rate,Iter,sent,Rec)= send_rateless_det_Iter_retro_delta(UN_msg,1024,32,I_ord,0.15,deltaplist,[300,250,200,150],50)
	#~ print sent ,Rec
	#~ print Iter
	#~ print sent.tolist()==Rec.tolist()

#~ print send_rateless_det_Iter_retro_delta_sim(16,2,[0.04,0.15,0.2,0.25],0.04,10,2,100)

#~ print send_rateless_det_Iter_retro_delta_sim(1024,32,[0.04,0.15,0.2,0.25],0.1,600,100,10)
#~ print send_rateless_det_Iter_retro_delta_CRC_sim(1024,32,[0.04,0.15,0.2,0.25],0.1,600,100,10)

#----------------------Iter_retro

#~ UN_msg=np.random.randint(2,size=10)
#~ print UN_msg
#~ I_ord=pcon.getreliability_order(16)
#~ deltaG=2
#~ print send_rateless_det_Iter_retro(UN_msg,16,2,I_ord,0.25,plist,[12,6,4,3])

#~ for i in range(10):
	#~ UN_msg=np.random.randint(2,size=508)
	#~ #print UN_msg
	#~ print "with retro"
	#~ I_ord=pcon.getreliability_order(1024)
	#~ (achieved_rate,Iter,Rec)= send_rateless_det_Iter_retro_CRC(UN_msg,1024,32,I_ord,0.15,plist,[540,270,180,135])
	#~ print Iter
	#~ print UN_msg.tolist()==Rec.tolist()
	#~ print "without CRC"
	#~ (achieved_rate,Iter,Rec)= send_rateless_det(UN_msg,1024,32,I_ord,0.15,plist,[540,270,180,135])
	#~ print Iter
	#~ print UN_msg.tolist()==Rec.tolist()
#~ print send_rateless_det_Iter_retro_CRC_sim(1024,8,plist,0.15,200,10)
#~ print send_rateless_det_Iter_retro_sim(1024,8,plist,0.15,200,10)
#~ print send_rateless_det_Iter_retro_CRC_sim(1024,8,plist,0.15,200,10)

#----------------------------------Iter-det

#~ for i in range(10):
	#~ UN_msg=np.random.randint(2,size=520)
	#~ #print UN_msg
	#~ I_ord=pcon.getreliability_order(1024)
	#~ (achieved_rate,Iter,Rec)= send_rateless_det(UN_msg,1024,20,I_ord,0.15,plist,[540,270,180,135])
	#~ print Iter
	#~ print UN_msg.tolist()==Rec.tolist()
#~ print send_rateless_det_sim(1024,20,plist,0.25,200,10)	
#~ print send_rateless_det_sim(1024,8,plist,0.15,200,10)
