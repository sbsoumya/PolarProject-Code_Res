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

files=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro_NB_1_246in512_T9_18-09-13_18-49-17.txt',\
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

#----surface plot
fig = plt.figure()
ax = fig.gca(projection='3d')
p1=list(np.linspace(0.01,0.2,20))
p2=list(np.linspace(0.01,0.2,20))
p1m,p2m=np.meshgrid(p1,p2)
#print p1
#print p2

(w,x,y,s)=(8,9,10,11)
z=np.zeros([20,20])
theory=np.zeros([20,20])
for i in range(20):
	thisfile=files[i]
	print thisfile
	lines=ml.getline(thisfile,[w,x,y,s])
	point=len(lines[1])
	#p2=lines[1]
	#p1=lines[0]
	for j in range(point):
		#z[i][j]=float(lines[2][j])/(1-10**lines[3][j])
		z[i][j+i]=float(lines[2][j])/(1-10**lines[3][j])
		z[j+i][i]=z[i][j+i]
		
for i in range(20):
	for  j in range(20):
		
		if p1[i]>p2[j]:
			theory[i][j]=2*h(p1[i])+h(p2[j])
		else:
			theory[i][j]=2*h(p2[j])+h(p1[i])
	

#print z
surf1 = ax.plot_surface(p1m,p2m,z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
surf2 = ax.plot_surface(p1m,p2m,theory, cmap=cm.coolwarm, linewidth=0, antialiased=True)



# Customize the z axis.
#ax.set_zlim(0, 4)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#surf(p1,'FaceColor','interp')

# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.title("$X-p_1-Y-p_2-Z$,\n $p_1 \leq p_2$, $t$=9, $n$=512, $\delta$=0.05 ")
#plt.zlabel('$\l(p)$')
plt.xlabel('flipover probability $p_1$')
plt.ylabel('flipover probability $p_2$')
plt.show()
