#--------------------------------------------
# Name:       plotter.py
# Purpose:    Generic plotter
#
# Author:      soumya
#
# Created:     19/08/2017
#----------------------------------------

import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import matlib as ml

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


#-------------------------------------------polar_channel_FERvsR

#to be automated

#files for derate channel=design
#~ filename0="../V_12/simresults/polarchannel_FERvsR_derate1024_0.04_17-12-27_16-43-37.txt"
#~ filename0="../V_12/simresults/polarchannel_FERvsR_derate1024_0.04_17-11-02_17-21-53.txt"
#~ filename1="../V_12/simresults/polarchannel_FERvsR_derate1024_0.15_17-11-02_20-00-43.txt"
#~ filename2="../V_12/simresults/polarchannel_FERvsR_derate1024_0.2_17-11-02_22-39-12.txt"
#~ filename3="../V_12/simresults/polarchannel_FERvsR_derate1024_0.25_17-11-03_01-18-37.txt"


#files for det
#~ #filename3="./Det-0p04.txt"
S_r1=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r1=[0.0390624999999996, 0.09765625000001392, 0.14453124999998804, 0.19140624999997566, 0.23828125000006578, 0.28515625000002565, 0.33203124999995987, 0.3906250000000557, 0.4374671875000589, 0.48346679687498345, 0.5242374999999059]
FER1=[-float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -4.0, -3.2218487496163566, -2.9208187539523753]

#filename3="./Det-0p15.txt"
S_r2=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r2=[0.039062499999961066, 0.09765625000011077, 0.13994888671868472, 0.17317480468747914, 0.17373681640628544, 0.10435768229167539, 0.08954882812498975, 0.0983235677083474, 0.10971041666668142, 0.12158216145832909, 0.13331276041664292]
FER2=[-float("inf"), -float("inf"), -3.3979400086720375, -3.3979400086720375, -2.2518119729937998, -1.7721132953863266, -2.958607314841775, -3.3979400086720375, -3.154901959985743, -2.769551078621726, -2.207608310501746]
#filename3="./Det-0p2.txt"
S_r3=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r3=[0.03903710937499962, 0.09640966796885206, 0.07169472656249883, 0.06672740885416338, 0.061283951822933454, 0.07131995442708976, 0.0830354817708233, 0.09771158854168059, 0.10940416666668139, 0.12111796874999575, 0.13283463541664278]
FER3=[-float("inf"), -4.301029995663981, -2.2924298239020637, -2.3979400086720375, -2.309803919971486, -2.3767507096020997, -1.7033348097384688, -1.489454989793388, -1.2612194415156308, -0.4409316659654632, -0.23128791962233644]

#filename3="./Det-0p25.txt"
S_r4=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r4=[0.036045898437471755, 0.058646647135410374, 0.03651582031249728, 0.04788505859374391, 0.059570312500016445, 0.07129143880208975, 0.08300781249998997, 0.09765625000001392, 0.10938229166668141, 0.12109374999999577, 0.1328124999999761]
FER4=[-5, -2.657577319177794, -2.2676062401770314, -0.4463596637686458, -0.44830608487277523, -0.4592952166892377, -0.2522775379644916, -0.08682216600953196, -0.03067729388779786, -0.0006084382809090492, -4.3431619807505604e-05]

#det iter retro
#0.04
S_r12=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r12=[0.0390624999999996, 0.09765625000001392, 0.14453124999998804, 0.19140624999997566, 0.23828125000006578, 0.28515625000002565, 0.33203124999995987, 0.3906250000000557, 0.43743437500005894, 0.48362421874998357, 0.5266015624999054]
FER12=[-float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -2.958607314841775]
#0.15
S_r22=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r22=[0.0390624999999996, 0.09765625000001392, 0.1412720703124868, 0.1787447265624828, 0.19336920572921457, 0.16230143229168117, 0.16541796874998516, 0.18608398437501644, 0.19661614583336295, 0.19622434895834215, 0.18994843750000995]
FER22=[-float("inf"), -float("inf"), -3.6989700043360187, -3.5228787452803374, -2.207608310501746, -1.7695510786217261, -2.3872161432802645, -2.337242168318426, -2.0861861476162833, -1.6595558851598817, -1.595166283380062]
#0.2
S_r32=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r32=[0.039042968749999615, 0.09682942708334653, 0.09475589192708198, 0.10742037760415353, 0.10678574218751909, 0.10504680989583197, 0.11507926432293938, 0.11692382812501542, 0.11332708333334564, 0.12230872395832863, 0.133755468749977]
FER32=[-float("inf"), -4.0, -2.3979400086720375, -2.5528419686577806, -2.008773924307505, -1.9665762445130504, -1.7904849854573692, -1.4400933749638876, -1.2358238676096693, -0.4375881670502726, -0.2289272167788052]
#0.25
S_r42=[0.0390625, 0.09765625, 0.14453125, 0.19140625, 0.23828125, 0.28515625, 0.33203125, 0.390625, 0.4375, 0.484375, 0.53125]
A_r42=[0.036966796875000645, 0.06905110677083275, 0.06537991536457549, 0.07354944661457673, 0.0707953450520921, 0.07964651692708911, 0.08574983723957566, 0.09767252604168059, 0.10937500000001474, 0.12109374999999577, 0.1328124999999761]
FER42=[-float("inf"), -2.537602002101044, -2.3979400086720375, -0.6397853867046477, -0.5295895090240693, -0.4983930775811706, -0.2664817485655124, -0.08496970974083916, -0.0318440628500295, -0.0003910410285829482, -8.686758342857122e-05]






p=[0.04,0.15,0.2,0.25]


#~ table0 = []
#~ with open(filename0,'r') as f:
    #~ for line in f:
        #~ table0.append(json.loads(line))
#~ plt.semilogy(table0[7],[10**i for i in table0[8]],'k-o',label="Polar Code for p="+str(p[0]))
#~ table0 = []
#~ with open(filename1,'r') as f:
    #~ for line in f:
        #~ table0.append(json.loads(line))
#~ plt.semilogy(table0[7],[10**i for i in table0[8]],'k-o',label="Polar Code for p="+str(p[1]))
#~ table0 = []
#~ with open(filename2,'r') as f:
    #~ for line in f:
        #~ table0.append(json.loads(line))
#~ plt.semilogy(table0[7],[10**i for i in table0[8]],'k-o',label="Polar Code for p="+str(p[2]))
#~ table0 = []
#~ with open(filename3,'r') as f:
    #~ for line in f:
        #~ table0.append(json.loads(line))
#~ plt.semilogy(table0[7],[10**i for i in table0[8]],'k-o',label="Polar Code for p="+str(p[3]))



#~ plt.semilogy(S_r1,[10**i for i in FER1],'g-o',label="Inc-Frz with PHY-ED$^{*}$")
#~ plt.semilogy(S_r2,[10**i for i in FER2],'b-o',label="Inc-Frz with PHY-ED$^{*}$")
#~ plt.semilogy(S_r3,[10**i for i in FER3],'r-o',label="Inc-Frz with PHY-ED$^{*}$")
#~ plt.semilogy(S_r32,[10**i for i in FER32],'y-o',label="Inc-Frz with PHY-ED$^{*}$")

#achieved rate comparisons
#~ plt.plot(S_r1,A_r2,marker="o")
#~ plt.plot(S_r1,A_r22)
#~ plt.plot(S_r1,A_r3,marker="o")
#~ plt.plot(S_r1,A_r32)
#~ plt.xlabel('Initial Rate')
#~ plt.ylabel('Frame Error rate.')
#~ plt.title('FER vs Rate for Error control coding \nN=1024,p='+str(p[1])+',Capacity='+str(pl.CapacityBSC(1,p[1])))
#~ plt.legend(loc="best")
#~ plt.grid(True)

#~ plt.figtext(0.005, 0.03, "$^{*}$Compound Channel=$\{$0.04,0.15,0.2,0.25$\}$")#+filename0+"\n"+filename3)


#~ msg_length=range(50,600,50)
#~ fig=plt.figure()
#~ fig.suptitle("N=1024,T=20")
#~ #plt.subplot(221)
#~ for i in range(5):
	#~ A_r_m=[A_r1[i],A_r2[i],A_r3[i],A_r4[i]]
	#~ A_r_mT=[A_r1[i]*(1-10**FER1[i]),A_r2[i]*(1-10**FER2[i]),A_r3[i]*(1-10**FER3[i]),A_r4[i]*(1-10**FER4[i])]
	#~ A_r_m2T=[A_r12[i]*(1-10**FER12[i]),A_r22[i]*(1-10**FER22[i]),A_r32[i]*(1-10**FER32[i]),A_r42[i]*(1-10**FER42[i])]
	#~ plt.plot(p,A_r_m,marker='o',label=str(msg_length[i])+"A_R")
	#~ plt.plot(p,A_r_mT,marker='+',label=str(msg_length[i])+"T")
	#~ plt.plot(p,A_r_m2T,marker='^',label=str(msg_length[i])+"T_retro")
	#~ plt.grid(True)
	#~ #plt.title("N=1024")
	#~ plt.ylabel('Achieved Rate')
	#~ plt.legend(loc="best")
	
#~ plt.subplot(222)
#~ for i in range(5):
	
	#~ Iter_m=[float(S_r1[i])/A_r1[i],float(S_r2[i])/A_r2[i],float(S_r3[i])/A_r3[i],float(S_r4[i])/A_r4[i]]	
	
	#~ plt.plot(p,Iter_m,marker='o',label=str(msg_length[i]))
	#~ plt.grid(True)
	#~ plt.ylabel('Iter')
	#~ #plt.legend(loc="best")

#~ plt.subplot(212)
#~ for i in range(5):
	#~ FER_m=[FER1[i],FER2[i],FER3[i],FER4[i]]
	#~ plt.semilogy(p,[10**j for j in FER_m],marker='o',label=str(msg_length[i]))
	#~ plt.figtext(0.005, 0.03, "$\{$0.04,0.15,0.2,0.25$\}$")#+filename0+"\n"+filename3)
	#~ plt.ylabel('FER')
	#~ plt.xlabel('p')
	#~ plt.legend(loc="upper left")
	#~ plt.grid(True)

#~ plt.savefig("./simresults/FERvsP"+"_Detbits1024_1.png", bbox_inches='tight')

#~ msg_length=range(50,600,50)

#~ fig=plt.figure()
#~ fig.suptitle("N=1024,T=20")
#~ plt.subplot(221)
#~ for i in range(5,11):
	
	#~ A_r_m=[A_r1[i]*(1-10**FER1[i]),A_r2[i]*(1-10**FER2[i]),A_r3[i]*(1-10**FER3[i]),A_r4[i]*(1-10**FER4[i])]
	
	#~ plt.plot(p,A_r_m,marker='o',label=str(msg_length[i]))
	#~ plt.grid(True)
	
	#~ plt.ylabel('Achieved Rate')
	#~ #plt.legend(loc="best")
#~ plt.subplot(222)
#~ for i in range(5,11):
	
	#~ Iter_m=[float(S_r1[i])/A_r1[i],float(S_r2[i])/A_r2[i],float(S_r3[i])/A_r3[i],float(S_r4[i])/A_r4[i]]	
	
	#~ plt.plot(p,Iter_m,marker='o',label=str(msg_length[i]))
	#~ plt.grid(True)
	#~ plt.ylabel('Iter')
	#~ #plt.legend(loc="best")

#~ plt.subplot(212)
#~ for i in range(5,11):
	#~ FER_m=[FER1[i],FER2[i],FER3[i],FER4[i]]
	#~ plt.semilogy(p,[10**j for j in FER_m],marker='o',label=str(msg_length[i]))
	#~ plt.figtext(0.005, 0.03, "$\{$0.04,0.15,0.2,0.25$\}$")#+filename0+"\n"+filename3)
	#~ plt.ylabel('FER')
	#~ plt.xlabel('p')
	#~ plt.legend(labelspacing = 1.0,loc="upper left",prop={'size':10})
	#~ plt.grid(True)

#~ plt.savefig("./simresults/FERvsP"+"_Detbits1024_2.png", bbox_inches='tight')
	
#~ plt.show()

#------------------------------------------------------------------	
msg_length=range(50,600,50)
fig=plt.figure()
fig.suptitle("N=1024,T=20,Iter-retro Throughput for varying initial code rate R.")
#plt.subplot(221)
for i in [2,4,6,8,10]:
	#A_r_m=[A_r1[i],A_r2[i],A_r3[i],A_r4[i]]
	#A_r_mT=[A_r1[i]*(1-10**FER1[i]),A_r2[i]*(1-10**FER2[i]),A_r3[i]*(1-10**FER3[i]),A_r4[i]*(1-10**FER4[i])]
	A_r_m2T=[A_r12[i]*(1-10**FER12[i]),A_r22[i]*(1-10**FER22[i]),A_r32[i]*(1-10**FER32[i]),A_r42[i]*(1-10**FER42[i])]
	#plt.plot(p,A_r_m,marker='o',label=str(msg_length[i])+"AR")
	#plt.plot(p,A_r_mT,marker='>',label=str(msg_length[i])+"T")
	plt.plot(p,A_r_m2T,marker='^',label="R="+str(float(msg_length[i])/1024))
	plt.grid(True)
	#plt.title("N=1024")
	plt.ylabel('Throughput=R*(1-FER)/E[Iterations]')
	plt.xlabel('BSC(p)')
	plt.legend(loc="best")
	
plt.savefig("./simresults/TPT_iterretro_Detbits1024.png", bbox_inches='tight')
	
#~ msg_length=range(50,600,50)
#~ fig=plt.figure()
#~ fig.suptitle("N=1024,T=20")
#~ #plt.subplot(221)
#~ for i in range(3,6):
	#~ A_r_m=[A_r1[i],A_r2[i],A_r3[i],A_r4[i]]
	#~ A_r_mT=[A_r1[i]*(1-10**FER1[i]),A_r2[i]*(1-10**FER2[i]),A_r3[i]*(1-10**FER3[i]),A_r4[i]*(1-10**FER4[i])]
	#~ A_r_m2T=[A_r12[i]*(1-10**FER12[i]),A_r22[i]*(1-10**FER22[i]),A_r32[i]*(1-10**FER32[i]),A_r42[i]*(1-10**FER42[i])]
	#~ plt.plot(p,A_r_m,marker='o',label=str(msg_length[i])+"AR")
	#~ plt.plot(p,A_r_mT,marker='>',label=str(msg_length[i])+"T")
	#~ plt.plot(p,A_r_m2T,marker='^',label=str(msg_length[i])+"Tretro")
	#~ plt.grid(True)
	#~ #plt.title("N=1024")
	#~ plt.ylabel('Achieved Rate')
	#~ plt.legend(loc="best")
	
#~ plt.savefig("./simresults/TPT_Detbits1024_2.png", bbox_inches='tight')
	
#~ msg_length=range(50,600,50)
#~ fig=plt.figure()
#~ fig.suptitle("N=1024,T=20")
#~ #plt.subplot(221)
#~ for i in range(6,9):
	#~ A_r_m=[A_r1[i],A_r2[i],A_r3[i],A_r4[i]]
	#~ A_r_mT=[A_r1[i]*(1-10**FER1[i]),A_r2[i]*(1-10**FER2[i]),A_r3[i]*(1-10**FER3[i]),A_r4[i]*(1-10**FER4[i])]
	#~ A_r_m2T=[A_r12[i]*(1-10**FER12[i]),A_r22[i]*(1-10**FER22[i]),A_r32[i]*(1-10**FER32[i]),A_r42[i]*(1-10**FER42[i])]
	#~ plt.plot(p,A_r_m,marker='o',label=str(msg_length[i])+"AR")
	#~ plt.plot(p,A_r_mT,marker='>',label=str(msg_length[i])+"T")
	#~ plt.plot(p,A_r_m2T,marker='^',label=str(msg_length[i])+"Tretro")
	#~ plt.grid(True)
	#~ #plt.title("N=1024")
	#~ plt.ylabel('Achieved Rate')
	#~ plt.legend(loc="best")
	
#~ plt.savefig("./simresults/TPT_Detbits1024_3.png", bbox_inches='tight')
	
#~ msg_length=range(50,600,50)
#~ fig=plt.figure()
#~ fig.suptitle("N=1024,T=20")
#~ #plt.subplot(221)
#~ for i in range(9,11):
	#~ A_r_m=[A_r1[i],A_r2[i],A_r3[i],A_r4[i]]
	#~ A_r_mT=[A_r1[i]*(1-10**FER1[i]),A_r2[i]*(1-10**FER2[i]),A_r3[i]*(1-10**FER3[i]),A_r4[i]*(1-10**FER4[i])]
	#~ A_r_m2T=[A_r12[i]*(1-10**FER12[i]),A_r22[i]*(1-10**FER22[i]),A_r32[i]*(1-10**FER32[i]),A_r42[i]*(1-10**FER42[i])]
	#~ #plt.plot(p,A_r_m,marker='o',label=str(msg_length[i])+"AR")
	#~ plt.plot(p,A_r_mT,marker='>',label=str(msg_length[i])+"T")
	#~ plt.plot(p,A_r_m2T,marker='^',label=str(msg_length[i])+"Tretro")
	#~ plt.grid(True)
	#~ #plt.title("N=1024")
	#~ plt.ylabel('Achieved Rate')
	#~ plt.legend(loc="best")
	
#~ plt.savefig("./simresults/TPT_Detbits1024_4.png", bbox_inches='tight')

plt.show()
