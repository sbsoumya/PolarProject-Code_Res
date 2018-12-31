#---------------------------------------------------
# Name:       lambdaplotter.py
# Purpose:    plotter to be used with lambda simulations
#
#
# Author:      soumya
#
# Created:    24/10/2017
#---------------------------------------------


import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import pandas as pd
from scipy import stats, integrate
import polarconstruct as pcon
import lambdathreshold as lmb
import math as ma
import matlib as ml

plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.rc('savefig',dpi=300) 
plt.rc('figure', figsize=[8,5]) 


#import seaborn as sns
#sns.set(color_codes=True)

#-------------------------------------------polar_channel_FERvsR

#to be automated
#./simresults/llrsgndict-512-0p03-18-05-10_12-50-13.txt
#./simresults/llrsgndict-512-0p11-18-05-10_12-50-57.txt
fig=plt.figure()
plt.subplots_adjust(top=0.95,bottom=0.15)
ax=plt.subplot(111)

filename="./simresults/llrsgndict-512-0p03-18-05-10_12-50-13.txt"
LLRdict=lmb.load_LLRdict(filename)
N=512
design_p=0.03
runsim=1000
channel_plist=[0.03,0.11,0.17]
skip=0
C=pl.CapacityBSC(N,design_p)
G=int(C)
F=N-G
color=["red","blue","green"]
plt.figure(1)
j=0

for channel_p in channel_plist:
	j+=1
	marker='o'
	alpha=1
	if j>1:
		marker='x'
		alpha=0.2
	
	for i in range(runsim):
		# all channels
		LLRchannels=LLRdict[str(channel_p)][i][0]
		SentBitchannels=LLRdict[str(channel_p)][i][1]
		ReceivedBitchannels=LLRdict[str(channel_p)][i][2]
		
		#abs(llr)
		RV=[abs(llr) for llr in LLRchannels]
		
		#f_Irv
		#RV=[lmb.f_Irv(llr,int(sentbit)) for llr,sentbit in zip(LLRchannels,SentBitchannels)]
				
		#f_Irv_rcv
		#RV=[lmb.f_Irv(llr,int(rcvbit)) for llr,rcvbit in zip(LLRchannels,ReceivedBitchannels)]
		
		#f_Irv_abs
		#RV=[lmb.f_Irv_abs(abs(llr)) for llr,rcvbit in zip(LLRchannels,ReceivedBitchannels)]
		#RV=[lmb.f_Irv_abs(abs(llr))-lmb.f_Irv(llr,int(rcvbit)) for llr,rcvbit in zip(LLRchannels,ReceivedBitchannels)]
		#RV2=[int(rcvbit) for rcvbit in ReceivedBitchannels]
		#RV=[1-ml.logdomain_sum(0,-llr*(1-2*int(rcvbit)))/ma.log(2) for llr,rcvbit in zip(LLRchannels,ReceivedBitchannels)]
		#RV3=[1-ml.logdomain_sum(0,-abs(llr))/ma.log(2)+2 for llr in LLRchannels]
		
		#RV=[llr for llr,rcvbit in zip(LLRchannels,ReceivedBitchannels)]
		#RV3=[abs(llr) for llr in LLRchannels]
		
		#f_Irv_altered
		#RV=[-lmb.f_Irv(-llr,int(sentbit)) for llr,sentbit in zip(LLRchannels,SentBitchannels)]
		
		if i==0:
			plt.scatter(range(N)[::skip+1],RV[::skip+1],marker=marker,color=color[j-1],label='$p=$'+str(channel_p))
		else:
			plt.scatter(range(N)[::skip+1],RV[::skip+1],marker=marker,color=color[j-1])
			
		#plt.scatter(range(N)[::skip+1],RV2[::skip+1],marker=marker,alpha=alpha,color='k')
		#plt.scatter(range(N)[::skip+1],RV3[::skip+1],marker=marker,alpha=alpha,color='g')
		
		

fnick="absllr"
f="$|\Lambda_1(j)|$"	

#~ fnick="f_Irv"
#~ f="$log 2/(1+e^{-llr*(1-2u)})$"

#~ fnick="f_Irv_rcv"
#~ f="$log 2/(1+e^{-llr*(1-2r)})$"

#fnick="f_Irv_abs"
#f="$log 2/(1+e^{-|llr|})$"

#~ fnick="f_Irv_altered"
#~ f="$-log 2/(1+e^{llr*(1-2u)})$"

#plt.title(f+" for p$_{guess}$=0.11,\emph{Compound Channel=$\{$0.03,0.11,0.17$\}$ }")
plt.xlabel('Bit channel $j$')
plt.ylabel(f)
plt.legend(loc="upper right")
plt.grid(True)

plt.savefig("./simresults/lambda_"+fnick+"_0p11"+"_"+".png", bbox_inches='tight')

plt.show();





