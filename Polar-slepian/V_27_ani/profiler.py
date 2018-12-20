#-------------------------------------------
# Name:       profiler.py
# Purpose:    various profilers
#
# Author:      soumya
#
# Created:    18/09/2017
#-------------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
import polarconstruct as pcon
from datetime import datetime
import json
import polarfile as pf
#-----------------------------------------
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
#-----------------------------------------
import profile
import time
from timeit import default_timer as timer
import json
from datetime import datetime

nlist=[10,11,12,13]
design_p=0.3
channel_p=design_p

runsim=100
stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
f1=open("./simresults/timing_"+str(design_p)+"_"+stamp+".txt",'w')
f2=open("./simresults/timplot_"+str(design_p)+"_"+stamp+".txt",'w')

OneMBlist=[]
	
#-------------------------------------------------------construction
for n in nlist:
	N=2**n #bits
	
	start = timer()
	for i in range(runsim):
		I=pcon.getGChZCK(design_p,N,N/2)[0]
	end = timer()

	G=len(I) #number of good channels
	D=np.zeros(N-G,dtype=int).tolist()#frozen data
	
	print "Timing REPORT for each string (in Secs)"
	print "---------------------------------------"
	print "N="+str(N)
	print "p_channel="+str(channel_p)
	print "sim ran :"+str(runsim)
	print "Rate:"+str(float(G)/N)
	
	json.dump( "Timing REPORT for each string (in Secs)",f1) ;f1.write("\n")
	json.dump( "---------------------------",f1) ;f1.write("\n")
	json.dump( "N="+str(N),f1) ;f1.write("\n");
	json.dump( "p_channel="+str(channel_p),f1) ;f1.write("\n")
	json.dump("sim ran :"+str(runsim),f1) ;f1.write("\n")
	json.dump("Rate:"+str(float(G)/N),f1) ;f1.write("\n")

	TC=(end-start)/runsim

	print "Time for construction:"+str(TC)	
	json.dump("Time for construction:"+str(TC)	,f1) ;f1.write("\n")
	UN=np.random.randint(2,size=G)

	#-----------------------------------------------------Encoding
	start = timer()
	for i in range(runsim):
		XN=ec.polarencodeG(UN,N,I,list(D))
		#XN=ec.polarencodeGR(UN,N,I,list(D))
	end = timer()

	TE=(end-start)/runsim
	print "Time for encoding:"+str(TE)
	json.dump("Time for encoding:"+str(TE)	,f1) ;f1.write("\n")


	#---------------------------------------------------channel

	start = timer()
	for i in range(runsim):
		YN=pl.BSCN(channel_p,XN)
	end = timer()

	TCh=(end-start)/runsim
	print "Time for channel:"+str(TCh)
	json.dump("Time for channel:"+str(TCh)	,f1) ;f1.write("\n")





	#-------------------------------------------------Decoding
	start = timer()
	for i in range(runsim):
		UN_hat=ec.polarSCdecodeG(YN,N,design_p,I,list(D))
	UN_decoded=ec.getUN_sUN_hat,I)
	end = timer()

	TD=(end-start)/runsim
	print "Time for decoding:"+str(TD)
	json.dump("Time for decoding:"+str(TD)	,f1) ;f1.write("\n")


	Tsim=TE+TCh+TD
	print "Total time for Each simulation(excluding construction):"+str(Tsim)
	json.dump("Total time for Each simulation(excluding construction):"+str(Tsim)	,f1) ;f1.write("\n")

	#-------------------------------------------------for 1 MB

	print "\nAnalysis for 1MB file:"
	
	json.dump("\nAnalysis for 1MB file:"	,f1) ;f1.write("\n")
	print "------------------------"
	Blocks=float(1024*1024*8)/N
	print "Blocks="+str(Blocks)
	print "Construction:"+str(TC)

	print "Encode Decode:"+str(Blocks*Tsim)
	Ttot=Blocks*Tsim+TC
	OneMBlist.append(Ttot)
	

	m, s = divmod(Ttot, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)
	json.dump("%d:%02d:%02d" % (h, m, s)	,f1) ;f1.write("\n")

json.dump(nlist,f2) ;f2.write("\n")
json.dump(OneMBlist,f2) ;f2.write("\n")
#json.dump([n*(2**n) for n in nlist],f2) ;f2.write("\n")


#------------------------------Profiler

"""
#I=range(N)
#D=[]
#--------------------------------------------------call graph 
#---------check pycallgraph.png
with PyCallGraph(output=GraphvizOutput()):
    d=ec.polarSCdecodeG(np.array(YN),N,p,I,D)


print d
print ec.getUN_s(d,I)

#-----------------------------profiler
profile.run('ec.polarSCdecodeG(np.array(YN),N,p,I,D);print')
"""
