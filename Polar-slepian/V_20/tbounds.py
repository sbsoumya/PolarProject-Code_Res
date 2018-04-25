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
"""
N=1024
p1=0.08
p2=0.2
(I,Z1)=pcon.getreliability_orderZ(N,p1)
(I,Z2)=pcon.getreliability_orderZ(N,p2)
plt.plot(range(N),[10**Z for Z in Z1],"g")
plt.plot(range(N),[10**Z for Z in Z2],"r")
plt.plot(range(N),[10**z1-10**z2 for (z1,z2) in zip(Z1,Z2)],"k")
plt.show()
"""

	
def pmdguarantee(Tlist,N,NR_p1,p,a):
	pmd=np.array(mdindeZ(Tlist,N,NR_p1,p))
	pmdl=list(pmd)
	closest=ml.takeClosest(pmdl,a)
	#print Tlist
	#print pmd
	#print closest
	T= list(Tlist)[pmdl.index(closest)-1]
	return T

#print .5-np.sqrt(1-np.power(1,2))/2 
#print mdindeZ([1,2,4,8,16,32,64],1024,540,0.2)
#print mdindeZ([1,2,4,8,16,32,64],1024,360,0.3)
	
#==================================================ANAmaxTPT-T
# uses above indeZ estimate of pmd and finds the tpt vs T vector for a scheme with maxiter=2
def maxTPT_ana(Tlist,F1,F2,N,NR_p1,p):
	PMD=np.array(mdindeZ(Tlist,N,NR_p1,p))
	
	E_Iter=PMD + (1-PMD)*2
	#print E_Iter
	
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
def mdunionZ(Tlist,N,NR_p1,p_2):		
	(I,Z)=pcon.getreliability_orderZ(N,p_2)
	lhs=[]
	for T in Tlist:
	  Zinv=[.5-np.sqrt(1-np.power(z,2))/2 for z in np.power(10,Z[NR_p1-T:NR_p1])]
	  lhsT=1-sum(Zinv)
	  print lhsT
	  lhs.append(lhsT)

	return lhs
plt.plot([1,2,4,8,16],mdunionZ([1,2,4,8,16],1024,400,0.0192),"k")
plt.plot([1,2,4,8,16],mdindeZ([1,2,4,8,16],1024,400,0.0192),"b")
plt.show()
#===============================================1-PsT(subblock)

#for p=p2
#~ PSTCD=[0.5099, 0.248, 0.06440000000000001, 0.0039000000000000146, 0.0, 0.0, 0.0, 0.0]
#~ PST=[0.5057, 0.24939999999999996, 0.061000000000000054, 0.0031999999999999806, 0.0, 0.0, 0.0, 0.0]

#=================================================Plot PMD estimates
#results for p=p2
"""
complist=[0.08349999999999963, 0.19249999999999973]
p_1=complist[0]
p_2=complist[1]

N=1024
R_p1=540
rhs=0.01
Tlist=[1,2,4,8,16,32,64,128]

fig=plt.figure()
plt.subplot(321)
p=p_2
PSTCD=[0.5099, 0.248, 0.06440000000000001, 0.0039000000000000146, 0.0,0.0, 0.0, 0.0]
PST=[0.5057, 0.24939999999999996, 0.061000000000000054, 0.0031999999999999806,0.0, 0.0, 0.0, 0.0]
#plt.plot(Tlist,mdcompletepol(Tlist),"b",label="COMPOL")
plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-ro",label="Ana,"+str(p))
plt.semilogy(Tlist,PST,":r^",label="$1-P_S^T$ Simulation")
#plt.semilogy(Tlist,PSTCD,":r>",label="$1-P_S^T$ ,Simulation decoding with $p_2$")
#plt.plot(Tlist,[rhs]*len(Tlist),"k",label="$P_{MD}$ required.")
plt.title("$p=$"+str(p))
plt.grid(True)
plt.ylabel('$P_{MD}=P_{p}(L_{T}=K_{T})$')

plt.subplot(322)
p=p_2
PSTCD=[0.5099, 0.248, 0.06440000000000001, 0.0039000000000000146, 0.0,0.0, 0.0, 0.0]
PST=[0.5057, 0.24939999999999996, 0.061000000000000054, 0.0031999999999999806,0.0, 0.0, 0.0, 0.0]
#plt.plot(Tlist,mdcompletepol(Tlist),"b",label="COMPOL")
plt.plot(Tlist,mdindeZ(Tlist,N,R_p1,p),"-ro",label="Ana,"+str(p))
plt.plot(Tlist,PST,":r^",label="$1-P_S^T$ Simulation")
#plt.semilogy(Tlist,PSTCD,":r>",label="$1-P_S^T$ ,Simulation decoding with $p_2$")
#plt.plot(Tlist,[rhs]*len(Tlist),"k",label="$P_{MD}$ required.")
plt.title("$p=$"+str(p))
plt.grid(True)
plt.legend(loc="best")


plt.subplot(326)
p=0.11
PSTCD=[0.7883, 0.45399999999999996, 0.11819999999999997, 0.016599999999999948, 0.0009000000000000119, 0.00029999999999996696, 9.999999999998899e-05, 0.0006000000000000449]
PST=[0.7956, 0.45820000000000005, 0.1119, 0.018399999999999972, 0.00029999999999996696, 9.999999999998899e-05, 0.00039999999999995595, 9.999999999998899e-05]
plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-go",label="Ana,"+str(p))
plt.semilogy(Tlist,PST,":g^",label="$1-P_S^T$ Simulation")
plt.plot(Tlist,PSTCD,":g>",label="$1-P_S^T$ ,Simulation decoding with $p_2$")
plt.title("$p=$"+str(p))
plt.grid(True)
plt.xlabel('T')
plt.subplot(325)
p=0.13
PST=[0.6597999999999999, 0.3275, 0.08450000000000002, 0.007399999999999962, 0.0, 0.0, 0.0, 0.0]
plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-bo",label="Ana,"+str(p))
plt.semilogy(Tlist,PST,":b^",label="$1-P_S^T$ Simulation")
plt.title("$p=$"+str(p))
plt.grid(True)
plt.xlabel('T')
plt.ylabel('$P_{MD}=P_{p}(L_{T}=K_{T})$')
plt.subplot(324)
p=0.15
PST=[0.5696, 0.28159999999999996, 0.06879999999999997, 0.005199999999999982, 0.0, 0.0, 0.0, 0.0]
plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-mo",label="Ana,"+str(p))
plt.semilogy(Tlist,PST,":m^",label="$1-P_S^T$ Simulation")
plt.title("$p=$"+str(p))
plt.grid(True)

plt.subplot(323)
p=0.17
PST=[0.5283, 0.2652, 0.0645, 0.0048000000000000265, 0.0, 0.0, 0.0, 0.0]
plt.semilogy(Tlist,mdindeZ(Tlist,N,R_p1,p),"-co",label="Ana,"+str(p))
plt.semilogy(Tlist,PST,":c^",label="$1-P_S^T$ Simulation")
plt.title("$p=$"+str(p))
plt.grid(True)
plt.ylabel('$P_{MD}=P_{p}(L_{T}=K_{T})$')

fig.suptitle("Estimation of $P_{MD}$ for N=1024,\n $p_1=$"+str(p_1)+",$R_{P_1}=$"+str(R_p1))


plt.grid(True)

plt.show()

"""
#========================================================= throughput analysis
"""
plist=[0.11,0.13,0.15,0.17,0.19]
color=["b","g","r","m","c"]
FER1=[0.997475,1,1,1,1]
FR1=[0.999372,1,1,1,1]
FER2=[0.0207642,0.201347,0.679183,0.96743,0.99968]
FR2=[0.0101438,0.107136,0.43727,0.830596,0.982694]

Tlist=np.arange(1,128,1)

#===============================tpt analytical
fig=plt.figure()
maxtptl=[]
maxtl=[]
for i in range(len(plist)):
	tpt=maxTPT_ana(Tlist,FER1[i],FER2[i],1024,540,plist[i])
	#print tpt
	maxtpt=max(tpt)
	maxtptl.append(maxtpt)
	maxt=Tlist[list(tpt).index(maxtpt)]
	maxtl.append(maxt)
	plt.plot(maxt,maxtpt,"^"+color[i])
	plt.plot(Tlist,tpt,":"+color[i],label="TPT-ANA,p="+str(plist[i]))

plt.plot(maxtl,maxtptl,'-.k',label="max-TPT-ANA")

#=============================tpt actual

ftpt=[" "]*5
ftpt[0]="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt540in1024_c0p11_18-04-22_15-50-04.txt"
ftpt[1]="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt540in1024_c0p13_18-04-22_15-51-11.txt"
ftpt[2]="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt540in1024_c0p15_18-04-22_15-52-38.txt"
ftpt[3]="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt540in1024_c0p17_18-04-22_15-53-37.txt"
ftpt[4]="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt540in1024_c0p19_18-04-22_15-54-40.txt"
Tlist=[1,2,4,8,16,32,64,128]
tptsim=[]
maxtptlsim=[]
maxtlsim=[]
for i in range(len(plist)):
	tptsim=ml.getline(ftpt[i],[-2])[0]
	plt.plot(Tlist,tptsim,"-"+color[i],label="TPT-sim,p="+str(plist[i]))
	maxtptsim=max(tptsim)
	maxtptlsim.append(maxtptsim)
	maxtsim=Tlist[list(tptsim).index(maxtptsim)]
	maxtlsim.append(maxtsim)
	plt.plot(maxtsim,maxtptsim,"o"+color[i])






#plt.plot(maxtlsim,maxtptlsim,'y',label="max-TPT-sim")
plt.title("TPT vs T")
plt.ylabel('TPT')
plt.xlabel('T')
plt.grid(True)
plt.legend(loc="best")
plt.show()	
"""
#==============================================T vs P
"""
pmg=[]
for i in range(len(plist)):
	pmg.append(pmdguarantee(np.arange(40,1,-2),1024,540,plist[i],FER2[i]))
	
plt.plot(plist,pmg,'-b^',label="$P_{MD}\leq FER_p^{2-iter}$")
plt.plot(plist,maxtl,'-r^', label="T for max-TPT-ANA")
#plt.plot(plist,maxtlsim,'-r^', label="T for max-TPT-sim")
plt.title("$p$ vs T required, for $p_1<p<p_2$")
plt.ylabel('T')
plt.xlabel('$BSC(p)$')
plt.ylim(0,20)
plt.grid(True)
plt.legend(loc="best")
plt.show()	

"""


























