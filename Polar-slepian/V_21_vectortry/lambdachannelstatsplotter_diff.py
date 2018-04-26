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

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')


import seaborn as sns
sns.set(color_codes=True)

#-------------------------------------------polar_channel_FERvsR

#to be automated

#filename1="./simresults/llrsgndict-1024-0p04-17-11-23_17-28-36.txt"
filename="./simresults/llrsgndict-1024-0p04-18-02-15_14-58-19.txt"
LLRdict=lmb.load_LLRdict(filename)
N=1024
design_p=0.04
runsim=1000
channel_plist=[0.04,0.15]
skip=0
C=pl.CapacityBSC(N,design_p)
G=int(C)
F=N-G
color=["red","blue","green","yellow"]

llr_ch1=np.zeros(runsim)
sbit_ch1=np.zeros(runsim)
rbit_ch1=np.zeros(runsim)

llr_ch2=np.zeros(runsim)
sbit_ch2=np.zeros(runsim)
rbit_ch2=np.zeros(runsim)

mean={}
var={}

for ch in range(N):
		plt.figure()
	  
		for i in range(runsim):
		
			llr_ch1[i]=(LLRdict["0.04"][i][0][ch])
			sbit_ch1[i]=(LLRdict["0.04"][i][1][ch])
			rbit_ch1[i]=(LLRdict["0.04"][i][2][ch])
			
			llr_ch2[i]=(LLRdict["0.15"][i][0][ch])
			sbit_ch2[i]=(LLRdict["0.15"][i][1][ch])
			rbit_ch2[i]=(LLRdict["0.15"][i][2][ch])
	
		f_ch=[lmb.f_Irv(llr1,sb1)-lmb.f_Irv(llr2,sb2) for (llr1,sb1,llr2,sb2) in zip(llr_ch1,sbit_ch1,llr_ch2,sbit_ch2)]
		sns.distplot(f_ch,label="m="+str(np.mean(f_ch))+"\n v="+str(np.var(f_ch)))

	
		plt.title("diff of g for design_p=0.04, Rel_Order="+str(ch)+"/"+str(N)+" G="+str(G))
		plt.legend(loc="best")
		plt.savefig("./simresults/stats/diff/diff_stats_0p04"+"_"+str(ch)+".png", bbox_inches='tight')	
		plt.close()


