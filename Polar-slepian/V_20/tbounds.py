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
	
#print .5-np.sqrt(1-np.power(1,2))/2 
#print mdindeZ([1,2,4,8,16,32,64],1024,540,0.2)
#print mdindeZ([1,2,4,8,16,32,64],1024,360,0.3)
	
#==================================================ANAmaxTPT-T
# uses above indeZ estimate of pmd and finds the tpt vs T vector for a scheme with maxiter=2
def maxTPT_ana(Tlist,F1,F2,N,NR_p1,p):
	PMD=np.array(mdindeZ(Tlist,N,NR_p1,p))
	E_Iter=PMD + (1-PMD)*2
	print E_Iter
	
	FER=PMD*F1 + (1-PMD)*F2
	TPT=(NR_p1-np.array(Tlist))*(1-FER)/(N*E_Iter)
	return TPT

# maxTPT_ana([1,2,4,8,16,32,64,128],.9,.01,1024,540,0.11)
#~ plt.plot(np.arange(1,100,1),maxTPT_ana(np.arange(1,100,1),.9,.01,1024,540,0.11),"-g^")
#~ plt.plot(np.arange(1,100,1),maxTPT_ana(np.arange(1,100,1),.9,.01,1024,540,0.13),"-r>")
#~ plt.plot(np.arange(1,100,1),maxTPT_ana(np.arange(1,100,1),.9,.01,1024,540,0.15),"-yo")
#~ plt.plot(np.arange(1,100,1),maxTPT_ana(np.arange(1,100,1),.9,.01,1024,540,0.17),"-b*")
#~ plt.show()
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

N=1024
R_p1=540
rhs=0.01
Tlist=[1,2,4,8,16,32,64,128]

figure=plt.plot()
#~ #plt.subplot(211)
p=p_2
PSTCD=[0.5099, 0.248, 0.06440000000000001, 0.0039000000000000146, 0.0,0.0, 0.0, 0.0]
PST=[0.5057, 0.24939999999999996, 0.061000000000000054, 0.0031999999999999806,0.0, 0.0, 0.0, 0.0]
#plt.plot(Tlist,mdcompletepol(Tlist),"b",label="COMPOL")
plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-ro",label="Ana,"+str(p))
plt.semilogy(Tlist,PST,":r^",label="$1-P_S^T$ Simulation")
plt.semilogy(Tlist,PSTCD,":r>",label="$1-P_S^T$ ,Simulation decoding with $p_2$")
#plt.plot(Tlist,[rhs]*len(Tlist),"k",label="$P_{MD}$ required.")

#~ #plt.subplot(212)
#~ p=0.11
#~ PSTCD=[0.7883, 0.45399999999999996, 0.11819999999999997, 0.016599999999999948, 0.0009000000000000119, 0.00029999999999996696, 9.999999999998899e-05, 0.0006000000000000449]
#~ PST=[0.7956, 0.45820000000000005, 0.1119, 0.018399999999999972, 0.00029999999999996696, 9.999999999998899e-05, 0.00039999999999995595, 9.999999999998899e-05]
#~ plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-go",label="Ana,"+str(p))
#~ plt.semilogy(Tlist,PST,":g^",label="$1-P_S^T$ Simulation")
#~ plt.plot(Tlist,PSTCD,":g>",label="$1-P_S^T$ ,Simulation decoding with $p_2$")

#~ #plt.subplot(221)
#~ p=0.13
#~ PST=[0.6597999999999999, 0.3275, 0.08450000000000002, 0.007399999999999962, 0.0, 0.0, 0.0, 0.0]
#~ plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-bo",label="Ana,"+str(p))
#~ plt.semilogy(Tlist,PST,":b^",label="$1-P_S^T$ Simulation")

#~ #plt.subplot(222)
#~ p=0.15
#~ PST=[0.5696, 0.28159999999999996, 0.06879999999999997, 0.005199999999999982, 0.0, 0.0, 0.0, 0.0]
#~ plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-mo",label="Ana,"+str(p))
#~ plt.semilogy(Tlist,PST,":m^",label="$1-P_S^T$ Simulation")

#plt.subplot(222)
#~ p=0.17
#~ PST=[0.5283, 0.2652, 0.0645, 0.0048000000000000265, 0.0, 0.0, 0.0, 0.0]
#~ plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-co",label="Ana,"+str(p))
#~ plt.semilogy(Tlist,PST,":c^",label="$1-P_S^T$ Simulation")

plt.title("Estimation of $P_{MD}$ for N=1024,\n $p_1=$"+str(p_1)+",$p=$"+str(p)+",$R_{P_1}=$"+str(R_p1))
plt.ylabel('$P_{MD}=P_{p}(L_{T}=K_{T})$')
plt.xlabel('T')
plt.grid(True)
plt.legend(loc="best")
plt.show()

