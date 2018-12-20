
import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import polarconstruct as pcon
import matplotlib.pyplot as plt
import matlib as ml
import os


channel_plist=list(np.linspace(0.05,0.45,10))

def genfile(blocks,N,plist):
	

	XN=np.random.randint(2,size=blocks*N)
	for p in plist:
		directory="./simresults/rsynccomp/"+str(p).replace(".","p")[:5]
		if not os.path.exists(directory):
			os.makedirs(directory)
		f2=open(directory+"/filebsc.txt","w")
		f2.write(ml.bittostring(1*pl.BSCN(p,XN)))
		
	directory="./simresults/rsynccomp/orig"
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	f1=open(directory+"/filebsc.txt","w")
	
	f1.write(ml.bittostring(XN))
	return 0
	
genfile(10000,1024,list(np.linspace(0.05,0.45,10)))

