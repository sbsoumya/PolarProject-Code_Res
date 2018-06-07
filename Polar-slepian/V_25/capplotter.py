#--------------------------------------------
# Name:       capplotter.py
# Purpose:    plotter for capacity and achieved rate
#
# Author:      soumya
#
# Created:     19/08/2017
#----------------------------------------

import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#-------------------------------------------Capacity 
p=[0.04,0.15,0.2,0.25]
Cap=[pl.CapacityBSC(1,i) for i in p]
reln1=[0.592051,0.24815,0.167721,0.108925]
reln1LTPT=[0.596488,0.199893,0.128894,0.0739803]
#reln1KRX=[0.59,0.190323,0.117742]


#--------------nonRateless
#~ #0.2
#~ r3=[0.02734375, 0.0546875, 0.0830078125, 0.1103515625, 0.138671875, 0.166015625, 0.1943359375, 0.2216796875, 0.25, 0.27734375]
#~ e3=[float("inf"), float("inf"), float("inf"), -2.886056647693163, -1.6575773191777938, -0.9867413347164835, -0.4487940562520938, -0.18889439298206961, -0.05070759858797432, -0.00718147993332044]
#~ #0.04
#~ r1=[0.0751953125, 0.1513671875, 0.2265625, 0.302734375, 0.3779296875, 0.4541015625, 0.5302734375, 0.60546875, 0.681640625, 0.7568359375]
#~ e1=[float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), -3.5228787452803374, -1.5044556624535514, -0.5705707356182124, -0.08788427092114617, -0.0012612837441822772]
#~ #0.15
#~ r2=[0.0380859375, 0.0771484375, 0.1162109375, 0.1552734375, 0.1943359375, 0.2333984375, 0.2724609375, 0.3115234375, 0.3505859375, 0.3896484375]
#~ e2=[float("inf"), float("inf"), float("inf"), -4.0, -2.1191864077192086, -1.1944991418415998, -0.5775743236287953, -0.21070138884055886, -0.04662694927330402, -0.0039263455147246756]
#~ #0.25
#~ r4=[0.0185546875, 0.037109375, 0.0556640625, 0.0751953125, 0.09375, 0.1123046875, 0.1318359375, 0.150390625, 0.1689453125, 0.1884765625]
#~ e4=[float("inf"), float("inf"), -4.0, -2.309803919971486, -1.469800301796918, -0.8579235389267152, -0.401100112936117, -0.18555262147751236, -0.06003170944866383, -0.01202108412451794]

#0.04
r1=[0.0751953125, 0.1513671875, 0.2265625, 0.302734375, 0.3779296875, 0.4541015625, 0.5302734375, 0.60546875, 0.681640625, 0.7568359375]
e1=[-float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -3.958607314841775, -2.026410376572743, -0.7622803680037463, -0.1366771398795441, -0.0026354619510352293]
#0.25
r4=[0.01887218755408672, 0.037744375108173439, 0.056616562662260159, 0.075488750216346878, 0.094360937770433584, 0.11323312532452029, 0.13210531287860702, 0.15097750043269376, 0.16984968798678046, 0.18872187554086717]
e4=[-float("inf"), -float("inf"), -4.301029995663981, -2.3467874862246565, -1.4934949675951281, -0.8583307830337908, -0.4074568570953883, -0.18509346953361394, -0.05966783050214782, -0.012794188254436508]
#0.15
r2=[0.039015969528359964, 0.078031939056719929, 0.11704790858507991, 0.15606387811343986, 0.19507984764179981, 0.23409581717015976, 0.27311178669851977, 0.31212775622687972, 0.35114372575523967, 0.39015969528359962]
e2=[-float("inf"), -float("inf"), -float("inf"), -3.657577319177794, -2.1319436381769585, -1.1996954224438015, -0.5772952826232076, -0.2111813814904237, -0.044966829666105754, -0.004250763240366621]
#0.2
r3=[0.02780719051126377, 0.05561438102252754, 0.083421571533791317, 0.11122876204505508, 0.13903595255631884, 0.16684314306758261, 0.1946503335788464, 0.22245752409011016, 0.25026471460137395, 0.27807190511263769]
e3=[-float("inf"), -float("inf"), -4.698970004336019, -3.065501548756432, -1.687188173787912, -1.0047158923107404, -0.4508863381561614, -0.19178227293728894, -0.04646258478471957, -0.006427109494063763]




#----------------------------LTPT
#-channel
#~ #0.2
#~ a3=[0.07031249999998743, 0.13694765624997643, 0.13333769531248768, 0.14180175781249074, 0.16254375000000532, 0.16621660156246945, 0.17002001953123919, 0.17198554687497855, 0.19129238281251879, 0.2360437500000312]
#~ ae3=[-3.3010299956639813, -0.7599502278873523, -0.8847224086040987, -0.272214825817094, -0.1993516446360119, -0.08841629901892423, -0.06288348923294615, -0.01399006814673879, -0.002045995930597039, -0.0019151120634443696]
#~ #0.04
#~ a1=[0.07031249999998743, 0.14062499999997485, 0.2226562499999607, 0.29296874999996964, 0.37500000000006006, 0.4453124999999214, 0.5273437499998724, 0.5975964843749434, 0.6772406250000327, 0.7260375000001107]
#~ ae1=[float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), float("inf"), -2.161150909262745, -0.9854794612420763, -0.14709324120304632, -0.031517051446064856]
#~ #0.15
#~ a2=[0.07031249999998743, 0.14062499999997485, 0.21833671874996463, 0.22744628906247896, 0.19683750000003075, 0.2215874999999609, 0.2540830078124453, 0.2615742187499732, 0.2597935546875008, 0.29204999999998343]
#~ ae2=[float("inf"), -2.9208187539523753, -0.9476909003526766, -0.47833898488792664, -0.8982529260536337, -0.5647928967592525, -0.20307892466983124, -0.16001944232165735, -0.2487979054116469, -0.15995666939650605]
#~ #0.25
#~ a4=[0.06921562499998792, 0.08343632812498741, 0.10488964843748128, 0.09949707031250928, 0.11111562500000455, 0.11368457031247926, 0.13253466796871846, 0.1503055664062357, 0.17589746093751077, 0.2254375000000402]
#~ ae4=[-1.1290111862394248, -0.5412111182891549, -0.22863302914221934, -0.24818221226312082, -0.07268097504034392, -0.0459022795208104, -0.00017375254558756316, 0.0, 0.0, 0.0]
#file
#0.25
a3=[0.06933164062498791, 0.08272968749998756, 0.10421425781248213, 0.09899169921875837, 0.11069062500000452, 0.11384414062497913, 0.13269287109371858, 0.15018603515623563, 0.17672441406251155, 0.22366875000004027]
ae3=[-1.1301817920206718, -0.6761293934594911, -0.4899914870597653, -0.6167233495923496, -0.2926853664112919, -0.32532253212680107, -0.04527520902093701, -0.004891542255259376, -0.0008694587126288915, -0.00047798687109621183]
#0.2
a4=[0.07031249999998743, 0.13663828124997662, 0.13403906249998773, 0.14203124999999042, 0.1621250000000052, 0.16408281249997184, 0.1693520507812378, 0.17243876953122853, 0.1909751953125187, 0.23479375000003136]
ae4=[-2.8239087409443187, -0.7574585717016158, -0.8904214530956133, -0.5198492747267196, -0.42887372291568837, -0.3347005005001029, -0.2892059000696726, -0.20398103065285073, -0.10957898119908571, -0.08708744882390304]
#0.15
a2=[0.07031249999998743, 0.14062499999997485, 0.21826992187496458, 0.22516113281247882, 0.19663750000003116, 0.22177304687496097, 0.2543598632811953, 0.2608769531249733, 0.2591025390625021, 0.29338749999998404]
ae2=[-float("inf"), -2.853871964321762, -0.906578314837765, -0.4925489390980302, -1.0589857562944303, -0.8434508486682187, -0.44225225835853177, -0.31131327571587647, -0.45444549276593504, -0.40660315769979327]
#0.04
a1=[0.07031249999998743, 0.14062499999997485, 0.2226562499999607, 0.29296874999996964, 0.37500000000006006, 0.4453124999999214, 0.5273437499998724, 0.5975367187499434, 0.6774785156250325, 0.72513750000011]
ae1=[-float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -4.0, -2.0969100130080562, -0.9838026464875609, -0.14935376481693347, -0.03306083697888694]


#-----------------------------KRX
#~ #0.2
#~ k3=[0.0234375, 0.046875, 0.07421875, 0.09765625, 0.125, 0.1484375, 0.17578125, 0.19921875, 0.2265625, 0.25]
#~ ke3=[-float("inf"), -float("inf"), -2.4814860601221125, -1.8096683018297086, -0.5846927077744326, -0.06833876031551878, -0.012199714248127573, -0.0030070181092943012, -0.00034757463392091225, 0.0]
#~ #0.04
#~ k1=[0.0703125, 0.140625, 0.22265625, 0.29296875, 0.375, 0.4453125, 0.52734375, 0.59765625, 0.6796875, 0.75]
#~ ke1=[-float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -float("inf"), -2.0915149811213505, -0.9484616094846725, -0.14953756723848344, -0.003882523862711993]
#~ #0.15
#~ k2=[0.03515625, 0.0703125, 0.111328125, 0.146484375, 0.1875, 0.22265625, 0.263671875, 0.298828125, 0.33984375, 0.375]
#~ ke2=[-float("inf"), -float("inf"), -float("inf"), -1.8860566476931633, -1.0376306643299789, -0.5554867936659571, -0.15552282425431863, -0.01542768437836777, -0.0002172015458642319, 0.0]
#~ #0.25
#~ k4=[0.017578125, 0.03515625, 0.0556640625, 0.0732421875, 0.09375, 0.111328125, 0.1318359375, 0.1494140625, 0.169921875, 0.1875]
#~ ke4=[-float("inf"), -float("inf"), -0.45321064836874186, -0.4443011052810986, -0.23269568254672676, -0.04744970610179836, -8.686758342857122e-05, 0.0, 0.0, 0.0]

#~ plt.plot(k3,ke3,k1,ke1,k2,ke2,k4,ke4)
#~ plt.subplot(2,1,1)
#~ plt.plot(a3,ae3,a1,ae1,a2,ae2,a4,ae4)
#~ plt.grid(True)
#~ plt.subplot(2,1,2)
#~ plt.plot(r3,e3,r1,e1,r2,e2,r4,e4)

plt.plot(p,Cap,'b-o',label="Capacity")#
plt.plot(p,reln1,'g-o',label="Polar Code, $10^{-1}$ FER")
plt.plot(p,reln1LTPT,'r-o',label="In-Frz with PHY-ED, $10^{-1}$ FER")
#plt.plot(p[:3],reln1KRX,'k-o',label="KRX")
plt.legend(loc="best")
plt.xlabel('flipover probability p')
plt.ylabel('Rate')
plt.title("Rateloss in SW compression with In-Frz and PHY-ED, N=1024")
plt.grid(True)
plt.show()

#to be automated

#~ filename1="./simresults/polarchannel_FERvsR_derate1024_0.04_17-11-02_17-21-53.txt"
#~ filename3="./simresults/polarchannel_FERvsR_derate_rateless_LTPT1024_0.04_17-11-07_10-10-56.txt"



#~ table = []
#~ with open(filename1,'r') as f:
    #~ for line in f:
        #~ table.append(json.loads(line))

#~ #for row in table:
#~ #	print(row)


#~ table2 = []
#~ with open(filename2,'r') as f:
    #~ for line in f:
        #~ table2.append(json.loads(line))
        
#~ table3 = []
#~ with open(filename3,'r') as f:
    #~ for line in f:
        #~ table3.append(json.loads(line))


#~ plt.subplot(2,1,1)
#~ plt.semilogy(table[7],[10**i for i in table[8]],'r',label="Channel_p=design_p")
#~ #plt.semilogy(table2[8],[10**i for i in table2[9]],'b',label="channel_p>design_p = 0.04")
#~ plt.semilogy(table3[10],[10**i for i in table3[12]],'g',label="Rateless LTPT")
#~ plt.xlabel('sent Rate')
#~ plt.ylabel('Frame Error rate.')
#~ plt.title('FER vs Rate Rateless LTPT design \nN=1024,Capacity='+str()+",channel_p="+str("0.04"))
#~ plt.legend(loc="best")
#~ plt.grid(True)

#~ plt.figtext(0.005, 0.03, "Compound Channel=[0.04,0.15,0.2,0.25]\n"+filename1+"\n"+filename3)

#~ plt.subplot(2,1,2)
#~ print table3[10]
#~ print table3[11]
#~ plt.plot(table3[10],table3[11])
#~ plt.title("Sent rate vs achieved rate")
#~ plt.xlabel('Sent Rate')
#~ plt.ylabel('Achieved Rate')
#plt.grid(True)


plt.show()

#------------------------------------------------------------------	