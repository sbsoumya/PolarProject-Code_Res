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

import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
from datetime import datetime
import json
import polarconstruct as pcon
from pprint import pprint
import matlib as ml
import lambdathreshold as lmb
import copy
#plist=[0.04,0.15,0.2,0.25] #16 12 6 4 3
#plist=[0.04,0.15,0.2,0.25] #16 12 6 4 3
	
#----------------------------------------adjusts Glist for R,R/2.. 
def adjustG(Glist): #input Glist is sorted
	MaxG=max(Glist)
	lenG=len(Glist)
	lcm=ml.get_lcm_for(range(1,lenG+1))
	return [int(MaxG/lcm)*(lcm/(i+1)) for i in range(lenG)]
	
	return 0

def getGlist(MaxG,lenG): 
	lcm=ml.get_lcm_for(range(1,lenG+1))
	return [int(MaxG/lcm)*(lcm/(i+1)) for i in range(lenG)]
	
	return 0
	
#=======================================================================Rx knows channels	
#decodable if actual rate is greater than present rate
def is_decodable_kRx(ActualG,PresentG):	
	return ActualG>=PresentG        

def send_rateless_kRx(UN,N,channel_p,compound_plist_u,derate,use_adjusted_Rate): 
	#print "In send rateless..."
	#Reliability ordering
	#print "R_order"
	I_ord=pcon.getreliability_order(N)
	#print I_ord
	#compound channel
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	Ratelist = pl.getRatelist(compound_plist,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	
	
	#print "Compund Channel"
	#print plist
	#print Glist
	#print "will be working with below to meet R R/2 R/3 R/4 constraint"
	Glist=adjustG(Glist)
	#print Glist
	
	#given Channel might not be an entry in compound but within bounds	
	R=pl.getRatelist([channel_p],derate)[0]  #calculates rate for given channel
	G=int(R*N)
	
	#print "Actual channel"
	#print channel_p
	#print G
	if use_adjusted_Rate:
		G=Glist[compound_plist.index(channel_p)]
	
	
    #----------------------------------------------------Iterations start
	
	Iterhistory={} #contains indexes of UN sent in each iteration
	
	
	decoded=False
	# for first Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_R=Ratelist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(len(UN))
	#Iter_data={}
	#print float(len(Iter_I))/N
    
	#print "Forward decoding"		
	while not decoded:
		
		#print "Iter"+str(Iter)
		
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
		
		#pprint(Iterhistory)
		
		
		
		#For simulation of Rx knows channel case
		#Assuming Rx knows the capacity of the channel
		#hence as long as the rate used is above
		#the capacity is declares Not decodable	
		#the rate at which decoding is possible and the rate achieved is same
		#print Iterhistory
		
		
		if not is_decodable_kRx(G,Iter_G):
			
			
			# picking out all the channels that are suspected to be bad in past
			# iterations and putting them for next iteration.
			# Note first iteration Whole UN is sent
			# in next only suspected bad channels are sent
			prev_I=Iter_I
			Iter+=1
			
			#New channel params
			Iter_p=compound_plist[Iter]
			Iter_R=Ratelist[Iter]
			Iter_G=Glist[Iter]
			Iter_I=I_ord[:Iter_G]
			
			tosend_ind=[]
			for i in range(Iter):
				#picking out the bad channels from prev iterations
				sent_ind=Iterhistory[i][0]
				sent_ind_last_iter=sent_ind[:Glist[Iter-1]]
				
					
				bad_ind=sent_ind_last_iter[Iter_G:]
				#print bad_ind
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind=list(set(tosend_ind))
			
			Iter_UN_ind.sort()
			#print Iter_UN_ind
			
			
		else:
			#the final reliable good channels is that of last iteration
			final_Iter=Iter
			final_G=Iter_G
			#channel_p is already updated
			final_p=Iter_p
			final_I=I_ord[:final_G]
			decoded= True
			
	
	#pprint(Iterhistory)		
	
	#final decoding
	#number retrodecoding needed = iter-1
	
	#print "Final Decoding..."
	#print final_p
	#print final_G
	#print Iter
	
	

	
	for Iter in range(final_Iter-1,-1,-1):
			#print "Here"
			#print "Iter"+str(Iter)+"-"*10
		
			#print "Prev frozen"
			Prev_correct_ind=Iterhistory[Iter+1][0]
			Prev_correct_data=Iterhistory[Iter+1][1]
			#print Prev_correct_ind
			#print Prev_correct_data
			
			#print "Inc frozen needed"
			IncFreeze_ind_UN=[i for i in Prev_correct_ind if i in Iterhistory[Iter][0]] 
			#basically intersection with some order picking the indexes of the prev iter frozen data needed in this iter i.e, 12
			#print IncFreeze_ind_UN
			
			#picking the data i.e. u12
			IncFreeze_ind_ind=[Prev_correct_ind.index(j) for j in IncFreeze_ind_UN]
			IncFreeze_data=[Prev_correct_data[k] for k in IncFreeze_ind_ind]
			
			#print IncFreeze_data
			
			#finding the channels where 12 went in this iter 16 15 14 "13"<--- here
			#i.e, removing the top channel_G channels (as they are good) from top Iter_i_G channels
			Iter_G=Glist[Iter]
			IncFreeze_ind=I_ord[:Iter_G][final_G:]
			#print "Inc Frozen Data going in"
			#print IncFreeze_ind
			
			#print "Frozen zeroes"
			Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data as per iteration
			#print len(Iter_D)		
				
			Iter_YN=Iterhistory[Iter][2]
			Iter_UN_hat=ec.polarIncFrzSCdecodeG(Iter_YN,N,final_p,final_I,list(Iter_D),IncFreeze_ind,IncFreeze_data,False)
			Iter_UN_decoded=ec.getUN(Iter_UN_hat,final_I,False)
			
			#print Iter_UN_decoded
			
			#history update
			Iterhistory_ind_upd=list(Prev_correct_ind)
			Iterhistory_ind_upd.extend(Iterhistory[Iter][0][:final_G]) #ie adding 5,6,11 to 4,10,12
			Iterhistory_data_upd=np.hstack((Prev_correct_data,Iter_UN_decoded)) #same as extend
			
			#print "Update"
			#print Iterhistory_ind_upd
			#print Iterhistory_data_upd
			
			#print "sorted"
			
			(Iterhistory[Iter][0],Iterhistory[Iter][1])=ml.sortAextend(Iterhistory_ind_upd,Iterhistory_data_upd.tolist())
			#print Iterhistory[Iter][0]
			#print Iterhistory[Iter][1]
	         
	         
	#pprint(Iterhistory)
	final_decoded= Iterhistory[0][1]
	achieved_rate=float(len(UN))/((final_Iter+1)*N)
	return (achieved_rate,np.array(final_decoded))
	
#R R/2 R/3 R/4.....		
def send_rateless_kRx_sim(N,compound_plist_u,channel_p,derate,runsim,BER_needed):

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	
	Ratelist = pl.getRatelist(compound_plist_u,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	Glist=adjustG(Glist)
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	#UN=np.random.randint(2,size=Glist[0])
	#print UN
	for i in range(runsim):
		UN=np.random.randint(2,size=Glist[0])
		(achievedrate,UN_decoded)=send_rateless_kRx(UN,N,channel_p,compound_plist_u,derate,True)
		#achievedrate will be same for all simulations for a given value of derate
		if BER_needed:
			errcnt=errcnt+np.logical_xor(UN,UN_decoded)
						
		if UN.tolist()!=UN_decoded.tolist():
			block_errorcnt+=1
	used_rate=float(Glist[0])/N	
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
	
		
	if BER_needed:
		return (achievedrate,used_rate,ber_exp,block_error)
	else:
		return (achievedrate,used_rate,block_error)

#=======================================================================LT PT
#decodable if actual rate is greater than present rate
def is_decodable_LTPT(llr,I,LT,PT):
	#find of good channels above LT
	#print len(I)
	perc=lmb.perc_goodchannel_llr(llr,I,LT)	
	return perc>=PT        

def send_rateless_LTPT(UN,N,channel_p,compound_plist_u,derate,LTPTdict,use_adjusted_Rate): 
	#print "In send rateless..."
	#Reliability ordering
	#print "R_order"
	I_ord=pcon.getreliability_order(N)
	#print I_ord
	#compound channel
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	Ratelist = pl.getRatelist(compound_plist,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	
	
	#print "Compund Channel"
	#print plist
	#print Glist
	#print "will be working with below to meet R R/2 R/3 R/4 constraint"
	Glist=adjustG(Glist)
	#print Glist
	
	#given Channel might not be an entry in compound but within bounds	
	R=pl.getRatelist([channel_p],derate)[0]  #calculates rate for given channel
	G=int(R*N)
	
	#print "Actual channel"
	#print channel_p
	#print G
	if use_adjusted_Rate:
		G=Glist[compound_plist.index(channel_p)]
	
	
    #----------------------------------------------------Iterations start
	
	Iterhistory={} #contains indexes of UN sent in each iteration
	
	
	decoded=False
	# for first Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_R=Ratelist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(len(UN))
	#Iter_data={}
	
    
	#print "Forward decoding"		
	while not decoded:
		
		#print "Iter"+str(Iter)
		
		Iter_UN=[UN[i] for i in Iter_UN_ind]
		 
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeG(Iter_UN,N,Iter_I,list(Iter_D),False)   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		(Iter_llr,Iter_UN_hat)=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),True)		
		Iter_UN_decoded=ec.getUN(Iter_UN_hat,Iter_I,False)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		
		#pprint(Iterhistory)
		
		
		
		#For simulation of Rx knows channel case
		#Assuming Rx knows the capacity of the channel
		#hence as long as the rate used is above
		#the capacity is declares Not decodable	
		#the rate at which decoding is possible and the rate achieved is same
		Iter_LT=LTPTdict[str(Iter_p)][0]
		Iter_PT=LTPTdict[str(Iter_p)][1]
		
		
		if not is_decodable_LTPT(Iter_llr,Iter_I,Iter_LT,Iter_PT):
			
			
			# picking out all the channels that are suspected to be bad in past
			# iterations and putting them for next iteration.
			# Note first iteration Whole UN is sent
			# in next only suspected bad channels are sent
			prev_I=Iter_I
			Iter+=1
			
			#New channel params
			Iter_p=compound_plist[Iter]
			Iter_R=Ratelist[Iter]
			Iter_G=Glist[Iter]
			Iter_I=I_ord[:Iter_G]
			
			tosend_ind=[]
			for i in range(Iter):
				#picking out the bad channels from prev iterations
				sent_ind=Iterhistory[i][0]
				sent_ind_last_iter=sent_ind[:Glist[Iter-1]]
				
					
				bad_ind=sent_ind_last_iter[Iter_G:]
				#print bad_ind
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind=list(set(tosend_ind))
			
			Iter_UN_ind.sort()
			#print Iter_UN_ind
			
			
		else:
			#the final reliable good channels is that of last iteration
			final_Iter=Iter
			final_G=Iter_G
			#channel_p is already updated
			final_p=Iter_p
			final_I=I_ord[:final_G]
			decoded= True
			
	
	#pprint(Iterhistory)		
	
	#final decoding
	#number retrodecoding needed = iter-1
	
	#print "Final Decoding..."
	#print final_p
	#print final_G

	
	for Iter in range(final_Iter-1,-1,-1):
			#print "Iter"+str(Iter)+"-"*10
		
			#print "Prev frozen"
			Prev_correct_ind=Iterhistory[Iter+1][0]
			Prev_correct_data=Iterhistory[Iter+1][1]
			#print Prev_correct_ind
			#print Prev_correct_data
			
			#print "Inc frozen needed"
			IncFreeze_ind_UN=[i for i in Prev_correct_ind if i in Iterhistory[Iter][0]] 
			#basically intersection with some order picking the indexes of the prev iter frozen data needed in this iter i.e, 12
			#print IncFreeze_ind_UN
			
			#picking the data i.e. u12
			IncFreeze_ind_ind=[Prev_correct_ind.index(j) for j in IncFreeze_ind_UN]
			IncFreeze_data=[Prev_correct_data[k] for k in IncFreeze_ind_ind]
			
			#print IncFreeze_data
			
			#finding the channels where 12 went in this iter 16 15 14 "13"<--- here
			#i.e, removing the top channel_G channels (as they are good) from top Iter_i_G channels
			Iter_G=Glist[Iter]
			IncFreeze_ind=I_ord[:Iter_G][final_G:]
			#print "Inc Frozen Data going in"
			#print IncFreeze_ind
			
			#print "Frozen zeroes"
			Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data as per iteration
			#print len(Iter_D)		
				
			Iter_YN=Iterhistory[Iter][2]
			Iter_UN_hat=ec.polarIncFrzSCdecodeG(Iter_YN,N,final_p,final_I,list(Iter_D),IncFreeze_ind,IncFreeze_data,False)
			Iter_UN_decoded=ec.getUN(Iter_UN_hat,final_I,False)
			
			#print Iter_UN_decoded
			
			#history update
			Iterhistory_ind_upd=list(Prev_correct_ind)
			Iterhistory_ind_upd.extend(Iterhistory[Iter][0][:final_G]) #ie adding 5,6,11 to 4,10,12
			Iterhistory_data_upd=np.hstack((Prev_correct_data,Iter_UN_decoded)) #same as extend
			
			#print "Update"
			#print Iterhistory_ind_upd
			#print Iterhistory_data_upd
			
			#print "sorted"
			
			(Iterhistory[Iter][0],Iterhistory[Iter][1])=ml.sortAextend(Iterhistory_ind_upd,Iterhistory_data_upd.tolist())
			#print Iterhistory[Iter][0]
			#print Iterhistory[Iter][1]
	
		         
	#pprint(Iterhistory)
	final_decoded= Iterhistory[0][1]
	achieved_rate=float(len(UN))/((final_Iter+1)*N)
	return (achieved_rate,np.array(final_decoded))
		
#------------In det iter retro format
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
	
def send_rateless_LTPT_new(UN_msg,N,LTPTdict,I_ord,channel_p,compound_plist,Glist): 
	UN=UN_msg
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
		(Iter_llr,Iter_UN_hat)=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(Iter_D),True)		
		Iter_UN_decoded=ec.getUN(Iter_UN_hat,Iter_I,False)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded,Iter_YN]
		
		
		Iter_LT=LTPTdict[str(Iter_p)][0]
		Iter_PT=LTPTdict[str(Iter_p)][1]

		if not is_decodable_LTPT(Iter_llr,Iter_I,Iter_LT,Iter_PT) and Iter<maxiter:
			
			
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
			
	Iter_UN_retro_decoded=Iter_retro_decode(Iterhistory,Iter,N,I_ord,Glist,Iter_G,Iter_p,Iter_I)		
	
	#final==================================
	final_Iter=Iter
	if not is_decodable_LTPT(Iter_llr,Iter_I,Iter_LT,Iter_PT): # two find the cases where final iter did not send ACK
		return_iter=0
	else:
		return_iter=final_Iter+1
	final_decoded=Iter_UN_retro_decoded
	final_UN_msg=final_decoded[:Glist[0]]
	achieved_rate=float(len(UN_msg))/((final_Iter+1)*N)
	return (achieved_rate,return_iter,np.array(final_UN_msg))


def send_rateless_LTPT_new_sim(N,LTPTdict,compound_plist_u,channel_p,msg_length,runsim): #using bestchannel sent rate in place of derate

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlist(msg_length,lenG)
	print Glist
	block_errorcnt=0
	Iter_probdict={}
	achievedrate=0
	print "msg_length:"+str(Glist[0])
	print "channel_p:"+str(channel_p)
	
	for i in range(runsim):
		UN_msg=np.random.randint(2,size=Glist[0])
		(achievedrate_sim,Iter,UN_msg_decoded)=send_rateless_LTPT_new(UN_msg,N,LTPTdict,I_ord,channel_p,compound_plist,Glist)
		achievedrate+=float(achievedrate_sim)/runsim
		if UN_msg.tolist()!=UN_msg_decoded.tolist():
			block_errorcnt+=1
		try:
			Iter_probdict[Iter]+=1
		except:
			Iter_probdict[Iter]=1
			
	used_rate=float(Glist[0])/N	
	block_error=float(block_errorcnt)/runsim
	
	for Iter in Iter_probdict:
		Iter_probdict[Iter]=float(Iter_probdict[Iter])/runsim
		
	return (used_rate,achievedrate,block_error,Iter_probdict)
#----------------------------------------------------------------new format end
	
#R R/2 R/3 R/4.....		
def send_rateless_LTPT_sim(N,compound_plist_u,channel_p,derate,LTPTdict,runsim,BER_needed):

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	
	Ratelist = pl.getRatelist(compound_plist,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	Glist=adjustG(Glist)
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	achievedrate=0
	for i in range(runsim):
		UN=np.random.randint(2,size=Glist[0])
		(achievedrate_sim,UN_decoded)=send_rateless_LTPT(UN,N,channel_p,compound_plist_u,derate,LTPTdict,True)
		achievedrate+=float(achievedrate_sim)/runsim
		if BER_needed:
			errcnt=errcnt+np.logical_xor(UN,UN_decoded)
						
		if UN.tolist()!=UN_decoded.tolist():
			block_errorcnt+=1
	used_rate=float(Glist[0])/N	
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
		
	if BER_needed:
		return (achievedrate,used_rate,ber_exp,block_error)
	else:
		return (achievedrate,used_rate,block_error)





#---------------------------------------------------------------------------------bin		
def send_rateless_LTPT_sim_bin(ERR_DICT,DP,N,compound_plist_u,channel_p,derate,LTPTdict,runsim):
	
	
	
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	
	Ratelist = pl.getRatelist(compound_plist,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	Glist=adjustG(Glist)
	
	for i in range(runsim):
		UN=np.random.randint(2,size=Glist[0])
		(achievedrate_sim,UN_decoded)=send_rateless_LTPT(UN,N,channel_p,compound_plist_u,derate,LTPTdict,True)
		
		#Number of times this rate occurs
		try:
			ERR_DICT[format(achievedrate_sim,'.'+str(DP)+'f')][0]+=1
		except:
			ERR_DICT[format(achievedrate_sim,'.'+str(DP)+'f')]=[1,0]
		
		#ERRORS
		if UN.tolist()!=UN_decoded.tolist():
			ERR_DICT[format(achievedrate_sim,'.'+str(DP)+'f')][1]+=1
					
	return ERR_DICT

#=======================================================================1Iter polar
def send_polar(UN,N,channel_p,compound_plist_u,derate,use_adjusted_Rate): 
	I_ord=pcon.getreliability_order(N)
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	Ratelist = pl.getRatelist(compound_plist,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	
	Glist=adjustG(Glist)

	R=pl.getRatelist([channel_p],derate)[0]  #calculates rate for given channel
	G=int(R*N)
	
	Iterhistory={} 
	# for first one Tx
	Iter=0
	Iter_UN=UN
	Iter_p=compound_plist[0]
	Iter_R=Ratelist[0]
	Iter_G=Glist[0]
	Iter_I=I_ord[:Iter_G]
	Iter_UN_ind=range(len(UN))
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
	
	final_Iter=Iter
	final_decoded= Iterhistory[0][1]
	achieved_rate=float(len(UN))/((final_Iter+1)*N)
	return (achieved_rate,np.array(final_decoded))
	
#R R/2 R/3 R/4.....		
def send_polar_sim(N,compound_plist_u,channel_p,derate,runsim,BER_needed):

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	
	Ratelist = pl.getRatelist(compound_plist_u,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	Glist=adjustG(Glist)
	
	if BER_needed:
		errcnt=np.zeros(G)
	
	block_errorcnt=0
	#UN=np.random.randint(2,size=Glist[0])
	#print UN
	for i in range(runsim):
		#print i
		UN=np.random.randint(2,size=Glist[0])
		(achievedrate,UN_decoded)=send_polar(UN,N,channel_p,compound_plist_u,derate,True)
		#print achievedrate
		#achievedrate will be same for all simulations for a given value of derate
		
		if BER_needed:
			errcnt=errcnt+np.logical_xor(UN,UN_decoded)
						
		if UN.tolist()!=UN_decoded.tolist():
			block_errorcnt+=1
	used_rate=float(Glist[0])/N	
	if BER_needed:		
		berN=errcnt/runsim
		ber_exp=np.log10(berN).tolist()
	
	block_error=float(block_errorcnt)/runsim
	
		
	if BER_needed:
		return (achievedrate,used_rate,ber_exp,block_error)
	else:
		return (achievedrate,used_rate,block_error)

#--------------------------------------------------------------Simulations

#~ N=1024
#~ print "N="+str(N)
#~ derate=0.5
#~ print "Working with "+str(derate)+"*Capacity"
#~ Ratelist = pl.getRatelist(plist,derate)       #best rate first
#~ Glist=[int(N*r) for r in Ratelist]
#~ Glist=adjustG(Glist)
#~ UN=np.random.randint(2,size=Glist[0])

#~ p=0.04
#~ (achieved_rate,d)=send_rateless_kRx(UN,N,p,plist,derate,True)
#~ print np.array(d)
#~ print UN
#~ print "Actual rate"
#~ print pl.getRatelist([p],derate)[0]
#~ print "Achieved rate"
#~ print achieved_rate

#~ print "block_error:"
#~ print d!=UN.tolist()



		
	

