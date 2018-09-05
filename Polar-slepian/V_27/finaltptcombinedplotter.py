from tbounds import *
from pprint import pprint
complist=[0.03,0.11,0.17]

plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.rc('savefig',dpi=300) 
plt.rc('figure', figsize=[8,3]) 

"""
fig=plt.figure()
plt.subplots_adjust(top=0.95,bottom=0.15,right=0.8,left=0.09)
ax=plt.subplot(111)
#fig.suptitle("HARQ schemes  ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) 
#+"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$ \}$")
(x,y,z)=(9,10,11)
#plt.title("Effect of $n$ on $\eta$ for RT-Polar scheme, $\delta$="+str(0.05)) 
maxiters=3

#-----64
N=64
R_p1=18
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_18in64_T1_18-05-07_14-33-16.txt"
T=1
lines=ml.getline(fileT1,[x,y,z])
point=len(lines[0])
channel_c=np.array([pl.CapacityBSC(1,p) for p in lines[0]])
MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.go',label='$n=$'+str(N)+', t='+str(T))
#plt.plot(lines[0],channel_c-np.array([float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]),'-.go',label='t='+str(T)+'bits, $n=$'+str(N))
#----128
N=128
R_p1=42
fileT2="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_42in128_T2_18-05-17_12-15-41.txt"
T=2
lines=ml.getline(fileT2,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT2,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-yv',label='$n=$'+str(N)+', t='+str(T))
#plt.plot(lines[0],channel_c-np.array([float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]),'-yx',label='t='+str(T)+'bits, $n=$'+str(N))
#----256
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_114in256_T9_18-05-17_12-17-08.txt"
N=256
R_p1=114
(x,y,z)=(9,10,11)
T=9
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.rx',label='$n=$'+str(N)+', t='+str(T))
#plt.plot(lines[0],channel_c-np.array([float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]),'-.rv',label='t='+str(T)+'bits, $n=$'+str(N))
#~ #-----512
N=512
R_p1=246
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T9_18-05-17_12-19-25.txt"
T=9
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='$n=$'+str(N)+', t='+str(T))
#plt.plot(lines[0],channel_c-np.array([float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]),'-m^',label='t='+str(T)+'bits, $n=$'+str(N))
#----1024
N=1024
R_p1=510
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T9_18-05-17_12-21-48.txt"
T=9
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],3)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.b+',label='$n=$'+str(N)+', t='+str(T))
#plt.plot(lines[0],channel_c-np.array([float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]),'-.b>',label='t='+str(T)+'bits, $n=$'+str(N))
#~ #2048-------
N=2048
R_p1=1020
fileT8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_1020in2048_T8_18-05-17_12-28-05.txt"
T=8
lines=ml.getline(fileT8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT8,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c>',label='$n=$'+str(N)+', t='+str(T))
#plt.plot(lines[0],channel_c-np.array([float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]),'-c+',label='t='+str(T)+'bits, $n=$'+str(N))


channel_plist=list(np.linspace(0.01,0.2,20))

plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

plt.ylabel('$\eta(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.025,0.175])
plt.grid(True)
plt.legend(loc="upper right", ncol=2, columnspacing=0.1,handletextpad =0.1,borderaxespad=0.1,numpoints=1)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

plt.show()

"""

#~ #========================================================
#512 - 5 iter-----and 3 iter

fig=plt.figure()
plt.subplots_adjust(hspace=0.3,top=0.95,bottom=0.15)
ax=plt.subplot(111)
ax.locator_params(axis='y', nbins=5)
#-----512
(x,y,z)=(9,10,11)
N=512
#fig.suptitle("Performance of RT-Polar scheme,$\delta$="+str(0.05)+', $n=$'+str(N), fontsize="20") 
R_p1=240

fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_240in512_T9_3I_18-05-19_13-37-50.txt"

#fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_240in512_T11_3I_18-05-08_22-58-34.txt"
T=9
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],3)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='$r=3$')

complist=[0.03,0.11,0.17,0.2,0.23]

fileT9_5_iter="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_240in512_T9_5I_18-05-16_21-35-04.txt"
#fileT11_5_iter="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_240in512_T11_5I_18-05-08_20-15-47.txt"
N=512
R_p1=240
T=9
lines=ml.getline(fileT9_5_iter,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9_5_iter,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-bx',label='$r=5$')
#~ fig.suptitle("HARQ schemes  ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) 
#~ +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$,p_4= $"+str(np.round(complist[3],decimals=3))+"$,p_5= $"+str(np.round(complist[4],decimals=3))+"$ \}$")

#-------------------------UK
#~ T=0
#~ fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK240in512_T0_5I_18-05-09_16-38-53.txt"
#~ #fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-09_15-23-02.txt"
#~ lines=ml.getline(fileUK,[x,y,z])
#~ point=len(lines[0])
#~ maxiters=5
#~ MeanIters=pl.getMeanIter(ml.getline(fileUK,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='Decoding failure, $NR_1=$'+str(R_p1))


channel_plist=lines[0]
#plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

plt.ylabel('$\eta(p)$')
#plt.xlabel('BSC(p)')
plt.grid(True)
plt.xlim([0.025,0.235])
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel('flipover probability $p$')
plt.show()


#~ #==============================CRC
#~ #-----512
"""
ax=plt.subplot(111)
ax.locator_params(axis='y', nbins=5)
N=512
R_p1=246
fileT8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T8_18-05-09_20-15-49.txt"
fileCRCT8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC246in512_T8_18-05-09_20-16-27.txt"

T=8
(x,y,z)=(9,10,11)
maxiters=3
lines=ml.getline(fileT8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT8,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-mo',label='RB-Polar, t='+str(T)+'bits')
lines=ml.getline(fileCRCT8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileCRCT8,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-b^',label='CRC,'+str(T)+'bits')

fileT32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC1020in2048_T32_18-05-09_20-20-08.txt"
fileCRCT32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_1020in2048_T32_18-05-09_20-17-57.txt"

N=2048
R_p1=1020
T=32
(x,y,z)=(9,10,11)
maxiters=3
lines=ml.getline(fileT32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT32,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-rx',label='RB-Polar, t='+str(T)+'bits')
lines=ml.getline(fileCRCT32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileCRCT32,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-g>',label='CRC,'+str(T)+'bits')



#plt.title("Throughput vs p") 
plt.ylabel('$\eta(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.025,0.175])
plt.grid(True)
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

plt.show()
"""

#==============================================================================Benchmark
#~ #================================512vs FR 
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


"""
#-------------------------plot
fig=plt.figure()
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
N=512
#plt.title("Performance of RT-Polar scheme,$\delta$="+str(0.05)+', $n=$'+str(N)) 
#-----512
N=512
R_p1=246
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T9_18-05-17_12-19-25.txt"
T=9
(x,y,z)=(9,10,11)
maxiters=3
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='RB-Polar, t='+str(T))
"""
#------BAC
"""
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T9_18-06-12_16-00-41.txt"
T=9
(x,y,z)=(9,11,12)
maxiters=3
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[14])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-y^',label='RT-Polar-BAC $p_1=p_0/2$ , t='+str(T))
"""
"""
#-------------------------UK
T=0
(x,y,z)=(9,10,11)
#fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-04_23-31-44.txt"
fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-09_15-23-02.txt"
lines=ml.getline(fileUK,[x,y,z])
point=len(lines[0])
maxiters=3
MeanIters=pl.getMeanIter(ml.getline(fileUK,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.ro',label='Ideal Detection')

#-------------------------LTPT
T=0
(x,y,z)=(10,11,12)
#fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-04_23-31-44.txt"
fileLTPT="./simresults/polarchannel_FERvsR_rateless_Det_LTPT_246in512_18-05-10_15-26-03.txt"
lines=ml.getline(fileLTPT,[x,y,z])
point=len(lines[0])
maxiters=3
MeanIters=pl.getMeanIter(ml.getline(fileLTPT,[14])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-gx',label='LT-Polar')
"""
#--------------L4

"""
#./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T9_18-06-08_14-20-13.txt
N=512
R_p1=246
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T9_18-06-08_14-20-13.txt"
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T9_L118-06-08_14-59-59.txt"
T=9
(x,y,z)=(9,10,11)
maxiters=3
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='RB-Polar, L=4, t='+str(T))
"""
"""




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
	
plt.plot(plist,TPTmax,'-.b>',label='Standard Polar')

channel_plist=list(np.linspace(0.01,0.2,20))
plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

plt.ylabel('$\eta(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.025,0.175])
#plt.ylim([0.15,0.9])
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)


plt.show()
"""

#===============================M for 1024

"""
fig=plt.figure()
N=1024
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.85,left=0.09)
#fig.suptitle("HARQ schemes  \n N=1024,ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$ \}$")
#plt.title("Effect of $\delta$ on $\eta$ for RT-Polar scheme, $n$="+str(N)) 

#~ #-----------------378

fileT10="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_378in1024_T10_18-05-17_12-29-55.txt"
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_378in1024_T1_18-04-29_16-36-30.txt"
R_p1=378
maxiters=3
complist=[0.03,0.11,0.17]
N=1024
(x,y,z)=(9,10,11)
#~ T=1
#~ lines=ml.getline(fileT1,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':g^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

T=10
lines=ml.getline(fileT10,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT10,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-gx',label='$\delta$='+str(0.005)+', t='+str(T))
#-------------------510

fileT17="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T17_18-05-17_12-22-16.txt"
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T1_18-04-28_15-29-44.txt"
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T9_18-05-17_12-21-48.txt"
R_p1=510
maxiters=3
complist=[0.03,0.11,0.17]
N=1024
(x,y,z)=(9,10,11)

#~ T=1
#~ lines=ml.getline(fileT1,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':m^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))
T=9
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],3)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-cv',label='$\delta$='+str(0.05)+', t='+str(T))

#~ T=17
#~ lines=ml.getline(fileT17,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT17,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.mv',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

#~ #------------------678
fileT10="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_678in1024_T10_18-05-17_12-31-27.txt"
fileT16="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_678in1024_T16_18-05-17_12-31-58.txt"
fileT31="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_678in1024_T31_18-05-17_12-32-32.txt"


complist=[0.03,0.11,0.17]
N=1024
R_p1=678
maxiters=3
(x,y,z)=(9,10,11)
#~ T=10
#~ lines=ml.getline(fileT10,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT10,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':c^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))


T=16
lines=ml.getline(fileT16,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT16,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-bo',label='$\delta$='+str(0.5)+', t='+str(T))


#~ T=31
#~ lines=ml.getline(fileT31,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT31,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.cv',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

channel_plist=list(np.linspace(0.01,0.2,20))
plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

plt.ylabel('$\eta(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.025,0.175])
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

plt.show()
"""
#===============================M for 512
"""
fig=plt.figure()
N=512
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.85,left=0.09)
#fig.suptitle("HARQ schemes  \n N=1024,ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$ \}$")
#plt.title("Effect of $\delta$ on $\eta$ for RT-Polar scheme, $n$="+str(N)) 

#~ #-----------------192

fileT6="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_192in512_T6_18-05-17_14-15-54.txt"
fileT10="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_192in512_T10_18-05-17_14-14-17.txt"
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_192in512_T1_18-05-17_14-14-02.txt"
R_p1=192
maxiters=3
complist=[0.03,0.11,0.17]
N=512
(x,y,z)=(9,10,11)
T=1
lines=ml.getline(fileT1,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':g^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

T=6
lines=ml.getline(fileT6,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT6,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':g^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

T=10
lines=ml.getline(fileT10,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT10,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-gx',label='$\delta$='+str(0.005)+', t='+str(T))
#-------------------246

fileT8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T8_18-05-09_20-15-49.txt"
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T1_18-05-06_23-18-45.txt"
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T9_18-05-17_12-19-25.txt"
R_p1=246
maxiters=3
complist=[0.03,0.11,0.17]
N=512
(x,y,z)=(9,10,11)

T=1
lines=ml.getline(fileT1,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':m^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))
T=9
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],3)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-cv',label='$\delta$='+str(0.05)+', t='+str(T))

T=8
lines=ml.getline(fileT8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT8,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.mv',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

#~ #------------------372
#fileT10="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_678in1024_T10_18-05-17_12-31-27.txt"
fileT16="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_372in512_T16_18-05-17_12-57-59.txt"
#fileT31="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_678in1024_T31_18-05-17_12-32-32.txt"


complist=[0.03,0.11,0.17]
N=512
R_p1=372
maxiters=3
(x,y,z)=(9,10,11)
#~ T=10
#~ lines=ml.getline(fileT10,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT10,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':c^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))


T=16
lines=ml.getline(fileT16,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT16,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-bo',label='$\delta$='+str(0.5)+', t='+str(T))


#~ T=31
#~ lines=ml.getline(fileT31,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT31,[13])[0],maxiters)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.cv',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

channel_plist=list(np.linspace(0.01,0.2,20))
plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

plt.ylabel('$\eta(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.02,0.18])
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

plt.show()
"""
#===============================M for 256
"""

fig=plt.figure()
N=256
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.85,left=0.09)
#fig.suptitle("HARQ schemes  \n N=1024,ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$ \}$")
#plt.title("Effect of $\delta$ on $\eta$ for RT-Polar scheme, $n$="+str(N)) 

#~ #-----------------78

fileT5="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_78in256_T5_18-05-17_14-27-27.txt"
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_78in256_T1_18-05-17_14-26-54.txt"
R_p1=78
maxiters=3
complist=[0.03,0.11,0.17]
N=1024
(x,y,z)=(9,10,11)
T=1
lines=ml.getline(fileT1,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':g^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

T=5
lines=ml.getline(fileT5,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT5,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-gx',label='$\delta$='+str(0.005)+', t='+str(T))
#-------------------114

fileT5="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_114in256_T5_18-05-17_12-18-33.txt"
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_114in256_T1_18-05-07_15-24-52.txt"
fileT9="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_114in256_T9_18-05-17_12-17-08.txt"
R_p1=114
maxiters=3
complist=[0.03,0.11,0.17]
N=256
(x,y,z)=(9,10,11)

T=1
lines=ml.getline(fileT1,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':m^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))
T=9
lines=ml.getline(fileT9,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[13])[0],3)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-cv',label='$\delta$='+str(0.05)+', t='+str(T))

T=5
lines=ml.getline(fileT5,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT5,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.mv',label='CB '+str(T)+', $NR_1=$'+str(R_p1))

#~ #-----------------186
fileT7="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_186in256_T7_18-05-17_14-42-53.txt"
fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_186in256_T11_18-05-17_14-43-08.txt"


complist=[0.03,0.11,0.17]
N=256
R_p1=186
maxiters=3
(x,y,z)=(9,10,11)
T=7
lines=ml.getline(fileT7,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT7,[13])[0],maxiters)
#plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':c^',label='CB '+str(T)+', $NR_1=$'+str(R_p1))


T=11
lines=ml.getline(fileT11,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-bo',label='$\delta$='+str(0.5)+', t='+str(T))


channel_plist=list(np.linspace(0.01,0.2,20))
plt.plot(channel_plist,[pl.CapacityBSC(1,p) for p in channel_plist],"k",label="Capacity")

plt.ylabel('$\eta(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.02,0.18])
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

plt.show()
"""
