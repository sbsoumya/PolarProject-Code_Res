#!/usr/bin/env python
import sys
sys.path.insert(0, './cfunctions/boost')
import PolarCode
import polarconstruct as pcon
import polarencdec as ec
import numpy as np


I=pcon.getreliability_order(16)
print ec.bitreverseorder(I,4)
p=.01
z=np.sqrt(4*p*(1-p))
m1 = PolarCode.PolarCode(4,11,z,0)
print ("n =",m1.n)
print m1.info_length
print m1.design_p
print m1.crc_size

#m1.setvector([1,0,1,1,0,0,1])
#print (m1.getvector())
#print m1.encode([1,1,0,1,1,1,0,0,1,1,0])

#m1.channel_ordering=bitreversed[7, 3, 5, 6, 1, 2, 4, 0]
print m1.channel_ordering
#print m1.encode([1,1,0,1,1,1,0,0,1,1,0])
#print m1.frozen_bits
frozen_bits=list([0]*11)
frozen_bits.extend([1,0,1,1,1])
print frozen_bits
m1.frozen_bits=frozen_bits
print m1.frozen_bits
print m1.encode([1,1,0,1,1,1,0,0,1,1,0])
