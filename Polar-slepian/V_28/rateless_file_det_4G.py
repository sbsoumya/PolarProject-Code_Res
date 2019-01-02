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
	


#==================================================================4-party
def anydecoded(decoded):
    anydecode=0 
    for key in decoded:
		anydecode+=sum(decoded[key])
    return anydecode

def anydecodedat(decoded,at):
	return sum(decoded[at])
#-------------------------------------------table navigation

def getneighbours(nodes,decoded,at,exclude):
	neighbours=[]
	for key in decoded:
		if key!=at and decoded[key][nodes.index(at)]!=0 and decoded[key][nodes.index(at)]!="F":
			if decoded[key][nodes.index(at)]==decoded[at][nodes.index(key)]:
				neighbours.append(key)
				
	return set(neighbours)-set(exclude)
	
def isnavigable(nodes,decoded,src,dst):
	Path=[]
	isnav=isnavi(nodes,decoded,src,dst,[],Path)
	return (Path,isnav)
	
def isnavi(nodes,decoded,src,dst,exclude,Path):
	navigable=False
	neighbours=getneighbours(nodes,decoded,src,exclude)
	if len(neighbours)==0:
		return False
	if dst in neighbours:
		Path[:]=list(exclude)+[src,dst] # a bad hack, TBLW
		navigable=True
		return navigable
	else:
		exclude.append(src)
		
		for n in neighbours:
			navigable=navigable or isnavi(nodes,decoded,n,dst,exclude,Path)
		return navigable
def getdecstep(decoded,at,neighbour):
	# feed neighbour to this function only
	return decoded[at][nodes.index(neighbour)]
	
	
"""	
nodes=["A","B","C","D"]
        
decoded={"A":np.array([0,0,0,1]),
         "B":np.array([0,0,3,0]),
         "C":np.array([0,3,0,2]),
         "D":np.array([1,0,2,0]),}
         
#print getneighbours(nodes,decoded,"C",[])
        
print isnavigable(nodes,decoded,"A","B")

print getdecstep(decoded,"B","C")
"""
#-------------------------------------------------------------------------main function		

def send_rateless_file_Iter_retro_4G(Orig_data,N,I_ord,channel_p,compound_plist,Glist,T,printFT): 
	# T < deltaG
	#compound channel
    #----------------------------------------------------Iterations start
	nodes=Orig_data.keys()
	M=len(nodes)
	decoded={}
	for n in nodes:
		decoded[n]=np.zeros(M).tolist()
	maxiter=len(compound_plist)-1
	Rev_data={}
	for n in nodes:
		Rev_data[n]=ec.polarencode(Orig_data[n],N)
	
	decoded_vector={}
	decoded_origdata={}
	err={}
	Iter_lock={}
	Iter_key={}
	
	Iter=-1
	Iter_errorfree=[0,0,0]
			
	final_Iter=[]
	final_Iter_F=[]
	final_Iter_p=[]
	final_Iter_I=[]
	
    
	D=[{},{},{}]
	Step=0
    #--------------------------------------Forward decoding all try to decode each other
	 #Step 1
    	
	while anydecoded(decoded)==0 and Iter<maxiter:
		#if Iter<maxiter:
		Iter+=1
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		Iter_T=I_ord[Iter_G-T:Iter_G] 
		Iter_F=list(set(range(N))-set(Iter_I)) 
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		
        #Data transmission for node n
		for n in nodes:
			Iter_lock[n]=ec.getUN(Rev_data[n],Iter_T,False)
			#bits frozen sent over errorrfree channel
			# Note while decoding the data is assumed to be in sorted order
			D[Step][n]=ec.getUN(Rev_data[n],Iter_F,True)
			Iter_key[n]={}
            
        #Decoding for node n (this takes care of reverse decoding too)
		for n in nodes:
			decoded_vector[n]={} #decoded vectors AT node n
			decoded_vector[n][n]=Rev_data[n]
			for q in nodes:
				if q!=n:
                    #decoded values of q at node n
					decoded_vector[n][q]=ec.polarSCdecodeG(Orig_data[n],N,Iter_p,Iter_I,list(D[Step][q]),False) 
					Iter_key[n][q]=ec.getUN(decoded_vector[n][q],Iter_T,False)
		
		#Note decoded[n][n] is never made 1 
		for n in nodes:
			for q in nodes:
				if q!=n:
					if not is_mismatch(Iter_key[n][q],Iter_lock[q]):
						decoded[n][nodes.index(q)]=Step+1
						decoded[q][nodes.index(n)]=Step+1 #reverse
	
		for n in nodes:
			Iter_errorfree[Step]+=len(D[Step][n])+len(Iter_lock[n])


			
	final_Iter.append(Iter)
	final_Iter_F.append(Iter_F)
	final_Iter_p.append(Iter_p)
	final_Iter_I.append(Iter_I)
    #Not if the following happens the second step does not happen as all iterations are exhautsed
	#only last step happens
	if not anydecoded(decoded):
		if final_Iter[0]==maxiter:
			for n in nodes:
				for q in nodes:
					if q!=n:
						decoded[n][nodes.index(q)]=Step+1 # evrything in table is made 1
                        decoded_vector[n][q]=Rev_data[q]
             
                Iter_errorfree[0]=M*N
                
	print decoded
	print 
		
	#Step 2 till F  one side communications-------------------------------------------------------------
	#********************************************************************************************START HERE		
	#The nodes with nothing decoded communicate
	Iter=final_Iter[0]
	Step+=1
   	while all([anydecodedat(decoded,n) for n in nodes])==0 and Iter < maxiter:
		Iter+=1
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		Iter_T=I_ord[Iter_G-T:Iter_G] 
		Iter_F=list(set(range(N))-set(Iter_I)) 
        for n in nodes:
            if not anydecodedat(decoded,n):
                # node with no decoded vector transmits
                Iter_lock[n]=ec.getUN(Rev_data[n],Iter_T,False)
                D[Step][n]=ec.getUN(Rev_data[n],Iter_F,True)
                decoded_vector[n]={} #decoded vectors AT node n
                decoded_vector[n][n]=Rev_data[n] 
                Iter_key[n]={}
                
                #All other nodes(q) decoding n
                for q in nodes:
                    if q!=n and anydecodedat(decoded,n)==0: #stops this step once one node decodes this
                        decoded_vector[q][n]=ec.polarSCdecodeG(Orig_data[q],N,Iter_p,Iter_I,list(D[Step][n]),False) 
                        Iter_key[q][n]=ec.getUN(decoded_vector[q][n],Iter_T,False)
                        if not is_mismatch(Iter_key[q][n],Iter_lock[n]):                   
							decoded[q][nodes.index(n)]=Step+1
                            #reverse
							D[Step][q]=ec.getUN(Rev_data[q],Iter_F,True)# reverse
							decoded_vector[n][q]=ec.polarSCdecodeG(Orig_data[n],N,Iter_p,Iter_I,list(D[Step][q]),False)
							decoded[n][nodes.index(q)]=Step+1 #reverse
							Iter_errorfree[Step]=len(D[Step][n])-len(D[Step-1][n])+len(D[Step][q])-len(D[Step-1][q])
							Step+=1
							final_Iter.append(Iter)
							final_Iter_F.append(Iter_F)
							final_Iter_p.append(Iter_p)
							final_Iter_I.append(Iter_I)

	
	#if some nodes have no decoded vectors even after last iter, last step
	# last step is 3
	if final_Iter[-1]==maxiter:
		revNotover=True
		for n in nodes:
			
			if not anydecodedat(decoded,n):
				# Everybody gets broadcast
				for q in nodes:
					if q!=n:
						decoded_vector[q][n]=Orig_data[n]
						decoded[q][nodes.index[n]]=Step
				
				#for every node with no decoding all transferred
				prevcom=sum([len(D[i][n]) for i in range(Step)])		
				Iter_errorfree[Step]=Iter_errorfree[Step]+N-prevcom-t

				#connecting this node to some node
				for q in nodes:
					if q!=n and (1 in decoded[q]):
						decoded_vector[n][q]=Orig_data[q]
						decoded[n][nodes.index[q]]=Step
						# considered that all these floating nodes was connected to some node decoded in first step
						if revNotover:
							prevcom=sum([len(D[i][q]) for i in range(Step)])		
							Iter_errorfree[Step]=Iter_errorfree[Step]+N-prevcom-t
							revNotover = False
						
	print decoded
	#final decoding-----------------------------------------------------------------
	
	for n in nodes:
		for q in nodes:
			if q!=n:
				try:
					if decoded[n][nodes.index(q)]==0:
						(Path,isnav)=isnavigable(nodes,decoded,n,q)
						prevnode=n
						for i in range(len(Path)-1):
							if decoded[n][nodes.index(Path[i+1])]==0:
								decstep=getdecstep(decoded,prevnode,Path[i+1])
								decoded_vector[n][Path[i+1]]=ec.polarSCdecodeG(decoded_vector[n][prevnode],N,final_Iter[decstep],final_Iter_I[decstep],list(D[decstep][Path[i+1]]),False)
								decoded[n][nodes.index(Path[i+1])]="F"
				except:
					print "Final decoding error"
					print "src="+n+",dst="+q
					print decoded
				

	
	for n in nodes:
		decoded_origdata[n]={}
		err[n]={}
		for q in nodes:
			decoded_origdata[n][q]= ec.polarencode(decoded_vector[n][q],N)
			#err[n][q]=(decoded_origdata[n][q].tolist() != Orig_data[n][q].tolist())
			err[n][q]=0

	Total_error_free= sum(Iter_errorfree)
	
	error=0
	error= (sum([err[n][q] for (n,q) in zip(nodes,nodes)])) >0 
	#print error

	
	if not error:	
		Emp_comp_len=Total_error_free
	else:
		Emp_comp_len=4*N

		
	return (Total_error_free,error,decoded,Emp_comp_len)

	
def send_rateless_file_Iter_retro_det_4G_sim(N,T,compound_plist_u,channel_p,error_free_msg_length,runsim,printFT):
	#error_free_msg_length is the initial error_free_msg_length, that is the frozen bits considered+T.
	compound_plist=list(compound_plist_u) #best channel first
	compound_plist.sort()
	I_ord=pcon.getreliability_order(N)
	lenG=len(compound_plist)
	Glist=getGlistfile(N- (error_free_msg_length-T),lenG)
	Fp1=N-Glist[0] #initial errorfree (simulation monitoring param)
	
	print "channel_p:"
	print channel_p
	print "error_free_msg:"+str(Fp1+T)
	block_errorcnt=0
	
	errorfree_ach_rate=0
	Emp_comp=0


    #-------------- Simulation input formation
    
	nodes=["A","B","C","D"]	
	M = len(nodes)

	Orig_data={}
    #---------------------
	for i in range(runsim):
		XN=np.random.randint(2,size=N)
		Orig_data[nodes[0]]=XN

        #MC 
		for i in range(M-1):
			Orig_data[nodes[i+1]]=pl.BSCN(channel_p[i],Orig_data[nodes[i]])
			
		#Tree
		for i in range(M-1):
			Orig_data[nodes[i+1]]=pl.BSCN(channel_p[i],Orig_data[nodes[0]])
		
		
		(Total_error_free,error,decoded,Emp_comp_len)=send_rateless_file_Iter_retro_4G(Orig_data,N,I_ord,channel_p,compound_plist,Glist,T,printFT)
		errorfree_ach_rate+=float(Total_error_free)/(N*runsim) # calculates E{D}/N
		Emp_comp+=float(Emp_comp_len)/(N*runsim)
		block_errorcnt+=error
		
	#print block_errorcnt
	block_error=float(block_errorcnt)/runsim

	# the last simulation decoded is returned	
	return (errorfree_ach_rate,block_error,decoded,Emp_comp)
	
