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

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#import seaborn as sns
#sns.set(color_codes=True)

#-------------------------------------------polar_channel_FERvsR

#to be automated

filename1="./simresults/llrdict-1024-0p04-17-11-03_16-56-11.txt"




table = []
with open(filename1,'r') as f:
    for line in f:
        table.append(json.loads(line))

#23 if prob_checker file, 20 if llrdict file
LLRdict=table[0]



channel_plist=[0.04,0.15,0.2,0.25]
N=1024
#channel_plist=[0.1]
color=["red","blue","green","yellow"]


runsim=1000

plt.figure(1)
#index=range(len(RI))
j=0
for channel_p in channel_plist:
	j+=1
	marker='o'
	alpha=1
	if j>1:
		marker='x'
		alpha=0.2
		
	#plt.figure(j)
	for i in range(1):
		plt.scatter(range(N),LLRdict[str(channel_p)][i],marker=marker,color=color[j-1],label='p$_{channel}$='+str(channel_p))
	for i in range(1,runsim):
		plt.scatter(range(N),LLRdict[str(channel_p)][i],marker=marker,alpha=alpha,color=color[j-1])
			
		#plt.xticks(index,RI,rotation="vertical")
		
	#plt.hold(True)
	plt.title("$|LLR|$ for p$_{guess}$=0.04,\emph{Compound Channel=$\{$0.04,0.15,0.2,0.25$\}$ }")

plt.xlabel('Polarized bit Channel as per Reliability Ordering.')
plt.ylabel('$|LLR|$')

#densitydata=[LLRdict[str('0.04')][i][0] for i in range(runsim)]
#sns.distplot(densitydata)
plt.legend(loc="best")
plt.grid(True)
plt.show();

#------------------------------------------highly specific to file


