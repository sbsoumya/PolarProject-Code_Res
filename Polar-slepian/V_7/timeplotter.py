#generic plotter
#-------------------------------------


import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl

#-------------------------------------------timing

#~ #to be automated

#~ filename1="./simresults/timplot_0.3_19-10-17_16-33-11.txt"
#~ filename2="./simresults/timplot_0.3_20-10-17_10-11-05.txt"


#~ table = []
#~ with open(filename1,'r') as f:
    #~ for line in f:
        #~ table.append(json.loads(line))

#~ table2 = []
#~ with open(filename2,'r') as f:
    #~ for line in f:
        #~ table2.append(json.loads(line))

#~ plt.plot(table[0],table[1],'r',label='NonRecursive')
#~ #plt.plot(table2[0],table2[2],'b',label='NlogN')
#~ plt.plot(table2[0],table2[1],'g',label='Recursive Encoding')

#~ plt.xlabel('blocklength log2N')
#~ plt.ylabel('time in sec.')
#~ plt.title('timing for 1 MB file')
#~ plt.legend(loc="best")
#~ plt.grid(True)

#~ plt.figtext(0.005, 0.03, filename1+'\n'+filename2)

#~ plt.show()

#------------------------------------------------------------------	

#to be automated

filename1="./simresults/blocktimes.txt"

table=[]
table.append([10,11,12,13])
#NonRecursive(Encode,Decode,Total)
table.append([0.0287354803085,0.139898400307,0.566985170841,2.35099009991])
table.append([0.0920639801025,0.203505890369,0.490626399517,1.17260741949])
table.append([0.120817821026,0.343437001705,1.05767530918,3.52372240067])
#NlogN
table.append([10*1024,11*2048,12*4096,13*8192])
#Recursive
table.append([0.0105401611328,0.0292995214462,0.0908936405182,0.311909191608])
table.append([0.0873624682426,0.200129852295,0.47218818903,1.16889888048])
table.append([0.0979208683968,0.229463493824,0.563149499893,1.48094025135])

plt.plot(table[0],table[1],label='NonRecursive Encode')
plt.plot(table[0],table[2],label='Decode')
plt.plot(table[0],table[3],label='NonRecursive total')
#plt.plot(table[0],[x/10000 for x in table[4]],label='Nlog(N)/10000')
plt.plot(table[0],table[5],label='Recursive Encode')
plt.plot(table[0],table[7],label='Recursive total')

plt.xlabel('blocklength log2N')
plt.ylabel('time in sec.')
plt.title('timing for comparison to NLogN')
plt.legend(loc="best")
plt.grid(True)

plt.figtext(0.005, 0.03, filename1)

plt.show()
