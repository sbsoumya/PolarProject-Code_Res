#generic plotter
#-------------------------------------


import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#-------------------------------------------polar_channel_FERvsR

#to be automated

filename1="./simresults/polarFile_FERvsR_2048_0.1_24-10-17_13-02-13.txt"
filename2="./simresults/polarFile_FERvsR_1024_0.1_25-10-17_10-10-39.txt"
#filename3="./simresults/polarchannel_FERvsR_4096_0.1_12-09-17_23-46-04.txt"


filename1="./simresults/polarFile_FERvsR_2048_0.1_24-10-17_13-02-13.txt"
filename2="./simresults/polarFile_FERvsR_1024_0.1_25-10-17_10-10-39.txt"
#filename1="./simresults/polarchannel_FERvsR_llr1024_0.1_26-10-17_19-03-10.txt"

table = []
with open(filename1,'r') as f:
    for line in f:
        table.append(json.loads(line))

#for row in table:
#	print(row)

table2 = []
with open(filename2,'r') as f:
    for line in f:
        table2.append(json.loads(line))
#table3 = []
#with open(filename3,'r') as f:
#    for line in f:
#        table3.append(json.loads(line))


plt.semilogy(table2[7],[10**i for i in table2[8]],'r-o',label="N=1024")
plt.semilogy(table[7],[10**i for i in table[8]],'b-^',label="N=2048")
#plt.semilogy(table3[7],[10**i for i in table3[8]],'g',label="N=4096")
plt.xlabel('Rate')
plt.ylabel('Frame Error rate.')
plt.title('FER vs Rate for SW with Polar Code over BSC(p)\nCapacity='+str(pl.CapacityBSC(1,0.1))+',p='+str(0.1))
plt.legend(loc="best")
plt.grid(True)

#plt.figtext(0.005, 0.03, filename1)

plt.show()

#------------------------------------------------------------------	
