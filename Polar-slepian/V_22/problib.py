#-------------------------------------------------------------------------------
# Name:       problib.py
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
from scipy.stats import norm
#import matplotlib.pyplot as plt
import matlib as ml

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
#---------------------------------------------------------------
#nats entropy	
def binary_entropy_nats(prob):
    return -prob*np.log(prob) - (1-prob)*np.log(1-prob)
 
def binary_entropy_nats_prime(prob):
    return np.log((1-prob)/prob)
 
def inverse_binary_entropy_nats(entropy_val, num_iter=3):
    guess = (np.arcsin((entropy_val/np.log(2))**(1/.645)))/np.pi
    for i in range(num_iter):
        guess = guess + np.nan_to_num((entropy_val-binary_entropy_nats(guess))/binary_entropy_nats_prime(guess))
    return guess

#===========================================================BSC channel
#---------------------------------------------------------N BSC channel
def BSCN(p,inbitarray):
	N=np.size(inbitarray)
	flip=np.random.binomial(1,p,N) #generates N ber(p) instances
	outbitarray=np.logical_xor(inbitarray,flip)
	return outbitarray

def ZBSC(p):
	return ma.sqrt(4*p*(1-p))
	
def CapacityBSC(N,p):
	return (1-h(p))*N

def V(p):
	return p*(1-p)*(np.log2(np.log2((1-p)/p)))

def Inversecap1024(C):
	table = []
	with open("./simresults/p_vs_cap.txt",'r') as f:
		for line in f:
			table.append(json.loads(line))
			
	#~ print table[0]
	#~ print table[1]
	#~ print ml.takeClosest(table[1],C)
	return table[0][table[1].index(ml.takeClosest(table[1],C))]

#~ print Inversecap1024(10)




	
def FBCapBSC(N,p,e):
	Qc=norm.ppf(1-10**e)
	C=CapacityBSC(N,p)
	return C-np.sqrt(N*V(p))*Qc
	

#~ B=range(200,2200,200)
#~ plt.plot(B,[CapacityBSC(b,0.11)/b for b in B])
#~ plt.plot(B,[FBCapBSC(b,0.08,-4)/b for b in B])
#~ plt.show()

#~ E=[-6,-5,-4,-3,-2]
#~ p=np.arange(0.01,0.51,0.01)
#~ p2=[0.04,0.15,0.2,0.25]
#~ print [CapacityBSC(1024,pi) for pi in p2]
#~ plt.plot(p,[CapacityBSC(1024,pi) for pi in p],marker='o')
#~ for e in E:
	#~ plt.plot(p,[FBCapBSC(1024,pi,e) for pi in p],label=str(e),marker='o')
	#~ print [FBCapBSC(1024,pi,e) for pi in p2]
#~ plt.legend(loc="best")
#~ plt.grid(True)

#~ plt.show()


#print FBCapBSC(1024,0.15,-float("inf"))
	

#------------------------------------------27-12-2017
#returns a list of rates for a list of 'p'
#where each rate is a given fraction (derate) capacity of 'p' 	
def getRatelist(plist,derate):
	#insert derating
	Ratelist=[ CapacityBSC(1,p)*derate for p in plist]
	return Ratelist
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
#===========================================================Other
def bitbertober(bitber_exp):
	ber=sum([10**i for i in bitber_exp])
	ber_exp=np.log10(ber)
	return ber_exp

#print NCkflips(4,3)
#print BSCepatflip(8)
def getMeanIter(Iterprobdict,maxiter):
	MI=[]
	for d in Iterprobdict:
		mi=0
		for k in d:
			if int(k)>0:
				mi+=int(k)*d[k]
			else:
				mi+=maxiter*d[k]
		MI.append(mi)	
	return MI
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
