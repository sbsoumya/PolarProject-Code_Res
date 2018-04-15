import math
import hashlib

def rollingcheck(chunk,k,l):
#Rolling checksum 
	M=2**16;
	i=0;
	a=0;
	b=0;
	s=0;
		
	for chunk_byte in chunk:
		i +=1;
		#print chunk_byte;
		a += chunk_byte;         #use sum
		b += (l-i+1)*chunk_byte;
		
	s= ( a % M) + 2**16 * (b % M);
	#print s 
	#print "---------------------"
	return s

def getMD5(chunk):
	MD5=hashlib.md5(str(chunk))
	return MD5.digest();
	
	

