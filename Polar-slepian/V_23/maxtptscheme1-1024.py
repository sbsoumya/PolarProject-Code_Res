from tbounds import *


#=================================================choice of R
#~ N=1024
#~ p1=0.03
#~ p2=0.11
#~ p3=0.17
#~ (I,Z1)=pcon.getreliability_orderZ(N,p1)
#~ (I,Z2)=pcon.getreliability_orderZ(N,p2)
#~ (I,Z3)=pcon.getreliability_orderZ(N,p3)
#~ plt.plot(range(N),[10**Z for Z in Z1],"g",label="$p_1=0.03,R_1=510/1024$")
#~ plt.plot(range(N),[10**Z for Z in Z2],"r",label="$p_2=0.11,R_2=255/1024$")
#~ plt.plot(range(N),[10**Z for Z in Z3],"b",label="$p_3=0.17,R_3=170/1024$")
#~ #plt.plot(range(N),[10**z1-10**z2 for (z1,z2) in zip(Z1,Z2)],"k")
#~ print pl.CapacityBSC(1024,p1)/3

#~ plt.title("Choice of $R$ based on $Z(W) \leq 5*10^{-2}$,N =1024 \nand satisfying $R_2=R_1/2,R_3=R_1/3$ ") 
#~ plt.legend(loc="best")
#~ plt.grid(True)
#~ print pl.CapacityBSC(1024,p2)
#~ print pl.CapacityBSC(1024,p3)
#~ print pl.Inversecap1024(pl.CapacityBSC(1024,p1)/3)
#~ plt.show()

#=================================================Plot PMD estimates
#~ # PF is mismatch, pm is match

#~ complist=[0.03,0.11,0.17]
#~ p_1=complist[0]
#~ p_2=complist[1]
#~ p_3=complist[2]
#~ N=1024
#~ NR_p1=510
#~ NR_p2=510/2
#~ NR_p3=510/3

#~ TlistANA=[1,2,4,8,16,32,64,128]


#~ fig=plt.figure()
#~ fig.suptitle("Estimation of $P_{MD},P_{F}$ for N=1024,$NR_1=$"+str(NR_p1)+"\n p_1=$"+str(p_1)+"$p_2=$"+str(p_2)+"$p_3=$"+str(p_3))

#~ plt.subplot(221)
#~ #pf1
#~ PF1=pfunionZ(TlistANA,N,NR_p1,p_1) 
#~ pf1file="./simresults/polarchannel_FERvsp_FRSB0p03_510in1024_18-04-26_21-57-42.txt"
#~ (x,y,z)=(8,9,10)
#~ lines=ml.getline(pf1file,[x,y,z])
#~ Tlist=lines[0]
#~ PF1sim=[10**e for e in lines[1]]
#~ plt.semilogy(TlistANA,PF1,"-r^",label="Ana")
#~ plt.semilogy(Tlist,PF1sim,":b^",label="Sim")
#~ plt.grid(True)
#~ plt.legend(loc="best")
#~ plt.ylabel('$P_{F,1}$')
#~ plt.xlabel('$T$')

#~ plt.subplot(222)
#~ #pm1
#~ PMD1=mdindeZ(TlistANA,N,NR_p1,p_2)
#~ PMD11=mdmaxZ(TlistANA,N,NR_p1,p_2)
#~ pmd1file="./simresults/polarchannel_FERvsp_FRSB0p11_510in1024_18-04-26_21-56-52.txt"
#~ (x,y,z)=(8,9,10)
#~ lines=ml.getline(pmd1file,[x,y,z])
#~ Tlist=lines[0]
#~ PMD1sim=lines[2]
#~ plt.semilogy(TlistANA,PMD1,"-r^",label="Ana")
#~ plt.semilogy(TlistANA,PMD11,"-g^",label="Ana-max")
#~ plt.semilogy(Tlist,PMD1sim,":b^",label="Sim")
#~ plt.legend(loc="best")
#~ plt.ylabel('$P_{MD,1}$')
#~ plt.xlabel('$T$')
#~ plt.grid(True)

#~ plt.subplot(223)
#~ #Pf2
#~ PF2=pfunionZ(TlistANA,N,NR_p2,p_2)
#~ pf2file="./simresults/polarchannel_FERvsp_FRSB0p11_255in1024_18-04-26_22-02-37.txt"
#~ (x,y,z)=(8,9,10)
#~ lines=ml.getline(pf2file,[x,y,z])
#~ Tlist=lines[0]
#~ PF2sim=[10**e for e in lines[1]]
#~ plt.semilogy(TlistANA,PF2,"-r^",label="Ana")
#~ plt.semilogy(Tlist,PF2sim,":b^",label="Sim")
#~ plt.legend(loc="best")
#~ plt.ylabel('$P_{F,2}$')
#~ plt.xlabel('$T$')
#~ plt.grid(True)

#~ plt.subplot(224)
#~ #pm2
#~ PMD2=mdindeZ(TlistANA,N,NR_p2,p_3)
#~ PMD21=mdmaxZ(TlistANA,N,NR_p2,p_3)
#~ pmd2file="./simresults/polarchannel_FERvsp_FRSB0p17_255in1024_18-04-26_21-59-03.txt"
#~ (x,y,z)=(8,9,10)
#~ lines=ml.getline(pmd2file,[x,y,z])
#~ Tlist=lines[0]
#~ PMD2sim=lines[2]
#~ plt.semilogy(TlistANA,PMD2,"-r^",label="Ana")
#~ plt.semilogy(TlistANA,PMD21,"-g^",label="Ana-max")
#~ plt.semilogy(Tlist,PMD2sim,":b^",label="Sim")
#~ plt.legend(loc="best")
#~ plt.ylabel('$P_{MD,2}$')
#~ plt.xlabel('$T$')
#~ plt.grid(True)
#~ plt.show()
#========================================================= throughput analysis


complist=[0.03,0.11,0.17]
p_1=complist[0]
p_2=complist[1]
p_3=complist[2]
N=1024
NR_p1=510
NR_p2=510/2
NR_p3=510/3

FER3file="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T0_doiter3_18-04-26_22-04-23.txt"
FER2file="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T0_doiter2_18-04-26_22-05-14.txt"
FER1file="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T0_doiter1_18-04-26_22-06-46.txt"

TPTfilep1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt510in1024_c0p03_18-04-27_14-50-18.txt"
TPTfilep2="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt510in1024_c0p11_18-04-27_14-48-37.txt"
TPTfilep3="./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt510in1024_c0p17_18-04-27_14-47-21.txt"

#number of p and tpt is same, dont confuse
(x,z)=(9,11)
FER1iter=np.array([10**i for i in  ml.getline(FER1file,[x,z])[1]])
FER2iter=np.array([10**i for i in  ml.getline(FER2file,[x,z])[1]])
FER3iter=np.array([10**i for i in  ml.getline(FER3file,[x,z])[1]])



print FER1iter,FER2iter,FER3iter

TlistANA=np.arange(1,NR_p2-NR_p3,2)
PMD1=np.array(mdindeZ(TlistANA,N,NR_p1,p_2))
PMD2=np.array(mdindeZ(TlistANA,N,NR_p2,p_3))
PF1=np.array(pfunionZ(TlistANA,N,NR_p1,p_1))
PF2=np.array(pfunionZ(TlistANA,N,NR_p2,p_2))

FER1est=[estimateFER(TlistANA,N,NR_p1,p_1,1),estimateFER(TlistANA,N,NR_p1,p_2,1),estimateFER(TlistANA,N,NR_p1,p_3,1)]
FER2est=[estimateFER(TlistANA,N,NR_p1,p_1,2),estimateFER(TlistANA,N,NR_p1,p_2,2),estimateFER(TlistANA,N,NR_p1,p_3,2)]
FER3est=[estimateFER(TlistANA,N,NR_p1,p_1,3),estimateFER(TlistANA,N,NR_p1,p_2,3),estimateFER(TlistANA,N,NR_p1,p_3,3)]
#===============================tpt 
fig=plt.figure()
plt.subplot(311)
plt.title("Throughput vs T")
#for p1
E_Iterp1=(1-PF1)+2*PF1
FERp1=FER1iter[0]*(1-PF1)+FER2iter[0]*(PF1)
TPTANAp1=(NR_p1-np.array(TlistANA))*(1-FERp1)/(N*E_Iterp1)
plt.plot(TlistANA,TPTANAp1,"-r^",label="TPT-ANA,p="+str(p_1))
plt.plot(TlistANA[list(TPTANAp1).index(max(TPTANAp1))],max(TPTANAp1),"ko",label="max(TPT-ANA)")
FERp1=np.multiply(FER1est[0],(1-PF1))+np.multiply(FER2est[0],(PF1))
TPTANAp1=(NR_p1-np.array(TlistANA))*(1-FERp1)/(N*E_Iterp1)
plt.plot(TlistANA,TPTANAp1,"-c^",label="TPT-FER,p="+str(p_1))
plt.plot(TlistANA[list(TPTANAp1).index(max(TPTANAp1))],max(TPTANAp1),"yo",label="max(TPT-FER)")


(x,z)=(9,-2)
lines=ml.getline(TPTfilep1,[x,z])
plt.plot(lines[0],lines[1],"-b^",label="TPT-sim,p="+str(p_1))
plt.plot(lines[0][lines[1].index(max(lines[1]))],max(lines[1]),"go",label="max(TPT-sim)")
plt.legend(loc="lower right")
plt.ylabel('$TPT$')
plt.grid(True)


plt.subplot(312)
#for p=p2
E_Iterp2=PMD1+2*np.multiply(1-PMD1,1-PF2)+3*np.multiply(1-PMD1,PF2)
FERp2=FER1iter[1]*PMD1+FER2iter[1]*np.multiply(1-PMD1,1-PF2)+FER3iter[1]*np.multiply(1-PMD1,PF2)
TPTANAp2=(NR_p1-np.array(TlistANA))*(1-FERp2)/(N*E_Iterp2)
plt.plot(TlistANA,TPTANAp2,"-r^",label="TPT-ANA,p="+str(p_2))
plt.plot(TlistANA[list(TPTANAp2).index(max(TPTANAp2))],max(TPTANAp2),"-ko",label="max(TPT-ANA)")
FERp2=np.multiply(FER1est[1],PMD1)+np.multiply(FER2est[1],1-PMD1,1-PF2)+np.multiply(FER3est[1],1-PMD1,PF2)
TPTANAp2=(NR_p1-np.array(TlistANA))*(1-FERp2)/(N*E_Iterp2)
plt.plot(TlistANA,TPTANAp2,"-c^",label="TPT-FER,p="+str(p_2))
plt.plot(TlistANA[list(TPTANAp2).index(max(TPTANAp2))],max(TPTANAp2),"-yo",label="max(TPT-FER)")

(x,z)=(9,-2)
lines=ml.getline(TPTfilep2,[x,z])
plt.plot(lines[0],lines[1],"-b^",label="TPT-sim,p="+str(p_2))
plt.plot(lines[0][lines[1].index(max(lines[1]))],max(lines[1]),"go",label="max(TPT-sim)")
plt.legend(loc="lower right")
plt.ylabel('$TPT$')
plt.grid(True)


plt.subplot(313)
#for p=p3
E_Iterp3=2*(1-PMD2)+3*PMD2
FERp3=FER2iter[2]*(1-PMD2)+FER3iter[2]*PMD2
TPTANAp3=(NR_p1-np.array(TlistANA))*(1-FERp2)/(N*E_Iterp3)
plt.plot(TlistANA,TPTANAp3,"-r^",label="TPT-ANA,p="+str(p_3))
plt.plot(TlistANA[list(TPTANAp3).index(max(TPTANAp3))],max(TPTANAp3),"ko",label="max(TPT-ANA)")
FERp3=np.multiply(FER2est[2],(1-PMD2))+np.multiply(FER3est[2],PMD2)
TPTANAp3=(NR_p1-np.array(TlistANA))*(1-FERp2)/(N*E_Iterp3)
plt.plot(TlistANA,TPTANAp3,"-c^",label="TPT-FER,p="+str(p_3))
plt.plot(TlistANA[list(TPTANAp3).index(max(TPTANAp3))],max(TPTANAp3),"yo",label="max(TPT-FER)")


(x,z)=(9,-2)
lines=ml.getline(TPTfilep3,[x,z])
plt.plot(lines[0],lines[1],"-b^",label="TPT-sim,p="+str(p_3))
plt.plot(lines[0][lines[1].index(max(lines[1]))],max(lines[1]),"go",label="max(TPT-sim)")
plt.legend(loc="lower right")
plt.ylabel('$TPT$')
plt.xlabel('$T$')
plt.grid(True)

plt.show()

#====================================final scheme performance

#~ fileT32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T32_18-04-28_15-31-33.txt"
#~ fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T1_18-04-28_15-29-44.txt"
#~ fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T11_18-05-07_15-32-05.txt"
#~ fileT8="/home/smart/Desktop/Project/code/Polar-slepian/V_22/simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T8_18-04-28_15-30-03.txt"
#~ complist=[0.03,0.11,0.17]
#~ N=1024
#~ fig=plt.figure()
#~ fig.suptitle("HARQ schemes  \n N=1024,ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$ \}$")
#~ R_p1=510
#~ maxiters=3
#~ (x,y,z)=(9,10,11)
#~ T=1
#~ lines=ml.getline(fileT1,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-r^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1))


#~ T=11
#~ lines=ml.getline(fileT11,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],3)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-b^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1))

#~ T=8
#~ lines=ml.getline(fileT8,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT8,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-b^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1))



#~ T=32
#~ lines=ml.getline(fileT32,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT32,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-g^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1))

#~ T=1
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep1,[x,z])
#~ plt.plot(complist[0],lines[1][lines[0].index(1)],"ro")
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep2,[x,z])
#~ plt.plot(complist[1],lines[1][lines[0].index(1)],"ro")
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep3,[x,z])
#~ plt.plot(complist[2],lines[1][lines[0].index(1)],"ro")

#~ T=8
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep1,[x,z])
#~ plt.plot(complist[0],lines[1][lines[0].index(8)],"bo")
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep2,[x,z])
#~ plt.plot(complist[1],lines[1][lines[0].index(8)],"bo")
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep3,[x,z])
#~ plt.plot(complist[2],lines[1][lines[0].index(8)],"bo")

#~ T=32
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep1,[x,z])
#~ plt.plot(complist[0],lines[1][lines[0].index(32)],"go")
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep2,[x,z])
#~ plt.plot(complist[1],lines[1][lines[0].index(32)],"go")
#~ (x,z)=(9,-2)
#~ lines=ml.getline(TPTfilep3,[x,z])
#~ plt.plot(complist[2],lines[1][lines[0].index(32)],"go")

#~ #==================UK
#~ T=0
#~ fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK510in1024_T0_18-05-03_15-42-41.txt"
#~ lines=ml.getline(fileUK,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileUK,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='Decoding failure, $NR_1=$'+str(R_p1))

#~ channel_plist=list(np.linspace(0.01,0.2,20))
#~ plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")



#~ plt.ylabel('Throughput=($NR_1-T$)*(1-FER)/N*E[Iterations]')
#~ plt.xlabel('BSC(p)')
#~ plt.grid(True)
#~ plt.legend(loc="best")

#~ plt.show()
