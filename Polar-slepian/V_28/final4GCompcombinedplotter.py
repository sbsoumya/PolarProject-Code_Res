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

#4G
#MC1
"""
files5=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_MC1_1_246in512_T9_19-01-03_22-34-32.txt']


"""

#Tree
#[[3.187757812499985, 3.290859374999999, 3.30259375, 3.3347109375000095, 3.338242187500015, 3.3743437500000306, 3.3696953125000375, 3.365187500000039, 3.3550234375000434, 3.383257812500045, 3.356179687500045, 3.347273437500051, 3.343351562500049, 3.3550312500000485, 3.338539062500051, 3.3695390625000456, 3.3710703125000494, 3.3672968750000463, 3.3564296875000483, 3.3540078125000496]]
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_Tree_1_246in512_T50_19-01-05_12-01-56.txt']
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_Tree_1_246in512_T50_19-01-05_19-24-04.txt']
N=512
t=50

"""
#MC2
#[[3.374218750000034, 3.38678125000004, 3.374414062500037, 3.3561953125000445, 3.3741875000000454, 3.3686171875000475, 3.3906328125000464, 3.359882812500048, 3.3686484375000463, 3.395367187500046, 3.3692187500000483, 3.3657343750000464, 3.3788750000000447, 3.368789062500049, 3.376554687500051, 3.3814062500000497, 3.3848906250000454, 3.3919453125000496, 3.3874921875000488, 3.404804687500047]]
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_MC2_1_246in512_T50_19-01-05_12-33-07.txt']
N=512
t=50
"""
"""
#MC1
#[[3.4052812500000336, 3.378984375000036, 3.3744140625000423, 3.378531250000044, 3.360085937500047, 3.3724609375000445, 3.3675078125000457, 3.3606718750000493, 3.393578125000045, 3.377937500000051, 3.3856718750000483, 3.390546875000048, 3.3786796875000493, 3.4064375000000484, 3.395718750000048, 3.4007734375000487, 3.405046875000043, 3.425281250000048, 3.413953125000047, 3.401304687500048]]
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_MC_1_246in512_T50_19-01-05_12-08-06.txt']
files4=['./simresults/polarfile_FERvsR_rateless_Det_Iter_retro4G_NB_MC1_1_256in512_T50_19-01-06_17-03-28.txt']
#special
N=512
t=50
"""

#==============================================================================Benchmark

#----given p_1
fig = plt.figure()
ax=plt.subplot(111)
plt.subplots_adjust(top=0.95,bottom=0.2,right=0.85,left=0.08)
# COMPRESSION PLOTS-----------------------------

(w,x,y)=(8,9,12)
z=np.zeros([20])
theory=np.zeros([20])

usefile=0

thisfile=files4[usefile]
print thisfile
lines=ml.getline(thisfile,[w,x,y])
p0=lines[0][0]
p1=lines[0][1]
p2=lines[1]
Empirical=lines[2]
point=len(p2)

for  j in range(20):
	theory[j]=2*(max(h(p2[j]),h(p0)))+min(h(p0),h(p2[j]))+h(p1)	



plt.plot(p2,Empirical,label="RB-PDE",color="green", marker="^")
plt.plot(p2,theory,label="Theoretical",color="black",marker=">")
plt.ylabel("$\l(p',p'',p''')$")
plt.xlabel("flipover probability $p'''$")
plt.ylim(0,4)
plt.title("4-party MC $p_0 < p_1 < p_2$,\n $t$="+str(t)+", $n$="+str(N)+", $p_0=$"+str(p0)+", $p_1=$"+str(p1))
plt.grid(True)

plt.grid(True)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),columnspacing=0.1,handletextpad =0.1,numpoints=1)
plt.show()

