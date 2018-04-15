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
import matlib as ml

#-------------------------------------------polar_channel_FERvsR

#to be automated

#files for derate channel=design
#filename0="./simresults/polarchannel_FERvsR_derate1024_0.04_17-11-02_17-21-53.txt"
filename0="./simresults/polarchannel_FERvsR_derate1024_0.15_17-11-02_20-00-43.txt"
#filename0="./simresults/polarchannel_FERvsR_derate1024_0.2_17-11-02_22-39-12.txt"
#filename0="./simresults/polarchannel_FERvsR_derate1024_0.25_17-11-03_01-18-37.txt"
#1 Iter-----------------------
#filename1="./simresults/polarchannel_FERvsR_derate_1Iter1024_0.04_17-11-23_17-04-04.txt"
filename1="./simresults/polarchannel_FERvsR_derate_1Iter1024_0.15_17-11-23_17-04-09.txt"
#filename1="./simresults/polarchannel_FERvsR_derate_1Iter1024_0.2_17-11-23_17-04-00.txt"
#filename1="./simresults/polarchannel_FERvsR_derate_1Iter1024_0.25_17-11-23_17-04-13.txt"


#file for greedy channel design
#filename4="./simresults/polarchannel_FERvsR_derate_greedy21024_0.04_17-11-03_09-54-02.txt"
filename4="./simresults/polarchannel_FERvsR_derate_greedy21024_0.15_17-11-03_12-32-26.txt"
#filename4="./simresults/polarchannel_FERvsR_derate_greedy21024_0.2_17-11-03_15-11-28.txt"
#filename4="./simresults/polarchannel_FERvsR_derate_greedy21024_0.25_17-11-03_17-50-32.txt"

#file for derate KRX
#filename2="./simresults/polarchannel_FERvsR_derate_rateless1024_0.04_17-11-03_10-56-51.txt"
filename2="./simresults/polarchannel_FERvsR_derate_rateless1024_0.15_17-11-03_10-58-00.txt"
#filename2="./simresults/polarchannel_FERvsR_derate_rateless1024_0.2_17-11-03_10-58-43.txt"
#filename2="./simresults/polarchannel_FERvsR_derate_rateless1024_0.25_17-11-03_10-59-09.txt"

#files for LTPT
#filename3="./simresults/polarchannel_FERvsR_derate_rateless_LTPT1024_0.04_17-11-07_10-10-56.txt"
filename3="./simresults/polarchannel_FERvsR_derate_rateless_LTPT1024_0.15_17-11-07_10-11-01.txt"
#filename3="./simresults/polarchannel_FERvsR_derate_rateless_LTPT1024_0.2_17-11-07_10-10-51.txt"
#filename3="./simresults/polarchannel_FERvsR_derate_rateless_LTPT1024_0.25_17-11-07_10-10-50.txt"

#p=0.04
p=0.15
#p=0.2
#p=0.25

table0 = []
with open(filename0,'r') as f:
    for line in f:
        table0.append(json.loads(line))


table1 = []
with open(filename1,'r') as f:
    for line in f:
        table1.append(json.loads(line))

#for row in table:
#	print(row)


table2 = []
with open(filename2,'r') as f:
    for line in f:
        table2.append(json.loads(line))
print len(table2)
        
table3 = []
with open(filename3,'r') as f:
    for line in f:
        table3.append(json.loads(line))


plt.subplot(2,1,1)
plt.semilogy(table0[7],[10**i for i in table0[8]],'k-o',label="Channel_p=design_p ")
plt.semilogy(table1[7],[10**i for i in table1[8]],'r-o',label="Channel_p=design_p ,1Iter")
plt.semilogy(table2[9],[10**i for i in table2[10]],'b-o',label="Rateless KRX")
(A_r,BER)=ml.sortAextend(table3[11],table3[12])
plt.semilogy(A_r,[10**i for i in BER],'g-o',label="Rateless LTPT")


plt.xlabel('Achieved Rate')
plt.ylabel('Frame Error rate.')
plt.title('FER vs Rate Rateless LTPT design \nN=1024,channel_p='+str(p)+',Capacity='+str(pl.CapacityBSC(1,p)))
plt.legend(loc="best")
plt.grid(True)

plt.figtext(0.005, 0.03, "Compound Channel=[0.04,0.15,0.2,0.25]\n"+filename0+"\n"+filename1+"\n"+filename2+"\n"+filename3)

plt.subplot(2,1,2)
print table3[10]
print table3[11]
plt.plot(table3[10],table3[11],'g-o',label="Rateless LTPT")
plt.plot(table2[8],table2[9],'b-o',label="Rateless KRX")
plt.title("Sent rate vs achieved rate")
plt.ylabel('Achieved Rate')
plt.xlabel('Sent Rate')
plt.legend(loc="best")
plt.grid(True)


plt.show()

#------------------------------------------------------------------	
