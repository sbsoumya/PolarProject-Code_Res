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

plist=[0.833 0.192 0.2455 0.278]
	
def getreliability_order(N):
	return getGChZCK(0.01,N,N)
	
def getRatelist(plist):
	#insert derating
	Ratelist=[ pl.CapacityBSC(1,p) for p in plist]
    return Ratelist
#---------------------------------------------------------------Rx knows channels	
#decodable if actual rate is greater than present rate
def is_decodable_kRx(ActualRate,PresentRate):	
	return ActualRate>=PresentRate           

def send_rateless_kRx(UN,N,D,channel_p,compound_plist_u): 
	
	#Reliability ordering
	I_ord=getreliability_order(N)
	
	#compound channel
	compound_plist=list(compound_plist_u).sort() #best channel first
	Ratelist = getRatelist(compound_plist)       #best rate first
	Glist=[int(N*r) for r in Ratelist]
	
	#given Channel might not be an entry in compound but within bounds	
	R=getratelist([channel_p])[0]  #calculates rate for given channel
	G=int(R*N)
	
	
	
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
			
	while not decoded:
		
		Iter_UN=[UN[i] for i in Iter_UN_ind]
		 
		Iter_D=np.zeros(N-Iter_G,dtype=int).tolist()      #frozen data
		Iter_XN=ec.polarencodeGR_u(Iter_UN,N,I,list(D))   #data goes in as per R.I
		
		#--------------------Note channel_p used for flipping
		Iter_YN=pl.BSCN(channel_p,Iter_XN)
		
		#-----------------------decoding based on this tx only
		Iter_UN_hat=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(D))		
		Iter_UN_decoded=ec.getUN_u(Iter_UN_hat,Iter_I)
		
		#storage needed for final decoding
		Iterhistory[Iter]=[Iter_UN_ind,Iter_UN_decoded]
		
		
		#For simulation of Rx knows channel case
		#Assuming Rx knows the capacity of the channel
		#hence as long as the rate used is above
		#the capacity is declares Not decodable	
		#the rate at which decoding is possible and the rate achieved is same
		
		
		
		if not is_decodable_kRx(R,Iter_R):
			
			
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
				bad_ind=sent_ind[Iter_G:]
				tosend_ind.extend(bad_ind)
			
			Iter_UN_ind=list(set(tosend_ind)).sort()
			
			
		else:
			decoded= True
			
			
	#final decoding
	
	
	
	
#R R/2 R/3 R/4.....			
			
            		
		
		
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

		
	

