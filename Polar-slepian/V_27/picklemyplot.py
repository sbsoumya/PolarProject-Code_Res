'''
To save python objects of any sort, to a file.
'''
import pickle as pkl
import matplotlib.pyplot as plt

def savefiginteractive(fig,filename):
	pkl.dump(  fig,  open(filename,  'wb')  )
	#pkl.dump(  fig,  open(filename,  'wb'), fix_imports=True  )  # fix_imports makes it py2x compatible - untested


'''
Load python objects from file
'''
def loadfiginteractive(filename):
# import other modules needed to work with the figure, such as np, plt etc.
	figx = pkl.load(  open(filename,  'rb')  )
	return figx

#~ x=[1,2,3,4,5]
#~ y=[1,2,3,4,5]
#~ fig=plt.figure()
#~ plt.plot(x,y)
#~ savefiginteractive(fig,'test.fig')
#~ plt.show()
#~ fig=loadfiginteractive('test.fig')
#~ plt.show()
