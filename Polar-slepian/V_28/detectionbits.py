#---------------------------------------------------
# Name:       detectionbits.py
# Purpose:    Function for simulation of detection bits
#
#
# Author:      soumya
#
# Created:    17/03/2018
# Updated:    17/03/2018
#---------------------------------------------
import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import pandas as pd
from scipy import stats, integrate
import polarconstruct as pcon
import polarencdec as ec
import seaborn as sns
from datetime import datetime
import math as ma
import csv
import matlib as ml


def get_Detdict(channel_p,design_p,I,Tlist,N,runsim,RI):
	#runs for a given channel and true p
	#T list contains number of bits to be repeated
	Detdict={}
	Detdictcsv={}
	n=int(ma.log(N,2))
	G=len(I)
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	fname="./simresults/Detdict"+"-G-"+str(G)+"of"+str(N)+"-des-"+str(design_p).replace(".","p")+"-ch"+str(channel_p).replace(".","p")+"-"+stamp
	f2=open(fname+".txt",'w')
	
	
	for T in Tlist:
		print "\nrunning for "+str(T)+" Detection bits.."
		
		errcnt=np.zeros(T)
		Detdict[str(T)]=[]
		Detdictcsv[str(T)]=[]
			
		for i in range(runsim):
			UN_msg=list(np.random.randint(2,size=G-T))
			#print UN_msg
			UN_lock=list(UN_msg)[:T]
			#print UN_det
			UN=np.array(UN_msg+UN_lock)#The lock is sent as key
			#print UN
			#sending zeroes as frozen 
			# change when needed
			#FD=np.random.randint(2,size=N-len(I))
			FD=np.zeros(N-len(I),dtype=int)
			#print FD
			#the following are intermediate steps of encoding 
			# done to get VN
			# same as XN=ec.polarencodeG(UN,N,I,list(FD),False)
			#here VN is done seperately as it recorded as per reliability ordering
			VN=ec.formVN_u(list(UN),N,I,list(FD))
			#print VN
			XN=ec.polarencrec(VN,n-1,n)
			YN=pl.BSCN(channel_p,XN)
			UN_hat=ec.polarSCdecodeG(YN,N,design_p,I,FD,False)
			
			UN_decoded=ec.getUN(UN_hat,I,False)
			#print UN_decoded
			UN_decoded_lock=list(UN_decoded)[:T] # received lock
			UN_decoded_key=list(UN_decoded)[-T:] # received key
			#print UN_decoded_key
			#print UN_decoded_det
			#ch_err=np.logical_xor(UN_decoded_key,UN_decoded_det)
			#print ch_errcnt
			
			#---------------------------------
			Detdict[str(T)].append([ec.getchannel(VN,RI,False),ec.getchannel(UN_hat,RI,False),\
			UN_decoded_lock,UN_decoded_key,np.logical_xor(UN_decoded_lock,UN_decoded_key).tolist(),UN_decoded_lock!=UN_decoded_key])
			#print Detdict
			
			Detdictcsv[str(T)].append(["".join(str(x) for x in ec.getchannel(VN,RI,False)),"".join(str(x) for x in ec.getchannel(UN_hat,RI,False)),\
			"".join(str(x) for x in UN_decoded_lock),"".join(str(x) for x in UN_decoded_key)])
			
	json.dump(Detdict,f2);
	for T in Tlist:
		with open(fname+"T"+str(T)+".csv",'wb') as resultFile:
			wr = csv.writer(resultFile, dialect='excel')
			wr.writerow(["Sent"]+["Decoded"]+["Decodedlock"]+["Decodedbits"])
			for sim in range(runsim):	
				wr.writerow([str('"')+Detdictcsv[str(T)][sim][0]+str('"')]+[str('"')+Detdictcsv[str(T)][sim][1]+str('"')]+[str('"')+Detdictcsv[str(T)][sim][2]+str('"')]+[str('"')+Detdictcsv[str(T)][sim][3]+str('"')])
	return fname+".txt"

def load_Detdict(filename):
	f1=open(filename,'r')
	return json.load(f1);

def prob_detmatch(Detdict,runsim):
	#print Detdict
	Detmatch_probdict={}
	for T in Detdict:
		mismatchcnt=0
		for i in range(runsim):
			#print Detdict[T][i][5]
			mismatchcnt=mismatchcnt+Detdict[T][i][5]
		Detmatch_probdict[T]=1-float(mismatchcnt)/runsim
	Tlist=Detmatch_probdict.keys()
	Tlist.sort()
	return (Tlist,Detmatch_probdict)
