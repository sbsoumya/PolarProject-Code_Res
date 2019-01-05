from tbounds import *
from pprint import pprint

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from problib import h



complist=[0.03,0.11,0.17]

plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.rc('savefig',dpi=300) 
plt.rc('figure', figsize=[8,3]) 
"""
#1024-128
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_512in1024_T128_18-10-24_22-17-27.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_512in1024_T128_18-10-25_04-00-13.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_512in1024_T128_18-10-25_11-32-29.txt']

files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_512in1024_T128_19-01-01_00-15-57.txt',
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_512in1024_T128_19-01-01_06-05-34.txt', 
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_512in1024_T128_19-01-01_13-42-56.txt']
N=1024
t=128

#1024-128 5 -iter
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_512in1024_T128_18-10-25_01-54-51.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_512in1024_T128_18-10-25_07-38-07.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_512in1024_T128_18-10-25_15-12-28.txt']
"""
#512
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_246in512_T9_18-10-26_00-50-41.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_246in512_T9_18-10-26_03-27-03.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_246in512_T9_18-10-26_06-51-46.txt']
#Emprirical
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_246in512_T9_18-12-31_23-46-35.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_246in512_T9_19-01-01_02-17-33.txt',
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_246in512_T9_19-01-01_05-34-17.txt']
files5=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_246in512_T9_19-01-04_22-10-40.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_246in512_T9_19-01-05_01-14-58.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_246in512_T9_19-01-05_04-41-19.txt']


N=512
t=9

"""
#8192
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_4096in8192_T150_18-11-24_22-11-07.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_4096in8192_T150_18-11-27_20-26-02.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_4096in8192_T150_18-12-01_19-30-14.txt']
N=8192
t=150

#8192
# this needs divide by runsim
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_4096in8192_T1000_18-12-17_22-16-05.txt',
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_4096in8192_T1000_18-12-20_20-23-35.txt', 
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_4096in8192_T1000_18-12-24_19-09-34.txt']
N=8192
t=1000
runsim=1000
"""
#4G
#MC1
"""
files5=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_MC1_1_246in512_T9_19-01-03_22-34-32.txt']

"""
#==============================================================================Benchmark

#----given p_1
fig = plt.figure()
# COMPRESSION PLOTS-----------------------------
ax=plt.subplot(211)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
#p2=list(np.linspace(0.01,0.2,20))
(w,x,y,s,e)=(8,9,10,11,-2)
z=np.zeros([20])
theory=np.zeros([20])

usefile=2

thisfile=files4[usefile]
print thisfile
lines=ml.getline(thisfile,[w,x,y,s,e])
p1=lines[0]
p2=lines[1]
achrate=lines[2]
errexp=lines[3]
Empirical=lines[4]
EmpiricalCRC=ml.getline(files5[usefile],[-2])[0]
print Empirical
print EmpiricalCRC
point=len(lines[1])

for j in range(point):
	z[j]=float(lines[2][j])/(1-10**lines[3][j])
	

for  j in range(20):
		
	if p1>p2[j]:
		theory[j]=2*h(p1)+h(p2[j])
	else:
		theory[j]=2*h(p2[j])+h(p1)

plt.plot(p2,z,label="l(p) by formula",color="blue",marker="^")
plt.plot(p2,theory,label="Theory Sum Capacity",color="black",marker=">")
plt.plot(p2,Empirical,label="Empirical Compression",color="green", marker="<")
plt.plot(p2,EmpiricalCRC,label="EmpiricalCRC",color="red",marker="o")
plt.ylabel('$\l(p)$')
plt.xlabel('flipover probability $p_2$')
plt.title("$X-p_1-Y-p_2-Z$,\n $t$="+str(t)+", $n$="+str(N)+", $p_1=$"+str(p1))
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

#ERROR PLOTS--------------------------------------------

#error array
errorarray=	ml.getline(thisfile,[13])[0]
Darray=ml.getline(thisfile,[16])[0]
compA=[]
compB=[]
compC=[]
compSum=[]
err_Y2X=[]
err_Z2X=[]
err_X2Y=[]
err_Z2Y=[]
err_X2Z=[]
err_Y2Z=[]
print errorarray
for i in range(20):
	err_Y2X.append(10**errorarray[i][0])
	err_Z2X.append(10**errorarray[i][1])
	err_X2Y.append(10**errorarray[i][2])
	err_Z2Y.append(10**errorarray[i][3])
	err_Y2Z.append(10**errorarray[i][4])
	err_X2Z.append(10**errorarray[i][5])
	
	compA.append(float(Darray[i][0])/N/(1-10**errorarray[i][2]-10**errorarray[i][5]))	
	compB.append(float(Darray[i][1])/N/(1-10**errorarray[i][0]-10**errorarray[i][4]))
	compC.append(float(Darray[i][2])/N/(1-10**errorarray[i][1]-10**errorarray[i][3]))
	compSum.append(float(Darray[i][0])/N/(1-10**errorarray[i][2]-10**errorarray[i][5])+float(Darray[i][1])/N/(1-10**errorarray[i][0]-10**errorarray[i][4])+float(Darray[i][2])/N/(1-10**errorarray[i][1]-10**errorarray[i][3]))


#plt.plot(p2,compA,label="l for A")
#plt.plot(p2,compB,label="l for B")
#plt.plot(p2,compC,label="l for C")
#plt.plot(p2,compSum,label="sum l(p)")

ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

print len(err_Y2X)
print len(err_Z2X)
ax=plt.subplot(212)
#plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
plt.plot(p2,[10**lines[3][j] for j in range(20)],'ro-',label="total error")
#plt.plot(p2,[float(10**lines[3][j])/runsim for j in range(20)],'ro-',label="total error")

plt.plot(p2,err_Y2X,label="Y at X")
plt.plot(p2,err_Z2X,label="Z at X")
plt.plot(p2,err_X2Y,label="X at Y")
plt.plot(p2,err_Z2Y,label="Z at Y")
plt.plot(p2,err_X2Z,label="X at Z")
plt.plot(p2,err_Y2Z,label="Y at Z")
#plt.plot(p2,comp)
plt.xlabel('flipover probability $p_2$')
plt.ylabel('error')

plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)
#plt.legend(loc='best')
plt.show()

