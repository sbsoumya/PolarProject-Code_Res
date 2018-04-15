from random import *

def guess_random1characflip(i,chunk):
	chunk_size=len(chunk);
	randbyte_index=randint(0,chunk_size-1)
	randchunk=bytearray(chunk)
	randchunk[randbyte_index]=randint(0,128)
	return randchunk
	
