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
N=1024
#to be automated
msg_length=500
#TPT files
Iterretrofile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_472in1024_T8_18-03-31_01-40-12.txt"
IterretroCRCfile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC472in1024_T8_18-03-31_01-40-06.txt"
#polarCSIR8="./simresults/polarchannel_FERvsp_derate472in1024_18-03-31_14-22-16.txt"
Iterretrofile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_18-03-31_01-41-22.txt"
IterretroCRCfile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC508in1024_T32_18-03-31_01-40-26.txt"
#polarCSIR32="./simresults/polarchannel_FERvsp_derate508in1024_18-03-31_14-17-58.txt"


#BLER files
iter4="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter4_18-04-01_22-17-23.txt"
iter3="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter3_18-04-01_22-19-33.txt"
iter5="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter5_18-04-01_22-14-53.txt"
iter1="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter1_18-03-31_19-42-58.txt"
iter2="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter2_18-03-31_19-42-34.txt"

FR4="./simresults/polarchannel_FERvsp_FR103in1024_18-03-31_21-09-17.txt"
FR3="./simresults/polarchannel_FERvsp_FR148in1024_18-03-31_21-08-39.txt"
FR2="./simresults/polarchannel_FERvsp_FR238in1024_18-03-31_21-08-06.txt"
FR1="./simresults/polarchannel_FERvsp_FR508in1024_18-03-31_21-07-30.txt"
FR5="./simresults/polarchannel_FERvsp_FR76in1024_18-03-31_21-09-55.txt"

Rp1_8=472
Rp1_32=508

fig=plt.figure()
fig.suptitle("HARQ schemes  \n N=1024,ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$, p_3= $"+str(np.round(complist[2],decimals=3)) +"$,p_4=$"+str(np.round(complist[3],decimals=3)) +"$,p_5=$"+str(np.round(complist[4],decimals=3)) +"$ \}$")
plt.title("Throughput for $R_{p_1} =500,R_{p_1}=300,R_{p_1}=100$") 

#TPT plot
#TPT 500===========================================================================================
(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
#-----Capacity
plt.plot(lines[0],[pl.CapacityBSC(1,p) for p in lines[0]],'k',label='Capacity')
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[13])[0],5)
plt.plot(lines[0],[float(Rp1_8)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-g^',label='CB 8bits, $NR_{p_1}=$'+str(Rp1_8))
lines=ml.getline(IterretroCRCfile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile8,[13])[0],5)
plt.plot(lines[0],[float(Rp1_8)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.g',label='CRC8,$NR_{p_1}=$'+str(Rp1_8))
(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-r^',label='CB 32bits,$NR_{p_1}=$'+str(Rp1_32))
lines=ml.getline(IterretroCRCfile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile32,[12])[0],5)
plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.r',label='CRC32,$NR_{p_1}=$'+str(Rp1_32))

#TPT 300=====================================================================================
#TPT files
Iterretrofile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_292in1024_T8_18-03-31_01-47-17.txt"
IterretroCRCfile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC292in1024_T8_18-03-31_01-46-05.txt"
polarCSIR8="../simresults/polarchannel_FERvsp_derate292in1024_18-03-31_20-51-24.txt"
Iterretrofile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_328in1024_T32_18-03-31_01-47-56.txt"
IterretroCRCfile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC328in1024_T32_18-03-31_01-46-39.txt"
polarCSIR32="./simresults/polarchannel_FERvsp_derate328in1024_18-03-31_20-51-13.txt"


Rp1_8=292
Rp1_32=328

(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[13])[0],5)
plt.plot(lines[0],[float(Rp1_8)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-k^',label='CB 8bits, $NR_{p_1}=$'+str(Rp1_8))
lines=ml.getline(IterretroCRCfile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile8,[13])[0],5)
plt.plot(lines[0],[float(Rp1_8)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.k',label='CRC8,$NR_{p_1}=$'+str(Rp1_8))
(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-b^',label='CB 32bits,$NR_{p_1}=$'+str(Rp1_32))
lines=ml.getline(IterretroCRCfile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile32,[12])[0],5)
plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.b',label='CRC32,$NR_{p_1}=$'+str(Rp1_32))

#TPT 100==========================================================================================
#TPT files
Iterretrofile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_112in1024_T8_18-03-31_01-52-34.txt"
IterretroCRCfile8="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC112in1024_T8_18-03-31_01-53-25.txt"
polarCSIR8="./simresults/polarchannel_FERvsp_derate112in1024_18-03-31_20-51-18.txt"
Iterretrofile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_100in1024_T32_18-03-31_11-19-16.txt"
IterretroCRCfile32="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC100in1024_T32_18-03-31_11-20-16.txt"
#polarCSIR32="./simresults/polarchannel_FERvsp_derate88in1024_18-03-31_20-51-30.txt"

Rp1_8=112
Rp1_32=88

(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[13])[0],5)
plt.plot(lines[0],[float(Rp1_8)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-y^',label='CB 8bits, $NR_{p_1}=$'+str(Rp1_8))
lines=ml.getline(IterretroCRCfile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile8,[13])[0],5)
plt.plot(lines[0],[float(Rp1_8)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.y',label='CRC8,$NR_{p_1}=$'+str(Rp1_8))
(x,y,z)=(9,10,11)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[13])[0],5)
plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-c^',label='CB 32bits,$NR_{p_1}=$'+str(Rp1_32))
lines=ml.getline(IterretroCRCfile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(IterretroCRCfile32,[13])[0],5)
plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.c',label='CRC32,$NR_{p_1}=$'+str(Rp1_32))

#~ (x,y,z)=(6,7,8)
#~ lines=ml.getline(polarCSIR8,[x,y,z])
#~ point=len(lines[0])
#~ plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'g',label='PC opt for "p",$NR_{p_1}=$'+str(Rp1_8) )
#~ lines=ml.getline(polarCSIR32,[x,y,z])
#~ point=len(lines[0])
#~ plt.plot(lines[0],[float(Rp1_32)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'r',label='PC opt for "p",$NR_{p_1}=$'+str(Rp1_32) )

plt.ylabel('Throughput=R*(1-FER)/E[Iterations]')
plt.xlabel('BSC(p)')
plt.grid(True)
plt.legend(loc="best")

plt.savefig("./simresults/TPT_iterretro_Detbits_1024.png", bbox_inches='tight')
#plt.savefig("./simresults/TPT_FER_iterretro_Detbits"+str(msg_length)+"1024.png", bbox_inches='tight')
pp.savefiginteractive(fig,"./simresults/TPT_iterretro_Detbits_1024.fig")
#pp.savefiginteractive(fig,"./simresults/TPT_FER_iterretro_Detbits"+str(msg_length)+"1024.fig")


plt.show()
#=================================================files

#~ #Polar Derate delta and retro
#~ ./simresults/polarchannel_FERvsp_deratedelta496in1024_18-03-31_14-14-51.txt
#~ ./simresults/polarchannel_FERvsp_derate508in1024_18-03-31_14-17-58.txt
#~ ./simresults/polarchannel_FERvsp_derate472in1024_18-03-31_14-22-16.txt
#~ ./simresults/polarchannel_FERvsp_deratedelta96in1024_18-03-31_20-51-03.txt
#~ ./simresults/polarchannel_FERvsp_derate328in1024_18-03-31_20-51-13.txt
#~ ./simresults/polarchannel_FERvsp_deratedelta296in1024_18-03-31_20-50-58.txt
#~ ./simresults/polarchannel_FERvsp_derate112in1024_18-03-31_20-51-18.txt
#~ ./simresults/polarchannel_FERvsp_derate292in1024_18-03-31_20-51-24.txt
#~ ./simresults/polarchannel_FERvsp_derate88in1024_18-03-31_20-51-30.txt


#~ #det Iter retro
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_472in1024_T8_18-03-31_01-40-12.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_112in1024_T8_18-03-31_01-52-34.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_292in1024_T8_18-03-31_01-47-17.txt

#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_100in1024_T32_18-03-31_11-19-16.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_18-03-31_01-41-22.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_328in1024_T32_18-03-31_01-47-56.txt

#~ #det Iter retro CRC
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC112in1024_T8_18-03-31_01-53-25.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC292in1024_T8_18-03-31_01-46-05.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC472in1024_T8_18-03-31_01-40-06.txt

#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC100in1024_T32_18-03-31_11-20-16.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC508in1024_T32_18-03-31_01-40-26.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_CRC328in1024_T32_18-03-31_01-46-39.txt
#~ #FR
#~ ./simresults/polarchannel_FERvsp_FR76in1024_18-03-31_21-09-55.txt
#~ ./simresults/polarchannel_FERvsp_FR232in1024_18-03-31_21-13-18.txt
#~ ./simresults/polarchannel_FERvsp_FR298in1024_18-03-31_21-12-40.txt
#~ ./simresults/polarchannel_FERvsp_FR364in1024_18-03-31_21-11-58.txt
#~ ./simresults/polarchannel_FERvsp_FR430in1024_18-03-31_21-11-22.txt
#~ ./simresults/polarchannel_FERvsp_FR496in1024_18-03-31_21-10-46.txt
#~ ./simresults/polarchannel_FERvsp_FR103in1024_18-03-31_21-09-17.txt
#~ ./simresults/polarchannel_FERvsp_FR148in1024_18-03-31_21-08-39.txt
#~ ./simresults/polarchannel_FERvsp_FR238in1024_18-03-31_21-08-06.txt
#~ ./simresults/polarchannel_FERvsp_FR508in1024_18-03-31_21-07-30.txt

#~ #doiter iterretro
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter4_18-04-01_22-17-23.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter3_18-04-01_22-19-33.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter5_18-04-01_22-14-53.txt

#~ #doiter
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter1_18-03-31_19-42-58.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_508in1024_T32_doiter2_18-03-31_19-42-34.txt


#~ #doiterdelta
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_delta_496in1024_T32_doiter1_18-03-31_19-44-25.txt
#~ ./simresults/polarchannel_FERvsR_rateless_Det_Iter_delta_496in1024_T32_doiter2_18-03-31_20-30-16.txt




