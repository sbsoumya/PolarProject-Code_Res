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




#derate
#filename1="./simresults/polarchannel_FERvsR_derate1024_0.04_17-12-27_13-46-44.txt"
#filename1="./simresults/polarchannel_FERvsR_derate1024_0.04_17-12-27_18-29-15.txt"

#filename1="./simresults/polarchannel_FERvsR_derate1024_0.2_17-12-27_16-42-56.txt"
#filename1="./simresults/polarchannel_FERvsR_derate1024_0.25_17-12-27_16-44-39.txt"
#filename1="./simresults/polarchannel_FERvsR_derate1024_0.04_17-12-27_16-43-37.txt"
filename1="./simresults/polarchannel_FERvsR_derate1024_0.15_17-12-27_16-44-12.txt"



#derate_pch
#filename2="./simresults/polarchannel_FERvsR_derate_pch1024_0.04_17-12-27_13-47-57.txt"
#filename2="./simresults/polarchannel_FERvsR_derate_pch1024_0.04_17-12-27_18-29-24.txt"

#--FDin
#filename1="./simresults/polarchannel_FERvsR_derate_pch1024_0.04_17-12-27_14-12-45.txt"
#--FDout
#filename2="./simresults/polarchannel_FERvsR_derate_pch1024_0.04_17-12-27_14-12-21.txt"

#send_polar
#filename3="./simresults/polarchannel_FERvsR_derate_sendpolar1024_0.04_17-12-27_13-49-19.txt"
#filename3="./simresults/polarchannel_FERvsR_derate_sendpolar1024_0.04_17-12-27_18-29-08.txt"#1000
#---FD sendpolar comp
#filename3="./simresults/polarchannel_FERvsR_derate_sendpolar1024_0.04_17-12-27_13-49-19.txt"

#100000
#filename3="../V_11/simresults/polarchannel_FERvsR_derate_sendpolar1024_0.25_17-12-26_20-01-29.txt"
#filename3="../V_11/simresults/polarchannel_FERvsR_derate_sendpolar1024_0.04_17-12-26_20-01-38.txt"
filename3="../V_11/simresults/polarchannel_FERvsR_derate_sendpolar1024_0.15_17-12-26_20-01-48.txt"
#filename3="../V_11/simresults/polarchannel_FERvsR_derate_sendpolar1024_0.2_17-12-26_20-01-31.txt"





#1Iter
#--------------20-12-2017 files
#filename1="./simresults/polarchannel_FERvsR_derate1024_0.04_17-12-20_17-51-57.txt"
#filename2="./simresults/polarchannel_FERvsR_derate_1Iter1024_0.04_17-12-20_17-52-06.txt"

#filename4="./simresults/polarchannel_FERvsR_derate_1Iter1024_0.04_17-12-27_13-49-16.txt"
#filename4="./simresults/polarchannel_FERvsR_derate_1Iter1024_0.04_17-12-27_18-29-21.txt" #1000
#p=0.04
#p=0.15
p=0.2
#p=0.25


table1 = []
with open(filename1,'r') as f:
    for line in f:
        table1.append(json.loads(line))

#~ table2 = []
#~ with open(filename2,'r') as f:
    #~ for line in f:
        #~ table2.append(json.loads(line))
#~ print len(table2)
        
table3 = []
with open(filename3,'r') as f:
    for line in f:
        table3.append(json.loads(line))
        
#~ table4 = []
#~ with open(filename4,'r') as f:
    #~ for line in f:
        #~ table4.append(json.loads(line))



plt.semilogy(table1[7],[10**i for i in table1[8]],'r-o',label="derate ")
#~ plt.semilogy(table2[7],[10**i for i in table2[8]],'b-o',label="derate pch")
plt.semilogy(table3[7],[10**i for i in table3[8]],'g-o',label="sendpolar")
#~ plt.semilogy(table4[7],[10**i for i in table4[8]],'k-o',label="1ITER")
#plt.semilogy(table3[11],[10**i for i in table3[12]],'g-o',label="Rateless LTPT")
plt.xlabel('Achieved Rate')
plt.ylabel('Frame Error rate.')
plt.title('0p04 resolver \nN=1024,channel_p='+str(p)+',Capacity='+str(pl.CapacityBSC(1,p)))
plt.legend(loc="best")
plt.grid(True)

plt.figtext(0.005, 0.03, "Compound Channel=[0.04,0.15,0.2,0.25]\n"+filename1+"\n"+filename3)

plt.show()

#------------------------------------------------------------------	
