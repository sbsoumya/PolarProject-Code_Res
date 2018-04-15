#!/usr/bin/env python

import math 
from hashlist import *

S= 50  #chunk size

#Sender ================================================================
print "SENDER\n----------------"
send_file= open("data.txt","rb")

sender_RC_file =open("SenRC.txt","w")
sender_MD5_file =open("SenMD5.txt","w")

(send_RC_list,send_MD5_list,No_of_chunks)=genhashlist(send_file,S);

#for debugging
for RC in send_RC_list:
	sender_RC_file.write(str(RC)+"\n");
for MD5 in send_MD5_list:
	sender_MD5_file.write(str(MD5)+"\n");

#Receiver ==============================================================
print "RECEIVER\n----------------"
rcv_file= open("rcvdata.txt","rb")

rcv_RC_file =open("RxRC.txt","w")   
rcv_MD5_file =open("RxMD5.txt","w") 
      						
(rcv_RC_list,rcv_MD5_list,dummy)=genhashlist(rcv_file,S);


#for debugging
for RC in rcv_RC_list:
	rcv_RC_file.write(str(RC)+"\n");

for MD5 in rcv_MD5_list:
	rcv_MD5_file.write(str(MD5)+"\n");
		
#hashmismatch===========================================================
#finding number of chunk transfers required---------
#actual transfer and reconstruction is not attempted.not required for analysis.

transfers=No_of_chunks

#index of RC match
MatchRC=[ i-j for i,j in zip(rcv_RC_list,send_RC_list)];
Mi=[i for i, e in enumerate(MatchRC) if e == 0]

print Mi;

#index of MD5 match
MatchMD5=[];

for i in Mi:
	if send_MD5_list[i]==rcv_MD5_list[i]:
		transfers -= 1;
		MatchMD5.append(i);
		
print "\n-------------------------\nTOTAL BLOCKS = "+str(No_of_chunks);
print "Matches :\n"
print  MatchMD5;
print "Transfer required ="+str(transfers)+" blocks."
		
		
		




		


