'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Make data.
X = [1,1,1,1,2,2,2,3,3,4]
Y = [1,2,3,4,2,3,4,3,4,4]
Z=  [0.1,0.2,0.1,0.1,0.2,0.3,-.4,0.5,0.5,0.2]
for i in range(len(X)):
	ax.scatter(X[i],Y[i],Z[i])
ax.surface(X,Y,Z)

plt.show()
