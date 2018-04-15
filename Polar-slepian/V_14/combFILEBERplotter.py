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

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


#-------------------------------------------polar_channel_FERvsR

#to be automated
#~ -rw-rw-r-- 1 smart smart      543 Dec 29 08:46 polarfile_FERvsR_derate_rateless_kRx1024_0.04_17-12-28_16-25-30.txt
#~ -rw-rw-r-- 1 smart smart      731 Dec 29 09:19 polarfile_FERvsR_derate_rateless_LTPT1024_0.04_17-12-28_16-38-28.txt
#~ -rw-rw-r-- 1 smart smart      789 Dec 30 03:02 polarfile_FERvsR_derate_rateless_LTPT1024_0.15_17-12-28_16-38-42.txt
#~ -rw-rw-r-- 1 smart smart      596 Dec 30 04:51 polarfile_FERvsR_derate_rateless_kRx1024_0.15_17-12-28_16-25-38.txt
#~ -rw-rw-r-- 1 smart smart      793 Dec 30 14:24 polarfile_FERvsR_derate_rateless_LTPT1024_0.2_17-12-28_16-38-18.txt
#~ -rw-rw-r-- 1 smart smart      576 Dec 30 21:51 polarfile_FERvsR_derate_rateless_kRx1024_0.2_17-12-28_16-25-21.txt
#~ -rw-rw-r-- 1 smart smart      753 Dec 31 00:05 polarfile_FERvsR_derate_rateless_LTPT1024_0.25_17-12-28_16-39-03.txt
#~ -rw-rw-r-- 1 smart smart      545 Dec 31 11:04 polarfile_FERvsR_derate_rateless_kRx1024_0.25_17-12-28_16-25-46.txt
#~ -rw-rw-r-- 1 smart smart      462 Dec 31 20:35 polarfile_FERvsR_derate_sendpolar1024_0.04_17-12-27_20-28-59.txt
#~ -rw-rw-r-- 1 smart smart      501 Dec 31 20:36 polarfile_FERvsR_derate_sendpolar1024_0.2_17-12-27_20-28-44.txt
#~ -rw-rw-r-- 1 smart smart      509 Dec 31 21:03 polarfile_FERvsR_derate_sendpolar1024_0.25_17-12-27_20-29-16.txt
#~ -rw-rw-r-- 1 smart smart      491 Dec 31 21:09 polarfile_FERvsR_derate_sendpolar1024_0.15_17-12-27_20-29-08.txt

#~ /home/smart/Desktop/Project/fromserver/polarFile_FERvsR_1024_0.2_18-01-02_18-13-31.txt
#~ /home/smart/Desktop/Project/fromserver/polarFile_FERvsR_1024_0.15_18-01-02_18-15-01.txt
#~ /home/smart/Desktop/Project/fromserver/polarFile_FERvsR_1024_0.25_18-01-02_18-12-56.txt


#files for sendpolar (equivalent to rateless
#filename1="./simresults/polarfile_FERvsR_derate_sendpolar1024_0.04_17-12-27_20-28-59.txt"
#filename1="./simresults/polarfile_FERvsR_derate_sendpolar1024_0.2_17-12-27_20-28-44.txt"
#filename1="./simresults/polarfile_FERvsR_derate_sendpolar1024_0.25_17-12-27_20-29-16.txt"
#filename1="./simresults/polarfile_FERvsR_derate_sendpolar1024_0.15_17-12-27_20-29-08.txt"

#files for derate pch 
#filename1="./simresults/polarFile_FERvsR_1024_0.2_18-01-02_18-13-31.txt"
#filename1="./simresults/polarFile_FERvsR_1024_0.15_18-01-02_18-15-01.txt"
filename1="./simresults/polarFile_FERvsR_1024_0.25_18-01-02_18-12-56.txt"

#file for derate KRX
#filename2="./simresults/polarfile_FERvsR_derate_rateless_kRx1024_0.04_17-12-28_16-25-30.txt"
#filename2="./simresults/polarfile_FERvsR_derate_rateless_kRx1024_0.15_17-12-28_16-25-38.txt"
#filename2="./simresults/polarfile_FERvsR_derate_rateless_kRx1024_0.2_17-12-28_16-25-21.txt"
#filename2="./simresults/polarfile_FERvsR_derate_rateless_kRx1024_0.25_17-12-28_16-25-46.txt"

#files for LTPT
#filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.04_17-12-28_16-38-28.txt"
#filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.15_17-12-28_16-38-42.txt"
#filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.2_17-12-28_16-38-18.txt"
#filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.25_17-12-28_16-39-03.txt"

#files LTPT rlf new
#filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.04_18-01-15_23-35-56.txt"
#filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.15_18-01-15_23-36-12.txt"
#filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.2_18-01-15_23-35-37.txt"
filename3="./simresults/polarfile_FERvsR_derate_rateless_LTPT1024_0.25_18-01-15_23-36-35.txt"

#for higher reference
#filename2="./simresults/polarFile_FERvsR_1024_0.2_18-01-02_18-13-31.txt"
#filename2="./simresults/polarFile_FERvsR_1024_0.15_18-01-02_18-15-01.txt"
#filename2="./simresults/polarFile_FERvsR_1024_0.25_18-01-02_18-12-56.txt"

#p=0.04
#p=0.15
#p=0.2
p=0.25

#p1=0.04
#p1=0.15
#p1=0.2
#p1=0.25

#~ table0 = []
#~ with open(filename0,'r') as f:
    #~ for line in f:
        #~ table0.append(json.loads(line))


table1 = []
with open(filename1,'r') as f:
    for line in f:
        table1.append(json.loads(line))

#for row in table:
#	print(row)


#~ table2 = []
#~ with open(filename2,'r') as f:
    #~ for line in f:
        #~ table2.append(json.loads(line))
#~ print len(table2)
        
table3 = []
with open(filename3,'r') as f:
    for line in f:
        table3.append(json.loads(line))


#plt.subplot(2,1,1)
plt.semilogy(table1[7],[10**i for i in table1[8]],'k-o',label="Polar Code for p="+str(p))
#plt.semilogy(table2[7],[10**i for i in table2[8]],'b',linestyle=":",label="Polar Code for p="+str(p1))
#plt.semilogy(table1[7],[10**i for i in table1[8]],'r-o',label="1Iter")
#plt.semilogy(table2[9],[10**i for i in table2[10]],'b-o',label="Rateless KRX")
(A_r,BER)=ml.sortAextend(table3[11],table3[12])
plt.semilogy(A_r,[10**i for i in BER],'g-o',label="Inc-Frz with PHY-ED$^{*}$")


plt.xlabel('Achieved Rate')
plt.ylabel('Frame Error rate.')
plt.title('FER vs Rate for SW compression \nN=1024,p='+str(p)+',Capacity='+str(pl.CapacityBSC(1,p)))
plt.legend(loc="best")
plt.grid(True)

plt.figtext(0.005, 0.03, "$^{*}$Compound Channel=$\{$0.04,0.15,0.2,0.25$\}$")#+filename0+"\n"+filename3)

#~ plt.subplot(2,1,2)
#~ print table3[10]
#~ print table3[11]
#~ plt.plot(table3[10],table3[11],'g-o',label="Rateless LTPT")
#~ plt.plot(table2[8],table2[9],'b-o',label="Rateless KRX")
#~ plt.title("Sent rate vs achieved rate")
#~ plt.ylabel('Achieved Rate')
#~ plt.xlabel('Sent Rate')
plt.legend(loc="best")
plt.grid(True)


plt.show()

#------------------------------------------------------------------	
