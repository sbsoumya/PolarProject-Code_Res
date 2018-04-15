#---------------------------------------------------
# Name:       thetafinder.py
# Purpose:    plotter to be used to find theta
#
#
# Author:      soumya
#
# Created:    27/10/2017
#---------------------------------------------


import matplotlib.pyplot as plt
import json
import numpy as np
import problib as pl
import pandas as pd
from scipy import stats, integrate
import polarconstruct as pcon
import lambdathreshold as lmb

#import seaborn as sns
#sns.set(color_codes=True)


plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#-------------------------------------------polar_channel_FERvsR

#to be automated

filename="./simresults/llrdict-1024-0p04-17-11-03_16-56-11.txt"
filename="./simresults/llrdict-1024-0p15-17-11-03_16-55-50.txt"
filename="./simresults/llrdict-1024-0p2-17-11-03_16-55-25.txt"

LLRdict=lmb.load_LLRdict(filename)
N=1024
design_p=0.2
runsim=1000
channel_plist=[0.2,0.25]
C=pl.CapacityBSC(N,design_p)
G=int(C)

#------------------------------------LT
#G=250
LT=float(np.log2(N)/N)
LT=30

#print LT
Fdict=lmb.perc_goodchannel_WD(LLRdict,channel_plist,N,LT,G,runsim)
PT=44
Ppercdict=lmb.PrOffracaboveFT(Fdict,channel_plist,PT,runsim)
#print Ppercdict

color=["green","yellow"]
plt.figure(1)
index= range(runsim)
j=1
for channel_p in channel_plist:
	j+=1
	plt.scatter(index,Fdict[str(channel_p)],color=color[j-2],label="p$_{channel}=$"+str(channel_p))
	
plt.legend(loc="best")
plt.title("Thresholds for PHY-ED \n $\lambda$="+str(LT)+",$\Theta$="+str(PT)+",p$_{guessed}$="+str(design_p))
plt.xlabel("Simulation number"+"\n"+"P($\Theta$ \% of goodchannels $\geq\lambda$)="+str(Ppercdict))
plt.grid(True)
plt.ylabel("\% of good channels with $|LLR| \geq \lambda$")

#plt.figtext(0.005, 0.03, "P("+str(PT)+"\% of goodchannels $\geq\lambda$)="+str(Ppercdict))#+"\n"+filename)

plt.show()

#----------------------------------------------------------LTvec
#~ LTvec2stdev=[1708.4676895006,834.4563615692,825.3459916051,814.0157768782,800.2125212369,778.3126956598,750.1824235046,717.5137365598,675.0405976315,645.6114740408,399.6949613433,394.111852504,388.4378959245,386.2060512909,381.8076109851,374.9575233376,374.6632525716,369.6130243142,361.6914722737,354.0573953743,361.542578544,355.6180630963,349.0440387824,339.0441283368,325.481164983,344.7902612802,338.2972851798,329.1298890414,320.143221501,306.6464341017,322.8499220286,316.3853143347,615.2213254848,306.3157238394,287.9345065111,297.0534311846,278.0520280365,257.3921243563,304.9210772513,297.5593576711,289.9251932669,185.515966319,181.8637160033,178.7514826448,276.472301254,175.4559891618,175.770398546,171.316893005,167.7351086451,167.2598201792,168.6710710988,164.2213804085,165.9677054966,161.8556838641,158.9239192438,260.4213672389,160.3844020371,156.9535276864,233.4590979347,153.3444826461,153.0356573903,160.2884305959,149.5889652277,155.2407409988,150.45543626,145.4727459821,150.119897589,146.8768678436,140.3755582104,140.1262569652,143.7136652117,139.6497868198,238.6444428082,133.7189565505,148.7338697929,287.8058853936,128.6819069247,143.2974633871,278.0099693295,133.952509539,139.1495797307,130.3205036942,139.0430458881,268.2621569218,135.2648387424,125.1346090106,130.1149332456,127.9754441108,255.4961183044,125.0446602342,118.0679655783,117.715279639,208.3303677211,113.5370281924,235.6694358238,118.8355479592,114.8980626879,109.235136834,137.2997845973,108.9246635226,133.5635530293,129.7700890933,125.7098788831,81.8521593665,121.8055611324,101.6799159575,77.4044899091,75.7395965291,117.8753348248,74.83715528,72.9876328636,117.3926647526,72.4057987352,70.647170423,113.5705909326,206.6234099847,106.3175870595,70.6126234979,102.8811488913,67.9160923086,68.8851458305,108.1549025979,69.0898685907,65.8558429065,90.2590736982,94.9157156975,67.1932867739,63.7762546583,63.4137474726,63.3515695805,175.9272596801,63.5407752577,61.0009489393,61.0807313449,107.6809130071,101.2193990265,60.1563579006,103.5842416416,89.2171658844,57.4761757716,58.8980857062,57.9853607479,125.5559822038,98.7860068031,62.7726158405,58.9523861065,55.4160951389,121.6005893728,61.3911238269,56.2372995898,116.1289273591,59.1557819726,52.9883262474,50.433818639,114.2898913811,183.0955071617,55.5594402303,56.8375600975,52.2778105059,89.9694534151,109.7940305794,51.7940358176,79.4016533812,49.8928933331,49.0473248165,91.9296148973,103.2220512769,49.4955955105,103.6399009094,87.0468071838,46.4239265584,50.9271084009,47.5585342278,47.2042972149,98.7624409526,48.2123653655,45.0353371928,81.7025026225,57.710716686,45.4902212924,80.3634925428,44.0261121267,91.0233565188,52.8428744677,44.5191098429,41.174433547,51.3215081742,41.8492414734,31.1604326147,68.3293687649,48.6907111786,48.9785932336,90.1223235036,72.5025316697,45.1064666596,30.6001138783,46.0639039467,83.7335209783,82.9385690086,38.880005679,164.1707906939,37.8481016238,40.6857398185,37.3973228162,26.8577758398,43.5286567602,76.1331303446,35.8819665228,37.6715239723,25.6417028072,25.9463068614,41.8892979755,76.6617574324,44.463078782,70.371268599,37.4816295198,24.3360286285,24.6158823924,39.8172618642,42.5811005487,31.6765067747,35.7792730583,64.6420047009,23.4390220583,23.1875651298,64.135413576,48.9683210369,39.6033886652,22.4522872606,20.4993569884,36.2181076905,78.8807934793,68.323426013,24.1782538269,37.3095542795,45.9894955131,31.1186944976,32.0107111561,20.5073546064,18.8260293803,71.7934676375,19.5404533734,34.6396549866,42.7687142203,28.1266797786,30.2383360603,36.3902615698,18.8712215608,18.7485120191,55.9600703811,39.9098935414,39.9885077241,17.9637189096,17.231409377,32.9367234808,64.7886074352,161.9298193277,18.1784041501,31.3332916166,32.4145364738,17.2577483886,36.4506798202,52.8222141114,25.6845066508,15.6201959066,56.4435130367,30.2532730025,16.6091816697,29.8320486335,15.6321939023,33.0760283073,27.0666523559,19.4374058498,27.6885194311,13.662671294,32.6658777562,32.3942654896,15.341023306,56.3934546689,66.9211116377,13.8023275017,42.9377833439,25.105389713,16.3180866721,25.0843030706,26.6852393256,22.223457105,13.3570725018,14.3803111138,29.95103921,29.9868947009,13.845571117,27.2324281758,60.9620961823,12.0894597862,14.463781467,11.0457366635,13.2199072992,24.917499703,21.1210966988,8.2245476364,25.8810865922,21.3261079209,24.2622550956,15.2700452629,12.2628947265,24.6621534707,25.0266764316,54.3292240621,9.2965947239,22.3233782891,9.5538543235,11.0272926365,46.2213978852,21.0394949409,6.184840767,26.9275076061,21.4598493037,12.2138336922,31.04299377,9.4290533977,10.6891136639,10.5008008687,21.7066717638,20.9839738345,9.4515510563,16.2176878843,13.8995158165,5.7999149083,23.9140352524,61.3271282787,17.5157792247,10.806805084,7.6430682135,18.1534722072,7.8830047536,45.6632808064,18.4296307993,10.6987341714,17.111522233,9.6117254628,17.8102154345,4.5814792327,10.1965615701,19.5319124755,55.2375837448,8.9232851389,3.6804455464,30.665826518,16.2169569454,6.2346211348,14.7232925108,5.811911977,19.1155746387,12.9022279246,8.4057458185,10.804238232,18.8054985155,7.8341944707,13.3559187218,8.3938242351,6.1279489279,14.5670183408,8.7337093552,3.9272365,21.8352483374,2.8468651747,30.9464098666,49.8324383699,15.8230509417,10.3521517747,13.8868598893,5.7777942801,7.0182252096,10.7051994329,5.0543788558,6.92083757,4.7905130818,6.6318945247,17.6348164211,1.5300008672,5.9633907904,1.7374664861,15.6046910872,6.1863883343,5.3171246311,4.4034720842,10.5583017633,3.5314335653,9.485449901,6.5939459048,37.1174370159,1.4433535293,5.0580236848,7.8946773835,4.4321149675,2.5067313587,22.2470379254,1.5050837357,3.4461868296,8.132140149,14.5627777717,4.5617879466,0.9710817714,12.3546356497,3.5362804343,0.9778469057,5.8181516665,13.8368875884,3.8244716431,3.3379293442,2.4780901678,4.9732221951,2.7999199192,30.3100418708,15.1711539941,1.0627462469,8.4211419881,3.0236946234,1.7244542108,5.2380468236,6.5716272023,2.9928930597,-0.0708493658,17.5772901937,0.154216817,10.484617482,-0.0068973332,2.6762573526,0.0437920163,2.0585726903,1.7000047054,1.4827244508,2.8868978819,0.0346956977,2.9646542415,5.8737567722,12.9541012529,1.2449700808,20.4033569463,-1.2183032328,3.4435616635,-0.8089877165,1.9737324071,7.3487166489,-0.6167521092,0.2727412902,-1.7294171695,-0.3039175664,-0.0412742964,-0.9274697427,-2.1339460124,1.0329692759,-0.0883585456,2.5910226608,9.3506476061,0.7517922569,-0.7839063896,-3.7112311648,-3.0864124382,-1.4458616128,-4.5133751953,-1.2792653649,-2.2098206451,6.5841330713,-3.0838043189,5.128413728,-4.8584493931,-1.7840225945,-1.2610884673,-1.9241930614,0.6208257588,-2.2952512245,-3.3926053193,1.1176199712,-1.1274450974,-4.4921751759,-1.8428648217,0.6610612583,-3.5847155851,-3.8027645295,1.7753021492,-3.7470979502,-1.1675823329,-4.2312086505,-2.5944672751,1.3397477314,-2.7799580943,-2.2987220055,-3.862868665,-1.4118259303,-2.3790127162,-3.6567526116,-4.7327201842,2.3295736723,-1.7057944909,-2.0175275946,-2.3990129701,-1.9050392586,-0.0090120084,-4.0390476983,-0.0227545229,-3.262525996,-0.158570552,-3.4984988892,-2.3274143892,-4.4017435079,-3.3177608347,-2.4069158045,0.3253408631,-2.534447183,-2.4464938499]
#~ LTvec1Stdev=[1748.4097670693,856.5280794298,848.5232518613,837.3584913807,823.4587032813,802.4411074794,776.1506138535,743.4095944621,705.1599150956,679.08789946,413.1782121098,407.5764074557,402.6191074488,399.9321695592,395.5423165028,388.9598609614,388.8259089259,384.1189507918,376.4690347062,368.6662308733,376.141907015,370.7714911544,364.2567560933,354.4229068004,341.1749931924,359.2119531035,353.414487319,344.5088485062,335.1376761743,321.8020031918,339.2441488335,333.1686363835,660.0125265785,323.8624365575,304.0043025704,314.1622931302,296.2110658317,276.2682564658,323.7957167172,317.1793648917,309.0051863528,194.1357279332,190.3782423719,187.1764044842,295.7903361695,184.21691467,184.3719221375,180.3170785187,177.0738208931,176.2011787573,177.7285662091,173.3086935111,174.8168539581,171.2952943488,168.3792438176,279.8944107259,169.458843922,166.2448995849,252.0544134609,162.5837222969,162.2535317028,169.158177375,159.0184951123,164.2635272575,160.2559148237,154.9059805097,159.0840138564,155.8783000635,149.96021461,149.6422082246,152.6751470095,148.9930921559,258.960237743,143.0877905368,158.3162943227,312.3004315284,137.901835087,153.4382193603,304.0846643846,143.4155005904,149.5273977854,139.8592958028,148.8435274104,294.4559641954,145.1285302138,134.8274291802,140.3124083966,138.6296381721,281.6526546717,135.5229194745,127.8444648776,128.8985676713,229.5585932645,124.2452808662,262.8273705457,129.4433212593,125.5629932414,119.4818351646,148.835406024,119.9813714329,144.8359823999,141.2254152616,137.4485166175,87.3512377778,133.6902391396,112.9554967801,83.3696233872,81.4912977984,129.0554981244,80.7258740593,78.9266174693,129.1173800799,78.1918610405,76.9280325834,125.3782523216,236.296525311,116.8145867598,76.3109168112,113.2111489883,73.8882083983,74.6012465152,119.8931162885,75.0749388489,71.7660630822,102.105767364,105.9633566695,72.720424211,69.8451819026,69.3343446232,69.2021833466,200.7317868227,69.3363362276,67.1963221357,67.1834799487,119.3638906243,112.8482828909,66.0181813618,115.4413223771,99.9940228631,63.6080419281,64.9298253279,63.6275313865,140.5751217116,110.4736494269,69.2115290191,64.7504364178,61.2860335603,136.248592223,67.3189011685,62.1185029046,131.5374563211,65.1223929739,59.347065004,56.8459571103,129.2205035009,212.1841717749,61.8784483308,62.9239948112,58.2469480016,101.776390358,125.1356933534,58.4730694924,89.9030138336,55.999821618,56.0296656227,103.8836473072,118.8878449719,56.0208951645,119.1802643221,99.5614192123,52.7931977639,57.301338326,53.8570743531,53.8864949569,114.7310738554,54.6080542653,51.4243551358,93.5297105529,64.6635272799,52.1835255333,92.3130965933,50.8714036621,107.5920614674,60.2894568689,51.1047191727,47.8987182698,58.1906639546,48.5393392247,35.1794595372,79.2605216077,55.9128810919,56.0040887295,106.3549385612,84.6583204982,51.2160279412,34.1983855288,53.2547760346,100.1217757081,100.401044893,45.7583588268,194.5854909311,44.8996397651,47.1907570197,44.208438751,30.9297816784,50.8731595807,89.4772258328,42.7806071082,44.501542274,29.7416778737,29.8895854516,49.2866488108,94.3183581713,51.5073596594,84.2892091538,43.9605584586,28.3154177331,28.580586416,47.1410323436,49.4150248643,38.9640420638,42.0481207569,76.105096503,27.2165359731,27.3456855598,77.9699254331,58.2686856196,46.7660343457,26.3935848877,24.6371050266,43.6078450652,94.4874640757,85.8360406163,28.0651468153,44.4150380845,55.1489322213,37.9732351622,38.5422880678,24.4235786024,23.1280905019,88.4389651366,24.0104391724,41.858431573,52.0334427394,35.5258295607,36.5486993329,43.6236108184,22.8320890284,23.0102317365,69.6482020752,49.512011785,49.5095716094,22.0377678933,21.3771850337,40.0292008832,81.5769786567,196.1104636391,22.4175663612,38.6869677051,39.4187486719,21.5090046666,46.1344864914,64.6845619683,32.234957445,19.9783276626,74.4601505238,37.6152300503,20.7672486375,37.0069202173,20.1557101775,43.2057288488,33.5544365266,23.9039847962,35.0958158275,18.2766784703,42.2316249711,42.4583608931,19.4674104087,73.00472814,83.9242126865,18.1443619131,56.9562658205,31.446628997,21.0193987872,32.5676563331,33.8844722363,28.8367392178,17.6558702393,18.6157233591,39.6613377313,39.8945934854,18.1154475555,35.1995511111,78.4947995551,16.582618966,19.1210729215,15.5158457095,17.2313372564,31.5130813862,27.5385026585,11.0708840546,36.4244795787,28.6429426768,32.1588295702,19.6560382941,17.0868091059,34.993251026,35.0810318496,71.8385821374,13.9183878537,29.4865421196,14.315079052,15.1968150306,62.7640108898,28.3765916104,9.0512934372,36.5499924371,29.4722502965,16.774442169,44.8368671958,13.8747559618,15.6363567522,14.47434921,32.0565530532,28.5180173497,13.7695518885,23.1466489494,19.8672411984,8.4567384102,33.3008571704,81.4897630623,24.3581841114,15.332660407,12.2918348524,25.1845894801,12.0053165756,62.9068194693,28.7635224642,15.1050442091,25.1184399805,14.1220949393,28.4054758411,7.5245285596,16.4777068711,29.6134858448,76.0719882518,13.654830201,6.722455784,48.3967486988,23.1440862554,10.4780129015,25.4865517939,10.5588891914,28.5989355065,20.9989378889,12.2557009852,17.592321071,32.5307351588,12.2797339767,20.1667210412,12.7551018463,10.2423071581,22.2751724616,14.7091907631,6.7140177862,31.538576827,5.7717400259,49.3038717505,69.8758284864,25.5947888692,18.4385234361,20.447572197,9.792576762,13.3109314443,21.6274421608,9.7077193466,11.38800506,8.9122246373,12.6871100847,27.7684701901,4.4870988676,10.3533838522,4.689706783,24.549591272,10.4648826241,10.2609593532,8.4967844562,20.7717813764,8.2079792434,16.7000211004,14.7467102249,58.0801969805,4.7425977412,11.1487238593,14.6302445867,10.7852333354,6.8167383092,39.4193770697,4.3318207043,7.6577969982,18.4666799544,24.773493746,8.9934150571,3.9527612687,21.465606434,7.8522550718,3.8572687299,13.4579510291,23.5580255183,8.459965062,9.5108591886,6.5365535399,12.3323744286,9.1979099846,49.0538017146,27.8791431933,4.1216380828,17.7586577379,7.3279007679,6.1817078071,12.0231446028,16.3856665312,7.297119414,2.6957254667,32.7098290703,6.8511517804,20.4690750619,2.8771127543,10.2105215196,4.3614145484,9.6511955866,5.8530827153,7.7549030763,7.3627719523,4.310724673,13.2484647324,16.2762287951,24.9073703811,7.3042449801,38.7304423853,1.9616011391,12.8133704981,4.2162694279,6.0338910577,16.9763559156,3.3478056421,7.6816398437,4.9843032401,4.0271623629,2.8665159464,1.8103925662,5.3686977808,5.6513984752,10.0586593338,13.1473407005,21.7257865232,4.8274731221,1.8558075478,3.1606481277,0.733118443,4.8206668022,3.245162744,1.5356196491,2.676513175,26.6771277122,1.1958396639,18.0392595622,2.3145831659,2.5136867976,2.4763313187,0.7539358642,10.8746686472,3.7961296868,7.9670910315,7.2581477219,1.7016159905,5.5562568862,0.3331828228,6.0938506955,2.8503777394,1.1066181816,15.0004245348,0.0731920004,3.0877711023,2.3205920964,1.4470998595,24.7097079663,-0.02330536,8.0108682602,2.2564757119,1.0518666967,1.9327497663,6.448568677,4.4494305468,13.9811977957,0.9400380096,0.6940852501,1.685449385,3.6660464323,12.2362321161,1.280707466,8.7269848826,0.6143005201,5.5412151928,6.081658949,1.7564042687,1.4399293707,0.8415611517,1.1805307642,11.6255910515,0.211508549,-0.0367456532]
#~ G=250

#~ Fdict=lmb.perc_goodchannel_LTvec_WD(LLRdict,channel_plist,N,LTvec1Stdev,G,runsim)
#~ PT=80
#~ Ppercdict=lmb.PrOffracaboveFT(Fdict,channel_plist,PT,runsim)
#~ print Ppercdict

#~ color=["red","blue","green","yellow"]
#~ plt.figure(1)
#~ index= range(runsim)
#~ j=1
#~ for channel_p in channel_plist:
	#~ j+=1
	#~ plt.scatter(index,Fdict[str(channel_p)],color=color[j-2],label="Channel_p"+str(channel_p))
	
#~ plt.legend(loc="best")
#~ plt.title("Threshold Vector"+" design_p=0.1"+" Rate="+str(float(G)/N)+" Capacity="+str(C/N))
#~ plt.xlabel("Simulation number")
#~ plt.ylabel("% of good channels with LLR>Threshold")

#~ plt.figtext(0.005, 0.03, "P("+str(PT)+"% of goodchannels>Threshold)="+str(Ppercdict))

#~ plt.show()	

