#-------------------------------------------------------------------------------
# Name:       flipstrings.py
# Purpose:    generates all strings of length n with k flips
#           
# Author:      soumya
#
# Created:     -
#----------------------------------------

import itertools

def kbits(n, k):
    result = []
    for bits in itertools.combinations(range(n), k):
        s = ['0'] * n
        for bit in bits:
            s[bit] = '1'
        result.append(''.join(s))
    return result

print kbits(128, 3)

