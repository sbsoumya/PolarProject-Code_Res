import matplotlib.pyplot as plt



cbdata=[[1.0000,    0.7846,    0.5862],
    [1.2500,    0.7846,    0.4636],
    [1.5000,    0.6375,    0.3355],
    [1.7500,    0.4904,    0.2267],
    [2.0000,    0.4113,    0.1206],
    [2.2500,    0.3018,    0.0698],
    [2.5000,    0.2032,    0.0393],
    [2.7500,    0.1099,    0.0173],
    [3.0000,    0.0815,    0.0084]]
    
x=[snr[0] for snr in cbdata]
l1CB=[fer[1] for fer in cbdata]
l4CB=[fer[2] for fer in cbdata]

print x
print l1CB
print l4CB

crcdata=[[   1.0000  ,  0.8500 ,   0.5000],
    [1.2500  ,  0.7612 ,   0.4146],
    [1.5000  ,  0.5313 ,   0.3072],
    [1.7500  ,  0.4595 ,   0.2000],
    [2.0000   , 0.3953 ,   0.1371],
    [2.2500  ,  0.2757 ,   0.0836],
    [2.5000  ,  0.2000 ,   0.0503],
    [2.7500  ,  0.1342 ,   0.0223],
    [3.0000  ,  0.0832 ,   0.0067],]
l1CRC=[fer[1] for fer in crcdata]
l4CRC=[fer[2] for fer in crcdata]


nocrcdata=[[   1.0000,    0.5050,    0.3072],
    [1.2500,    0.4250,    0.2394],
    [1.5000,    0.3091,    0.1211],
    [1.7500,    0.2125,    0.0728],
    [2.0000,    0.1735,    0.0372],
    [2.2500,    0.0807,    0.0184],
    [2.5000,    0.0442,    0.0115],
    [2.7500,    0.0189,    0.0067],
    [3.0000,   0.0119 ,   0.0033]]

l1NCRC=[fer[1] for fer in nocrcdata]
l4NCRC=[fer[2] for fer in nocrcdata]

plt.semilogy(x,l1CB,label="L=1,CB")
plt.semilogy(x,l1CRC,label="L=1,CRC")
plt.semilogy(x,l4CB,label="L=4,CB")
plt.semilogy(x,l4CRC,label="L=4,CRC")
plt.semilogy(x,l1NCRC,label="L=1")
plt.semilogy(x,l4NCRC,label="L=4")

plt.grid(True)
plt.title("N=256,CRC size=16,AWGN channel")
plt.legend(loc="best")
plt.ylabel("FER")
plt.xlabel("SNR(db)")

plt.show()
