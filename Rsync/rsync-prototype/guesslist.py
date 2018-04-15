from guess import *
from checksum import *

def makeguess(chunk_id,rcv_hashentry,send_RC,send_MD5,Guess_iter,guessfile):
    chunk= rcv_hashentry[0]
    converged=False;
    
    for i in range(0,Guess_iter):
		if converged:
			break
			
		guess=guess_random1characflip(i,chunk);
		guessRC=rollingcheck(guess,chunk_id,len(chunk));
		guessMD5=getMD5(guess);
		
		#guessfile.write(str(guess)+","+str(guessRC)+","+str(guessMD5)+"\n")
		guessfile.write(str(guess)+","+str(guessRC)+"\n")
		
		if guessRC==send_RC:
			if guessMD5==send_MD5:
				converged=True
				print "\nCONVERGED :"+str(chunk)+" :: "+str(guess)+"\n"+" at " +str(i)+"th guess" 
			

    return (guess,converged)
			
			
			
	
