from tbounds import *
from pprint import pprint
complist=[0.03,0.11,0.17]

fig=plt.figure()
#~ fig.suptitle("HARQ schemes  ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) 
#~ +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$ \}$")
#~ (x,y,z)=(9,10,11)
#~ maxiters=3

#~ #----256
#~ fileT12="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_114in256_T12_18-05-07_15-25-17.txt"
#~ N=256
#~ R_p1=114
#~ (x,y,z)=(9,10,11)
#~ T=12
#~ lines=ml.getline(fileT12,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT12,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-b^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))

#~ #----1024
#~ N=1024
#~ R_p1=510
#~ fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T11_18-05-07_15-32-05.txt"
#~ T=11
#~ lines=ml.getline(fileT11,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],3)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-g^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))

#~ #-----64
#~ N=64
#~ R_p1=18
#~ fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_18in64_T1_18-05-07_14-33-16.txt"
#~ T=1
#~ lines=ml.getline(fileT1,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-r^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))
#~ #----128
#~ N=128
#~ R_p1=42
#~ fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_42in128_T1_18-05-07_15-12-49.txt"
#~ T=1
#~ lines=ml.getline(fileT1,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))
#-----512
#~ N=512
#~ R_p1=246
#~ fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T11_18-05-06_23-19-05.txt"
#~ T=11
#~ lines=ml.getline(fileT11,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N)+",3-Iter")
#2048-------
#~ N=2048
#~ R_p1=1020
#~ fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_1020in2048_T11_18-05-06_22-59-43.txt"
#~ T=11
#~ lines=ml.getline(fileT11,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-y^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))


#~ plt.ylabel('Throughput=($NR_1-T$)*(1-FER)/N*E[Iterations]')
#~ plt.xlabel('BSC(p)')
#~ plt.grid(True)
#~ plt.legend(loc="best")

#~ plt.show()

#========================================================
#~ #512 - 5 iter-----and 3 iter
#~ #-----512
#~ (x,y,z)=(9,10,11)
#~ N=512
#~ R_p1=240
#~ fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_240in512_T11_3I_18-05-08_22-58-34.txt"
#~ T=11
#~ lines=ml.getline(fileT11,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],3)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N)+",3-Iter")

#~ complist=[0.03,0.11,0.17,0.2,0.23]
#~ fileT11_5_iter="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_240in512_T11_5I_18-05-08_20-15-47.txt"
#~ N=512
#~ R_p1=240
#~ T=11
#~ lines=ml.getline(fileT11_5_iter,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11_5_iter,[13])[0],5)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N)+",5-iter")
#~ fig.suptitle("HARQ schemes  ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) 
#~ +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$,p_4= $"+str(np.round(complist[3],decimals=3))+"$,p_5= $"+str(np.round(complist[4],decimals=3))+"$ \}$")

#~ #-------------------------UK
#~ T=0
#~ fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK240in512_T0_5I_18-05-09_16-38-53.txt"
#~ #fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-09_15-23-02.txt"
#~ lines=ml.getline(fileUK,[x,y,z])
#~ point=len(lines[0])
#~ maxiters=5
#~ MeanIters=pl.getMeanIter(ml.getline(fileUK,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='Decoding failure, $NR_1=$'+str(R_p1))


#~ channel_plist=lines[0]
#~ plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

#~ plt.ylabel('Throughput=($NR_1-T$)*(1-FER)/N*E[Iterations]')
#~ plt.xlabel('BSC(p)')
#~ plt.grid(True)
#~ plt.legend(loc="best")

#~ plt.show()

#==============================================================================KP
#================================512vs FR 
#-------------------calc
#------UK
#~ print "UK"+"="*20
#~ N=512
#~ R_p1=246
#~ (x,y,z)=(9,10,11)
#~ T=0
#~ fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-04_23-31-44.txt"
#~ lines=ml.getline(fileUK,[x,y,z])
#~ point=len(lines[0])
#~ channel_p=np.round(lines[0],decimals=2)
#~ maxiters=3
#~ Iterprob=ml.getline(fileUK,[13])[0]
#~ MeanIters=pl.getMeanIter(Iterprob,maxiters)
#~ Averagerate=[float(R_p1-T)/(MeanIters[i]) for i in range(point)]
#~ FER=lines[2]
#~ tpt=[float(R_p1-T)/(MeanIters[i]*N)*(1-10**FER[i]) for i in range(point)]
#~ print "R_p1 :"+str(R_p1)+"/"+str(N)
#~ print "T:"+str(T)
#~ print "channel_p: \n",channel_p
#~ print "Iters:"
#~ pprint(zip(channel_p,Iterprob))
#~ print "Mean Iters :\n", zip(channel_p,MeanIters)
#~ print "Average rate :\n",zip(channel_p,Averagerate)
#~ print "FER :\n",zip(channel_p,FER)
#~ print "TPT :\n",zip(channel_p,tpt)

#~ print "CB-scheme"+"="*20
#~ N=512
#~ R_p1=246
#~ fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T11_18-05-06_23-19-05.txt"
#~ T=11
#~ (x,y,z)=(9,10,11)
#~ maxiters=3
#~ lines=ml.getline(fileT11,[x,y,z])
#~ point=len(lines[0])
#~ channel_p=np.round(lines[0],decimals=2)
#~ Iterprob=ml.getline(fileT11,[13])[0]
#~ MeanIters=pl.getMeanIter(Iterprob,maxiters)
#~ Averagerate=[float(R_p1-T)/(MeanIters[i]) for i in range(point)]
#~ FER=lines[2]
#~ tpt=[float(R_p1-T)/(MeanIters[i]*N)*(1-10**FER[i]) for i in range(point)]
#~ print "R_p1 :"+str(R_p1)+"/"+str(N)
#~ print "T:"+str(T)
#~ print "channel_p: \n",channel_p
#~ print "Iters:"
#~ pprint(zip(channel_p,Iterprob))
#~ print "Mean Iters :\n", zip(channel_p,MeanIters)
#~ print "Average rate :\n",zip(channel_p,Averagerate)
#~ print "FER :\n",zip(channel_p,FER)
#~ print "TPT :\n",zip(channel_p,tpt)

#~ #------FR schemes
#~ print "FR"+str("=")*20
#~ channel_plist=list(np.linspace(0.01,0.2,20))
#~ design_plist=channel_plist
#~ Llist=list(np.linspace(np.log10(0.001),np.log10(0.5),8))
#~ Llist=np.log10([0.02,0.03,0.08,0.1,0.2,0.3,0.4])
#~ #print np.power(10,Llist)
#~ print('\t'.join(map(str,np.round(design_plist,decimals=2))))
#~ for Lexp in Llist:
	#~ print "Zmax="+str(np.round(10**Lexp,decimals=4))
	#~ Rlist=[len(pcon.getGChZCL(p,N,Lexp)[0]) for p in design_plist]
	#~ print('\t'.join(map(str,Rlist)))

#~ #-------------------------plot
#~ #-----512
N=512
R_p1=246
fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T11_18-05-06_23-19-05.txt"
T=11
(x,y,z)=(9,10,11)
maxiters=3
lines=ml.getline(fileT11,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))

#-------------------------UK
T=0
#fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-04_23-31-44.txt"
fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-09_15-23-02.txt"
lines=ml.getline(fileUK,[x,y,z])
point=len(lines[0])
maxiters=3
MeanIters=pl.getMeanIter(ml.getline(fileUK,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='Decoding failure, $NR_1=$'+str(R_p1))

channel_plist=list(np.linspace(0.01,0.2,20))
plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

#---------------------------------cp=dp
N=512
fileFR={}
fileFR["0e005"]="./simresults/polarchannel_FERvsp_FR0e005in512_18-05-08_23-47-09.txt"
fileFR["0e1"]="./simresults/polarchannel_FERvsp_FR0e1in512_18-05-08_23-53-00.txt"
fileFR["0e05"]="./simresults/polarchannel_FERvsp_FR0e05in512_18-05-08_23-46-32.txt"
fileFR["0e5"]="./simresults/polarchannel_FERvsp_FR0e5in512_18-05-09_00-43-29.txt"
fileFR["0e4"]="./simresults/polarchannel_FERvsp_FR0e4in512_18-05-09_14-25-53.txt"
fileFR["0e3"]="./simresults/polarchannel_FERvsp_FR0e3in512_18-05-09_14-25-30.txt"
fileFR["0e2"]="./simresults/polarchannel_FERvsp_FR0e2in512_18-05-09_14-25-08.txt"
fileFR["0e08"]="./simresults/polarchannel_FERvsp_FR0e08in512_18-05-09_14-24-36.txt"
fileFR["0e03"]="./simresults/polarchannel_FERvsp_FR0e03in512_18-05-09_14-23-04.txt"
fileFR["0e02"]="./simresults/polarchannel_FERvsp_FR0e02in512_18-05-09_14-17-33.txt"
fileFR["0e25"]="./simresults/polarchannel_FERvsp_FR0e25in512_18-05-09_15-21-47.txt"
#print fileFR

(x,y,z)=(-4,-3,-2)

zlist=fileFR.keys()
TPTZ={}
for Zmax in zlist:
	lines=ml.getline(fileFR[Zmax],[x,y,z])
	point=len(lines[0])
	plist=lines[0]
	#plt.plot(lines[0],[float(lines[1][i]*(1-10**lines[2][i]))/N for i in range(point)],label='$Z \leq $'+Zmax.replace("e","."))
	TPTZ[Zmax]=[float(lines[1][i]*(1-10**lines[2][i]))/N for i in range(point)]
	
TPTmax=[]		
for i in range(point):
	TPTmax.append(max([TPTZ[Zmax][i] for Zmax in zlist]))
	
plt.plot(plist,TPTmax,':k^',label='maxFR')


plt.title("Throughput vs p") 
plt.ylabel('Throughput')
plt.xlabel('BSC(p)')
plt.grid(True)
plt.legend(loc="best")

plt.show()







