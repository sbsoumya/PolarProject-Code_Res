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


#=====================================================================================================step_retro	
def Iter_retro_decode(pc1,Iterhistory_original,this_Iter,N,I_ord,Glist,this_Iter_G,this_Iter_p,this_Iter_I,list_size):	
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
			
			pc1.info_length=this_Iter_G
			#print len(Iter_D),len(IncFreeze_data),this_Iter_G
			Iter_UN_decoded=ec.polarIncFrzSCdecodeG_C(pc1,Iter_YN,this_Iter_p,list(Iter_D),IncFreeze_ind,list(IncFreeze_data),list_size)
						
			#print Iter_UN_decoded
			
			#history update
			Iterhistory_ind_upd=list(Prev_correct_ind)
			Iterhistory_ind_upd.extend(Iterhistory[Iter][0][:this_Iter_G]) #ie adding 5,6,11 to 4,10,12
			Iterhistory_data_upd=np.hstack((Prev_correct_data,Iter_UN_decoded)) #same as extend
			(Iterhistory[Iter][0],Iterhistory[Iter][1])=ml.sortAextend(Iterhistory_ind_upd,Iterhistory_data_upd.tolist())
	#print "retro decode"
	#print Iterhistory
	return Iterhistory[0][1]
	
def send_rateless_det_Iter_retro(pc1,UN_msg,N,T,I_ord,channel_p,compound_plist,Glist,list_size): 
    
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
		pc1.info_length=Iter_G
		
		Iter_UN=[UN[i] for i in Iter_UN_ind]
		 
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeG_C(pc1,Iter_UN,list(Iter_D))   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		Iter_UN_decoded=ec.polarSCdecodeG_C(pc1,Iter_YN,Iter_p,list(Iter_D),list_size)	
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		#print Iterhistory
		
		
		
		Iter_UN_retro_decoded=Iter_retro_decode(pc1,Iterhistory,Iter,N,I_ord,Glist,Iter_G,Iter_p,Iter_I,list_size)
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


def send_rateless_det_Iter_retro_sim(N,T,compound_plist_u,channel_p,msg_length,runsim,list_size): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	#I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlist(msg_length+T,lenG)
	#print Glist
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	print "msg_length:"+str(Glist[0]-T)
	print "channel_p:"+str(channel_p)
	
	pc1=ec.polarcode_init(N,Glist[0],compound_plist[0],0) #Iter_p is a dummy design_p
	I_ord=ec.bitreverseorder(pc1.channel_ordering,pc1.n)
	
	for i in range(runsim):
		UN_msg=np.random.randint(2,size=Glist[0]-T)
		(achievedrate_sim,Iter,UN_msg_decoded)=send_rateless_det_Iter_retro(pc1,UN_msg,N,T,I_ord,channel_p,compound_plist,Glist,list_size)
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
