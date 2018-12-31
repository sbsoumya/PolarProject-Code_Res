#==================================================================4-party
#from now feedback table is modified
def allnavigable_from(decoded,at):
        navigable={}
        for key in decoded:
        thisdecode=set(decoded[at])
        thisdecode.remove(0)
        for i in range(len(decoded)-2):
                for key in decoded:
                       #print key
                       #print thisdecode
                        atdecode=set(decoded[key])
                        atdecode.remove(0)
                       #print atdecode
                       #print thisdecode - atdecode
                        if len(thisdecode) == len(thisdecode - atdecode):
                                navigable[key]=False
                        else:
                                navigable[key]=True
                                thisdecode=list(thisdecode)
                                thisdecode.extend(list(atdecode))
                                thisdecode=set(thisdecode)
        allnavigable=True
        for key in navigable:
                allnavigable=allnavigable and navigable[key]

        return (allnavigable,navigable)
		
	
def send_rateless_file_Iter_retro_4G(XN,N,I_ord,channel_p,compound_plist,Glist,T,printFT): 
	# T < deltaG
	#compound channel
    #----------------------------------------------------Iterations start
    nodes=["A","B","C","D"]
	M=len(nodes)
	
	decoded={}
	for n in nodes:
		decoded[n]=np.zeroes(M)

	maxiter=len(compound_plist)-1
	#------------------for filing Tx side
	# reverse arikan :: THIS IS OF SIZE N 
	
	Orig_Data={}
	Rev_Data={}
	Orig_Data[Node[0]]=XN
	#MC model
	for i in range(M-1):
		Orig_Data[Node[i+1]]=pl.BSCN(channel_p[i],Orig_Data[Node[i]])
	#tree X centred
	for i in range(M-1):
		Ori
		
	#****************************************
		
		
		
		pl.BSCN(channel_p[i],Orig_Data[Node[i]])

	for n in nodes:
		Rev_Data[n]=ec.polarencode(Orig_Data[n],N)
	
	decoded_vector={}
	decoded_origdata={}
	Iter_lock={}
	Iter_key={}
	
	Iter=-1
	Iter_errorfree_1=0
	Iter_errorfree_2=0
	Iter_errorfree_3=0
	#-------------------------------------------Forward decoding all try to decode each other
	 #Step 1
	D1={}
  	while anydecoded(decoded)==0 and Iter<maxiter:
		#if Iter<maxiter:
		Iter+=1
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		Iter_T=I_ord[Iter_G-T:Iter_G] 
		Iter_F=list(set(range(N))-set(Iter_I)) 
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		
		for n in nodes:
			Iter_lock[n]=ec.getUN(Rev_Data[n],Iter_T,False)
			#bits frozen sent over errorrfree channel
			# Note while decoding the data is assumed to be in sorted order
			D1[n]=ec.getUN(Rev_Data[n],Iter_F,True)
			decoded_vector[n]={}
			decoded_vector[n][n]=Rev_Data[n] 
			Iter_key[n]={}
			for q in nodes:
				if q!=n:
					decoded_vector[n][q]=ec.polarSCdecodeG(Orig_Data[n],N,Iter_p,Iter_I,list(D1[q]),False)
					Iter_Key[n][q]=ec.getUN(decoded_vector[n][q],Iter_T,False)
		
		for n in nodes:
			for q in nodes:
				if q!=n:
					if not is_mismatch(Iter_lock[q],decoded_vector[n][q]):
						decoded[n][nodes.index(q)]=1
						decoded[q][nodes.index(n)]=1 #reverse
	
		for n in nodes:
			Iter_errorfree_1+=len(D1[n])+len(Iter_lock[n])


			
	final_Iter_1=Iter
	final_Iter_F_1=Iter_F
	final_Iter_p_1=Iter_p
	final_Iter_I_1=Iter_I
	#print decoded
	if not anydecoded(decoded): # deal with this in this case final iter will be maxiter
		if final_Iter_1==maxiter:
			for n in nodes:
				for q in nodes:
					if q!=n:
						decoded[n][q]=1
		
	#print decoded		
	#Step 2  one side communications-------------------------------------------------------------
	#********************************************************************************************START HERE		
	#At A only A communicates This is over and above prev com so Iterlock not required
	Iter=final_Iter_1
	#print anydecodedat(decoded,"atA")
	for n in nodes:
	while anydecodedat(decoded,"atA")==0 and Iter<maxiter: 
		tryatA=1		
		if Iter<maxiter:
		   Iter+=1
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		Iter_T=I_ord[Iter_G-T:Iter_G] 
		Iter_F=list(set(range(N))-set(Iter_I)) 
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_lock_U=ec.getUN(UN_N,Iter_T,False)

		#bits frozen sent over errorrfree channel
		# Note while decoding the data is assumed to be in sorted order
		D2_X=ec.getUN(UN_N,Iter_F,True)
    	#at B
		Iter_X2Y=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(D2_X),False)
		#at C
		Iter_X2Z=ec.polarSCdecodeG(Iter_ZN,N,Iter_p,Iter_I,list(D2_X),False)
		
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		Iter_X2Y_decoded_key=ec.getUN(Iter_X2Y,Iter_T,False)
		Iter_X2Z_decoded_key=ec.getUN(Iter_X2Z,Iter_T,False)
		
		if not is_mismatch(Iter_lock_U,Iter_X2Y_decoded_key):
			decoded["atB"][0]=2
			D2_Y=ec.getUN(VN_N,Iter_F,True)
			Iter_Y2X=ec.polarSCdecodeG(Iter_XN,N,Iter_p,Iter_I,list(D2_Y),False)
			decoded["atA"][0]=2
			Iter_errorfree_2=len(D2_X)+len(D2_Y)-len(D1_X)-len(D1_Y)
		else:					
		  if not is_mismatch(Iter_lock_U,Iter_X2Z_decoded_key):
			  decoded["atC"][0]=2
			  D2_Z=ec.getUN(VN_N,Iter_F,True)
			  Iter_Z2X=ec.polarSCdecodeG(Iter_XN,N,Iter_p,Iter_I,list(D2_Z),False)
			  decoded["atA"][1]=2
			  Iter_errorfree_2=len(D2_X)+len(D2_Z)-len(D1_X)-len(D1_Z) 
		
	
	#At B only B communicates This is over and above prev com 
	Iter=final_Iter_1
	while anydecodedat(decoded,"atB")==0 and Iter<maxiter: 
		tryatB=1 		
		if Iter<maxiter:
		   Iter+=1
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		Iter_T=I_ord[Iter_G-T:Iter_G] 
		Iter_F=list(set(range(N))-set(Iter_I)) 
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_lock_V=ec.getUN(VN_N,Iter_T,False)

		#bits frozen sent over errorrfree channel
		# Note while decoding the data is assumed to be in sorted order
		D2_Y=ec.getUN(VN_N,Iter_F,True)
    	#at A
		Iter_Y2X=ec.polarSCdecodeG(Iter_XN,N,Iter_p,Iter_I,list(D2_Y),False)
		#at C
		Iter_Y2Z=ec.polarSCdecodeG(Iter_ZN,N,Iter_p,Iter_I,list(D2_Y),False)
	
				
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		
		Iter_Y2X_decoded_key=ec.getUN(Iter_Y2X,Iter_T,False)
		Iter_Y2Z_decoded_key=ec.getUN(Iter_Y2Z,Iter_T,False)

		if not is_mismatch(Iter_lock_V,Iter_Y2X_decoded_key):
			decoded["atA"][0]=2
			D2_X=ec.getUN(UN_N,Iter_F,True)
			Iter_X2Y=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(D2_X),False)
			decoded["atB"][0]=2
			Iter_errorfree_2=len(D2_X)+len(D2_Y)-len(D1_X)-len(D1_Y)
		else:					
		  if not is_mismatch(Iter_lock_V,Iter_Y2Z_decoded_key):
			  decoded["atC"][1]=2
			  D2_Z=ec.getUN(VN_N,Iter_F,True)
			  Iter_Z2Y=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(D2_Z),False)
			  decoded["atB"][1]=2
			  Iter_errorfree_2=len(D2_Y)+len(D2_Z)-len(D1_Y)-len(D1_Z) 

	#At C only C communicates This is over and above prev com 
	while anydecodedat(decoded,"atC")==0 and Iter<maxiter: 
		tryatC=1		
		if Iter<maxiter:
		   Iter+=1
		
		Iter_p=compound_plist[Iter]
		Iter_G=Glist[Iter]
		Iter_I=I_ord[:Iter_G]
		Iter_T=I_ord[Iter_G-T:Iter_G] 
		Iter_F=list(set(range(N))-set(Iter_I)) 
		#data received at Rx over error-free channel
		#extra T bits for checking sent over error free channel(this is over and above iter_G)
		Iter_lock_W=ec.getUN(WN_N,Iter_T,False)

		#bits frozen sent over errorrfree channel
		# Note while decoding the data is assumed to be in sorted order
		D2_Z=ec.getUN(WN_N,Iter_F,True)
    	#at A
		Iter_Z2X=ec.polarSCdecodeG(Iter_XN,N,Iter_p,Iter_I,list(D2_Z),False)
		#at B
		Iter_Z2Y=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(D2_Z),False)
	
				
		#Note iterative retrodecode is not required as the frozen bits are transferred over error free channel
		
		Iter_Z2X_decoded_key=ec.getUN(Iter_Z2X,Iter_T,False)
		Iter_Z2Y_decoded_key=ec.getUN(Iter_Z2Y,Iter_T,False)

		if not is_mismatch(Iter_lock_W,Iter_Z2X_decoded_key):
			decoded["atA"][1]=2
			D2_X=ec.getUN(UN_N,Iter_F,True)
			Iter_X2Z=ec.polarSCdecodeG(Iter_ZN,N,Iter_p,Iter_I,list(D2_X),False)
			decoded["atC"][0]=2
			Iter_errorfree_2=len(D2_X)+len(D2_Z)-len(D1_X)-len(D1_Z)
		else:					
		  if not is_mismatch(Iter_lock_V,Iter_Y2Z_decoded_key):
			  decoded["atC"][0]=2
			  D2_Z=ec.getUN(VN_N,Iter_F,True)
			  Iter_Z2Y=ec.polarSCdecodeG(Iter_YN,N,Iter_p,Iter_I,list(D2_Z),False)
			  decoded["atA"][1]=2
			  Iter_errorfree_2=len(D2_Y)+len(D2_Z)-len(D1_Y)-len(D1_Z) 	  
    
    
	final_Iter_2=Iter
	final_Iter_F_2=Iter_F
	final_Iter_p_2=Iter_p
	final_Iter_I_2=Iter_I
	#print decoded
	# In case after the step 2 ny of the nodes have still not decoded anything
	if anydecodedat(decoded,"atA")==0 or anydecodedat(decoded,"atB")==0 or anydecodedat(decoded,"atC")==0 : # deal with this
		#in this case final iter is maxiter.also all the cases lead to FT being fully filled
		if final_Iter_2==maxiter:
			for key in decoded:
				for i in range(2):
					if decoded[key][i]==0:
					   decoded[key][i]=2
	#print decoded				
	#final decoding-----------------------------------------------------------------
	#atA
	# Y not decoded (Z must have been decoded)
	if decoded["atA"][0]==0:
		estimate_Z2X=ec.polarencode(Iter_Z2X,N)	
		if decoded["atC"][1]==1:
			D_needed=D1_Y
			p_needed=final_Iter_p_1
			I_needed=final_Iter_I_1
		else:
			D_needed=D2_Y
			p_needed=final_Iter_p_2
			I_needed=final_Iter_I_2
		Iter_Y2X=ec.polarSCdecodeG(estimate_Z2X,N,p_needed,I_needed,list(D_needed),False)
		decoded["atA"][0]="F"
	    
	#Z not decoded (Y must have been)		
	if decoded["atA"][1]==0:
		estimate_Y2X=ec.polarencode(Iter_Y2X,N)
		if decoded["atB"][1]==1:
			D_needed=D1_Z
			p_needed=final_Iter_p_1
			I_needed=final_Iter_I_1
		else:
			D_needed=D2_Z
			p_needed=final_Iter_p_2
			I_needed=final_Iter_I_2
		Iter_Z2X=ec.polarSCdecodeG(estimate_Y2X,N,p_needed,I_needed,list(D_needed),False)
		decoded["atA"][1]="F"
	
	#atB
	# X not decoded (Z must have been decoded)
	try:
		if decoded["atB"][0]==0:
			estimate_Z2Y=ec.polarencode(Iter_Z2Y,N)
			if decoded["atC"][0]==1:
				D_needed=D1_X
				p_needed=final_Iter_p_1
				I_needed=final_Iter_I_1
			else:
				D_needed=D2_X
				p_needed=final_Iter_p_2
				I_needed=final_Iter_I_2
			Iter_X2Y=ec.polarSCdecodeG(estimate_Z2Y,N,p_needed,I_needed,list(D_needed),False)
			decoded["atB"][0]="F"
			
	except:
		print "FINAl decoding error----------------------"
		print decoded
	    
	#Z not decoded (X must have been)		
	if decoded["atB"][1]==0:
		estimate_X2Y=ec.polarencode(Iter_X2Y,N)
		if decoded["atA"][1]==1:
			D_needed=D1_Z
			p_needed=final_Iter_p_1
			I_needed=final_Iter_I_1
		else:
			D_needed=D2_Z
			p_needed=final_Iter_p_2
			I_needed=final_Iter_I_2
		Iter_Z2Y=ec.polarSCdecodeG(estimate_X2Y,N,p_needed,I_needed,list(D_needed),False)
		decoded["atB"][1]="F"
	    
    #atC
	# X not decoded (Y must have been decoded)
	if decoded["atC"][0]==0:
		estimate_Y2Z=ec.polarencode(Iter_Y2Z,N)
		if decoded["atB"][0]==1:
			D_needed=D1_X
			p_needed=final_Iter_p_1
			I_needed=final_Iter_I_1
		else:
			D_needed=D2_X
			p_needed=final_Iter_p_2
			I_needed=final_Iter_I_2
		Iter_X2Z=ec.polarSCdecodeG(estimate_Y2Z,N,p_needed,I_needed,list(D_needed),False)
		decoded["atC"][0]="F"
	    
	#Y not decoded (X must have been)		
	if decoded["atC"][1]==0:
		estimate_X2Z=ec.polarencode(Iter_X2Z,N)
		if decoded["atA"][0]==1:
			D_needed=D1_Y
			p_needed=final_Iter_p_1
			I_needed=final_Iter_I_1
		else:
			D_needed=D2_Y
			p_needed=final_Iter_p_2
			I_needed=final_Iter_I_2
		Iter_Y2Z=ec.polarSCdecodeG(estimate_X2Z,N,p_needed,I_needed,list(D_needed),False)
		decoded["atC"][1]="F"
	
	  
	#final reverse arikan
	final_Y2X=ec.polarencode(Iter_Y2X,N)	
	final_Z2X=ec.polarencode(Iter_Z2X,N)    
	final_X2Y=ec.polarencode(Iter_X2Y,N)	
	final_Z2Y=ec.polarencode(Iter_Z2Y,N) 
	final_X2Z=ec.polarencode(Iter_X2Z,N)	
	final_Y2Z=ec.polarencode(Iter_Y2Z,N) 
	

	#errors
	err_Y2X = (final_Y2X.tolist() != YN.tolist())
	err_Z2X = (final_Z2X.tolist() != ZN.tolist())
	
	err_X2Y = (final_X2Y.tolist() != XN.tolist())
	err_Z2Y = (final_Z2Y.tolist() != ZN.tolist())
	
	err_Y2Z = (final_Y2Z.tolist() != YN.tolist())
	err_X2Z = (final_X2Z.tolist() != XN.tolist())
	
	Total_error_free= Iter_errorfree_1+Iter_errorfree_2
	# decoding of X and Y, decoding at Z, decoding OF Z at X and Y)
	error=0
	error= (err_X2Y+err_Y2X+err_Y2Z+err_X2Z+err_Z2Y+err_Z2X) >0 
	#print error
	if printFT:
		print decoded
		
	return (Total_error_free,error,decoded)
