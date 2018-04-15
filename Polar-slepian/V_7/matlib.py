#-------------------------------------------------------------------------------
# Name:       math-library
# Purpose:    math extra functions
#
# Author:      soumya
#
# Created:     04/08/2017
#----------------------------------------
from numpy import *

#For kronecker product using numpy.kron
#multiplies each element of first matrix with elements of second matrix

#clean up
def kronpow(A,n):
	n=n-1 
	if n==-1:
		return 0 #should return eye
	if n==0:
		return A	
	B=kron(A,A) #could have used eye
	for i in range(n-1):
		B=kron(B,A)
	return B

def logdomain_sum(x,y):

	if(x<y):
		z = y+log(1+exp(x-y));
	else:
		z = x+log(1+exp(y-x));
	return z

def logdomain_diff(x,y):

	z = x + log(1 - exp(y-x));
	return z
