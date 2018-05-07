from tbounds import *

complist=[0.03,0.11,0.17]

fig=plt.figure()
fig.suptitle("HARQ schemes  ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) 
+"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$,p_3= $"+str(np.round(complist[2],decimals=3))+"$ \}$")

maxiters=3

#----256
fileT12="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_114in256_T12_18-05-07_15-25-17.txt"
N=256
R_p1=114
(x,y,z)=(9,10,11)
T=12
lines=ml.getline(fileT12,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT12,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-b^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))

#----1024
N=1024
R_p1=510
fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_510in1024_T11_18-05-07_15-32-05.txt"
T=11
lines=ml.getline(fileT11,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],3)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-g^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))

#-----64
N=64
R_p1=18
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_18in64_T1_18-05-07_14-33-16.txt"
T=1
lines=ml.getline(fileT1,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-r^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))
#----128
N=128
R_p1=42
fileT1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_42in128_T1_18-05-07_15-12-49.txt"
T=1
lines=ml.getline(fileT1,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT1,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))
#-----512
N=512
R_p1=246
fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_246in512_T11_18-05-06_23-19-05.txt"
T=11
lines=ml.getline(fileT11,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-m^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))
#2048-------
N=2048
R_p1=1020
fileT11="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_1020in2048_T11_18-05-06_22-59-43.txt"
T=11
lines=ml.getline(fileT11,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT11,[13])[0],maxiters)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-y^',label='CB '+str(T)+'bits, $NR_1=$'+str(R_p1)+"/"+str(N))



plt.ylabel('Throughput=($NR_1-T$)*(1-FER)/N*E[Iterations]')
plt.xlabel('BSC(p)')
plt.grid(True)
plt.legend(loc="best")

plt.show()
