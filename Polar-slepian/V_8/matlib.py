# -------------------------------------------------------------------------------
# Name:       matlib.py
# Purpose:    mathlibrary
#             now includes sorting functions etc
#
# Author:      soumya
#
# Created:     04/08/2017
# ----------------------------------------
from numpy import *


# For kronecker product using numpy.kron
# multiplies each element of first matrix with elements of second matrix

# clean up
def kronpow(A, n):
    n = n - 1
    if n == -1:
        return 0  # should return eye
    if n == 0:
        return A
    B = kron(A, A)  # could have used eye
    for i in range(n - 1):
        B = kron(B, A)
    return B


def logdomain_sum(x, y):
    if (x < y):
        z = y + log(1 + exp(x - y));
    else:
        z = x + log(1 + exp(y - x));
    return z


def logdomain_diff(x, y):
    z = x + log(1 - exp(y - x));
    return z

#sorts A and sorts B accordingly 
def sortAextend(A,B):
	An=array(A)
	#print An
	Ai=argsort(A)
	#print Ai
	Bs=array(B)[Ai]
	#print Bs
	As=list(A)
	As.sort()
	return(As,Bs.tolist())
	
def lcm(a, b):
    if a > b:
        greater = a
    else:
        greater = b

    while True:
        if greater % a == 0 and greater % b == 0:
            lcm = greater
            break
        greater += 1

    return lcm

def get_lcm_for(your_list):
    return reduce(lambda x, y: lcm(x, y), your_list)

