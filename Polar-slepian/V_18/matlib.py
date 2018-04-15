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
from bisect import bisect_left
import binascii
import crc8
import json



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

#log(exp(X)+exp(Y))
def logdomain_sum(x, y):
    if (x < y):
        z = y + log(1 + exp(x - y));
    else:
        z = x + log(1 + exp(y - x));
    return z

#log(exp(X)-exp(Y))
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
    
def bucket(x,y,bucketsize):
	(x_s,y_s)=sortAextend(x,y)
	x_size=len(x_s)
	x_buckets=int(float(x_size)/bucketsize)
	x_bucketed=[]
	y_bucketed=[]
	for i in range(x_buckets):
		try:
			x_bucketed.append(mean(x_s[i*bucketsize:(i+1)*bucketsize]))
			y_bucketed.append(mean(y_s[i*bucketsize:(i+1)*bucketsize]))
		except:
			x_bucketed.append(mean(x_s[i*bucketsize:]))
			y_bucketed.append(mean(y_s[i*bucketsize:]))
	return (x_bucketed,y_bucketed)
	

def get_lcm_for(your_list):
    return reduce(lambda x, y: lcm(x, y), your_list)
    
def extract_data(indices,data,extractindices):
	extractindices_ind=[indices.index(i) for i in extractindices]
	return [data[j] for j in extractindices_ind]
	
def extract_otherdata(indices,data,extractindices):
	extractindices_ind=[indices.index(i) for i in indices if i not in extractindices]
	return [data[j] for j in extractindices_ind]
	
#print extract_otherdata([1,2,3,4,7,8],[2,3,4,1,6,5],[4,8])
def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before
       
#print takeClosest([1,2,3,4,5,6,7,10,15,19,45,71,73,97,98,99],72)

def bittostring(msg):
	padlength=len(msg)%8
	paddedmsg=list(msg)+list(zeros(padlength,dtype=int))
	charnumber=len(paddedmsg)/8
	msgstring=""
	for i in range(charnumber):
		singchararr=paddedmsg[i*8:i*8+8]
		singcharbin=""
		for j in range(8):
			singcharbin+=str(singchararr[j])
		msgstring+=chr(int(singcharbin,2))
	return msgstring
	
def getCRC(msg,length):
	if log2(length)> int(log2(length)):
		print "CRC length must be int"
		return
	else:
		msgstring=bittostring(msg)
		if length==32:
			crc=bin( binascii.crc32(msgstring) % (1<<32))
			crc=crc+"0"*(34-len(crc))
			return [int(i) for i in crc[2:]]
		if length==8:
			hash = crc8.crc8()
			hash.update(msgstring)
			crc= bin(int(hash.hexdigest(),16) % (1<<32) )
			crc=crc+"0"*(10-len(crc))
			return [int(i) for i in crc[2:]]

def getline(filename,lineno):
	table0 = []
	with open(filename,'r') as f:
		for line in f:
			table0.append(json.loads(line))
	print filename
	print  [table0[i] for i in lineno]
	return [table0[i] for i in lineno]

#~ UN_msg=random.randint(2,size=1024)
#~ print getCRC(UN_msg,32)
#~ print getCRC(UN_msg,32)
