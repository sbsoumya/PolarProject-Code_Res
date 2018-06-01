#!/usr/bin/env python

import PolarCode

m1 = PolarCode.PolarCode(3,6,5,0)
print ("n =",m1.n)
print m1.info_length
print m1.design_p
print m1.crc_size

#m1.setvector([1,0,1,1,0,0,1])
#print (m1.getvector())
print m1.encode([1,1,0,1,1,1])

m1.channel_ordering=[7, 3, 5, 6, 1, 2, 4, 0]
print m1.encode([1,1,0,1,1,1])
