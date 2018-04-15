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

#-------------------------------------------polar_channel_FERvsR

#to be automated

filename1="./simresults/polarchannel_FERvsR_derate1024_0.04_17-11-02_17-21-53.txt"
filename3="./simresults/polarchannel_FERvsR_derate_rateless_LTPT1024_0.04_17-11-07_10-10-56.txt"



table = []
with open(filename1,'r') as f:
    for line in f:
        table.append(json.loads(line))

#for row in table:
#	print(row)


#~ table2 = []
#~ with open(filename2,'r') as f:
    #~ for line in f:
        #~ table2.append(json.loads(line))
        
table3 = []
with open(filename3,'r') as f:
    for line in f:
        table3.append(json.loads(line))


plt.subplot(2,1,1)
plt.semilogy(table[7],[10**i for i in table[8]],'r',label="Channel_p=design_p")
#plt.semilogy(table2[8],[10**i for i in table2[9]],'b',label="channel_p>design_p = 0.04")
plt.semilogy(table3[10],[10**i for i in table3[12]],'g',label="Rateless LTPT")
plt.xlabel('sent Rate')
plt.ylabel('Frame Error rate.')
plt.title('FER vs Rate Rateless LTPT design \nN=1024,Capacity='+str(pl.CapacityBSC(1,0.04))+",channel_p="+str("0.04"))
plt.legend(loc="best")
plt.grid(True)

plt.figtext(0.005, 0.03, "Compound Channel=[0.04,0.15,0.2,0.25]\n"+filename1+"\n"+filename3)

plt.subplot(2,1,2)
print table3[10]
print table3[11]
plt.plot(table3[10],table3[11])
plt.title("Sent rate vs achieved rate")
plt.xlabel('Sent Rate')
plt.ylabel('Achieved Rate')
plt.grid(True)


plt.show()

#------------------------------------------------------------------	
