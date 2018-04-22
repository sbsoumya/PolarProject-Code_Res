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

#==========================================complete polarization bounds
def mdcompletepol(Tlist):
	return list(np.power(0.5,Tlist))
	
print mdcompletepol([1,2,4,8,16,32,64])

#==================================================Zindebounds
def mdindeZ(Tlist,N,NR_p1,p_2):
	(I,Z)=pcon.getreliability_orderZ(N,p_2)
	lhs=[]
	for T in Tlist:
		#print 1-np.power(10,Z[NR_p1-T:NR_p1])
		Zinv=[.5-np.sqrt(1-np.power(z,2))/2 for z in np.power(10,Z[NR_p1-T:NR_p1])]
		lhsT=np.prod(1-np.array(Zinv))
		#print lhsT
		lhs.append(lhsT)
	return lhs

#print .5-np.sqrt(1-np.power(1,2))/2 
print mdindeZ([1,2,4,8,16,32,64],1024,540,0.2)
#print mdindeZ([1,2,4,8,16,32,64],1024,360,0.3)
#=============================================union bounds(NOT OK)
#~ def mdunionZ(Tlist,N,NR_p1,p_2):		
	#~ (I,Z)=pcon.getreliability_orderZ(N,p_2)
	#~ lhs=[]
	#~ for T in Tlist:
		#~ print Z[NR_p1-T:NR_p1]
		#~ print [10**z for z in Z[NR_p1-T:NR_p1]]
		#~ print np.power(10,Z[NR_p1-T:NR_p1])
		#~ lhsT=1-sum(np.power(10,Z[NR_p1-T:NR_p1]))
		#~ #print lhsT
		#~ lhs.append(lhsT)

	#~ return lhs
#~ #print mdunionZ([8],1024,540,0.192)
#===============================================1-PsT(subblock)

#for p=p2
#~ PSTCD=[0.5099, 0.248, 0.06440000000000001, 0.0039000000000000146, 0.0, 0.0, 0.0, 0.0]
#~ PST=[0.5057, 0.24939999999999996, 0.061000000000000054, 0.0031999999999999806, 0.0, 0.0, 0.0, 0.0]

#=================================================sim
#results for p=p2

complist=[0.08349999999999963, 0.19249999999999973]
p_1=complist[0]
p_2=complist[1]
p=0.1
N=1024
R_p1=540
rhs=0.01

#for p=p2
PSTCD=[0.5099, 0.248, 0.06440000000000001, 0.0039000000000000146, 0.0,0.0, 0.0, 0.0]
PST=[0.5057, 0.24939999999999996, 0.061000000000000054, 0.0031999999999999806,0.0, 0.0, 0.0, 0.0]
Tlist=[1,2,4,8,16,32,64,128]
figure=plt.plot()
#plt.semilogy(Tlist,mdcompletepol(Tlist),"b",label="COMPOL")
plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),":ro",label="CONINDZ-Ana")
plt.semilogy(Tlist,PST,"-m^",label="$1-P_S^T$ Simulation")
plt.semilogy(Tlist,PSTCD,"-g>",label="$1-P_S^T$ ,Simulation decoding with $p_2$")
plt.semilogy(Tlist,[rhs]*len(Tlist),"k",label="$P_{MD}$ required.")
plt.title("Bounds on T for N=1024,$p=p_2$\n $p_1=$"+str(p_1)+",$p_2=$"+str(p)+",$R_{P_1}=$"+str(R_p1))
plt.ylabel('$P_{MD}=P_{p}(L_{T}=K_{T})$')
plt.xlabel('T')
plt.grid(True)
plt.legend(loc="best")
plt.show()
