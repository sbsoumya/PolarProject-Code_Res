#-------------------------------------------
# Name:       CSD channel
# Purpose:    rateless, LTPT, KRX and plane polar for CSD type simulations
#            
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
#plist=[0.04,0.15,0.2,0.25] #16 12 6 4 3
#plist=[0.04,0.15,0.2,0.25] #16 12 6 4 3
	
def getreliability_order(N):
	return pcon.getGChZCK(0.01,N,N)[0]
	
def getRatelist(plist,derate):
	#insert derating
	Ratelist=[ pl.CapacityBSC(1,p)*derate for p in plist]
	return Ratelist
	
def adjustG(Glist): #input Glist is sorted
	MaxG=max(Glist)
	lenG=len(Glist)
	lcm=ml.get_lcm_for(range(1,lenG+1))
	return [int(MaxG/lcm)*(lcm/(i+1)) for i in range(lenG)]
	
	return 0
	#for i in range(Glist):
	
#=======================================================================Polar vanilla
def send_polar(UN,N,channel_p,compound_plist_u,K,runsim): 
	I_ord=getreliability_order(N)
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	G=int(K)
	
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
			print "Here"
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
		
		
	
#=======================================================================Rx knows channels	
#decodable if actual rate is greater than present rate
def is_decodable_kRx(ActualG,PresentG):	
	return ActualG>=PresentG        

def send_rateless_kRx(UN,N,channel_p,compound_plist_u,derate,use_adjusted_Rate): 
	#print "In send rateless..."
	#Reliability ordering
	#print "R_order"
	I_ord=getreliability_order(N)
	#print I_ord
	#compound channel
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	Ratelist = getRatelist(compound_plist,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	
	
	#print "Compund Channel"
	#print plist
	#print Glist
	#print "will be working with below to meet R R/2 R/3 R/4 constraint"
	Glist=adjustG(Glist)
	#print Glist
	
	#given Channel might not be an entry in compound but within bounds	
	R=getRatelist([channel_p],derate)[0]  #calculates rate for given channel
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
			print "Here"
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
	
	Ratelist = getRatelist(compound_plist_u,derate)       #best rate first
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
#--------------------------------------------------------------Simulations

#~ N=1024
#~ print "N="+str(N)
#~ derate=0.5
#~ print "Working with "+str(derate)+"*Capacity"
#~ Ratelist = getRatelist(plist,derate)       #best rate first
#~ Glist=[int(N*r) for r in Ratelist]
#~ Glist=adjustG(Glist)
#~ UN=np.random.randint(2,size=Glist[0])

#~ p=0.04
#~ (achieved_rate,d)=send_rateless_kRx(UN,N,p,plist,derate,True)
#~ print np.array(d)
#~ print UN
#~ print "Actual rate"
#~ print getRatelist([p],derate)[0]
#~ print "Achieved rate"
#~ print achieved_rate

#~ print "block_error:"
#~ print d!=UN.tolist()

#=======================================================================LT PT
#decodable if actual rate is greater than present rate
def is_decodable_LTPT(llr,I,LT,PT):
	#find of good channels above LT
	perc=lmb.perc_goodchannel_llr(llr,I,LT)	
	return perc>=PT        

def send_rateless_LTPT(UN,N,channel_p,compound_plist_u,derate,LTPTdict,use_adjusted_Rate): 
	#print "In send rateless..."
	#Reliability ordering
	#print "R_order"
	I_ord=getreliability_order(N)
	#print I_ord
	#compound channel
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	Ratelist = getRatelist(compound_plist,derate)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	
	
	#print "Compund Channel"
	#print plist
	#print Glist
	#print "will be working with below to meet R R/2 R/3 R/4 constraint"
	Glist=adjustG(Glist)
	#print Glist
	
	#given Channel might not be an entry in compound but within bounds	
	R=getRatelist([channel_p],derate)[0]  #calculates rate for given channel
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
	
#R R/2 R/3 R/4.....		
def send_rateless_LTPT_sim(N,compound_plist_u,channel_p,derate,LTPTdict,runsim,BER_needed):

	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	
	Ratelist = getRatelist(plist,derate)       #best rate first
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

#--------------------------------------------------------------Simulations

#~ N=1024
#~ print "N="+str(N)
#~ derate=0.5
#~ print "Working with "+str(derate)+"*Capacity"
#~ Ratelist = getRatelist(plist,derate)       #best rate first
#~ Glist=[int(N*r) for r in Ratelist]
#~ Glist=adjustG(Glist)
#~ UN=np.random.randint(2,size=Glist[0])

#~ p=0.15
#~ (achieved_rate,d)=send_rateless_kRx(UN,N,p,plist,derate)
#~ print np.array(d)
#~ print UN
#~ print "Actual rate"
#~ print getRatelist([p],derate)[0]
#~ print "Achieved rate"
#~ print achieved_rate

#~ print "block_error:"
#~ print d!=UN.tolist()


			
            		
		

			
            		
		
		
"""		

def send_rateless_D():
	return 0;		
#------------------------------------------------------------------LT
#if all good channels are not above LT refurn false
def is_decodable_LT(llr,I,LT):#I and LT are for the present rate
	good_llr=ec.getchannel_u(llr,I)#I is as per reliability ordering
	decodable=True
	degraded=[]
	for i in range(len(good_llr)):
		l=good_llr(i)
		d=I(i)
		if l<LT:
			decodable=False
			degraded.append(d)
			
	return (decodable,degraded) 


def send_rateless_LT():
	return 0	
	
"""

		
	

