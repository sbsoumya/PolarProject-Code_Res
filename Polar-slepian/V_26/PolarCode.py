#!/usr/bin/env python
import sys
sys.path.insert(0, './cfunctions/boost')
import PolarCode
import polarconstruct as pcon
import polarencdec as ec
import numpy as np
import matlib as ml
import problib as pl
import numpy as np


UN=[1,1,0,1,1,1,1,0,1,1,0]
F=[0,1,1,0,1]
F1=list(F)
F2=list(F)
p=.01
z=np.sqrt(4*p*(1-p))
m1 = PolarCode.PolarCode(4,11,z,0)
print ("n =",m1.n)
print m1.info_length
print m1.design_p
print m1.crc_size
print m1.channel_ordering
I=pcon.getreliability_order(16)
#I=[15,2,3,4,5,6,7,8,9,0,1,10,11,12,13,14]
m1.channel_ordering=ec.bitreverseorder(I,4)
print ec.bitreverseorder(I,4)
print m1.channel_ordering
frozen_indices=I[-5:]
print frozen_indices
frozen_indices.sort()
Revfrozen_indices=ec.bitreverseorder(frozen_indices,4)

frozen_bits=list([0]*16)
for i in Revfrozen_indices:
	frozen_bits[i]=F.pop(0)

print frozen_bits
m1.frozen_bits=frozen_bits
print m1.frozen_bits
print m1.encode(UN)
print ec.polarencodeG(UN,16,I[:11],F1,False)
G=11
N=16
design_p=0.01
ED_size=0
pc1=ec.polarcode_init_defch(N,G,design_p,I,ED_size)
print ec.polarencodeG_C(pc1,UN,F2)
	

#=====================decode simulations----#MSB problem
print "==================="
p=0.01

I_ord=pcon.getreliability_order(16)

#I_ord=[15,2,3,4,5,6,7,8,9,0,1,10,11,12,13,14]
I=I_ord[:11]
F=[0,0,0,0,0]
D=list(F)
YN=[1,1,1,0,1,1,0,0,1,1,0,1,1,1,0,0]
llrYN=[pl.LLR(p,y) for y in YN]
print llrYN

UN_hat_ec=ec.polarSCdecodeG(YN,16,p,I,list(F),False)
UN_ec=ec.getUN(UN_hat_ec,I,False)

print UN_ec

p=.01
z=np.sqrt(4*p*(1-p))
m1 = PolarCode.PolarCode(4,11,z,0)
#m1.channel_ordering=ec.bitreverseorder(I_ord,4)

frozen_indices=ec.bitreverseorder(m1.channel_ordering[-5:],4)
frozen_indices.sort()
Revfrozen_indices=ec.bitreverseorder(frozen_indices,4)

frozen_bits=list([0]*16)
for i in Revfrozen_indices:
	frozen_bits[i]=D.pop(0)

print frozen_bits
m1.frozen_bits=frozen_bits
UN_pc=m1.decode_scl(llrYN,1)
print "\n"
print np.array(UN_pc)
