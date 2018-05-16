#--------------------------------------------
# Name:       plotter.py
# Purpose:    Generic plotter
#
# Author:      soumya
#
# Created:     19/08/2017
#----------------------------------------

#EQUAL M+T VERSION
import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import matlib as ml
import picklemyplot as pp

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
complist=[0.08349999999999963, 0.19249999999999973, 0.24549999999999977, 0.2784999999999998, 0.3009999999999998]

#-------------------------------------------polar_channel_FERvsR

#TPT 500=====================================================================================
#TPT files
N=1024

#TPT files
Iterretrofile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_532in1024_T8_18-04-21_01-18-21.txt"
IterretroCRCfile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC532in1024_T8_18-04-21_01-19-06.txt"
Iterretrofile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_18-03-31_01-41-22.txt"
IterretroCRCfile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC508in1024_T32_18-03-31_01-40-26.txt"

R_p1=540

fig=plt.figure()
fig.suptitle("HARQ schemes  \n N=1024,ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$, p_3= $"+str(np.round(complist[2],decimals=3)) +"$,p_4=$"+str(np.round(complist[3],decimals=3)) +"$,p_5=$"+str(np.round(complist[4],decimals=3)) +"$ \}$")
plt.title("Throughput for $NR_{p_1}=540,NR_{p_1}=360,NR_{p_1}=120$ where $NR_{p_1}$ is the number of channels considered good for $p=p_1$") 

(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
#-----Capacity
plt.plot(lines[0],[pl.CapacityBSC(1,p) for p in lines[0]],'k',label='Capacity')

T=8

MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-g^',label='CB '+str(T)+'bits, $NR_{p_1}=$'+str(R_p1))
lines=ml.getline(IterretroCRCfile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile8,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.g',label='CRC '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))
(x,y,z)=(8,9,10)

T=32

lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-r^',label='CB '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))
lines=ml.getline(IterretroCRCfile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile32,[12])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.r',label='CRC '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))

#TPT 300=====================================================================================
#TPT files
Iterretrofile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_352in1024_T8_18-04-21_01-17-34.txt"
IterretroCRCfile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC352in1024_T8_18-04-21_01-10-58.txt"
Iterretrofile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_328in1024_T32_18-03-31_01-47-56.txt"
IterretroCRCfile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC328in1024_T32_18-03-31_01-46-39.txt"
R_p1=360

T=8

(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-k^',label='CB '+str(T)+'bits, $NR_{p_1}=$'+str(R_p1))
lines=ml.getline(IterretroCRCfile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile8,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.k',label='CRC '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))

T=32

(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-b^',label='CB '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))
lines=ml.getline(IterretroCRCfile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile32,[12])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.b',label='CRC '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))

#TPT 100==========================================================================================
#TPT files
Iterretrofile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_112in1024_T8_18-03-31_01-52-34.txt"
IterretroCRCfile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC112in1024_T8_18-03-31_01-53-25.txt"
Iterretrofile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_100in1024_T32_18-03-31_11-19-16.txt"
IterretroCRCfile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC100in1024_T32_18-03-31_11-20-16.txt"

R_p1=120

T=8

(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-y^',label='CB '+str(T)+'bits, $NR_{p_1}=$'+str(R_p1))
lines=ml.getline(IterretroCRCfile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile8,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.y',label='CRC '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))

T=32

(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='CB '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))
lines=ml.getline(IterretroCRCfile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile32,[13])[0],5)
plt.plot(lines[0],[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.c',label='CRC '+str(T)+'bits,$NR_{p_1}=$'+str(R_p1))


plt.ylabel('Throughput=($R_{p_1}-T$)*(1-FER)/E[Iterations]')
plt.xlabel('BSC(p)')
plt.grid(True)
plt.legend(loc="best")

plt.savefig("./simresults/TPT_iterretro_Detbits_1024.png", bbox_inches='tight')
#plt.savefig("./simresults/TPT_FER_iterretro_Detbits"+str(msg_length)+"1024.png", bbox_inches='tight')
pp.savefiginteractive(fig,"./simresults/TPT_iterretro_Detbits_1024.fig")
#pp.savefiginteractive(fig,"./simresults/TPT_FER_iterretro_Detbits"+str(msg_length)+"1024.fig")


plt.show()
#=================================================files
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_352in1024_T8_18-04-21_01-17-34.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_532in1024_T8_18-04-21_01-18-21.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC352in1024_T8_18-04-21_01-10-58.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC532in1024_T8_18-04-21_01-19-06.txt

