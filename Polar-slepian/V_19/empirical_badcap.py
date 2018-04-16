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
#filename="./simresults/llrsgndict-1024-0p04-18-02-15_14-58-19.txt"


#--------------------------------LLR new files
#filename="./simresults/llrsgndict-1024-0p0835-18-04-14_20-04-58.txt"
#filename="./simresults/llrsgndict-1024-0p1925-18-04-14_20-06-05.txt"
#filename="./simresults/llrsgndict-1024-0p2455-18-04-14_20-07-15.txt"
filename="./simresults/llrsgndict-1024-0p2785-18-04-14_20-08-14.txt"



LLRdict=lmb.load_LLRdict(filename)
N=1024
runsim=1000
channel_plist=LLRdict.keys()
channel_plist.sort()
design_p=min(channel_plist)
print design_p
print channel_plist
G=int(pl.CapacityBSC(N,float(design_p)))
skip=0
F=N-G
#------------------------------------LT
#G=250
#absllr
#Edict=lmb.E_channel_abs_llr(LLRdict,channel_plist,N,G,runsim)

		
#f_Irv
#Edict=lmb.E_channel_Irv_WU(LLRdict,channel_plist,N,G,runsim)
Edict=lmb.E_channel_altIrv_WU(LLRdict,channel_plist,N,G,runsim)
#Edict=lmb.E_channel_formIrv_WU(LLRdict,channel_plist,N,G,runsim)
#f_Irv_abs
#Edict=lmb.E_channel_Irv_abs(LLRdict,channel_plist,N,G,runsim)

colors=["red","blue","green","yellow","black"]
color=colors[:len(channel_plist)]
plt.figure(1)
index= range(runsim)
j=1

for channel_p in channel_plist:
	j+=1
	plt.scatter([channel_p]*F,Edict[str(channel_p)],color=color[j-2],label="p$_{channel}=$"+str(channel_p))
	#~ print "CalcCap"
	#~ print sum(Edict[str(channel_p)])/1.28
	#~ print "ActCap"
	#~ print pl.CapacityBSC(N,float(channel_p))

for i in range(F):
	#Edictline=[Edict[str(cp)][i] for cp in channel_plist]
	plt.plot(channel_plist,[Edict[str(cp)][i] for cp in channel_plist],'k')
	


#fnick="absllr"
#f="$|LLR|$"	

#~ fnick="f_Irv"
#~ f="$log 2/(1+e^{-llr*(1-2u)})$"

#~ fnick="f_Irv_rcv"
#~ f="$log 2/(1+e^{-llr*(1-2r)})$"

#~ fnick="f_Irv_abs"
#~ f="$log 2/(1+e^{-|llr|})$"

fnick="f_Irv_altered"
f="$-log 2/(1+e^{llr*(1-2u)})$"
	


#plt.plot(channel_plist,[LT]*len(channel_plist),'m')
plt.legend(loc="best")
plt.title("Empirical E["+f+"] ,p$_{guessed}$="+str(design_p))
plt.xlabel("p$_{channel}$")
plt.grid(True)
#plt.ylabel("\% of good channels with $|LLR| \geq \lambda$")
plt.ylabel("E[] for Frozen channel ")
plt.savefig("./simresults/Ex_"+fnick+"-"+str(design_p).replace(".","p")+".png", bbox_inches='tight')

plt.show();

#1+e^{llr*(1-2u)}
