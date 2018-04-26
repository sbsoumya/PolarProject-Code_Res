#--------------------------------------------
# Name.       plotter.py
# Purpose.    Generic plotter
#
# Author.      soumya
#
# Created.     19/08/2017
#----------------------------------------

import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import matlib as ml
import picklemyplot as pp

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
complist=[0.044499999999999595, 0.1584999999999997, 0.21649999999999975, 0.2524999999999998, 0.2774999999999998]
N=1024
#-------------------------------------------polar_channel_FERvsR


#TPT files
Iterretrofile8="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_500in1024_T8_18-04-08_01-44-56.txt"
Iterretrofile32="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_500in1024_T32_18-04-08_01-45-58.txt"

E_p1=500

fig=plt.figure()
fig.suptitle("Universal Slepian Wolf Compression with Polar Codes  \n N=1024,ED for $\{p_1=$"+str(np.round(complist[0],decimals=3)) +"$,p_2=$"+str(np.round(complist[1],decimals=3)) +"$, p_3= $"+str(np.round(complist[2],decimals=3)) +"$,p_4=$"+str(np.round(complist[3],decimals=3)) +"$,p_5=$"+str(np.round(complist[4],decimals=3)) +"$ \}$")
plt.title("$NE_{p_1} = (N-NR_{p_1}+T)$= error\_free\_communication for $Y=X \oplus Ber(p_1) $") 

#TPT plot
#TPT 500===========================================================================================
(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
#-----Capacity
plt.plot(lines[0],[pl.h(p) for p in lines[0]],'k',label='$H(X/Y)$')
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[12])[0],5)
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================
plt.plot(lines[0],EFCOM,'-g^',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
#plt.plot(lines[0],EFTPT,':go',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================
plt.plot(lines[0],EFCOM,'-.g^',label='CB 32bits,$NE_{p_1}=$'+str(E_p1))
#plt.plot(lines[0],EFTPT,':g>',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
#TPT 700=====================================================================================
#TPT files
Iterretrofile8="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_700in1024_T8_18-04-08_01-47-53.txt"
Iterretrofile32="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_700in1024_T32_18-04-08_01-46-39.txt"
E_p1=700

(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[12])[0],5)
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================
plt.plot(lines[0],EFCOM,'-r^',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
#plt.plot(lines[0],EFTPT,':ro',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================
plt.plot(lines[0],EFCOM,'-.r^',label='CB 32bits,$NE_{p_1}=$'+str(E_p1))

#TPT 300=====================================================================================
#TPT files
Iterretrofile8="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_300in1024_T8_18-04-08_18-51-36.txt"
Iterretrofile32="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_300in1024_T32_18-04-08_18-51-06.txt"
E_p1=300
E_p1=300

(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[12])[0],5)
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================
plt.plot(lines[0],EFCOM,'-b^',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
#plt.plot(lines[0],EFTPT,':bo',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
plt.plot(lines[0],EFCOM,'-.b^',label='CB 32bits,$NE_{p_1}=$'+str(E_p1))

#TPT 900=====================================================================================
#TPT files
Iterretrofile8="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_900in1024_T8_18-04-08_01-48-32.txt"
Iterretrofile32="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_900in1024_T32_18-04-08_01-49-20.txt"
E_p1=900

(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile8,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile8,[12])[0],5)
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================

#plt.plot(lines[0],EFTPT,':yo',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
plt.plot(lines[0],EFCOM,'-y^',label='CB 8bits, $NE_{p_1}=$'+str(E_p1))
(x,y,z)=(8,9,10)
lines=ml.getline(Iterretrofile32,[x,y,z])
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(Iterretrofile32,[12])[0],5)
EFTPT=[(1-(1-float(lines[1][i])*MeanIters[i])*(1-10**lines[2][i])) for i in range(point)]
#==============
E_G=[(1-float(E_p1)/N)/MeanIters[i] for i in range(point)]
TPT= [E_G[i]*(1-10**lines[2][i]) for i in range(point)]
EFCOM=[1-TPT[i] for i in range(point)]
#===================================
plt.plot(lines[0],EFCOM,'-.y^',label='CB 32bits,$NE_{p_1}=$'+str(E_p1))
#--------------------------------------------
#E[G_final]=(1-E_{p_1})/E[Iterations]
#TPT = G_final*(1-FER)
#1-TPT = error free comm
#--------------------------------------------
plt.ylabel('Error free communication=$1-(1-E_{p_1})*(1-FER)/E[Iterations]$')
plt.xlabel('BSC(p)')
plt.grid(True)
plt.legend(loc="best")

plt.savefig("./simresults/TPT_iterfile_Detbits_1024.png", bbox_inches='tight')
#plt.savefig("./simresults/TPT_FER_iterretro_Detbits"+str(msg_length)+"1024.png", bbox_inches='tight')
pp.savefiginteractive(fig,"./simresults/TPT_iterfile_Detbits_1024.fig")
#pp.savefiginteractive(fig,"./simresults/TPT_FER_iterretro_Detbits"+str(msg_length)+"1024.fig")

#################################################
# Go back to sleep man! Ghost in the machine....
#################################################
# I didnt EVEN Notice this when was this written?
##################################################

plt.show()
#=================================================files
#file sim at serv 
#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_500in1024_T8_18-04-08_01-44-56.txt
#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_500in1024_T32_18-04-08_01-45-58.txt

#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_700in1024_T8_18-04-08_01-47-53.txt
#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_700in1024_T32_18-04-08_01-46-39.txt

#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_900in1024_T8_18-04-08_01-48-32.txt
#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_900in1024_T32_18-04-08_01-49-20.txt


#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_300in1024_T8_18-04-08_18-51-36.txt
#~ ./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_300in1024_T32_18-04-08_18-51-06.txt
