import numpy as np
import problib as pl
from timeit import default_timer as timer


def mysum(a,b):
	return (a+b,a-b)
	
vmysum=np.vectorize(mysum,excluded= 'b')
a=[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
b=1
#print vmysum(a,b)

#~ start=timer()
#~ X=np.random.randint(2,size=(1000,1024))
#~ #X2=np.random.randint(2,size=1024)
#~ Y=pl.vBSCN(0.5,X)
#~ end = timer()
#~ TC=(end-start)
#~ print "Time taken:"+str(TC)	
#~ #print 1*Y

start=timer()
for i in range(1000000):
	X=np.random.randint(2,size=1024)
	Y=pl.BSCN(0.5,X)
end = timer()
TC=(end-start)
print TC	
#print 1*Y

start=timer()
X=np.random.randint(2,size=(1000000,1024))
Y=pl.vBSCN(0.5,X,1024,1000000)
end = timer()
TC=(end-start)
print TC
#print 1*Y	
