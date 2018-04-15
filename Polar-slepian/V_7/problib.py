#-------------------------------------------------------------------------------
# Name:      probability/channel-library
# Purpose:    related to prob and channel
#
# Author:      soumya
#
# Created:     04/08/2017
#----------------------------------------
import numpy as np
import math as ma
import json
import collections as col
import itertools



#===============================================================ber rv
def ber(p):
	#can be done using a set of uniform draws mapped to 1 , say 2/10
	# and the other set mapped to 0
	
	return np.random.binomial(1,p) # ber is bin with n=1

#Note : bit is integer, inbitarray is integer array
#-------------------------------------------------------------------
def condp(p,y,x):
	if y==x:
		return 1-p
	else:
		return p

#------------------------------------------------------------------
def LLR(p,y):
    return ma.log(condp(p,y,0)/condp(p,y,1))
#------------------------------------------------------------------
def h(p):
	return (-p*ma.log(p,2)-(1-p)*ma.log(1-p,2))

#===========================================================BSC channel

#---------------------------------------------------------1 BSC channel
def BSC1(p,bit): #p is flip over 
	return ber(p)^bit

#---------------------------------------------------------n BSC channel
def BSCN(p,inbitarray):
	N=np.size(inbitarray)
	flip=np.random.binomial(1,p,N) #generates N ber(p) instances
	outbitarray=np.logical_xor(inbitarray,flip)
	return outbitarray

#old	
def BSCN_1(p,inbitarray):
	N=np.size(inbitarray)
	#print n
	outbitarray=np.array([])
	
	for i in range(n):
		outbitarray=np.append(outbitarray,BSC1(p,inbitarray[i]))

	return outbitarray #outbitarray is float


#returns error vector    
def BSCNe(p,inbitarray):
	return np.logical_xor(BSCN(p,inbitarray),inbitarray)
	
def ZBSC(p):
	return ma.sqrt(4*p*(1-p))
	
def CapacityBSC(N,p):
	return (1-h(p))*N
"""
N=1024	
plist=[0.0833,0.192,0.2455,0.278]
Cap=[CapacityBSC(N,p) for p in plist]
print Cap
print plist
"""	
def BSCepatMC(N,p,prec):
	# range(N+1) gives all error patterns
	#simulation is run runsim * | error patterns |
	runsim=(10**prec)*N
	errdict={} 
	for i in range(runsim):
		flip=np.random.binomial(1,p,N).tolist()
		flipstr= "".join(str(x) for x in flip)
		try:
			errdict[flipstr]+=float(1)/runsim
		except:
			errdict[flipstr]=float(1)/runsim
			
	print sum(errdict.values())
	
	errdict_ordered=col.OrderedDict(sorted(errdict.items(), key=lambda t: t[1], reverse=True)) #check 
	filename="./simresults/errdictMC_"+str(N)+"_"+str(p).replace(".","p")+".txt"	
	f1=open(filename,'w')
	json.dump(errdict_ordered,f1,indent=2)
	return filename
		
def BSCepatprob(N,p):
	errdict={} 
	for i in range(2**N):
		flip=bin(i)[2:].zfill(N)
		#print flip
		count1=col.Counter(flip)['1']
		
		P=(p**count1)*((1-p)**(N-count1))
		errdict[flip]=P
			
	print sum(errdict.values())
	
	errdict_ordered=col.OrderedDict(sorted(errdict.items(), key=lambda t: t[1], reverse=True)) #check 
	filename="./simresults/errdict_"+str(N)+"_"+str(p).replace(".","p")+".txt"	
	f1=open(filename,'w')
	json.dump(errdict_ordered,f1,indent=2)
	return errdict_ordered

def BSCepatflip(N):
	flipdict={}
	for i in range(2**N):
		flip=bin(i)[2:].zfill(N)
		fliplist=[int(d) for d in flip]
		try:
			flipdict[str(sum(fliplist))].append(fliplist)
		except:
			flipdict[str(sum(fliplist))]=[fliplist]
	
	filename="./simresults/flipdict_"+str(N)+".txt"	
	f1=open(filename,'w')
	json.dump(flipdict,f1)
	return flipdict
			
def nCkflips(n, k,filewrite):
	result = []
	try:
		f1=open("./simresults/"+str(n)+"C"+str(k)+".txt",'r')
		result=json.load(f1)
	except:
		
		for bits in itertools.combinations(range(n), k):
			s = ['0'] * n
			for bit in bits:
				s[bit] = '1'
			result.append(''.join(s))
			#result.append([int(i) for i in s])
		if filewrite:
			f1=open("./simresults/"+str(n)+"C"+str(k)+".txt",'w')
			json.dump(result,f1)
    
	return result

#print NCkflips(4,3)
#print BSCepatflip(8)

#----------------------------------------------------------------------

#s=0	
#for i in range(100):
#    s=s+ber(0.5)
#print s	

#s=0	
#for i in range(100):
#    s=s+BSC1(0.1,1)
#print s		

#print float(sum(BSCN(0.4,np.zeros((1000,), dtype=np.int))))/1000

#print sum(BSCN_1(0.2,np.zeros((1000,), dtype=np.int)))/1000
