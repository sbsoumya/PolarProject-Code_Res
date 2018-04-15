#---------------------------------------------------
# Name:       thetafinder.py
# Purpose:    plotter to be used to find theta
#
#
# Author:      soumya
#
# Created:    27/10/2017
#---------------------------------------------


import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import pandas as pd
from scipy import stats, integrate
import polarconstruct as pcon
import lambdathreshold as lmb

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


#-------------------------------------------polar_channel_FERvsR

#to be automated
#--------------------------ABSLLR files
#filename="./simresults/llrdict-1024-0p2-17-11-03_16-55-25.txt"
#filename="./simresults/llrdict-1024-0p04-17-11-03_16-56-11.txt"
#-----------------------------LLR files

#filename="./simresults/llrsgndict-1024-0p2-18-02-15_14-58-44.txt"
#filename="./simresults/llrsgndict-1024-0p15-18-02-15_14-58-32.txt"
filename="./simresults/llrsgndict-1024-0p04-18-02-15_14-58-19.txt"


LLRdict=lmb.load_LLRdict(filename)
N=1024
design_p=0.04
runsim=1000
channel_plist=[0.04,0.15,0.2,0.25]
C=pl.CapacityBSC(N,design_p)
G=int(C)

#------------------------------------LT
#G=250
LT=float(np.log2(N)/N)
LT=5
PT=12
print LT
#absllr
#Fdict=lmb.perc_channel_func_WD(LLRdict,channel_plist,N,LT,G,runsim,f_absllr=lmb.f_abs,use_bad=False,use_func_for_LT=True)
#LT=lmb.f_abs(LT)
		
#f_Irv
#Fdict=lmb.perc_channel_Irv_WU(LLRdict,channel_plist,N,LT,G,runsim,use_bad=True,use_func_for_LT=True)
#LT=lmb.f_Irv_abs(LT)


#f_Irv_abs
Fdict=lmb.perc_channel_func_WD(LLRdict,channel_plist,N,LT,G,runsim,f_absllr=lmb.f_Irv_abs,use_bad=True,use_func_for_LT=True)
LT=lmb.f_Irv_abs(LT)

Ppercdict=lmb.PrOffracaboveFT(Fdict,channel_plist,PT,runsim)
print Ppercdict

color=["red","blue","green","yellow"]
plt.figure(1)
index= range(runsim)
j=1
for channel_p in channel_plist:
	j+=1
	plt.scatter(index,Fdict[str(channel_p)],color=color[j-2],label="p$_{channel}=$"+str(channel_p))




#~ fnick="absllr-good"
#~ f="$|LLR|"	

#~ fnick="f_Irv"
#~ f="$log 2/(1+e^{-llr*(1-2u)})"

#~ fnick="f_Irv_rcv"
#~ f="$log 2/(1+e^{-llr*(1-2r)})"

fnick="f_Irv_abs"
f="$log 2/(1+e^{-|llr|})"

#~ fnick="f_Irv_altered"
#~ f="$-log 2/(1+e^{llr*(1-2u)})"
	
plt.legend(loc="best")
plt.title("Thresholds for PHY-ED \n $\lambda$="+str(LT)+",$\Theta$="+str(PT)+",p$_{guessed}$="+str(design_p))
plt.xlabel("Simulation number"+"\n"+"P(atleast $\Theta$ \% of badchannels $\geq\lambda$)="+str(Ppercdict)+"\n"+filename)
plt.grid(True)
#plt.ylabel("\% of good channels with $|LLR| \geq \lambda$")
plt.ylabel("\% of bad channels with "+f+" \geq \lambda$")

#plt.figtext(0.005, 0.03, "P("+str(PT)+"\% of goodchannels $\geq\lambda$)="+str(Ppercdict))#+"\n"+filename)
plt.savefig("./simresults/theta_"+fnick+"_0p04"+"_"+".png", bbox_inches='tight')

plt.show();
