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

import seaborn as sns
sns.set(color_codes=True)

#-------------------------------------------polar_channel_FERvsR

#to be automated

filename1="./simresults/llrsgndict-1024-0p04-17-11-23_17-28-36.txt"




table = []
with open(filename1,'r') as f:
    for line in f:
        table.append(json.loads(line))

print len(table)

#23 if prob_checker file, 20 if llrdict file
LLRdict=table[0]



channel_plist=[0.04,0.15]
N=1024
#channel_plist=[0.1]
color=["green","yellow"]


runsim=1000

plt.figure(1)
#index=range(len(RI))
j=0
for channel_p in channel_plist:
	j+=1
	#plt.figure(j)
	for i in range(runsim):
		plt.scatter(range(N),LLRdict[str(channel_p)][i],color=color[j-1])
			
		#plt.xticks(index,RI,rotation="vertical")
		
	#plt.hold(True)
	plt.title("LLR for 0.15 , compound_channel=[0.04,0.15,0.2,0.25]")



#densitydata=[LLRdict[str('0.04')][i][0] for i in range(runsim)]
#sns.distplot(densitydata)
plt.show();

#------------------------------------------highly specific to file


