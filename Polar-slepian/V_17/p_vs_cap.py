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

plist=np.arange(0.5,0.0005,-0.0005)
N=1024

Capp=[int(pl.CapacityBSC(N,p)) for p in plist]

with open("./simresults/p_vs_cap.csv",'wb') as resultFile:
		wr = csv.writer(resultFile, dialect='excel')
		wr.writerow(["p"]+["Cap for "+str(N)])
		for p in plist:
			wr.writerow([p,int(pl.CapacityBSC(N,p))])
			
f1=open("./simresults/p_vs_cap.txt",'w')
json.dump(plist.tolist(),f1);f1.write("\n")
json.dump(Capp,f1);f1.write("\n")
			
			

#~ plist=[0.057,0.083,0.113,0.149,0.245,0.315]
#~ Glist=[700,600,500,400,300,200]
#~ delta=100
