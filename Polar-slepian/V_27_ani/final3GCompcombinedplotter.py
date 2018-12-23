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

#unknown order
files=['/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_10_246in512_T9_18-10-13_04-55-08.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_9_246in512_T9_18-10-13_03-06-56.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_8_246in512_T9_18-10-13_01-25-38.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_7_246in512_T9_18-10-12_23-47-47.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_6_246in512_T9_18-10-11_23-19-03.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_5_246in512_T9_18-10-11_21-52-55.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_4_246in512_T9_18-10-11_20-35-03.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_3_246in512_T9_18-10-11_19-20-42.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_2_246in512_T9_18-10-11_18-08-44.txt',
'/home/smart/Project/code/Polar-slepian/V_27/simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_1_246in512_T9_18-10-11_16-57-14.txt']
#unknown order 2
files3=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_7_246in512_T9_18-10-14_11-05-34.txt',
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_8_246in512_T9_18-10-14_13-23-58.txt',
  './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_9_246in512_T9_18-10-14_15-44-04.txt',
   './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_10_246in512_T9_18-10-14_18-06-01.txt',
    './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_11_246in512_T9_18-10-14_20-29-54.txt',
     './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_12_246in512_T9_18-10-14_22-55-43.txt', 
     './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_13_246in512_T9_18-10-15_01-24-37.txt', 
     './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_14_246in512_T9_18-10-15_03-57-18.txt',
      './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_15_246in512_T9_18-10-15_06-35-50.txt',
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_16_246in512_T9_18-10-15_09-22-33.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_17_246in512_T9_18-10-15_12-16-43.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_18_246in512_T9_18-10-15_15-16-24.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_19_246in512_T9_18-10-15_18-19-56.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_20_246in512_T9_18-10-15_21-25-05.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_21_246in512_T9_18-10-16_00-32-14.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_22_246in512_T9_18-10-16_03-42-47.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_23_246in512_T9_18-10-16_06-57-56.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_24_246in512_T9_18-10-16_10-19-47.txt', 
       './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_25_246in512_T9_18-10-16_13-47-32.txt',
        './simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_26_246in512_T9_18-10-16_17-21-05.txt']


#Known order
files2=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_1_246in512_T9_18-09-13_18-49-17.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_2_246in512_T9_18-09-13_20-32-12.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_3_246in512_T9_18-09-13_22-11-34.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_4_246in512_T9_18-09-13_23-47-22.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_5_246in512_T9_18-09-14_01-17-25.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_6_246in512_T9_18-09-14_02-41-42.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_7_246in512_T9_18-09-14_04-01-30.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_8_246in512_T9_18-09-14_05-16-47.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_9_246in512_T9_18-09-14_06-27-18.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_10_246in512_T9_18-09-14_07-33-01.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_11_246in512_T9_18-09-14_08-33-38.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_12_246in512_T9_18-09-14_09-28-53.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_13_246in512_T9_18-09-14_10-19-40.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_14_246in512_T9_18-09-14_11-04-55.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_15_246in512_T9_18-09-14_11-44-50.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_16_246in512_T9_18-09-14_12-19-30.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_17_246in512_T9_18-09-14_12-48-34.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_18_246in512_T9_18-09-14_13-11-56.txt',\
 './simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_19_246in512_T9_18-09-14_13-29-38.txt', \
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_20_246in512_T9_18-09-14_13-41-32.txt']

#print files
N=1024
T=64
files3=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_7_512in1024_T64_18-10-22_22-03-48.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_8_512in1024_T64_18-10-23_03-49-50.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_9_512in1024_T64_18-10-23_11-20-52.txt']
N=1024
T=128
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_7_512in1024_T128_18-10-22_22-04-10.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_8_512in1024_T128_18-10-23_03-53-46.txt', 
'./simresults/polarfile_FERvsR_rateless_Det_Iter_retro3G_NB_9_512in1024_T128_18-10-23_11-29-08.txt']


#==============================================================================Benchmark
#~ #================================512vs FR 
#-------------------------plot
"""
fig=plt.figure()
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
N=512
c=0
m=["o","^",">"]
(w,x,y,z)=(8,9,10,11)
for thisfile in files:
	lines=ml.getline(thisfile,[w,x,y,z])
	point=len(lines[1])
	p2=lines[1]
	p1=lines[0]
	c+=1
	plt.plot(p2,[float(lines[2][i])/(1-10**lines[3][i]) for i in range(point) ],color=(np.random.rand(1)[0], np.random.rand(1)[0], np.random.rand(1)[0]),marker=m[c%3],\
	 label="$p_1$="+str(lines[0]))


plt.ylabel('$\l(p)$')
plt.xlabel('flipover probability $p_2$')
plt.xlim([0.01,0.2])
#plt.ylim([0.15,0.9])
plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)
plt.title("$X-p_1-Y-p_2-Z$,\n $p_1 \leq p_2$, $t$=9, $n$=512, $\delta$=0.05 ")
"""
"""
#----given p_1
fig = plt.figure()
#ax = fig.gca(projection='3d')
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.8,left=0.09)
p1=list(np.linspace(0.01,0.2,10))[:8]
p2=list(np.linspace(0.01,0.2,10))[:8]
p1m,p2m=np.meshgrid(p1,p2)
#print p1
#print p2
(w,x,y,s)=(8,9,10,11)
z=np.zeros([8,8])
theory=np.zeros([8,8])
start=4
end=5
for i in range(start,end):
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
		
for i in range(start,end):
	for  j in range(8):
		
		if p1[i]>p2[j]:
			theory[i][j]=2*h(p1[i])+h(p2[j])
		else:
			theory[i][j]=2*h(p2[j])+h(p1[i])
	

#print z
#surf1 = ax.plot_wireframe(p1m,p2m,z,color="green",label="General")
plt.plot(p2,z[start],label="General,$p_1=$"+str(lines[0]),color="blue",marker="^")
plt.plot(p2,theory[start],label="Sum Capacity,$p_1=$"+str(lines[0]),color="black",marker=">")
"""
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

plt.title("$X-p_1-Y-p_2-Z$, $t$=9, $n$=512, $\delta$=0.05 ")
#plt.zlabel('$\l(p)$')
plt.xlabel('flipover probability $p_1$')
plt.ylabel('flipover probability $p_2$')

plt.grid(True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)
#plt.legend(loc='best')
plt.show()
"""