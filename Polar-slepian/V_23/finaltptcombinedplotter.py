from tbounds import *

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
#512 - 5 iter-----and 3 iter
#-----512
#~ (x,y,z)=(9,10,11)
#~ N=512
#~ R_p1=246
#~ fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_240in512_T11_18-05-08_22-58-34.txt"
#~ T=11
#~ lines=ml.getline(fileT11,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],3)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N)+",3-Iter")

#~ complist=[0.03,0.11,0.17,0.2,0.23]
#~ fileT11_5_iter="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T11_18-05-08_20-15-47.txt"
#~ N=512
#~ R_p1=246
#~ T=11
#~ lines=ml.getline(fileT11_5_iter,[x,y,z])
#~ point=len(lines[0])
#~ MeanIters=pl.getMeanIter(ml.getline(fileT11_5_iter,[13])[0],5)
#~ plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N)+",5-iter")
#~ fig.suptitle("HARQ schemes  ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) 
#~ +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$,p_4= $"+str(np.round(complist[3],decimals=3))+"$,p_5= $"+str(np.round(complist[4],decimals=3))+"$ \}$")

#~ plt.ylabel('Throughput=($NR_1-T$)*(1-FER)/N*E[Iterations]')
#~ plt.xlabel('BSC(p)')
#~ plt.grid(True)
#~ plt.legend(loc="best")

#~ plt.show()

#================================512 vs FR
#~ #-----512
N=512
R_p1=246
fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T11_18-05-06_23-19-05.txt"
T=11
lines=ml.getline(fileT11,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],':',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N)+",3-Iter")








