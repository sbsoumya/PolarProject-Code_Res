#---------------------------------------------------
# Name:       lambda.py
# Purpose:    to find statistics of channel llrs
#             wrt some threshold 
#
#
# Author:      soumya
#
# Created:    24/10/2017
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

#LLRdict structure
#LLRdict[p]=[[llr of all channels in RI sim 1],[ sim 2]....for given p

#-----------------------functions to be used if llrdict is NOT available	
def P_allgood(channel_plist,design_p,I,N,LT,runsim,RI,LLRdict_needed):
	LLRdict={}
	Pdict={}
	
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	f1=open("./simresults/llrdict"+"-"+str(N)+"-"+str(design_p).replace(".","p")+"-"+stamp+".txt",'w')
	
	FD=np.zeros(N-len(I),dtype=int).tolist()
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Count_all_good=0
		LLRdict[str(channel_p)]=[]
			
		for i in range(runsim):
			
			
			UN=np.random.randint(2,size=len(I))
			UN_encoded=ec.polarencodeG(UN,N,I,list(FD),False)
			YN=pl.BSCN(channel_p,UN_encoded)
			(llr,d)=ec.polarSCdecodeG(YN,N,design_p,I,list(FD),True)
			L=abs(llr)
			
			#---------------------------------
			llr_Gmin=min(ec.getchannel(L,I,False))
			LLRdict[str(channel_p)].append(ec.getchannel(L,RI,False))
			Count_all_good+=(llr_Gmin>=LT)
	
		
		Pdict[str(channel_p)]=float(Count_all_good)/runsim
		
	json.dump(LLRdict,f1);
	if LLRdict_needed:	
		return (LLRdict,Pdict)
	else:
		return Pdict

def frac_goodchannel(channel_plist,design_p,I,N,LT,runsim,RI,LLRdict_needed):
	LLRdict={}
	Fdict={}
	G=len(I)
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	f1=open("./simresults/llrdict"+"-"+str(N)+"-"+str(design_p).replace(".","p")+"-"+stamp+".txt",'w')
	
	FD=np.zeros(N-len(I),dtype=int).tolist()
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		
		LLRdict[str(channel_p)]=[]
		Fdict[str(channel_p)]=[]
			
		for i in range(runsim):
			
			
			UN=np.random.randint(2,size=len(I))
			UN_encoded=ec.polarencodeG(UN,N,I,list(FD),False)
			YN=pl.BSCN(channel_p,UN_encoded)
			(llr,d)=ec.polarSCdecodeG(YN,N,design_p,I,list(FD),True)
			L=abs(llr)
			
			#---------------------------------
		
			LLRdict[str(channel_p)].append(ec.getchannel(L,RI,False))
			LLRgoodchannels=LLRdict[str(channel_p)][i][:G]
			num_goodchannel=sum(llr > LT for llr in LLRgoodchannels)
			Fdict[str(channel_p)].append(float(num_goodchannel)/N)
		
		
		
	json.dump(LLRdict,f1);
	if LLRdict_needed:	
		return (LLRdict,Fdict)
	else:
		return Fdict
	
#---------------------------functions to be used if llrdict is available	
def load_LLRdict(filename):
	f1=open(filename,'r')
	return json.load(f1);
	
def perc_goodchannel_WD(LLRdict,channel_plist,N,LT,G,runsim):
	#as I is a subsequence of RI , only G is needed
	Fdict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Fdict[str(channel_p)]=[]	
		for i in range(runsim):
			LLRgoodchannels=LLRdict[str(channel_p)][i][:G]
			num_goodchannel=sum(llr >= LT for llr in LLRgoodchannels)
			Fdict[str(channel_p)].append(float(num_goodchannel)*100/G)
		
	return Fdict
	
def perc_goodchannel_LTvec_WD(LLRdict,channel_plist,N,LTvec,G,runsim): #LTvec in order of good channels
	#as I is a subsequence of RI , only G is needed
	Fdict={}
	LTv=LTvec[:G] #LADjustment
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Fdict[str(channel_p)]=[]	
		for i in range(runsim):
			LLRgoodchannels=LLRdict[str(channel_p)][i][:G]
			
			num_goodchannel=sum(llr >= LT for llr,LT in zip(LLRgoodchannels,LTv))
			Fdict[str(channel_p)].append(float(num_goodchannel)*100/G)
		
	return Fdict
	
def PrOffracaboveFT(Fdict,channel_plist,PT,runsim):
	#as I is a subsequence of RI , only G is needed
	Ppercdict={}
	for channel_p in channel_plist:
		Ppercdict[str(channel_p)]=float(sum(perc>=PT for perc in Fdict[str(channel_p)]))/runsim
		
		
	return Ppercdict	

#----------------------------------fuctions for implementation of rateless LTPT
def perc_goodchannel_llr(llr,I,LT):
	G=len(I)
	L=abs(llr)
	LLRgoodchannels=ec.getchannel(L,I,False)
	perc=float(sum(llr >= LT for llr in LLRgoodchannels))*100/G
	return perc
