#-------------------------------------------------------------------------------
# Name:       polarencdec.py
# Purpose:    polar coding and decoding
#
# Author:      soumya
#
# Created:     04/08/2017
# Encoding: following arikan lectures
# Decoding : following Harish Vangala
#
#----------------------------------------
import sys
sys.path.insert(0, './cfunctions/boost')
import PolarCode as pc
import numpy as np
import matlib as ml
import math as ma
import problib as pl


#======================================================support functions
def getF(n):
	F=np.array([[1,0],[1,1]])
	return ml.kronpow(F,n) 

#print getF(3)
#---------------------------------------------------decoding likelihood
#l1=llr1, l2=llr2
#f=ma.log((1+ma.exp(l1+l2))/(exp(l1)+exp(l2)))
#NOTE:
#in UN_decoded root of computation tree is flevel 0 there are n levels(n+1 th level is Yn and not considered)
#in LL leaf is level 0 and there are n+1 levels
#flevel = n - level

def f(l1,l2):
	if l1==-float("inf") or l2==-float("inf"):
		return -float("inf")
	#fval=np.sign(l1)*np.sign(l2)*min(abs(l1),abs(l2))
	try:	
		#fval=ma.log((1+ma.exp(l1+l2))/(ma.exp(l1)+ma.exp(l2)))
		fval = ml.logdomain_sum(llr1+llr2,0) - ml.logdomain_sum(llr1,llr2);
		
	except:
		#print l1,l2 
		fval=np.sign(l1)*np.sign(l2)*min(abs(l1),abs(l2))
	return fval

def g(l1,l2,fbit):
	if fbit==-1 or l1==-float("inf") or l2==-float("inf"):
		return -float("inf")
	else:	
		gval=l2+((-1)**fbit)*l1
		return gval
    
def active_levels(i,n):
	i_bin="{0:0{width}b}".format(i,width=n)
	i_bin.zfill(n)
	acl=0
	for j in i_bin:
		if j=='0':
			acl+=1
		else:
			break;
	return min(acl+1,n+1)
	
def ML(llr):
	if llr==-float("inf"):
		return -1
	if llr>0:
		return 0
	else:
		return 1
		
def bitreverseorder(J,n):
	#J is list of indices
	RJ=[]
	for i in J:
	 RJ.append(int('{:0{width}b}'.format(i,width=n)[::-1], 2))		
	return RJ

def isupperrow(requested_row,level):
	setindex=int(requested_row/(2**level))
	if setindex%2==0:
		return True
	else:
		return False
	 
#this function does not return anything, populates UN[requested_row][level]	
def bitrequest(UN_decoded,requested_row,level,n):
	flevel=n-level
	#print level,flevel
	#print "IN bit req"
	
	
	if UN_decoded[requested_row][flevel]!= -1 or flevel==0:#UN_decoded vector
		return
	else:
		if isupperrow(requested_row,level):
			#print "upper row"
			#print requested_row,flevel-1
			#print requested_row+(2**(level)),flevel-1
			
			
			if UN_decoded[requested_row][flevel-1]== -1:				
				bitrequest(UN_decoded,requested_row,n-(flevel-1),n)	
				
					
			if UN_decoded[requested_row+(2**(level))][flevel-1] == -1:				
				bitrequest(UN_decoded,requested_row+(2**(level)),n-(flevel-1),n)
						
				
			#print UN_decoded[requested_row][flevel-1],UN_decoded[requested_row+(2**(level))][flevel-1]
			UN_decoded[requested_row][flevel]=int(UN_decoded[requested_row][flevel-1]) ^ int(UN_decoded[requested_row+(2**(level))][flevel-1])
			
				
				
		else:	
			#print "lower row"		
			#print requested_row,flevel-1
			if UN_decoded[requested_row][flevel-1]== -1:
				bitrequest(UN_decoded,requested_row,n-(flevel-1),n)
			
				
			
			UN_decoded[requested_row][flevel]=UN_decoded[requested_row][flevel-1]
			
		    
def getLLR(design_p,n,decodebit,requested_row,g_level,level,LL,UN_decoded,YN):
	p=design_p
	#g_level is last #print "start"
	if level<g_level:
		return
	#print "request"	
	#print requested_row,level
	#print decodebit,requested_row,level
	ffl=0
	gfl=0
	if LL[requested_row][level] == -float("inf"):
		if level==g_level:
		
			if decodebit==0:
				
				LL[requested_row][level]=pl.LLR(p,YN[requested_row])
				#print requested_row,level
				
			
			else:
				gfl=1
				#print "calling for g " + str(requested_row-2**(level - 1))+","+str(requested_row)
				
				getLLR(p,n,decodebit,requested_row-(2**(level - 1)),g_level,level-1,LL,UN_decoded,YN)
				getLLR(p,n,decodebit,requested_row,g_level,level-1,LL,UN_decoded,YN)
				bitrequest(UN_decoded,requested_row-(2**(level - 1)),level,n)
				
				
				LL[requested_row][level] = g(LL[requested_row-(2**(level - 1))][level-1],LL[requested_row][level-1],UN_decoded[requested_row-(2**(level - 1))][n-level])
				
		else:
		   	#print "calling for f " + str(requested_row)+","+str(requested_row+(2**(level - 1)))		    
			getLLR(p,n,decodebit,requested_row,g_level,level-1,LL,UN_decoded,YN)
			getLLR(p,n,decodebit,requested_row+(2**(level - 1)),g_level,level-1,LL,UN_decoded,YN)
		
			LL[requested_row][level]=f(LL[requested_row][level-1],LL[requested_row+(2**(level - 1))][level-1])
			ffl=1
	"""		
	print "back",requested_row,level
	if ffl==1:
		try:
			print LL[requested_row][level-1],LL[requested_row+(2**(level - 1))][level-1]
			print f(LL[requested_row][level-1],LL[requested_row+(2**(level - 1))][level-1])
		except:
			pass
	if gfl==1:
		try:
		
			print LL[requested_row-(2**(level - 1))][level-1],LL[requested_row][level-1],UN_decoded[requested_row-(2**(level - 1))][n-level]
			print g(LL[requested_row-(2**(level - 1))][level-1],LL[requested_row][level-1],UN_decoded[requested_row-(2**(level - 1))][n-level])
			print UN_decoded
		except:
			pass
		
	print LL
	"""
#------------------------------------------------------construction 
#---I is ascending 
#---UNx is filled in as it comes
	
def formVN_s(UN,N,I,FD):
	VN=[]
	
	for i in range(N):
		if i in I:
		    VN.append(UN.pop(0))
		else:
			VN.append(FD.pop(0))
			
	return VN

#---I is reliability ordered
#---UNx is filled in as it comes
#i.e UNx is formed as fer reliability ordering
def formVN_u(UN,N,I,FD):
	
	ind_FD=list(set(range(N))-set(I))
	ind_FD.sort();
	
	VN=[0]*N
	for i in I:
		VN[i]=UN.pop(0)
	for i in ind_FD:
		VN[i]=FD.pop(0)	
	return VN
#---------------------------------------------------------------------	
def getUN(d,I,isort):
	if isort:
		I.sort()
	return np.array([d[i] for i in I])
	
def getchannel(d,I,isort):
	if isort:
		I.sort()
	return [d[i] for i in I]
	
#-----------------------------------------------------------------------
def butterfly(u1,u2): #implements arikans F
	return(np.logical_xor(u1,u2),u2)
	
def polarencrec(UN,l,n):
	#print "l="+str(l)
	N=2**n
	XNl=np.zeros(N)	
	if l==0:	
		for i in range(N):
			if isupperrow(i,l):
				(XNl[i],XNl[i+1])=butterfly(UN[i],UN[i+1])
	else:
		XNlprev=polarencrec(UN,l-1,n)
		for i in range(N):
			if isupperrow(i,l):
				(XNl[i],XNl[i+2**l])=butterfly(XNlprev[i],XNlprev[i+2**l])
	#print XNl
	return XNl
	

		
		
#====================================================encode - decode good channels
#good channels versions
#try overloading 

#---------------------------------------------------recursive encoder	
def polarencodeG(UN,N,I,D,isort): 
	#Un is original bit array,I are good channels,D is data
	#to put UN in good channels(I) and D in frozen channels
	
	n=int(ma.log(N,2))
	
	VN=[]
	UNx=list(UN) #as pop is a destructive readout
	
	if len(UN)==len(I) and len(D)==N-len(I):
		if isort:
			VN=formVN_s(UNx,N,I,D)
		else:
			VN=formVN_u(UNx,N,I,D)
   	else:
		print "UN length"
		print len(UN)
		print "G"
		print len(I)
		print "F"
		print len(D)
		print "N-G"
		print N-len(I)
		print "DATA SIZE MISMATCH"
		return
	#print VN
	
	XN=polarencrec(VN,n-1,n)
	
	return XN        #XN enters channel

def polarSCdecodeG(YN,N,design_p,I,D,llr_needed):
	p=design_p
	n=int(ma.log(N,2))
	UN_decoded=np.zeros((N,n),dtype=int)-1
	LL=np.zeros((N,n+1))-float("inf") #likelihoods will rarely be equal to -float("inf")
	
	#assuming that D is popped from 0 while encoding
	#the indexes of D and ind_D will match one to one
	ind_D=list(set(range(N))-set(I))
	ind_D.sort()
	
	dec_order=bitreverseorder(range(N),n)
    
   
	for i in dec_order:
		
		#print "decoding "+ str(i)
		#print "--------------------"
		
		#LLR flow
		No_act_levels=active_levels(i,n)
		act_levels=n-np.array(range(No_act_levels),dtype=int)
		#print act_levels

		getLLR(p,n,i,i,min(act_levels),max(act_levels),LL,UN_decoded,YN)
		
		if i not in I:
			
			UN_decoded[i][0]=D[ind_D.index(i)]
		else:
			UN_decoded[i][0]=int(ML(LL[i][n]))
			
		
		
	if llr_needed:
		return (LL[:,n],np.transpose(UN_decoded[:,0]))
	else:
		return np.transpose(UN_decoded[:,0])
		

"""		
def polarSCdecodeGlist(YN,N,design_p,I,D,llr_needed,listsize):
	
		if llr_needed:
		return (LL[:,n],np.transpose(UN_decoded[:,0]))
	else:
		return np.transpose(UN_decoded[:,0])	
"""	

#This could be done by modifying D but patching for now		
def polarIncFrzSCdecodeG(YN,N,design_p,I,D,IncFreeze_ind,IncFreeze_data,llr_needed):
	p=design_p
	n=int(ma.log(N,2))
	UN_decoded=np.zeros((N,n),dtype=int)-1
	LL=np.zeros((N,n+1))-float("inf") #likelihoods will rarely be equal to -float("inf")
	
	#assuming that D is popped from 0 while encoding
	#the indexes of D and ind_D will match one to one
	ind_D=list(set(range(N))-set(I)-set(IncFreeze_ind))
	#print ind_D
	ind_D.sort()
	
	dec_order=bitreverseorder(range(N),n)
    
   
	for i in dec_order:
		
		#print "decoding "+ str(i)
		#print "--------------------"
		
		#LLR flow
		No_act_levels=active_levels(i,n)
		act_levels=n-np.array(range(No_act_levels),dtype=int)
		#print act_levels

		getLLR(p,n,i,i,min(act_levels),max(act_levels),LL,UN_decoded,YN)
		
		if i not in I:
			#if 
			#print i
			if i in IncFreeze_ind:
				UN_decoded[i][0]=IncFreeze_data[IncFreeze_ind.index(i)]
			else:
				UN_decoded[i][0]=D[ind_D.index(i)]
		else:
			UN_decoded[i][0]=int(ML(LL[i][n]))
			
		
		
	if llr_needed:
		return (LL[:,n],np.transpose(UN_decoded[:,0]))
	else:
		return np.transpose(UN_decoded[:,0])	
#======================================================encode - decode channel charac

#------------------------------------------------------------recursive encoder	
 	
	
def polarencode(UN,N): #Un is original bit array
	n=int(ma.log(N,2))
	XN=polarencrec(UN,n-1,n)
	return XN


def polarSCdecode(YN,N,design_p): #YN is OP of channel
	p=design_p
	n=int(ma.log(N,2))
	UN_decoded=np.zeros((N,n),dtype=int)-1
	LL=np.zeros((N,n+1))-float("inf") #likelihoods will rarely be equal to -float("inf")
	
	dec_order=bitreverseorder(range(N),n)
    
   
	for i in dec_order:
		
		#print "decoding "+ str(i)
		#print "--------------------"
		
		#LLR flow
		No_act_levels=active_levels(i,n)
		act_levels=n-np.array(range(No_act_levels),dtype=int)
		#print act_levels

		getLLR(p,n,i,i,min(act_levels),max(act_levels),LL,UN_decoded,YN)
		UN_decoded[i][0]=int(ML(LL[i][n]))
	
		"""
		print "final"	
		print 	LL
		print UN_decoded
		"""
	#print 	LL
	#print UN_decoded
	return np.transpose(UN_decoded[:,0])
#===================================================encode-decode list using tavildar c++implementations
def polarcode_init(N,G,design_p,ED_size): #ED_size=crc_size or cb_size right now cb to be kept 0
	n=int(ma.log(N,2))
	z=np.sqrt(4*design_p*(1-design_p))
	pc1=pc.PolarCode(n,G,z,ED_size)
	return pc1

def polarcode_init_defch(N,G,design_p,I_ord,ED_size): #ED_size=crc_size or cb_size right now cb to be kept 0
	n=int(ma.log(N,2))
	z=np.sqrt(4*design_p*(1-design_p))
	pc1=pc.PolarCode(n,G,z,ED_size)
	pc1.channel_ordering=bitreverseorder(I_ord,n)
	return pc1

def polarencodeG_C(pc1,UN,D):
	#isort is FALSE
	N=2**pc1.n
	I_ord=pc1.channel_ordering
	
	frozen_indices=I_ord[pc1.info_length-N:] #reverse indexing
	frozen_bits=list([0]*N)
	
	for i in range(pc1.info_length,N):
		frozen_bits[i]=D.pop(0)
		
	pc1.frozen_bits=frozen_bits	
	return np.array(pc1.encode(UN))
		

def polarSCdecodeG_C(pc1,YN,decode_p,D,list_size): 
	# decode_p is not neccessarily design p(should be but not neccessarily), not channel_p either, used for decoding
	#isort is FALSE
	N=2**pc1.n
	I_ord=pc1.channel_ordering
	
	frozen_indices=I_ord[pc1.info_length-N:]
	frozen_bits=list([0]*N)
	
	for i in frozen_indices:
		frozen_bits[i]=D.pop(0)
		
	pc1.frozen_bits=frozen_bits	
	
	llrYN=[pl.LLR(decode_p,y) for y in YN]
	return np.array(pc1.decode_scl(llrYN,list_size))
	
def polarSCdecodefileG_C(pc1,YN,decode_p,D,list_size): 
	# decode_p is not neccessarily design p(should be but not neccessarily), not channel_p either, used for decoding
	#isort is FALSE
	N=2**pc1.n
	I_ord=pc1.channel_ordering
	
	frozen_indices=I_ord[pc1.info_length-N:]
	frozen_bits=list([0]*N)
	
	for i in frozen_indices:
		frozen_bits[i]=D.pop(0)
		
	pc1.frozen_bits=frozen_bits	
	
	llrYN=[pl.LLR(decode_p,y) for y in YN]
	return np.array(pc1.decode_scl_file(llrYN,list_size))
		
	

def polarIncFrzSCdecodeG_C(pc1,YN,decode_p,D,IncFreeze_ind,IncFreeze_data,list_size):
	#llr_needed is False
		# decode_p is not neccessarily design p(should be but not neccessarily), not channel_p either, used for decoding
	#isort is FALSE
	N=2**pc1.n
	I_ord=bitreverseorder(pc1.channel_ordering,pc1.n)
	#print I_ord
	
	#---The entire set of frozen indices
	frozen_indices=I_ord[pc1.info_length-N:]
	frozen_indices.sort()
	frozen_bits=list([0]*N)
	
	Revfrozen_indices=bitreverseorder(frozen_indices,pc1.n)
	RevIncfrozen_indices=bitreverseorder(IncFreeze_ind,pc1.n)
	
	#print Revfrozen_indices,RevIncfrozen_indices
	
	#print len(Revfrozen_indices),len(RevIncfrozen_indices),len(D)
	
	for i in Revfrozen_indices:
		if i in RevIncfrozen_indices:
			frozen_bits[i]=IncFreeze_data.pop(0)
		else:
			frozen_bits[i]=D.pop(0)
				
	pc1.frozen_bits=frozen_bits
	llrYN=[pl.LLR(decode_p,y) for y in YN]
	return np.array(pc1.decode_scl(llrYN,list_size))

