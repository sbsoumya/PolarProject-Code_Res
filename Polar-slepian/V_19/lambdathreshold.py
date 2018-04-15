#---------------------------------------------------
# Name:       lambda.py
# Purpose:    to find statistics of channel llrs
#             wrt some threshold 
#
#
# Author:      soumya
#
# Created:    24/10/2017
# Updated:    14/02/2018
#---------------------------------------------
#import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import pandas as pd
from scipy import stats, integrate
import polarconstruct as pcon
import polarencdec as ec
#import seaborn as sns
from datetime import datetime
import math as ma
import csv
import matlib as ml

#LLRdict structure
#LLRdict[p]=[[ |llr| of all channels in RI sim 1],[ sim 2]....for given p

#LLRdictWU structure
#LLRdictWU[p]=[[llr of all channels in RI sim 1],"DATA in RI in sim1","Decoded data in RI sim1",[ sim 2]....for given p

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
	#f1=open("./simresults/llrdict"+"-"+str(N)+"-"+str(design_p).replace(".","p")+"-"+stamp+".txt",'w')
	f2=open("./simresults/llrsgndict"+"-"+str(N)+"-"+str(design_p).replace(".","p")+"-"+stamp+".txt",'w')
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
		
			LLRdict[str(channel_p)].append(ec.getchannel(llr,RI,False))
			LLRgoodchannels=abs(np.array(LLRdict[str(channel_p)][i][:G])).tolist()
			num_goodchannel=sum(llr > LT for llr in LLRgoodchannels)
			Fdict[str(channel_p)].append(float(num_goodchannel)/N)
		
		
		
	#json.dump(LLRdict,f1);
	json.dump(LLRdict,f2);
	if LLRdict_needed:	
		return (LLRdict,Fdict)
	else:
		return Fdict
#============================for generating LLRdictWU (NOT ABSOLUTE LLR)		
def get_LLRdictWU(channel_plist,design_p,I,N,runsim,RI):
	LLRdictWU={}
	G=len(I)
	stamp=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	#f2name defined twice correct!!
	f2name="./simresults/llrsgndict"+"-"+str(N)+"-"+str(design_p).replace(".","p")+"-"+stamp+".txt"
	f2=open("./simresults/llrsgndict"+"-"+str(N)+"-"+str(design_p).replace(".","p")+"-"+stamp+".txt",'w')
	n=int(ma.log(N,2))
	
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		
		LLRdictWU[str(channel_p)]=[]
			
		for i in range(runsim):
			UN=np.random.randint(2,size=G)
			FD=np.random.randint(2,size=N-len(I))
			#the following are intermediate steps of encoding 
			# done to get VN
			# same as XN=ec.polarencodeG(UN,N,I,list(FD),False)
			VN=ec.formVN_u(list(UN),N,I,list(FD))
			XN=ec.polarencrec(VN,n-1,n)
			YN=pl.BSCN(channel_p,XN)
			(llr,UN_hat)=ec.polarSCdecodeG(YN,N,design_p,I,FD,True)
			
			UN_decoded=ec.getUN(UN_hat,I,False)
			
			#---------------------------------
		
			LLRdictWU[str(channel_p)].append([ec.getchannel(llr,RI,False),"".join(str(x) for x in ec.getchannel(VN,RI,False)),"".join(str(x) for x in ec.getchannel(UN_hat,RI,False))])
		
	json.dump(LLRdictWU,f2);
	for channel_p in channel_plist:
		with open("./simresults/llrsgndict"+"-"+str(N)+"-"+str(design_p).replace(".","p")+"-On-"+str(channel_p).replace(".","p")+"-"+stamp+".csv",'wb') as resultFile:
			wr = csv.writer(resultFile, dialect='excel')
			wr.writerow(["","LLR in RI"]+[""]*(N-1)+["Data in RI"]+["Recovered Data in RI"])
			wr.writerow([""]+RI)
			for sim in range(runsim):	
				wr.writerow([str(sim+1)]+LLRdictWU[str(channel_p)][sim][0]+[str('"')+LLRdictWU[str(channel_p)][sim][1]+str('"')]+[str('"')+LLRdictWU[str(channel_p)][sim][2]+str('"')])
	return f2name

#get_LLRdictWD([0.04],0.04,[7,6,5,4],8,10,[7,6,5,4,3,2,1,0])

#---------------------------functions to be used if llrdict is available	

def load_LLRdict(filename):
	f1=open(filename,'r')
	return json.load(f1);
	

#===================Functions for LLRdict
	
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

def perc_channel_func_WD(LLRdict,channel_plist,N,LT,G,runsim,f_absllr,use_bad,use_func_for_LT):
	#as I is a subsequence of RI , only G is needed
	if use_func_for_LT:
		LT=f_absllr(LT)
		
	Fdict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Fdict[str(channel_p)]=[]	
		for i in range(runsim):
			if use_bad:
				LLRchannels=LLRdict[str(channel_p)][i][0][G:]
			else:
				LLRchannels=LLRdict[str(channel_p)][i][0][:G]
			
			num_channel=sum(f_absllr(llr) >= LT for llr in LLRchannels)
			#print len(LLRchannels)
			Fdict[str(channel_p)].append(float(num_channel)*100/len(LLRchannels))
		
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
	
def E_channel_abs_llr_G(LLRdict,channel_plist,N,G,runsim):
	#as I is a subsequence of RI , only G is needed
	#if use_func_for_LT:
	#	LT=f_Irv_abs(LT)
	#returns for G good channels
		
	Edict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Edict[str(channel_p)]=[]
		E_channel=np.zeros(G)	
		for i in range(runsim):
			LLRchannels=LLRdict[str(channel_p)][i][0][:G]
			SentBitchannels=LLRdict[str(channel_p)][i][1][:G]
			RV=[abs(llr) for llr,sentbit in zip(LLRchannels,SentBitchannels)]
			
			E_channel=E_channel+np.array(RV,dtype=float)/runsim
		
		Edict[str(channel_p)]=E_channel
		
	return Edict	
def E_channel_abs_llr_F(LLRdict,channel_plist,N,G,runsim):
	#as I is a subsequence of RI , only G is needed
	#if use_func_for_LT:
	#	LT=f_Irv_abs(LT)
	#returns for G good channels
		
	Edict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Edict[str(channel_p)]=[]
		E_channel=np.zeros(N-G)	
		for i in range(runsim):
			LLRchannels=LLRdict[str(channel_p)][i][0][G:]
			SentBitchannels=LLRdict[str(channel_p)][i][1][G:]
			RV=[abs(llr) for llr,sentbit in zip(LLRchannels,SentBitchannels)]
			
			E_channel=E_channel+np.array(RV,dtype=float)/runsim
		
		Edict[str(channel_p)]=E_channel
		
	return Edict	

#=======================Functions for LLRdictWU
	

def perc_channel_Irv_WU(LLRdict,channel_plist,N,LT,G,runsim,use_bad,use_func_for_LT):
	#as I is a subsequence of RI , only G is needed
	if use_func_for_LT:
		LT=f_Irv_abs(LT)
		print LT
		
	Fdict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Fdict[str(channel_p)]=[]	
		for i in range(runsim):
			if use_bad:
				LLRchannels=LLRdict[str(channel_p)][i][0][G:]
				SentBitchannels=LLRdict[str(channel_p)][i][1][G:]
				#print SentBitchannels
			else:
				LLRchannels=LLRdict[str(channel_p)][i][0][:G]
				SentBitchannels=LLRdict[str(channel_p)][i][1][:G]
				
			#num_channel=sum(f_Irv_abs(abs(llr)) >= LT for llr in LLRchannels)
			num_channel=sum(f_Irv(llr,int(sentbit)) >= LT for llr,sentbit in zip(LLRchannels,SentBitchannels))
			Fdict[str(channel_p)].append(float(num_channel)*100/len(LLRchannels))
		
	return Fdict

#returns  empirical average of f_Irv for the channels	
def E_channel_Irv_WU(LLRdict,channel_plist,N,G,runsim):
	#as I is a subsequence of RI , only G is needed
	#if use_func_for_LT:
	#	LT=f_Irv_abs(LT)
		
	Edict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Edict[str(channel_p)]=[]
		E_channel=np.zeros(N-G)	
		for i in range(runsim):
			LLRchannels=LLRdict[str(channel_p)][i][0][G:]
			SentBitchannels=LLRdict[str(channel_p)][i][1][G:]
			RV=[f_Irv(llr,int(sentbit)) for llr,sentbit in zip(LLRchannels,SentBitchannels)]
			
			E_channel=E_channel+np.array(RV,dtype=float)/runsim
		
		Edict[str(channel_p)]=E_channel
		
	return Edict
def E_channel_altIrv_WU(LLRdict,channel_plist,N,G,runsim):
	#as I is a subsequence of RI , only G is needed
	#if use_func_for_LT:
	#	LT=f_Irv_abs(LT)
		
	Edict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Edict[str(channel_p)]=[]
		E_channel=np.zeros(N-G)	
		for i in range(runsim):
			LLRchannels=LLRdict[str(channel_p)][i][0][G:]
			SentBitchannels=LLRdict[str(channel_p)][i][1][G:]
			RV=[-f_Irv(-llr,int(sentbit)) for llr,sentbit in zip(LLRchannels,SentBitchannels)]
			
			E_channel=E_channel+np.array(RV,dtype=float)/runsim
		
		Edict[str(channel_p)]=E_channel
		
	return Edict
	
def E_channel_Irv_abs(LLRdict,channel_plist,N,G,runsim):
	#as I is a subsequence of RI , only G is needed
	#if use_func_for_LT:
	#	LT=f_Irv_abs(LT)
		
	Edict={}
	for channel_p in channel_plist:
		print "\nrunning for "+str(channel_p)+"..."
		
		Edict[str(channel_p)]=[]
		E_channel=np.zeros(N-G)	
		for i in range(runsim):
			LLRchannels=LLRdict[str(channel_p)][i][0][G:]
			SentBitchannels=LLRdict[str(channel_p)][i][1][G:]
			RV=[f_Irv_abs(abs(llr)) for llr,sentbit in zip(LLRchannels,SentBitchannels)]
			
			E_channel=E_channel+np.array(RV,dtype=float)/runsim
		
		Edict[str(channel_p)]=E_channel
		
	return Edict

def PrOffracaboveFT(Fdict,channel_plist,PT,runsim):
	#as I is a subsequence of RI , only G is needed
	Ppercdict={}
	for channel_p in channel_plist:
		Ppercdict[str(channel_p)]=float(sum(perc>=PT for perc in Fdict[str(channel_p)]))/runsim
		
		
	return Ppercdict	
#---------------------------------functions for f_absllr,f_llr
def f_iden(x):
	return x
	
def f_abs(x):
	return abs(x)
	
def f_Irv_abs(absllr):
	return (ma.log(2)-ml.logdomain_sum(0,-absllr))/ma.log(2)
	
def f_Irv(llr,sentbit):
	return (ma.log(2)-ml.logdomain_sum(0,-llr*(1-2*sentbit)))/ma.log(2)
	 # unlike the theory here llr is p0/p1 s0 -llr

#----------------------------------fuctions for implementation of rateless LTPT
def perc_goodchannel_llr(llr,I,LT):
	G=len(I)
	L=abs(llr)
	LLRgoodchannels=ec.getchannel(L,I,False)
	perc=float(sum(llr >= LT for llr in LLRgoodchannels))*100/G
	return perc
	
# only for bad channels
def perc_bad_channel_Irv_WU_llr(llr,F,LT,Frozen_data,use_func_for_LT):
	B=len(F)
	if use_func_for_LT:
		LT=f_Irv_abs(LT)
	LLRbadchannels=ec.getchannel(llr,F,False)
	SentBitchannels=Frozen_data
	perc=float(sum(f_Irv(llr,int(sentbit)) >= LT for llr,sentbit in zip(LLRbadchannels,SentBitchannels)))*100/B
	return perc
