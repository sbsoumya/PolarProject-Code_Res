#!/usr/bin/env python

import math 
from hashlist import *
from guesslist import *

S= 50  #chunk size

#Sender ================================================================
print "SENDER\n----------------"
send_file= open("data.txt","rb")

send_RC_file =open("SenRC.txt","w")
send_MD5_file =open("SenMD5.txt","w")

(send_hashlist,No_of_chunks)=genhashlist2(send_file,S);

#for debugging
for hashentry in send_hashlist:
	send_RC_file.write(str(hashentry[1])+"\n");
	send_MD5_file.write(str(hashentry[2])+"\n");
		
#Note: the first element of hash entry is the chunk itself, Rcv will not 
#have(use) sender chunk. 

#Receiver ==============================================================
print "RECEIVER\n----------------"
rcv_file= open("rcvdata.txt","rb")

rcv_RC_file =open("RxRC.txt","w")   
rcv_MD5_file =open("RxMD5.txt","w") 
      						
(rcv_hashlist,dummy)=genhashlist2(rcv_file,S);


#for debugging
for hashentry in rcv_hashlist:
	rcv_RC_file.write(str(hashentry[1])+"\n");
	rcv_MD5_file.write(str(hashentry[2])+"\n");
		
#hashmismatch===========================================================
#finding number of chunk transfers required---------
#actual transfer and reconstruction is not attempted.not required for analysis.

transfers=No_of_chunks

rcv_RC_list=[i[1] for i in rcv_hashlist]
send_RC_list=[i[1] for i in send_hashlist]

#index of RC match
MatchRC=[ i-j for i,j in zip(rcv_RC_list,send_RC_list)];
Mi=[i for i, e in enumerate(MatchRC) if e == 0]

#print Mi;

#index of MD5 match
MatchMD5=[];

for i in Mi:
	if send_hashlist[i][2]==rcv_hashlist[i][2]:
		transfers -= 1;
		MatchMD5.append(i);
		
print "\n-------------------------\nTOTAL BLOCKS = "+str(No_of_chunks);
print "Matches :\n"
print  MatchMD5;
print "Transfer required ="+str(transfers)+" blocks."

#===============================================================guess
#index of mismatch (RC)
guessfile=open("guess.txt","wb") # used for debugging
MMi=set( range(0,No_of_chunks)) - set(Mi)
Guess_iter=10000
Converged_guess=[];
print "\nGuess.....\n"
for i in MMi:
	guessfile.write("\nGuess for:"+send_hashlist[i][0]+"   \nwith hash: "+str(send_hashlist[i][1])+","+str(send_hashlist[i][2])+"\n")
	(lastguess,converged)=makeguess(i,rcv_hashlist[i],send_hashlist[i][1],send_hashlist[i][2],Guess_iter,guessfile)
	if converged:
		Converged_guess.append(i)
		transfers -=1
		

print "Converged Guess :\n"
print  Converged_guess;
print "Transfer required ="+str(transfers)+" blocks."
		
	
		
		
		




		


