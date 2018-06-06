#!/usr/bin/env python
import sys
sys.path.insert(0, './cfunctions/boost')
import PolarCode
import polarconstruct as pcon
import polarencdec as ec
import numpy as np
import matlib as ml

UN=[1,1,1,1,1,1,1,0,1,1,0]
F=[0,1,1,0,1]
F1=list(F)
p=.01
z=np.sqrt(4*p*(1-p))
m1 = PolarCode.PolarCode(4,11,z,0)
print ("n =",m1.n)
print m1.info_length
print m1.design_p
print m1.crc_size
print m1.channel_ordering
I=pcon.getreliability_order(16)
print ec.bitreverseorder(I,4)

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
