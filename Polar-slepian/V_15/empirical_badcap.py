#---------------------------------------------------
# Name:       empiricalbadcap
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
skip=0
C=pl.CapacityBSC(N,design_p)
G=int(C)
G=400
F=N-G
P=F
#------------------------------------LT
#G=250
#absllr
Edict=lmb.E_channel_abs_llr(LLRdict,channel_plist,N,G,runsim)
#absllr Goodchannel
#Edict=lmb.E_good_channel_abs_llr(LLRdict,channel_plist,N,G,runsim)
#P=G
#f_Irv
#Edict=lmb.E_channel_altIrv_WU(LLRdict,channel_plist,N,G,runsim)


#f_Irv_abs
#Edict=lmb.E_channel_Irv_abs(LLRdict,channel_plist,N,G,runsim)
print P
print len(Edict["0.04"])

color=["red","blue","green","yellow"]
plt.figure(1)
index= range(runsim)
j=1

for channel_p in channel_plist:
	j+=1
	plt.scatter([channel_p]*P,Edict[str(channel_p)],color=color[j-2],label="p$_{channel}=$"+str(channel_p))
	

for i in range(P):
	#Edictline=[Edict[str(cp)][i] for cp in channel_plist]
	plt.plot(channel_plist,[Edict[str(cp)][i] for cp in channel_plist],'k')
	


#~ fnick="absllr-good"
#~ f="$|LLR|$"	

fnick="absllr-bad"
f="$|LLR|$"	

#~ fnick="f_Irv"
#~ f="$log 2/(1+e^{-llr*(1-2u)})$"

#~ fnick="f_Irv_rcv"
#~ f="$log 2/(1+e^{-llr*(1-2r)})$"

#~ fnick="f_Irv_abs"
#~ f="$log 2/(1+e^{-|llr|})$"

#~ fnick="f_Irv_altered"
#~ f="$-log 2/(1+e^{llr*(1-2u)})$"
	


#plt.plot(channel_plist,[LT]*len(channel_plist),'m')
plt.legend(loc="best")
plt.title("Empirical E["+f+"] ,p$_{guessed}$="+str(design_p))
plt.xlabel("p$_{channel}$")
plt.grid(True)
#plt.ylabel("\% of good channels with $|LLR| \geq \lambda$")
#plt.ylabel("E[] for good channel ")
plt.ylabel("E[] for bad channel ")
plt.savefig("./simresults/Ex_"+fnick+"_0p04"+"_"+".png", bbox_inches='tight')

plt.show();

#1+e^{llr*(1-2u)}
