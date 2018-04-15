#-------------------------------------------------------------------------------
# Name:       polarencdecsim.py
# Purpose:    encoding decoding simulations
#            
#
# Author:      soumya
#
# Created:     19/08/2017
#----------------------------------------
import numpy as np
import math as ma
import problib as pl
import polarencdec as ec
import polarconstruct as pcon
from datetime import datetime
import json

N=8
K=4

design_p=0.1
I=pcon.getGChZCK(design_p,N,K)[0]
#print I
G=len(I) #number of good channels
FD=np.zeros(N-G,dtype=int).tolist()#frozen data

YN=np.random.randint(2,size=N)



YN=np.array([0,1,1,1,1,1,1,1]) #N=8,K=4


print "YN:"
print YN.tolist()


d=ec.polarSCdecodeG(YN,N,design_p,I,list(FD),False)
print d
print ec.getUN(d,I,True).tolist()

"""
[0 1 1 1 1 1 1 1]
[0 0 0 0 0 0 0 1]
[0 0 0 1]
"""
"""

  Columns 1 through 21

     1     0     0     1     0     0     0     0     0     1     1     1     0     1     1     1     0     0     0     1     1

  Columns 22 through 42

     0     0     0     1     0     1     0     0     0     0     0     1     0     1     0     1     0     1     0     1     0

  Columns 43 through 63

     0     1     0     1     1     1     0     1     1     1     1     0     0     0     1     1     0     0     1     0     0

  Columns 64 through 84

     1     1     1     0     1     0     0     1     0     0     0     0     0     1     0     1     0     0     0     1     1

  Columns 85 through 105

     1     1     1     1     1     0     0     0     1     0     1     1     1     1     1     0     0     1     0     0     0

  Columns 106 through 126

     0     0     1     0     0     1     1     0     0     1     0     1     1     1     1     1     0     1     1     0     0

  Columns 127 through 147

     1     0     1     0     0     0     1     0     1     0     0     1     1     0     0     0     0     1     0     0     1

  Columns 148 through 168

     0     0     0     1     1     0     1     1     1     0     1     1     1     1     1     1     1     1     0     0     0

  Columns 169 through 189

     1     0     1     0     0     1     1     1     0     0     1     0     1     1     1     0     0     0     1     0     1

  Columns 190 through 210

     0     0     1     0     0     1     1     0     0     1     1     0     0     0     0     0     1     0     0     0     0

  Columns 211 through 231

     0     1     0     1     0     1     0     0     0     0     0     1     0     1     0     1     0     1     1     0     1

  Columns 232 through 252

     1     0     0     0     1     0     1     0     0     0     1     0     1     0     0     0     1     0     1     1     0

  Columns 253 through 273

     0     1     1     1     0     1     1     1     0     1     0     0     0     0     0     0     1     0     1     0     0

  Columns 274 through 294

     1     1     0     0     1     1     0     0     0     0     1     0     1     0     0     1     0     1     0     0     0

  Columns 295 through 315

     0     0     1     0     1     0     1     1     0     1     1     0     0     0     1     0     0     0     1     0     1

  Columns 316 through 336

     1     0     1     0     0     0     1     1     1     1     1     1     0     0     1     0     1     0     0     0     1

  Columns 337 through 357

     0     1     0     1     1     0     0     1     1     0     0     0     1     0     1     1     0     0     1     0     1

  Columns 358 through 378

     1     1     1     1     0     0     1     0     0     0     1     0     1     0     1     1     0     0     0     1     1

  Columns 379 through 399

     1     0     1     0     1     1     1     0     1     0     0     1     1     1     1     0     1     0     1     0     0

  Columns 400 through 420

     0     1     1     1     1     0     0     0     0     1     0     1     1     0     0     1     1     1     0     0     1

  Columns 421 through 441

     0     1     1     1     1     0     0     1     0     1     1     1     0     1     0     0     0     0     1     0     0

  Columns 442 through 462

     0     1     1     0     1     0     1     0     1     0     1     0     0     1     0     1     1     1     0     0     0

  Columns 463 through 483

     0     1     0     1     0     1     1     1     1     0     1     1     1     0     1     1     0     0     0     1     1

  Columns 484 through 504

     1     1     0     0     1     1     0     0     0     0     1     0     0     1     1     1     1     1     1     0     0

  Columns 505 through 525

     1     0     1     1     1     1     1     1     1     1     1     1     1     0     0     1     0     0     1     0     0

  Columns 526 through 546

     0     1     0     1     0     1     0     0     0     1     1     0     0     0     1     1     0     0     1     1     1

  Columns 547 through 567

     0     1     0     1     1     1     1     0     0     1     1     0     1     1     1     1     0     0     0     1     0

  Columns 568 through 588

     0     1     0     1     1     1     1     0     1     0     1     1     0     1     0     0     1     1     1     0     0

  Columns 589 through 609

     1     1     0     0     1     0     0     1     1     0     0     0     1     0     0     1     1     0     1     0     0

  Columns 610 through 630

     1     0     0     0     1     0     1     0     0     0     1     1     1     0     0     0     1     0     0     1     0

  Columns 631 through 651

     1     1     0     1     1     0     0     0     0     0     0     1     1     0     0     1     0     0     1     1     0

  Columns 652 through 672

     1     0     0     0     1     0     0     0     0     0     0     0     0     1     1     1     0     1     0     0     1

  Columns 673 through 693

     1     0     1     1     1     0     1     1     1     0     1     0     1     0     1     1     1     0     1     1     1

  Columns 694 through 714

     0     0     0     0     1     1     1     1     0     1     0     1     0     1     0     1     0     0     0     1     0

  Columns 715 through 735

     0     0     0     1     1     1     0     1     0     1     0     1     0     1     0     0     1     0     0     0     0

  Columns 736 through 756

     0     1     0     1     1     1     0     1     0     0     0     0     0     0     1     0     1     0     1     0     0

  Columns 757 through 777

     0     1     1     1     0     0     1     1     0     1     1     1     1     0     0     0     1     0     1     1     0

  Columns 778 through 798

     0     1     1     1     0     0     0     1     0     1     1     1     1     1     0     0     0     0     0     1     0

  Columns 799 through 819

     1     0     0     0     1     0     1     1     0     0     1     1     1     1     1     1     0     1     1     0     1

  Columns 820 through 840

     0     1     1     0     1     0     0     1     1     0     0     0     1     1     1     0     1     0     0     0     0

  Columns 841 through 861

     0     1     1     0     1     0     0     1     1     0     1     0     1     0     0     1     1     0     1     1     1

  Columns 862 through 882

     0     1     0     0     0     1     0     1     0     1     0     0     0     1     1     0     0     0     0     1     1

  Columns 883 through 903

     0     1     1     0     0     1     1     0     0     1     1     0     1     1     1     1     1     0     0     0     1

  Columns 904 through 924

     0     0     1     0     1     1     0     1     1     1     0     1     1     1     0     1     1     0     1     1     0

  Columns 925 through 945

     0     0     0     1     0     1     1     1     1     1     1     0     1     1     0     1     1     0     0     0     0

  Columns 946 through 966

     1     1     1     0     1     1     1     0     0     1     0     0     1     0     0     1     1     0     1     1     1

  Columns 967 through 987

     1     0     0     1     0     0     1     0     1     0     1     1     0     1     1     0     0     1     1     0     1

  Columns 988 through 1008

     0     0     1     0     1     0     1     1     0     0     1     0     1     1     1     1     0     1     0     0     0

  Columns 1009 through 1029

     0     1     0     0     1     1     0     0     0     0     0     1     0     0     1     1     1     0     1     0     1

  Columns 1030 through 1050

     1     0     0     0     0     0     1     0     0     0     1     1     0     0     0     0     0     1     1     0     0

  Columns 1051 through 1071

     1     0     1     1     1     0     0     1     1     1     0     1     1     0     0     1     0     1     1     0     1

  Columns 1072 through 1092

     1     1     1     0     1     1     0     1     1     0     0     0     0     0     0     1     1     0     1     0     1

  Columns 1093 through 1113

     0     1     0     0     1     0     0     1     0     0     0     0     1     1     1     1     0     0     1     1     1

  Columns 1114 through 1134

     1     1     1     1     0     0     1     1     1     1     1     1     1     1     0     1     0     1     1     0     0

  Columns 1135 through 1155

     0     1     1     1     0     1     1     0     1     0     1     1     1     0     0     1     1     1     0     0     0

  Columns 1156 through 1176

     1     0     1     1     1     0     0     1     1     1     1     0     1     0     1     1     1     1     0     0     0

  Columns 1177 through 1197

     0     0     1     1     1     1     0     1     1     1     0     0     0     1     0     0     0     0     0     1     0

  Columns 1198 through 1218

     0     1     0     0     1     1     0     0     0     0     1     1     1     1     0     1     0     1     1     0     1

  Columns 1219 through 1239

     0     0     1     0     0     1     0     0     1     0     0     1     0     1     1     0     0     1     1     1     0

  Columns 1240 through 1260

     1     1     0     0     0     1     0     1     1     0     0     0     1     1     0     0     1     0     0     0     0

  Columns 1261 through 1281

     1     0     0     1     1     1     1     0     0     1     1     1     1     1     1     0     1     0     0     1     0

  Columns 1282 through 1302

     0     1     0     0     1     1     0     1     1     0     0     1     1     1     0     0     0     0     1     1     0

  Columns 1303 through 1323

     1     1     0     0     1     0     1     1     0     1     0     0     1     0     0     0     1     0     1     1     1

  Columns 1324 through 1344

     1     0     1     1     0     0     1     0     1     0     1     1     0     0     1     1     1     0     0     1     0

  Columns 1345 through 1365

     1     1     1     1     0     1     1     1     0     1     0     1     0     0     1     0     1     0     0     1     0

  Columns 1366 through 1386

     0     1     0     1     0     0     1     1     1     0     0     1     1     1     0     1     0     0     0     1     1

  Columns 1387 through 1407

     0     1     1     1     0     1     1     1     0     1     1     0     1     1     0     1     0     1     1     0     0

  Columns 1408 through 1428

     0     1     1     0     0     0     1     1     1     1     1     1     1     1     0     0     1     1     0     1     1

  Columns 1429 through 1449

     0     0     1     1     1     0     0     0     1     0     1     0     0     1     0     0     0     0     1     0     1

  Columns 1450 through 1470

     0     0     0     0     0     0     1     1     1     1     1     0     0     0     0     1     0     1     1     0     0

  Columns 1471 through 1491

     1     0     1     0     1     0     1     0     0     1     0     1     0     1     1     1     1     1     1     1     0

  Columns 1492 through 1512

     1     1     1     1     0     1     0     1     0     1     0     0     0     1     1     0     0     0     1     0     1

  Columns 1513 through 1533

     0     0     1     1     1     1     1     1     1     0     1     0     0     1     1     0     1     1     0     1     1

  Columns 1534 through 1554

     1     1     0     1     1     1     1     0     0     0     0     0     0     0     1     1     1     1     1     1     0

  Columns 1555 through 1575

     1     1     1     0     0     0     0     1     0     1     1     0     1     1     0     1     1     0     1     0     0

  Columns 1576 through 1596

     1     1     1     1     1     1     0     1     1     0     0     1     0     1     0     0     1     0     1     0     0

  Columns 1597 through 1617

     0     1     1     0     1     0     1     1     1     1     0     1     1     0     1     0     0     0     0     1     0

  Columns 1618 through 1638

     0     0     0     1     1     0     0     0     0     0     1     1     0     0     0     0     1     0     1     0     0

  Columns 1639 through 1659

     0     1     0     0     0     1     0     1     0     1     0     0     0     1     1     1     1     1     1     0     1

  Columns 1660 through 1680

     0     1     1     0     1     1     1     1     1     1     0     0     1     0     1     1     0     0     1     0     1

  Columns 1681 through 1701

     1     0     0     1     0     1     1     0     0     1     1     1     1     0     0     1     1     1     1     0     0

  Columns 1702 through 1722

     0     0     1     1     1     1     0     1     1     1     1     1     0     1     1     0     1     0     0     0     0

  Columns 1723 through 1743

     0     0     1     1     1     0     1     1     0     0     1     0     1     1     1     0     0     1     1     0     1

  Columns 1744 through 1764

     1     1     1     0     1     0     0     0     0     1     1     1     1     0     0     1     0     1     1     1     0

  Columns 1765 through 1785

     0     0     0     1     0     1     0     1     0     0     1     0     0     0     0     0     1     1     0     1     1

  Columns 1786 through 1806

     0     0     0     0     0     0     1     0     1     1     1     0     0     0     0     1     0     0     1     0     0

  Columns 1807 through 1827

     0     0     1     0     0     0     0     0     1     0     0     1     1     0     1     0     1     0     1     0     0

  Columns 1828 through 1848

     0     0     0     0     1     0     0     0     0     0     1     0     0     1     1     0     1     1     0     0     0

  Columns 1849 through 1869

     0     0     1     0     0     1     0     1     1     1     1     0     0     0     0     0     1     1     1     1     0

  Columns 1870 through 1890

     0     1     0     0     0     0     1     0     1     0     1     0     1     1     1     1     0     1     0     1     0

  Columns 1891 through 1911

     0     1     1     1     0     1     1     1     0     0     1     0     0     0     1     1     0     1     0     1     0

  Columns 1912 through 1932

     0     1     0     1     0     1     1     1     1     1     0     1     0     0     1     1     0     0     1     0     0

  Columns 1933 through 1953

     1     1     0     1     1     1     1     1     0     0     1     0     0     1     1     0     1     1     1     0     0

  Columns 1954 through 1974

     1     0     1     1     0     0     1     1     1     1     1     1     1     0     0     0     0     1     1     0     1

  Columns 1975 through 1995

     0     0     1     0     0     0     1     0     1     0     0     0     1     1     0     0     1     0     1     0     1

  Columns 1996 through 2016

     1     0     1     1     1     0     0     1     0     0     0     0     1     1     0     1     1     1     0     1     0

  Columns 2017 through 2037

     0     0     1     1     1     1     1     1     1     1     1     0     1     1     1     1     0     1     0     1     0

  Columns 2038 through 2048

     0     0     1     1     1     1     0     0     0     1     0
     """
