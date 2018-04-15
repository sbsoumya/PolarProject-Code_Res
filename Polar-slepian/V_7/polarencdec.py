#-------------------------------------------------------------------------------
# Name:       polar library
# Purpose:    polar coding and decoding
#
# Author:      soumya
#
# Created:     04/08/2017
# Encoding: following arikan lectures
# Decoding : following Harish Vangala
#
#----------------------------------------

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
	 
	
#print isupperrow(3,0)	
#print isupperrow(3,1)	
#print isupperrow(3,2)	
#print isupperrow(3,3)	

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
			
			
		#print "updated UN "+str(requested_row)+" "+str(flevel)
		#print UN_decoded[requested_row][flevel]
		#print UN_decoded

			    
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
#------------------------------------------------------sorted construction and extraction
#---I is ascending 
#---UNx is filled in as it comes
	
def formVN_s(UN,N,I,D):
	VN=[]
	
	for i in range(N):
		if i in I:
		    VN.append(UN.pop(0))
		else:
			VN.append(D.pop(0))
			
	return VN
def getUN_s(d,I):
	I.sort()
	return np.array([d[i] for i in I])
	
def getchannel_s(d,I):
	I.sort()
	return [d[i] for i in I]
	
#-----------------------------------------------------------------------
#---I is reliability ordered
#---UNx is filled in as it comes
def formVN_u(UN,N,I,D):
	
	ind_D=list(set(range(N))-set(I))
	ind_D.sort();
	VN=[0]*N
	for i in I:
		VN[i]=UN.pop(0)
	for i in ind_D:
		VN[i]=D.pop(0)	
	return VN
	
def getchannel_u(d,I):
	return [d[i] for i in I]	
	
def getUN_u(d,I):
	return np.array([d[i] for i in I])	
#-----------------------------------------------------------------------
def butterfly(u1,u2): #implements arikans F
	return(np.logical_xor(u1,u2),u2)
		
#======================================================encode - decode channel charac
#=======finalized


def polarencode(UN,N): #Un is original bit array
	n=int(ma.log(N,2))
	Fn=getF(n)
	XNd=np.dot(UN,Fn)
	XN=np.mod(XNd,2)
	return XN        #XN enters channel
#------------------------------------------------------------recursive encoder	
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
	    	
	
def polarencodeR(UN,N): #Un is original bit array
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
		
		
#====================================================encode - decode good channels
#good channels versions
#try overloading 


def polarencodeG(UN,N,I,D): 
	#Un is original bit array,I are good channels,D is data
	#to put UN in good channels(I) and D in frozen channels
	
	n=int(ma.log(N,2))
	Fn=getF(n)
	VN=[]
	UNx=list(UN) #as pop is a destructive readout
	if len(UN)==len(I) and len(D)==N-len(I):
		for i in range(N):
			if i in I:
			    VN.append(UNx.pop(0))
			else:
				VN.append(D.pop(0))
	else:
		print len(UN)
		print len(I)
		print len(D)
		print N-len(I)
		print "DATA SIZE MISMATCH"
		return
	#print VN
	
	XNd=np.dot(VN,Fn)
	XN=np.mod(XNd,2)
	
	return XN        #XN enters channel
#---------------------------------------------------recursive encoder	
def polarencodeGR(UN,N,I,D): 
	#Un is original bit array,I are good channels,D is data
	#to put UN in good channels(I) and D in frozen channels
	
	n=int(ma.log(N,2))
	
	VN=[]
	UNx=list(UN) #as pop is a destructive readout
	
	if len(UN)==len(I) and len(D)==N-len(I):
		
		VN=formVN_s(UNx,N,I,D)
   	else:
		print len(UN)
		print len(I)
		print len(D)
		print N-len(I)
		print "DATA SIZE MISMATCH"
		return
	#print VN
	
	XN=polarencrec(VN,n-1,n)
	
	return XN        #XN enters channel
	
def polarencodeGR_u(UN,N,I,D): 
	#Un is original bit array,I are good channels,D is data
	#to put UN in good channels(I) and D in frozen channels
	
	n=int(ma.log(N,2))
	
    #VN=[]
	UNx=list(UN) #as pop is a destructive readout
	if len(UN)==len(I) and len(D)==N-len(I):
        
		VN=formVN_u(UNx,N,I,D)
     
	else:
		print len(UN)
		print len(I)
		print len(D)
		print N-len(I)
		print "DATA SIZE MISMATCH"
		return
	#print VN
	
	XN=polarencrec(VN,n-1,n)
	
	return XN        #XN enters channel
	
def polarSCdecodeG(YN,N,design_p,I,D):
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
			
		
		
		
		#print "final"	
		#print 	LL
		#print UN_decoded
		
	#print 	LL
	#print UN_decoded
	return np.transpose(UN_decoded[:,0])
	
def polarSCdecodeG_LLR(YN,N,design_p,I,D):
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
			
		
		
		
		#print "final"	
		#print 	LL
		#print UN_decoded
		
	#print 	LL
	#print UN_decoded
	return (LL[:,n],np.transpose(UN_decoded[:,0]))

	    
#----------------------------------------coding decoding sim
"""
n=7
p=0.3
UN=np.random.randint(2,size=2**n)	
print "UN:"
print UN
print "Polar coded:"
print polarencode(UN,len(UN))
print polarencodeR(UN,len(UN))
"""

	
"""
print "YN:"
print pl.BSCN(p,polarencode(UN,len(UN)))		
print "UN_hat:"
print polarSCdecode(pl.BSCN(p,polarencode(UN,len(UN))),len(UN),p)
"""
"""
n=3
p=0.3
UN=np.random.randint(2,size=2**n)
UN=[1,1,0,0,0,1,0,1]	
print "UN:"
print UN
print "Polar coded:"
print polarencode(UN,len(UN))
print "YN:"
print pl.BSCN(p,polarencode(UN,len(UN)))		
print "UN_hat:"
#print polarSCdecode(pl.BSCN(p,polarencode(UN,len(UN))),len(UN),p)

print polarSCdecode(np.array([1,1,0,0,1,0,0,1]),len(UN),p)
#op = [0 0 1 1 0 1 1 1]
"""
#---------------------------------------goodchannelsim
"""
n=4
p=0.01
I=[15,7,11,13,14]
UN=[1,1,1,1,0]
N=2**n	
print "UN:"
print UN
print "Polar coded:"
print polarencodeGR_u(UN,N,I,[1,0,0,0,0,0,0,0,0,0,0])
print polarencodeG(UN,N,I,[1,0,0,0,0,0,0,0,0,0,0])
"""
"""
print "YN:"
print pl.BSCN(p,polarencodeG(UN,N,I,[1,0,0,0,0,0,0,0,0,0,0]))		
print "UN_hat:"
print polarSCdecode(pl.BSCN(p,polarencode(UN,len(UN))),len(UN),p)
"""


"""
n=4
p=0.01
N=2**n
I=[15,7,11,13,14]

D=np.zeros(N-len(I),dtype=int).tolist()
#I=range(N)
#D=[]

d=polarSCdecodeG(np.array([ 1,  0,  1,  1,  1,  1,  0,  0,  1,  1,  0,  0,  0,  0,  1,  1]),N,p,I,D)
d2=polarSCdecodeG(np.array([1,1,1,0,1,0,0,1,1,0,0,1,0,1,1,0]),N,p,I,D)
print d
print d2

print getUN_u(d,I)
print getUN_s(d2,I)
"""

#---------------------------------------------------Lambdasim
"""
n=4
p=0.3
N=2**n
I=[15,7,11,13,14]

D=np.zeros(N-len(I),dtype=int).tolist()
#I=range(N)
#D=[]

(L,d)=polarSCdecodeG_LLR(np.array([1,1,1,0,1,0,0,1,1,1,1,0,0,0,0,1]),N,p,I,D)
print d,L
print getUN_sd,I)
"""
#---------------------------------------------------------------------
#print getF(3)
#print 	bitreverseorder(range(8),3)
#print active_levels(0,3)
#print active_levels(4,3)
#print polarencode([1,0,0,0,1,1,1,1],8)	

