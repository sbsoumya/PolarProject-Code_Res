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

#1024-128
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_512in1024_T128_18-10-24_22-17-27.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_512in1024_T128_18-10-25_04-00-13.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_512in1024_T128_18-10-25_11-32-29.txt']

#1024-128 5 -iter
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_512in1024_T128_18-10-25_01-54-51.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_512in1024_T128_18-10-25_07-38-07.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_512in1024_T128_18-10-25_15-12-28.txt']

#512
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_246in512_T9_18-10-26_00-50-41.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_246in512_T9_18-10-26_03-27-03.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_246in512_T9_18-10-26_06-51-46.txt']
N=512
T=9

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


#==============================================================================Benchmark

#----given p_1
fig = plt.figure()
#ax = fig.gca(projection='3d')
ax=plt.subplot(211)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
p1=list(np.linspace(0.01,0.2,20))
p2=list(np.linspace(0.01,0.2,20))
p1m,p2m=np.meshgrid(p1,p2)
#print p1
#print p2
(w,x,y,s)=(8,9,10,11)
z=np.zeros([20,20])
theory=np.zeros([20,20])
start=1
end=2
for i in range(start,end):
	thisfile=files4[i]
	print thisfile
	lines=ml.getline(thisfile,[w,x,y,s])
	point=len(lines[1])
	print lines[0]
	#p2=lines[1]
	#p1=lines[0]
	for j in range(20):
		#z[i][j]=float(lines[2][j])/(1-10**lines[3][j])
		z[i][j]=float(lines[2][j])/(1-float(10**lines[3][j])/runsim)

		#z[i][j+i]=float(lines[2][j])/(1-10**lines[3][j])
		#z[j+i][i]=z[i][j+i]
		
for i in range(start,end):
	for  j in range(20):
		
		if p1[i]>p2[j]:
			theory[i][j]=2*h(p1[i])+h(p2[j])
		else:
			theory[i][j]=2*h(p2[j])+h(p1[i])
			

#print z
#surf1 = ax.plot_wireframe(p1m,p2m,z,color="green",label="General")
print lines[0]
plt.plot(p2,z[start],label="General,$p_1=$"+str(lines[0]),color="blue",marker="^")
plt.plot(p2,theory[start],label="Theory Sum Capacity,$p_1=$"+str(lines[0]),color="black",marker=">")
plt.ylabel('$\l(p)$')
plt.xlabel('flipover probability $p_2$')
plt.title("$X-p_1-Y-p_2-Z$,\n $t$="+str(t)+", $n$="+str(N))
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)


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


plt.plot(p2,compA,label="l for A")
plt.plot(p2,compB,label="l for B")
plt.plot(p2,compC,label="l for C")
plt.plot(p2,compSum,label="sum l")
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)

print len(err_Y2X)
print len(err_Z2X)
ax=plt.subplot(212)
#plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
#plt.plot(p2,[10**lines[3][j] for j in range(20)],'ro-',label="total error")
plt.plot(p2,[float(10**lines[3][j])/runsim for j in range(20)],'ro-',label="total error")

plt.plot(p2,err_Y2X,label="Y at X")
plt.plot(p2,err_Z2X,label="Z at X")
plt.plot(p2,err_X2Y,label="X at Y")
plt.plot(p2,err_Z2Y,label="Z at Y")
plt.plot(p2,err_X2Z,label="X at Z")
plt.plot(p2,err_Y2Z,label="Y at Z")
#plt.plot(p2,comp)
plt.xlabel('flipover probability $p_2$')
plt.ylabel('error')




"""
#----surface plot
fig = plt.figure()
ax = fig.gca(projection='3d')
p1=list(np.linspace(0.01,0.2,10))[:8]
p2=list(np.linspace(0.01,0.2,10))[:8]
p1m,p2m=np.meshgrid(p1,p2)
#print p1
#print p2

(w,x,y,s)=(8,9,10,11)
z=np.zeros([8,8])
theory=np.zeros([8,8])

for i in range(8):
	thisfile=files[9-i]
	print thisfile
	lines=ml.getline(thisfile,[w,x,y,s])
	point=len(lines[1])
	print lines[0]
	#p2=lines[1]
	#p1=lines[0]
	for j in range(8):
		z[i][j]=float(lines[2][j])/(1-10**lines[3][j])
		#z[i][j+i]=float(lines[2][j])/(1-10**lines[3][j])
		#z[j+i][i]=z[i][j+i]
		
#print z
surf1 = ax.plot_wireframe(p1m,p2m,z,color="green",label="General")


#----surface plot known

p1=list(np.linspace(0.01,0.2,20))[:16]
p2=list(np.linspace(0.01,0.2,20))[:16]
p1m,p2m=np.meshgrid(p1,p2)
#print p1
#print p2

(w,x,y,s)=(8,9,10,11)
z=np.zeros([16,16])
theory=np.zeros([16,16])
for i in range(16):
	thisfile=files2[i]
	print thisfile
	lines=ml.getline(thisfile,[w,x,y,s])
	point=len(lines[1])
	print point
	print lines[0]
	#p2=lines[1]
	#p1=lines[0]
	for j in range(point -4):
		#z[i][j]=float(lines[2][j])/(1-10**lines[3][j])
		z[i][j+i]=float(lines[2][j])/(1-10**lines[3][j])
		z[j+i][i]=z[i][j+i]
		
for i in range(16):
	for  j in range(16):
		
		if p1[i]>p2[j]:
			theory[i][j]=2*h(p1[i])+h(p2[j])
		else:
			theory[i][j]=2*h(p2[j])+h(p1[i])

surf2 = ax.plot_wireframe(p1m,p2m,z,color='blue',label="Order known")
surf3 = ax.plot_wireframe(p1m,p2m,theory,color='red',label="Theory")

plt.title("$X-p_1-Y-p_2-Z$, $t=9, $n$=512, $\delta$=0.05 ")
#plt.zlabel('$\l(p)$')
plt.xlabel('flipover probability $p_1$')
plt.ylabel('flipover probability $p_2$')
"""
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)
#plt.legend(loc='best')
plt.show()
