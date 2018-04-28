#--------------------------------------------
# Name:       tbounds.py
# Purpose:    getting practical bounds on t
#
# Author:      soumya
#
# Created:     21/4/2018
#----------------------------------------

import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import polarconstruct as pcon
import matplotlib.pyplot as plt
import matlib as ml
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#==========================================complete polarization bounds
def mdcompletepol(Tlist):
	return list(np.power(0.5,Tlist))
	
#print mdcompletepol([1,2,4,8,16,32,64])

#==================================================Zindebounds
def mdindeZ(Tlist,N,NR_p1,p):
	(I,Z)=pcon.getreliability_orderZ(N,p)
	lhs=[]
	for T in Tlist:
		#print 1-np.power(10,Z[NR_p1-T:NR_p1])
		Zinv=[.5-np.sqrt(1-np.power(z,2))/2 for z in np.power(10,Z[NR_p1-T:NR_p1])]
		lhsT=np.prod(1-np.array(Zinv))
		#print lhsT
		lhs.append(lhsT)
	return lhs

def mdmaxZ(Tlist,N,NR_p1,p):
	(I,Z)=pcon.getreliability_orderZ(N,p)
	lhs=[]
	for T in Tlist:
		#print 1-np.power(10,Z[NR_p1-T:NR_p1])
		Zinv=[.5-np.sqrt(1-np.power(z,2))/2 for z in np.power(10,Z[NR_p1-T:NR_p1])]
		print np.power(10,Z[NR_p1-T:NR_p1])
		print Zinv
		lhsT=(1-max(np.array(Zinv)))
		#print lhsT
		lhs.append(lhsT)
	return lhs


def pmdguarantee(Tlist,N,NR_p1,p,a):
	pmd=np.array(mdindeZ(Tlist,N,NR_p1,p))
	pmdl=list(pmd)
	closest=ml.takeClosest(pmdl,a)
	#print Tlist
	#print pmd
	#print closest
	T= list(Tlist)[pmdl.index(closest)-1]
	return T

#=============================================union bounds
def pfunionZ(Tlist,N,NR_p1,p):		
	(I,Z)=pcon.getreliability_orderZ(N,p)
	lhs=[]
	for T in Tlist:
	  lhsT=sum(np.power(10,Z[NR_p1-T:NR_p1]))
	  #print lhsT
	  lhs.append(lhsT)

	return lhs
	
def estimateFER(Tlist,N,NR_p1,p,Iter):
	(I,Z)=pcon.getreliability_orderZ(N,p)
	FERlist=[]
	for T in Tlist:
	  FER=sum(np.power(10,Z[0:int(NR_p1/Iter)-T]))
	  #print lhsT
	  if FER<1:
		FERlist.append(FER)
	  else:
		FERlist.append(1) 
	return np.array(FERlist)

