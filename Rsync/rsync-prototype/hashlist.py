from checksum import *
from pprint import pprint
import hashlib

def genRClist(data_file,S):
     
	last_chunk_size=0;
	last_chunk_id=0
	RC_list=[];

	chunk=bytearray(data_file.read(S))
		
	while chunk != "":
		last_chunk_id += 1;
		last_chunk_size= len(chunk)
		#print chunk
		RC=rollingcheck(chunk,last_chunk_id,last_chunk_size)
		RC_list.append(RC);
		chunk=bytearray(data_file.read(S))
	
	
	#print last_chunk_id;	
	#print last_chunk_size; 
	print RC_list;
	return RC_list
	
def genMD5list(data_file,S):
     
	last_chunk_size=0;
	last_chunk_id=0
	MD5_list=[];

	chunk=bytearray(data_file.read(S))
		
	while chunk != "":
		last_chunk_id += 1;
		last_chunk_size= len(chunk)
		#print chunk
		MD5=hashlib.md5(str(chunk))
		MD5_list.append(MD5.digest());
		chunk=bytearray(data_file.read(S))
	
	
	#print last_chunk_id;	
	#print last_chunk_size; 
	print MD5_list;
	return MD5_list

def genhashlist(data_file,S):
     
	last_chunk_size=0;
	last_chunk_id=0
	RC_list=[];
	MD5_list=[];

	chunk=bytearray(data_file.read(S))
		
	while chunk != "":
		last_chunk_id += 1;
		last_chunk_size= len(chunk)
		#print chunk
		RC=rollingcheck(chunk,last_chunk_id,last_chunk_size)
		RC_list.append(RC);
		MD5=hashlib.md5(str(chunk))
		MD5_list.append(MD5.digest());
		chunk=bytearray(data_file.read(S))
	
	
	#print last_chunk_id;	
	#print last_chunk_size; 
	print RC_list;
	print MD5_list;
	return (RC_list,MD5_list,last_chunk_id)
	
def genhashlist2(data_file,S):
     
	  
	last_chunk_size=0;
	last_chunk_id=0
	hashlist=[]

	chunk=bytearray(data_file.read(S))
		
	while chunk != "":
		last_chunk_id += 1;
		last_chunk_size= len(chunk)
		#print chunk
		RC=rollingcheck(chunk,last_chunk_id,last_chunk_size)
		MD5=hashlib.md5(str(chunk))
		hashlist.append([chunk,RC,MD5.digest()])
		chunk=bytearray(data_file.read(S))
	
	
	
	#pprint(hashlist);	
	return (hashlist,last_chunk_id)
	
	
