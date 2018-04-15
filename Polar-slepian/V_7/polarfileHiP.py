import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
import polarconstruct as pcon
from datetime import datetime
import json
import polarfile as pf
from pprint import pprint

#=================================================================hiPset
def getHiPset(N,p,d,C):
	E=N*p
	v=ma.sqrt(N*p*(1-p)*ma.log(1/d))/C
	
	return (int(E-v),int(E+v))


#print getHiPset(128,0.1,0.5,10)
#print getHiPset(1024,0.1,0.8,10)
#print getHiPset(1024,0.1,0.2,10)

#-------------------------------------------Not-used
def getflippat(N):
	try:
		filename="./simresults/flipdict_"+str(N)+".txt"	
		f1=open(filename,'r')
		flipdict= json.load(f1)
	except:
		flipdict=pl.BSCepatflip(N)
	return flipdict

#=================================================================simulation		
N=32
p=0.1
d=0.8
C=10

tolerable_error= -2 #using ZCL for channel
runsim=100

try:
	I=pcon.getGCHsim('ZL',N,p,tolerable_error)
except:
	(I,E)=pcon.getGChZCL(p,N,tolerable_error)


(L,U)=getHiPset(N,p,d,C)
HiP=range(L,U+1)

#HiP=[4]

Block_err_dict={}

stamp=datetime.now().strftime("%d-%m-%y_%H-%M-%S")
f1=open("./simresults/polarfileHiP_"+str(N)+"_"+str(p)+"_"+stamp+".txt",'w')
	
print "HIGH PROBABILITY KNOWN PATTERN REPORT"
print "--------------------------------------"
print "N="+str(N)
print "p="+str(p)
print "delta="+str(d)
print "constant="+str(C)

R=float(len(I))/N
print "R="+str(R)
print "runsim="+str(runsim)

print "High Probabiltity flips"
print HiP
print "tolerable error exponent:"+str(tolerable_error)# channels selected as per this
print "Error probability for Known patterns..."

	
		
json.dump( "HIGH PROBABILITY KNOWN PATTERN REPORT",f1) ;f1.write("\n")
json.dump( "---------------------------",f1) ;f1.write("\n")
json.dump( "N="+str(N),f1) ;f1.write("\n")
json.dump( "p="+str(p),f1) ;f1.write("\n")
json.dump( "delta="+str(d),f1) ;f1.write("\n")
json.dump( "constant="+str(C),f1) ;f1.write("\n")
json.dump( "R="+str(R),f1) ;f1.write("\n")
json.dump( "runsim="+str(runsim),f1) ;f1.write("\n")
json.dump( "tolerable error exponent:"+str(tolerable_error),f1) ;f1.write("\n")
json.dump( "Good Channels:",f1) ;f1.write("\n")
json.dump( I,f1) ;f1.write("\n")
json.dump( "R="+str(R),f1) ;f1.write("\n")
json.dump("High Probabiltity flips",f1) ;f1.write("\n")
json.dump( HiP,f1);f1.write("\n")
json.dump("Error probability for Known patterns",f1);f1.write("\n")





for k in HiP:
	fliplist=pl.nCkflips(N,k,True)
	print str(len(fliplist))+" sequences for "+str(k)+"flips\n"
	json.dump(str(len(fliplist))+" sequences for "+str(k)+"flips",f1);f1.write("\n")
	#print fliplist
	for pattern in fliplist:
		
		block_errorcnt=0
		patternlist=[int(i) for i in pattern]
		#print patternlist
		
		for i in range(runsim):
			XN=np.random.randint(2,size=N)
			XN_decoded=pf.polarfile_known(XN,p,patternlist,I)
			if XN.tolist()!=XN_decoded.tolist():
					block_errorcnt+=1
		
		Block_err_dict[pattern]=float(block_errorcnt)/runsim
			
	
	

pprint(Block_err_dict)

json.dump(Block_err_dict,f1)




		    





