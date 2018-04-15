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

#----------------------------------------------------------Decoding

n=12
p=0.3
N=2**n
I=pcon.getGChZCL(p,N,-6)[0]
print len(I)
D=np.zeros(N-len(I),dtype=int).tolist()
YN=np.random.randint(2,size=2**n)
"""
#I=range(N)
#D=[]
#--------------------------------------------------call graph 
#---------check pycallgraph.png
with PyCallGraph(output=GraphvizOutput()):
    d=ec.polarSCdecodeG(np.array(YN),N,p,I,D)


print d
print ec.getUN(d,I)

#-----------------------------profiler
profile.run('ec.polarSCdecodeG(np.array(YN),N,p,I,D);print')
"""
#------------------------------timer
start = timer()
for i in range(100):
	print ec.polarSCdecodeG(np.array(YN),N,p,I,D)
end = timer()
print end-start
