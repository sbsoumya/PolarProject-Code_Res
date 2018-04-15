#--------------------------------------------
# Name:       plotter.py
# Purpose:    Generic plotter
#
# Author:      soumya
#
# Created:     19/08/2017
#----------------------------------------

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

FR4="./simresults/polarchannel_FERvsp_FR103in1024_18-03-31_21-09-17.txt"
FR3="./simresults/polarchannel_FERvsp_FR148in1024_18-03-31_21-08-39.txt"
FR2="./simresults/polarchannel_FERvsp_FR238in1024_18-03-31_21-08-06.txt"
FR1="./simresults/polarchannel_FERvsp_FR508in1024_18-03-31_21-07-30.txt"
FR5="./simresults/polarchannel_FERvsp_FR76in1024_18-03-31_21-09-55.txt"
FR6="./simresults/polarchannel_FERvsp_FRTV508in1024_18-04-13_23-15-53.txt"
FR6="./simresults/polarchannel_FERvsp_FRTV508in1024_18-04-14_19-30-01.txt"
FR6="./simresults/polarchannel_FERvsp_FRTV508in1024_18-04-14_22-14-20.txt"
fig=plt.figure()
N=1024

#~ #---------------FR
(x,z)=(6,7)
lines=ml.getline(FR1,[x,z])
point=len(lines[0])
plt.semilogy(lines[0],[10**i for i in lines[1]],'-^g',label="ZCON") 
(x,z)=(6,7)
lines=ml.getline(FR6,[x,z])
point=len(lines[0])
plt.semilogy(lines[0],[10**i for i in lines[1]],'-^r',label="TVCON") 
#~ lines=ml.getline(FR2,[x,z])
#~ point=len(lines[0])
#~ plt.semilogy(lines[0],[10**i for i in lines[1]],':r') 
#~ lines=ml.getline(FR3,[x,z])
#~ point=len(lines[0])
#~ plt.semilogy(lines[0],[10**i for i in lines[1]],':b') 
#~ lines=ml.getline(FR4,[x,z])
#~ point=len(lines[0])
#~ plt.semilogy(lines[0],[10**i for i in lines[1]],':y') 
#~ lines=ml.getline(FR5,[x,z])
#~ point=len(lines[0])
#~ plt.semilogy(lines[0],[10**i for i in lines[1]],':k') 
msg_length=508
plt.title("FER vs p for N="+str(N)+", K="+str(msg_length)) 
plt.ylabel('FER')
plt.xlabel('BSC(p)')
plt.grid(True)
plt.legend(loc="best")


#plt.savefig("./simresults/TPT_iterretro_Detbits_1024.png", bbox_inches='tight')
plt.savefig("./simresults/FRplot"+str(msg_length)+"1024.png", bbox_inches='tight')

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




