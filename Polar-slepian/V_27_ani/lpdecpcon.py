from lpdecheaders import *
import json
import math as ma
import polarencdec as ec
import polarconstruct as pcon
import numpy as np
#==================
def getreliability_order_TV(N,M):
	try:
		filename="./simresults/GC/GCTV"+str(N)+"_"+str(M)+".txt"
		f1=open(filename,'r')
		n=int(ma.log(N,2))
		return ec.bitreverseorder(json.load(f1),n)
		#return (json.load(f1))
	except:
		channel = BMSChannel.BSC(0.01)
		n=int(ma.log(N,2))
		frozenindices=computeFrozenIndices(channel, n, mu=M, threshold=None, rate=0)
		filename="./simresults/GC/GCTV"+str(N)+"_"+str(M)+".txt"
		f1=open(filename,'w')
		json.dump(frozenindices,f1)
		print len(frozenindices)
		return frozenindices
#~ a=getreliability_order_TV(1024,256)
#~ b=pcon.getreliability_order(1024)
#~ print a
#~ print b
#~ c=np.array(a)==np.array(b)
#~ print c
#~ print sum(c)
#~ g=700
#~ print len(set(a[g:]))
#~ print len(set(a[g:])-set(b[g:]))

#print numpy.array(a)==numpy.array(b)
