from tbounds import *
from pprint import pprint
complist=[0.03,0.11,0.17]

plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.rc('savefig',dpi=300) 
plt.rc('figure', figsize=[8,2]) 

#==============================================================================Benchmark
#~ #================================512vs FR 
#-------------------------plot

fig=plt.figure()
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.3,right=0.78,left=0.08)
N=512
#plt.title("Performance of RT-Polar scheme,$\delta$="+str(0.05)+', $n=$'+str(N)) 
#-----512
maxiters=3
N=512
R_p1=246
fileT9="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_246in512_T9_18-06-05_16-55-22.txt"
#fileT9="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T9_18-06-06_13-34-29.txt"
T=9

(x,y,z)=(8,9,10)
lines=ml.getline(fileT9,[x,y,z])
#print lines
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[12])[0],maxiters)
TPT=[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]
#plt.plot(lines[0],[1-t for t in TPT],'-m^',label='RE-Polar, t='+str(T))


plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-m^',label='RT-Polar DE, t='+str(T))


#plt.show()

#-------------------------UK
T=0

fileUK="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_UK246in512_UK_18-06-05_22-13-03.txt"
lines=ml.getline(fileUK,[x,y,z])
point=len(lines[0])
maxiters=3
MeanIters=pl.getMeanIter(ml.getline(fileUK,[12])[0],maxiters)
#plt.plot(lines[0],[1-float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.ro',label='Ideal Detection')
plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-.ro',label='Ideal Detection')

#~ (x,y,z)=(9,10,11)
#~ fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-09_15-23-02.txt"
#~ lines=ml.getline(fileUK,[x,y,z])
#~ point=len(lines[0])
#~ maxiters=3
#~ MeanIters=pl.getMeanIter(ml.getline(fileUK,[13])[0],maxiters)
#~ plt.plot(lines[0],[1-float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.bo',label='Ideal Detection ch')

#-------------------------LTPT
T=0
(x,y,z)=(10,11,12)
fileLTPT="./simresults/polarfile_FERvsR_rateless_Det_LTPT_246in512_T0_18-06-05_22-41-25.txt"
lines=ml.getline(fileLTPT,[x,y,z])
point=len(lines[0])
maxiters=3
MeanIters=pl.getMeanIter(ml.getline(fileLTPT,[14])[0],maxiters)
#plt.plot(lines[0],[1-float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-gx',label='LT-Polar')

#plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-gx',label='LT-Polar DE')



"""
#---------------------------------cp=dp
N=512
fileFR={}
fileFR["0e005"]="./simresults/polarfile_FERvsp_FR0e005in512_18-06-05_23-42-42.txt"
fileFR["0e1"]="./simresults/polarfile_FERvsp_FR0e1in512_18-06-05_23-47-59.txt"
fileFR["0e05"]="./simresults/polarfile_FERvsp_FR0e05in512_18-06-05_23-44-37.txt"
fileFR["0e5"]="./simresults/polarfile_FERvsp_FR0e5in512_18-06-05_23-50-33.txt"
fileFR["0e4"]="./simresults/polarfile_FERvsp_FR0e4in512_18-06-05_23-50-07.txt"
fileFR["0e3"]="./simresults/polarfile_FERvsp_FR0e3in512_18-06-05_23-49-20.txt"
fileFR["0e2"]="./simresults/polarfile_FERvsp_FR0e2in512_18-06-05_23-48-45.txt"
fileFR["0e08"]="./simresults/polarfile_FERvsp_FR0e08in512_18-06-05_23-47-30.txt"
fileFR["0e03"]="./simresults/polarfile_FERvsp_FR0e03in512_18-06-05_23-43-05.txt"
fileFR["0e02"]="./simresults/polarfile_FERvsp_FR0e02in512_18-06-05_23-43-28.txt"
fileFR["0e25"]="./simresults/polarfile_FERvsp_FR0e25in512_18-06-06_16-08-35.txt"
"""
"""
fileFR["0e005"]="./simresults/polarchannel_FERvsp_FR0e005in512_18-05-08_23-47-09.txt"
fileFR["0e1"]="./simresults/polarchannel_FERvsp_FR0e1in512_18-05-08_23-53-00.txt"
fileFR["0e05"]="./simresults/polarchannel_FERvsp_FR0e05in512_18-05-08_23-46-32.txt"
fileFR["0e5"]="./simresults/polarchannel_FERvsp_FR0e5in512_18-05-09_00-43-29.txt"
fileFR["0e4"]="./simresults/polarchannel_FERvsp_FR0e4in512_18-05-09_14-25-53.txt"
fileFR["0e3"]="./simresults/polarchannel_FERvsp_FR0e3in512_18-05-09_14-25-30.txt"
fileFR["0e2"]="./simresults/polarchannel_FERvsp_FR0e2in512_18-05-09_14-25-08.txt"
fileFR["0e08"]="./simresults/polarchannel_FERvsp_FR0e08in512_18-05-09_14-24-36.txt"
fileFR["0e03"]="./simresults/polarchannel_FERvsp_FR0e03in512_18-05-09_14-23-04.txt"
fileFR["0e02"]="./simresults/polarchannel_FERvsp_FR0e02in512_18-05-09_14-17-33.txt"
fileFR["0e25"]="./simresults/polarchannel_FERvsp_FR0e25in512_18-05-09_15-21-47.txt"
"""


"""
#print fileFR

(x,y,z)=(-4,-3,-2)

zlist=fileFR.keys()
TPTZ={}
for Zmax in zlist:
	lines=ml.getline(fileFR[Zmax],[x,y,z])
	#print lines
	point=len(lines[0])
	plist=lines[0]
	print Zmax
	print lines[1]
	#plt.plot(lines[0],[1-float(lines[1][i]*(1-10**lines[2][i][1]))/N for i in range(point)],label='$Z \leq $'+Zmax.replace("e","."))
	#TPTZ[Zmax]=[float(lines[1][i]*(1-10**lines[2][i][1]))/N for i in range(point)]
	TPTZ[Zmax]=[float((N-lines[1][i])/(1-10**lines[2][i][1]))/N for i in range(point)]
	
TPTmax=[]		
for i in range(point):
	#TPTmax.append(1-max([TPTZ[Zmax][i] for Zmax in zlist]))
	TPTmax.append(min([TPTZ[Zmax][i] for Zmax in zlist]))
	
	
#plt.plot(plist,TPTmax,'-.b>',label='FR-Polar')

channel_plist=list(np.linspace(0.01,0.2,20))
plt.plot(lines[0],[pl.h(p) for p in lines[0]],'k',label='$H(X|Y)$')

plt.ylabel('$\l(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.025,0.175])
#plt.ylim([0.15,0.9])
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)


plt.show()
"""
#===================================CRC
"""
#CRC
./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T0_18-06-15_18-17-30.txt
./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T0_18-06-15_19-20-25.txt
#T=8
./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T8_18-06-15_18-04-37.txt

#CRC32
./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T0_18-06-15_19-39-52.txt
#T=8
./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T8_18-06-15_18-04-37.txt
#T=32
./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T32_18-06-15_19-38-19.txt



#~ #================================512vs FR 

#-------------------------plot
fig=plt.figure()
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
N=512
#plt.title("Performance of RT-Polar scheme,$\delta$="+str(0.05)+', $n=$'+str(N)) 

#-----512
maxiters=3
N=512
R_p1=246
#fileT8="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T8_18-06-15_18-04-37.txt"
fileT9="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T9_18-06-06_13-34-29.txt"
T=9

(x,y,z)=(8,9,10)
lines=ml.getline(fileT9,[x,y,z])
#print lines
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[12])[0],maxiters)
TPT=[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]
#plt.plot(lines[0],[1-t for t in TPT],'-m^',label='RE-Polar, t='+str(T))


#plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-m^',label='RB-Polar DE, t='+str(T))

N=512
#plt.title("Performance of RT-Polar scheme,$\delta$="+str(0.05)+', $n=$'+str(N)) 
#-----512
maxiters=3
N=512
R_p1=246
fileT32="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T32_18-06-15_19-38-19.txt"
#fileT9="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T9_18-06-06_13-34-29.txt"
T=32

(x,y,z)=(8,9,10)
lines=ml.getline(fileT32,[x,y,z])
#print lines
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT32,[12])[0],maxiters)
TPT=[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]
plt.plot(lines[0],[1-t for t in TPT],'-m^',label='RE-Polar, t='+str(T))


#plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-g>',label='RB-Polar DE, t='+str(T))

#-------------------------CRC
#~ fig=plt.figure()
#~ ax=plt.subplot(111)
#~ plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
N=512
#plt.title("Performance of RT-Polar scheme,$\delta$="+str(0.05)+', $n=$'+str(N)) 
#-----512
maxiters=3
N=512
R_p1=246
fileT32="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T0_18-06-15_19-39-52.txt"
#fileT9="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T9_18-06-06_13-34-29.txt"
T=0

(x,y,z)=(8,9,10)
lines=ml.getline(fileT32,[x,y,z])
#print lines
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT32,[12])[0],maxiters)
#TPT=[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]
#plt.plot(lines[0],[1-t for t in TPT],'-m^',label='RE-Polar, t='+str(T))


#plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-bo',label='CRC, 32bits')

#~ fig=plt.figure()
#~ ax=plt.subplot(111)
#~ plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
N=512
#plt.title("Performance of RT-Polar scheme,$\delta$="+str(0.05)+', $n=$'+str(N)) 
"""
"""
#-----512
maxiters=3
N=512
R_p1=246
#fileT8="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T0_18-06-15_18-17-30.txt"
fileT9="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_246in512_T9_18-06-06_13-34-29.txt"
T=9

(x,y,z)=(8,9,10)
lines=ml.getline(fileT9,[x,y,z])
#print lines
point=len(lines[0])
MeanIters=pl.getMeanIter(ml.getline(fileT9,[12])[0],maxiters)
#TPT=[float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)]
#plt.plot(lines[0],[1-t for t in TPT],'-m^',label='RE-Polar, t='+str(T))


plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-m^',label='RE-Polar, t='+str(T))

#plt.show()

#-------------------------UK
T=0

fileUK="./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_UK246in512_UK_18-06-05_22-13-03.txt"
lines=ml.getline(fileUK,[x,y,z])
point=len(lines[0])
maxiters=3
MeanIters=pl.getMeanIter(ml.getline(fileUK,[12])[0],maxiters)
#plt.plot(lines[0],[1-float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.ro',label='Ideal Detection')
plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-.ro',label='Ideal Detection')

#~ (x,y,z)=(9,10,11)
#~ fileUK="./simresults/polarchannel_FERvsR_rateless_Det_Iter_retro_UK246in512_T0_18-05-09_15-23-02.txt"
#~ lines=ml.getline(fileUK,[x,y,z])
#~ point=len(lines[0])
#~ maxiters=3
#~ MeanIters=pl.getMeanIter(ml.getline(fileUK,[13])[0],maxiters)
#~ plt.plot(lines[0],[1-float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-.bo',label='Ideal Detection ch')

#-------------------------LTPT
T=0
(x,y,z)=(10,11,12)
fileLTPT="./simresults/polarfile_FERvsR_rateless_Det_LTPT_246in512_T0_18-06-05_22-41-25.txt"
lines=ml.getline(fileLTPT,[x,y,z])
point=len(lines[0])
maxiters=3
MeanIters=pl.getMeanIter(ml.getline(fileLTPT,[14])[0],maxiters)
#plt.plot(lines[0],[1-float(R_p1-T)/(MeanIters[i]*N)*(1-10**lines[2][i]) for i in range(point)],'-gx',label='LT-Polar')

plt.plot(lines[0],[float(lines[1][i])/(1-10**lines[2][i]) for i in range(point) ],'-gx',label='LT-Polar DE')



"""
"""
#---------------------------------cp=dp
N=512
fileFR={}
fileFR["0e005"]="./simresults/polarfile_FERvsp_FR0e005in512_18-06-05_23-42-42.txt"
fileFR["0e1"]="./simresults/polarfile_FERvsp_FR0e1in512_18-06-05_23-47-59.txt"
fileFR["0e05"]="./simresults/polarfile_FERvsp_FR0e05in512_18-06-05_23-44-37.txt"
fileFR["0e5"]="./simresults/polarfile_FERvsp_FR0e5in512_18-06-05_23-50-33.txt"
fileFR["0e4"]="./simresults/polarfile_FERvsp_FR0e4in512_18-06-05_23-50-07.txt"
fileFR["0e3"]="./simresults/polarfile_FERvsp_FR0e3in512_18-06-05_23-49-20.txt"
fileFR["0e2"]="./simresults/polarfile_FERvsp_FR0e2in512_18-06-05_23-48-45.txt"
fileFR["0e08"]="./simresults/polarfile_FERvsp_FR0e08in512_18-06-05_23-47-30.txt"
fileFR["0e03"]="./simresults/polarfile_FERvsp_FR0e03in512_18-06-05_23-43-05.txt"
fileFR["0e02"]="./simresults/polarfile_FERvsp_FR0e02in512_18-06-05_23-43-28.txt"
fileFR["0e25"]="./simresults/polarfile_FERvsp_FR0e25in512_18-06-06_16-08-35.txt"
"""
"""
fileFR["0e005"]="./simresults/polarchannel_FERvsp_FR0e005in512_18-05-08_23-47-09.txt"
fileFR["0e1"]="./simresults/polarchannel_FERvsp_FR0e1in512_18-05-08_23-53-00.txt"
fileFR["0e05"]="./simresults/polarchannel_FERvsp_FR0e05in512_18-05-08_23-46-32.txt"
fileFR["0e5"]="./simresults/polarchannel_FERvsp_FR0e5in512_18-05-09_00-43-29.txt"
fileFR["0e4"]="./simresults/polarchannel_FERvsp_FR0e4in512_18-05-09_14-25-53.txt"
fileFR["0e3"]="./simresults/polarchannel_FERvsp_FR0e3in512_18-05-09_14-25-30.txt"
fileFR["0e2"]="./simresults/polarchannel_FERvsp_FR0e2in512_18-05-09_14-25-08.txt"
fileFR["0e08"]="./simresults/polarchannel_FERvsp_FR0e08in512_18-05-09_14-24-36.txt"
fileFR["0e03"]="./simresults/polarchannel_FERvsp_FR0e03in512_18-05-09_14-23-04.txt"
fileFR["0e02"]="./simresults/polarchannel_FERvsp_FR0e02in512_18-05-09_14-17-33.txt"
fileFR["0e25"]="./simresults/polarchannel_FERvsp_FR0e25in512_18-05-09_15-21-47.txt"
"""
"""


#print fileFR

(x,y,z)=(-4,-3,-2)

zlist=fileFR.keys()
TPTZ={}
for Zmax in zlist:
	lines=ml.getline(fileFR[Zmax],[x,y,z])
	#print lines
	point=len(lines[0])
	plist=lines[0]
	print Zmax
	print lines[1]
	#plt.plot(lines[0],[1-float(lines[1][i]*(1-10**lines[2][i][1]))/N for i in range(point)],label='$Z \leq $'+Zmax.replace("e","."))
	#TPTZ[Zmax]=[float(lines[1][i]*(1-10**lines[2][i][1]))/N for i in range(point)]
	TPTZ[Zmax]=[float((N-lines[1][i])/(1-10**lines[2][i][1]))/N for i in range(point)]
	
TPTmax=[]		
for i in range(point):
	#TPTmax.append(1-max([TPTZ[Zmax][i] for Zmax in zlist]))
	TPTmax.append(min([TPTZ[Zmax][i] for Zmax in zlist]))
	
	
#plt.plot(plist,TPTmax,'-.b>',label='FR-Polar')
"""
channel_plist=list(np.linspace(0.01,0.2,20))
plt.plot(lines[0],[pl.h(p) for p in lines[0]],'k',label='$H(X_1|X_2)$')

plt.ylabel('$\l(p)$')
plt.xlabel('flipover probability $p$')
plt.xlim([0.025,0.175])
#plt.ylim([0.15,0.9])
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)


plt.show()
