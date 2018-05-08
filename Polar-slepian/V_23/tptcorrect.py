import matlib as ml
import problib as pl
import json


TPTfilelist=["./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt510in1024_c0p03_18-04-27_14-50-18.txt",
"./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt510in1024_c0p11_18-04-27_14-48-37.txt",
"./simresults/polarchannel_FERvsR_rateless_Det_Iter_maxtpt510in1024_c0p17_18-04-27_14-47-21.txt",
]
R_p1=510
N=1024
for TPTfile in TPTfilelist:
	(w,x,y,z,k)=(3,9,11,13,-2)
	lines=ml.getline(TPTfile,[w,x,y,z,k])
	maxiters=len(lines[0])
	print maxiters
	Tlist=lines[1]
	block_error_exp=lines[2]
	Iter_problist=lines[3]
	MeanIters=pl.getMeanIter(Iter_problist,maxiters)
	tpt=[float(R_p1-Tlist[i])/(MeanIters[i]*N)*(1-10**block_error_exp[i]) for i in range(len(Tlist))]
	#print lines
	print tpt
	print lines[4]
	f1=open(TPTfile,'a+')
	json.dump(tpt,f1);f1.write("\n")
	json.dump("The above tpt is the final tpt. previous one was having maxiters =2, where 3 was required",f1);
