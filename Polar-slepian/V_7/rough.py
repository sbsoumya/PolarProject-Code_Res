for j in act_levels:
			clubj=2**(j-1)
			skipj=j-1
			
			if j==0:

				#Initial LLRs
				if LL[0][0] == float("inf"): #checking first entry in stage 0 (col) 
					
					for ii in range(N):
						LL[ii][0]=pl.LLR(p,YN[ii]) 
						
			
			else:			
				#print j
				"""if j == min(act_levels):
					if i==0:
						#taken care in initialization
						pass	
						
					else:
						#print 'g'
					
				else:
					#print 'f'
					
			    """	
				
def LLR_rev_fly(l1,l2,fbit):
	return (g(l1,l2,fbit),f(l1,l2))

def bit_fwd_fly(b1,b2):
	if b1==-1 or b2==-1:
		return (-1 ,-1)
	else:
		return (b1^b2 , b2)					 
			
				
				
			
			
