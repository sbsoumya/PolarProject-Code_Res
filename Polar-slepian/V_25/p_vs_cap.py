#-------------------------------------------
# Name:       Ratelesschannel_detection bits
# Purpose:    Detection bits
#
# Author:      soumya
#
# Created:    22/03/2018
#-------------------------------------------

import numpy as np
import math as ma
import problib as pl
import matlib as ml
import csv
import json

def getGlist(MaxG,lenG): 
	lcm=ml.get_lcm_for(range(1,lenG+1))
	return [int(MaxG/lcm)*(lcm/(i+1)) for i in range(lenG)]

print getGlist(525,3)
#~ plist=np.arange(0.5,0.0005,-0.0005)
#~ N=1024

#~ Capp=[int(pl.CapacityBSC(N,p)) for p in plist]

#~ with open("./simresults/p_vs_cap.csv",'wb') as resultFile:
		#~ wr = csv.writer(resultFile, dialect='excel')
		#~ wr.writerow(["p"]+["Cap for "+str(N)])
		#~ for p in plist:
			#~ wr.writerow([p,int(pl.CapacityBSC(N,p))])
			
#~ f1=open("./simresults/p_vs_cap.txt",'w')
#~ json.dump(plist.tolist(),f1);f1.write("\n")
#~ json.dump(Capp,f1);f1.write("\n")
			
			

#~ plist=[0.057,0.083,0.113,0.149,0.245,0.315]
#~ Glist=[700,600,500,400,300,200]
#~ delta=100

#~ k=5
#~ checkpeakrate=528
#~ T=32
#~ delta=int(checkpeakrate/(2*(k-1)))
#~ offset=0
#~ peakrate=2*(k-1)*delta+offset
#~ ratelist=[peakrate-i*delta for i in range(0,k)]
#~ plist = [pl.Inversecap1024(peakrate-i*delta) for i in range(0,k)]
#~ print [R-T for R in ratelist]
#~ print plist
#~ print delta
#~ print max(ratelist)>= 2*(k-1)*delta


ratelist=[int(1024-300+32)/i for i in range(1,6)]
plist = [pl.Inversecap1024(r) for r in ratelist]
print ratelist
print plist

[756, 378, 252, 189, 151]
[0.044499999999999595, 0.1584999999999997, 0.21649999999999975, 0.2524999999999998, 0.2774999999999998]


#~ k=5
#~ peakrate=540
#~ T=32
#~ ratelist=[float(peakrate)/(i+1) for i in range(0,k)]
#~ plist = [pl.Inversecap1024(float(peakrate)/(i+1)) for i in range(0,k)]
#~ print ratelist
#~ print plist
#~ print [R-T for R in getGlist(max(ratelist),k)]

#delta
#~ [536, 469, 402, 335, 268]
#~ [0.10249999999999965, 0.12449999999999967, 0.1489999999999997, 0.1764999999999997, 0.20799999999999974]
#~ 67[296, 259, 222, 185, 148]
#~ [296, 259, 222, 185, 148]
#~ [0.19449999999999973, 0.21249999999999974, 0.23249999999999976, 0.2549999999999998, 0.2799999999999998]
#~ 37
#~ [120, 105, 90, 75, 60]
#~ [0.3009999999999998, 0.31349999999999983, 0.32699999999999985, 0.34199999999999986, 0.3579999999999999]
#~ 15

# integer
#~ [120.0, 60.0, 40.0, 30.0, 24.0]
#~ [0.3009999999999998, 0.3579999999999999, 0.3839999999999999, 0.3994999999999999, 0.4099999999999999]
#~ [120, 60, 40, 30, 24]
#~ [300.0, 150.0, 100.0, 75.0, 60.0]
#~ [0.19249999999999973, 0.2784999999999998, 0.31799999999999984, 0.34199999999999986, 0.3579999999999999]
#~ [600.0, 300.0, 200.0, 150.0, 120.0]
#~ [0.08349999999999963, 0.19249999999999973, 0.24549999999999977, 0.2784999999999998, 0.3009999999999998]
#~ [600, 300, 200, 150, 120]

[540.0, 270.0, 180.0, 135.0, 108.0]
[0.10099999999999965, 0.20699999999999974, 0.2579999999999998, 0.2894999999999998, 0.31099999999999983]
[508, 238, 148, 103, 76]

[496, 430, 364, 298, 232]
[0.10499999999999965, 0.12699999999999967, 0.1509999999999997, 0.17849999999999971, 0.20999999999999974]
66
True





