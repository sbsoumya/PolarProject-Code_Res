#generic plotter
#-------------------------------------


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

filename1="./simresults/lambda_prob_checker25-17-10_17-03-59.txt"
#filename1="./simresults/lambda_prob_checker25-17-10_18-11-24.txt"


table = []
with open(filename1,'r') as f:
    for line in f:
        table.append(json.loads(line))

print len(table)
LLRdict=table[23]
channel_plist=[0.1,0.2,0.3,0.4]
#channel_plist=[0.1]
color=["red","blue","green","yellow"]
goodchannels=table[8]

RI=[str(i) for i in table[10]]
N=len(RI)
runsim=1000

llrsum=np.zeros(N)

plt.figure(1)
index=range(len(RI))
j=1
for channel_p in channel_plist:
	j+=1
	#plt.figure(j)
	for i in range(runsim):
		plt.scatter(index,LLRdict[str(channel_p)][i],color=color[j-2])
		
		if channel_p==0.1:
			llrsum+=np.array(LLRdict[str(channel_p)][i])
		
		
		#plt.xticks(index,RI,rotation="vertical")
		
	#plt.hold(True)
	plt.title("Z order")

	
plt.figure(2)


densitydata=[LLRdict[str('0.1')][i][0] for i in range(runsim)]
sns.distplot(densitydata)

#------------------------------------------highly specific to file
RI_llr=pcon.getRI_LLR(llrsum,RI,N)

#rearrange
llr_index=[RI.index(i) for i in RI_llr]

plt.figure(3)

j=1

for channel_p in channel_plist:
	j+=1
	#plt.figure(j)
	for i in range(runsim):
		#rearrange
		plt.scatter(index,[LLRdict[str(channel_p)][i][k] for k in llr_index],color=color[j-2])
		
			
		#plt.xticks(index,RI,rotation="vertical")
	plt.scatter(index,[llrsum[k]/runsim for k in llr_index],color="black")	
	#plt.hold(True)
	plt.title("LLR_order")




plt.show()

#------------------------------------------------------------------	
